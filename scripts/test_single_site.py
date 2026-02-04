#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрый тест одного сайта для проверки исправлений
"""

import sys
import os

# Добавляем путь к скрипту
sys.path.insert(0, os.path.dirname(__file__))

import requests
import time
from urllib.parse import urlparse

def test_single_site(url):
    """Тестирует один сайт и показывает детальную информацию"""
    
    print("=" * 70)
    print(f"ТЕСТ САЙТА: {url}")
    print("=" * 70)
    
    # Нормализация
    if not url.startswith('http'):
        url = f'https://{url}'
    
    print(f"\n1. Исходный URL: {url}")
    
    try:
        # Делаем запрос с редиректами
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(
            url,
            headers=headers,
            timeout=10,
            allow_redirects=True,
            verify=False
        )
        
        final_url = response.url
        
        print(f"2. Финальный URL: {final_url}")
        print(f"3. Status Code: {response.status_code}")
        
        # HTTPS проверка
        is_https = final_url.startswith('https://')
        print(f"4. HTTPS: {'[OK] Yes' if is_https else '[FAIL] No (HTTP)'}")
        
        # HTML анализ
        if response.status_code == 200:
            html = response.text
            html_lower = html.lower()
            
            print(f"\n5. HTML Размер: {len(html)} символов")
            
            # Viewport проверка (детальная)
            print("\n6. MOBILE ПРОВЕРКА:")
            has_viewport_name = 'name="viewport"' in html_lower or "name='viewport'" in html_lower
            has_device_width = 'width=device-width' in html_lower
            has_initial_scale = 'initial-scale' in html_lower
            has_media_queries = '@media' in html_lower
            
            print(f"   - name=\"viewport\": {'[OK]' if has_viewport_name else '[FAIL]'}")
            print(f"   - width=device-width: {'[OK]' if has_device_width else '[FAIL]'}")
            print(f"   - initial-scale: {'[OK]' if has_initial_scale else '[FAIL]'}")
            print(f"   - @media queries: {'[OK]' if has_media_queries else '[FAIL]'}")
            
            is_mobile = has_viewport_name or has_device_width or has_media_queries
            print(f"\n   ИТОГ: {'[OK] Mobile Friendly' if is_mobile else '[FAIL] Not Mobile Friendly'}")
            
            # Если нашли viewport - показываем первые 200 символов где он есть
            if 'viewport' in html_lower:
                idx = html_lower.index('viewport')
                snippet = html[max(0, idx-50):idx+150]
                print(f"\n   SNIPPET с viewport:")
                print(f"   {snippet}")
            
        else:
            print(f"\n[FAIL] Сайт недоступен (Status: {response.status_code})")
            
    except Exception as e:
        print(f"\n[FAIL] Ошибка: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python test_single_site.py www.example.com")
        sys.exit(1)
    
    test_url = sys.argv[1]
    test_single_site(test_url)
