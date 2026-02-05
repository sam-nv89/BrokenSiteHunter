#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Вс помогательные функции для многоступенчатой проверки
v2.3 - External API Integration
"""

import re
import requests
import socket
import ssl
from datetime import datetime

from typing import Dict, List
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time
import random

# Timeout для внешних API
EXTERNAL_API_TIMEOUT = 10


def extract_canonical_url(html_content: str) -> str:
    """Извлекает canonical URL из HTML."""
    if not html_content:
        return None
    
    match = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\'](https?://[^"\']+)["\']',
        html_content,
        re.IGNORECASE
    )
    return match.group(1) if match else None


def check_hsts_header(response_headers: dict) -> bool:
    """Проверяет наличие HSTS заголовка (Strict-Transport-Security)."""
    if not response_headers:
        return False
    
    for header_name, header_value in response_headers.items():
        if header_name.lower() == 'strict-transport-security':
            return True
    
    return False


def check_ssl_local(url: str) -> Dict:
    """
    Checks SSL certificate locally using Python's ssl module.
    More reliable than external APIs as it uses local trust store.
    """
    results = {'success': False, 'valid': False, 'details': '', 'expiry': None, 'issuer': None}
    
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or url
        port = parsed.port or 443
        
        # Use default context (loads system CA store - Windows/Mac/Linux)
        context = ssl.create_default_context()
        
        with socket.create_connection((hostname, port), timeout=EXTERNAL_API_TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Check Expiry
                not_after_str = cert['notAfter']
                # Format: 'May 25 12:00:00 2026 GMT'
                ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
                expiry_date = datetime.strptime(not_after_str, ssl_date_fmt)
                remaining_days = (expiry_date - datetime.utcnow()).days
                
                # Get Issuer
                issuer_dict = dict(x[0] for x in cert['issuer'])
                issuer_org = issuer_dict.get('organizationName') or issuer_dict.get('commonName', 'Unknown')
                
                results['success'] = True
                results['valid'] = True
                results['expiry'] = remaining_days
                results['issuer'] = issuer_org
                results['details'] = f"Valid ({issuer_org}, {remaining_days} days left)"
                
                return results

    except ssl.SSLCertVerificationError as e:
        results['details'] = f"Verification Error: {e.verify_message}"
        # Try relaxed check for details (Self-signed or Chain issues)
        relaxed_res = check_ssl_relaxed(hostname, port)
        if relaxed_res:
            results['details'] += f" (Likely {relaxed_res})"
            
    except socket.timeout:
        results['details'] = "Connection Timeout"
    except Exception as e:
        results['details'] = f"Error: {str(e)[:50]}"
        
    return results

def check_ssl_relaxed(hostname, port):
    """Fallback to see if we can connect without verification."""
    try:
        context = ssl._create_unverified_context()
        with socket.create_connection((hostname, port), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                return "Self-signed/Chain issue"
    except:
        return None

def check_ssl_external(url: str) -> Dict:
    """
    Deprecated: Using local check instead. Kept for fallback only.
    """
    return check_ssl_local(url)


def check_https_multistep(url: str, html_content: str = None, response_headers: dict = None, response_obj=None) -> Dict:
    """
    Checks HTTPS status with Force Retry logic.
    If HTTP returns 403/Blocked but HTTPS port works, we consider it HTTPS.
    
    Returns:
        {
            'is_https': bool,
            'final_url': str,
            'ssl_valid': False, # calculated later in audit_website
            'ssl_error': None,
            'details': str
        }
    """
    results = {
        'is_https': False,
        'final_url': url,
        'ssl_valid': False,
        'ssl_error': 'Not HTTPS',
        'details': ''
    }
    
    details_parts = []
    
    # 1. URL Protocol Check
    if url.startswith('https://'):
        results['is_https'] = True
        details_parts.append("Protocol: HTTPS")
        
    # 2. Response URL Check (Redirects)
    if response_obj:
        if response_obj.url.startswith('https://'):
            results['is_https'] = True
            results['final_url'] = response_obj.url
            details_parts.append("Redirects to HTTPS")
            
    # 3. Headers Check (HSTS)
    if response_headers:
        if check_hsts_header(response_headers):
            details_parts.append("HSTS: Yes")
            # HSTS implies HTTPS execution, but we prioritize actual connection
            
    # 4. FORCE HTTPS CHECK (The Fix)
    # If standard checks failed to confirm HTTPS, try forcing it.
    if not results['is_https']:
        try:
            target_url = url.replace("http://", "https://")
            if not target_url.startswith("https://"):
                 target_url = "https://" + url.replace("http://", "")
            
            # Use short timeout, verify=False to just check connectivity/status
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
            resp = requests.get(target_url, headers=headers, timeout=5, verify=False)
            
            # If we got a response (even 403 Forbidden), the HTTPS server is listening!
            if resp.status_code < 600:
                results['is_https'] = True
                results['final_url'] = target_url # CRITICAL: Update final URL for SSL check
                details_parts.append(f"Force HTTPS: OK ({resp.status_code})")
        except:
             details_parts.append("Force HTTPS: No")

    # 5. PERFORM SSL CHECK (Restored)
    # Now that we know the final HTTPS URL, check the certificate
    if results['is_https']:
        # Use final_url if it starts with https, otherwise construct it
        check_url = results['final_url']
        if not check_url.startswith('https'):
             check_url = url.replace('http://', 'https://')
             if not check_url.startswith('https'): check_url = 'https://' + check_url
             
        ssl_res = check_ssl_local(check_url)
        results['ssl_valid'] = ssl_res['valid']
        if not ssl_res['valid']:
             results['ssl_error'] = ssl_res['details']
             details_parts.append(f"SSL: Invalid ({ssl_res['details']})")
        else:
             results['ssl_error'] = None
             details_parts.append("SSL: Valid")
    else:
        results['ssl_error'] = "Not HTTPS"

    # Finalize info
    results['details'] = "; ".join(details_parts)
    
    return results


def check_mobile_multistep(html_content: str, url: str = None) -> Dict:
    """
    Многоступенчатая проверка mobile-friendly.
    
    Стратегия:
    1. Viewport Meta Tag - ГЛАВНЫЙ критерий. Если есть -> True (гарантированно).
    2. Если нет Viewport, ищем CSS media queries или фреймворки как fallback.
    
    Returns:
        {
            'is_mobile_friendly': bool,
            'reasons': List[str],
            'methods': List[str]
        }
    """
    results = {
        'is_mobile_friendly': False,
        'reasons': [],
        'methods': []
    }
    
    if not html_content:
        results['reasons'].append('No HTML content available')
        return results
    
    # Level 1: Viewport Meta Tag (Критичный и достаточный)
    # Ищем <meta ... name="viewport" ...> (атрибуты в любом порядке)
    # Используем более надежный regex: поиск тега meta, в котором есть name=['"]viewport['"]
    viewport_match = re.search(
        r'<meta[^>]+name=["\']viewport["\'][^>]*>',
        html_content,
        re.IGNORECASE
    )
    
    if viewport_match:
        results['is_mobile_friendly'] = True
        results['methods'].append('Viewport meta tag')
        return results  # Гарантированный успех, так как браузер включит мобильный режим
        
    results['reasons'].append('Отсутствует viewport meta tag')
    
    # Level 2: Fallback checks (если viewport не найден, но сайт может быть адаптивным)
    
    # CSS Media Queries (inline only, so less reliable)
    has_media_queries = bool(re.search(
        r'@media.*?\((max-width|min-width|orientation)',
        html_content,
        re.IGNORECASE
    ))
    
    # Frameworks
    has_bootstrap = 'bootstrap' in html_content.lower()
    has_tailwind = 'tailwind' in html_content.lower()
    has_foundation = 'foundation' in html_content.lower()
    
    if has_media_queries:
        results['is_mobile_friendly'] = True
        results['methods'].append('CSS media queries (inline)')
        
    elif has_bootstrap or has_foundation or has_tailwind:
        results['is_mobile_friendly'] = True
        framework = 'Bootstrap' if has_bootstrap else ('Tailwind' if has_tailwind else 'Foundation')
        results['methods'].append(f'Responsive framework ({framework})')
    else:
        results['reasons'].append('Нет CSS media queries или популярных фреймворков')
    
    # Если мы здесь и ничего не нашли
    if not results['is_mobile_friendly']:
        # Последний шанс: проверка на специфичные мобильные классы (очень грубо)
        if 'col-xs-' in html_content or 'col-sm-' in html_content or 'd-md-none' in html_content:
             results['is_mobile_friendly'] = True
             results['methods'].append('Mobile css classes detected')
    
    return results


def extract_jquery_version(html_content: str) -> str:
    """Извлекает версию jQuery из HTML."""
    if not html_content:
        return None
    
    # Ищем jquery-x.x.x.js или jquery.min.js
    match = re.search(r'jquery[.-](\d+\.\d+\.?\d*)', html_content, re.IGNORECASE)
    if match:
        return match.group(1)
    
    return None


def get_jquery_release_year(version: str) -> str:
    """Определяет год выпуска jQuery по версии."""
    if not version:
        return "Unknown"
    
    if version.startswith('1.'):
        return "2006-2013"
    elif version.startswith('2.'):
        return "2013-2016"
    elif version.startswith('3.'):
        return "2016+"
    return "Unknown"


def check_seo(html_content: str) -> dict:
    """
    Analyzes Basic SEO tags.
    Returns: {'status': '...', 'details': '...', 'score': int}
    """
    results = {
        'status': '❌ Missing',
        'details': [],
        'score': 0
    }
    
    if not html_content:
        return results

    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 1. Title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ""
        has_title = bool(title_text)
        
        # 2. Description
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        desc_text = desc_tag.get('content', '').strip() if desc_tag else ""
        has_desc = bool(desc_text)
        
        # 3. H1
        h1_tags = soup.find_all('h1')
        h1_count = len(h1_tags)
        
        # 4. Open Graph Image
        og_image = soup.find('meta', property='og:image')
        has_og = bool(og_image and og_image.get('content'))

        # --- Evaluation ---
        issues = []
        score = 0
        
        if has_title:
            score += 2
            if len(title_text) < 10:
                issues.append("Short Title")
            elif len(title_text) > 70:
                issues.append("Long Title")
        else:
            issues.append("Missing Title")

        if has_desc:
            score += 2
            if len(desc_text) < 50:
                issues.append("Short Desc")
            elif len(desc_text) > 160:
                issues.append("Long Desc")
        else:
            issues.append("Missing Desc")
            
        if h1_count == 1:
            score += 1
        elif h1_count == 0:
            issues.append("Missing H1")
        else:
            issues.append(f"Multiple H1 ({h1_count})")
            
        if has_og:
            score += 1
        else:
            issues.append("Missing OG Image")

        # Determine Status
        # Max score = 6
        if not has_title or not has_desc:
            results['status'] = '❌ Missing' # Critical
        elif issues:
            results['status'] = '⚠️ Basic' # Has tags but with issues
        else:
            results['status'] = '✅ Optimized' # Perfect

        results['details'] = "; ".join(issues) if issues else "All Good"
        results['score'] = score
        
    except Exception as e:

        results['details'] = f"SEO Check Error: {str(e)[:50]}"

    return results


def extract_emails_from_website(url, html_content=None):
    """
    Extracts email addresses from a website with Smart Crawling & Fallback.
    Process:
    1. Parse Main Page (Regex)
    2. Find 'Contact' links dynamically (BeautifulSoup)
    3. Crawl top Contact pages
    4. Fallback: Pattern Guessing (info@domain.com) if nothing found
    """
    emails = set()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1'
    }
    
    # Strict Spam Filter
    spam_keywords = [
        'example.com', 'test@', 'noreply@', 'no-reply@', 'yoursite', 
        'yourdomain', 'your-email', 'email@', 'user@', 'admin@domain',
        'name@', 'lastname@', 'firstname', 'email.com', 'domain.com',
        'wixpress.com', 'sentry.io', '2x.png', 'bootstrap'
    ]
    
    email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
    
    def is_valid_email(email):
        email_lower = email.lower()
        for spam in spam_keywords:
            if spam in email_lower: return False
        if email_lower.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')): return False
        return True
    
    def extract_from_html(html):
        if not html: return []
        found = re.findall(email_pattern, html)
        return [e for e in found if is_valid_email(e)]
    
    # 1. Main Page
    contact_links = []
    
    if html_content:
        emails.update(extract_from_html(html_content))
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            for a in soup.find_all('a', href=True):
                href = a['href'].lower()
                text = a.get_text().lower()
                if 'contact' in href or 'contact' in text or 'about' in href:
                    full_link = urljoin(url, a['href'])
                    if full_link.startswith('http') and full_link not in contact_links:
                        contact_links.append(full_link)
        except: pass
    else:
        try:
            time.sleep(random.uniform(0.5, 1.0))
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            if response.status_code == 200:
                emails.update(extract_from_html(response.text))
                soup = BeautifulSoup(response.text, 'html.parser')
                for a in soup.find_all('a', href=True):
                    href = a['href'].lower()
                    if 'contact' in href or 'about' in href:
                        full_link = urljoin(url, a['href'])
                        if full_link.startswith('http') and full_link not in contact_links:
                             contact_links.append(full_link)
        except: pass
        
    # 2. Crawl Contact links
    if len(emails) == 0:
        target_links = contact_links[:2]
        if not target_links:
             target_links = [urljoin(url, p) for p in ['/contact', '/contact-us', '/about']]
             
        for link in target_links:
            try:
                time.sleep(random.uniform(0.5, 1.0))
                resp = requests.get(link, headers=headers, timeout=8, verify=False)
                if resp.status_code == 200:
                    emails.update(extract_from_html(resp.text))
                    if len(emails) >= 1: break
            except: continue
            
    # 3. Fallback
    if len(emails) == 0:
        try:
            domain = urlparse(url).netloc.replace('www.', '')
            if domain:
                return [f"info@{domain}", f"contact@{domain}"]
        except: pass
        
    # 4. Sort
    priority = ['info@', 'contact@', 'office@', 'admin@', 'hello@']
    em_list = list(emails)
    
    def get_prio(e):
        for i, p in enumerate(priority):
            if e.lower().startswith(p): return i
        return 100
    
    em_list.sort(key=get_prio)
    return em_list[:3]
