import pandas as pd
import sys
import os
import time
from audit_websites import audit_website, PAGESPEED_API_KEY, clean_website_url, format_website_status, format_security_status, format_speed_score, determine_lead_quality, get_technical_notes_severity
from apply_styles import apply_excel_formatting

# Force UTF-8 for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def recheck_offline_sites(input_file):
    print(f"📂 Загружаю файл: {input_file}")
    
    try:
        df = pd.read_excel(input_file, engine='openpyxl')
    except Exception as e:
        print(f"❌ Ошибка открытия файла: {e}")
        return

    # Find offline rows
    # Check column '🌐 Website Status' for '❌ Offline' or '⏱️ Timeout'
    if '🌐 Website Status' not in df.columns:
        print("❌ Колонка '🌐 Website Status' не найдена!")
        return
        
    offline_mask = df['🌐 Website Status'].astype(str).str.contains('❌ Offline|⏱️ Timeout', na=False)
    rows_to_check = df[offline_mask].index.tolist()
    
    total_recheck = len(rows_to_check)
    print(f"🔍 Найдено {total_recheck} сайтов со статусом Offline/Timeout.")
    
    if total_recheck == 0:
        print("✅ Нет сайтов для перепроверки.")
        return

    print("🚀 Начинаю перепроверку (Deep Check for Protection)...")
    
    # We need the source URL. 
    # The 'Website' column typically has "www.domain.com". We might need to look for 'Final URL' or reconstruction.
    # In audit_websites.py, 'Website' in df_final is cleaned. The original might be lost in the final report if not preserved.
    # However, for re-checking, we can try to use the 'Website' column content and prepend https:// if needed.
    
    updated_count = 0
    
    for i, idx in enumerate(rows_to_check):
        site_val = str(df.at[idx, 'Website'])
        if not site_val or site_val.lower() == 'nan':
             continue
             
        # Reconstruct URL (audit_website expects a raw URL, it normalizes it internally)
        url_to_check = site_val if site_val.startswith('http') else f"https://{site_val}"
        
        print(f"[{i+1}/{total_recheck}] Checking: {url_to_check} ...")
        
        # Run Audit
        result = audit_website(url_to_check, PAGESPEED_API_KEY, index=i+1, total=total_recheck)
        
        # Check if status changed
        new_avail = result['site_available']
        new_error = result.get('availability_error')
        
        # If it's now Online OR Protected (which is technically site_available=True in our new logic, or handled via error flag)
        # Wait, in audit_websites.py we set available=True for Protected sites in the new logic!
        
        if new_avail:
             print(f"   🎉 STATUS CHANGED! -> {new_error if new_error else 'Online'}")
             updated_count += 1
             
             # Update DataFrame Columns
             # 1. Website Status
             df.at[idx, '🌐 Website Status'] = format_website_status(new_avail, new_error)
             
             # 2. Security
             df.at[idx, '🔒 Security'] = format_security_status(result['is_https'], result['ssl_valid'], result.get('ssl_error'))
             
             # 3. Speed
             # If protected, we might not have speed, but let's try
             val_speed = '❌ Offline' if not new_avail else format_speed_score(result['load_time'])
             if new_error == 'Protected': val_speed = '⚠️ Protected' # Custom overrides if needed
             df.at[idx, '⚡ Speed'] = val_speed
             
             # 4. Mobile
             val_mobile = 'N/A'
             if new_avail:
                 val_mobile = '✅ Yes' if result['is_mobile_friendly'] else '❌ No'
             if new_error == 'Protected': val_mobile = '⚠️ Protected'
             df.at[idx, '📱 Mobile'] = val_mobile
             
             # 5. Design
             val_design = 'N/A'
             if new_avail:
                 val_design = f"⚠️ Outdated" if result['is_outdated'] else '✅ Modern'
             if new_error == 'Protected': val_design = '⚠️ Protected'
             df.at[idx, '🎨 Design'] = val_design
             
             # 6. SEO
             df.at[idx, '🔍 SEO'] = result.get('seo_status', 'N/A')
             
             # 7. Technical Notes
             df.at[idx, '💬 Technical Notes'] = result.get('technical_notes', '')
             
             # 8. Lead Quality
             # Recalculate severity and lead quality
             # We assume severity calculation logic is inside audit_website, but we need to map it to Lead Quality
             
             # audit_website returns 'issue_severity'.
             new_severity = result['issue_severity']
             current_rating = df.at[idx, '⭐ Customer Rating']
             
             # Note: 'Rating' format in Excel is string or float. 'determine_lead_quality' handles it.
             new_lead_quality = determine_lead_quality(new_severity, current_rating)
             df.at[idx, '🎯 Lead Quality'] = new_lead_quality
             
        else:
             print(f"   ❌ Still Offline ({new_error})")

        # Save periodically
        if (i + 1) % 10 == 0:
             print("💾 Intermediate save...")
             df.to_excel(input_file, index=False)

    print(f"\n✅ Re-check complete. Updated {updated_count} sites.")
    print(f"💾 Saving final file: {input_file}")
    df.to_excel(input_file, index=False)
    
    # Restore styles
    apply_excel_formatting(input_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python recheck_offline.py <file.xlsx>")
    else:
        recheck_offline_sites(sys.argv[1])
