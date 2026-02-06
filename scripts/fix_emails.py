import pandas as pd
import sys
import os
import time
from audit_websites_helpers import extract_emails_from_website

import sys
# Force UTF-8 for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Import logic to check if email is spam (reuse logic from helpers ideally, but we'll inline a checker for the dataframe filter)
SPAM_KEYWORDS = [
    '@example.com', '@test.com', '@mysite.com', '@yourdomain', '@yoursite',
    '@domain.com', '@email.com', '@company.com', '@nowhere.com',
    'noreply@', 'no-reply@', 'donotreply@',
    'wixpress.com', 'sentry.io', '2x.png', 'bootstrap', 'react'
]

def is_spam_email(email):
    if not email or pd.isna(email):
        return False # Empty is not "spam" to be fixed, it's just missing
    email_lower = str(email).lower()
    for spam in SPAM_KEYWORDS:
        if spam in email_lower:
            return True
    return False

def fix_emails(input_file, output_file):
    print(f"📂 Загружаю файл: {input_file}")
    
    try:
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
        else:
            df = pd.read_excel(input_file)
    except Exception as e:
        print(f"❌ Ошибка открытия файла: {e}")
        return

    if 'Email' not in df.columns:
        print("❌ Колонка 'Email' не найдена!")
        return
        
    # Find rows to fix
    rows_to_fix = []
    for index, row in df.iterrows():
        email = row.get('Email')
        if is_spam_email(email):
            rows_to_fix.append(index)
            
    total_fix = len(rows_to_fix)
    print(f"🔍 Найдено {total_fix} строк с некорректными Email (например, example.com)")
    
    if total_fix == 0:
        print("✅ Все email выглядят корректно. Исправления не требуются.")
        return

    print("🚀 Начинаю исправление...")
    
    fixed_count = 0
    for i, idx in enumerate(rows_to_fix):
        url = df.at[idx, 'Website'] # Assuming column name is 'Website' or 'URL'. Let's check logic.
        if pd.isna(url):
            url = df.at[idx, 'Final URL'] # Fallback
            
        current_email = df.at[idx, 'Email']
        print(f"[{i+1}/{total_fix}] Исправляю: {url} (Было: {current_email})")
        
        try:
            # Re-run extraction with UPDATED helpers logic (stricter)
            new_emails = extract_emails_from_website(url)
            
            if new_emails:
                new_email_str = ", ".join(new_emails)
                df.at[idx, 'Email'] = new_email_str
                print(f"   ✅ Найдено: {new_email_str}")
                fixed_count += 1
            else:
                # If scraping returns nothing (because filter blocked it), set to None or empty
                # But wait, helper might fallback to info@domain.com
                # If helper returns empty, it means even fallback failed or wasn't applicable.
                df.at[idx, 'Email'] = None 
                print(f"   ⚠️ Ничего не найдено (очищено)")
                
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")

        # Save periodically
        if (i + 1) % 10 == 0:
            print("💾 Промежуточное сохранение...")
            df.to_excel(output_file, index=False)

    print(f"\n✅ Готово! Исправлено {fixed_count} из {total_fix} записей.")
    print(f"💾 Результат сохранен в: {output_file}")
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python fix_emails.py <input_file> [output_file]")
    else:
        input_f = sys.argv[1]
        output_f = sys.argv[2] if len(sys.argv) > 2 else input_f.replace('.xlsx', '_fixed_emails.xlsx')
        fix_emails(input_f, output_f)
