import pandas as pd
import sys
import re

# Настройка UTF-8 для Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def analyze_audit_results():
    file_path = 'data/dentists_results_final_v2.8.xlsx'
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    # Total Processed
    total = len(df)
    
    # 1. SSL/HTTPS Issues
    # Column: '🔒 Security'
    # Look for "❌" or "⚠️"
    # Filter out empty or N/A if any
    ssl_issues = df[df['🔒 Security'].astype(str).str.contains('❌|⚠️', regex=True, na=False)]
    ssl_count = len(ssl_issues)

    # 2. Mobile Issues
    # Column: '📱 Mobile'
    # Look for "❌"
    mobile_issues = df[df['📱 Mobile'].astype(str).str.contains('❌', regex=True, na=False)]
    mobile_count = len(mobile_issues)

    # 3. Speed Issues (> 10s)
    # Column: '⚡ Speed' format: "2.49s 🟡 Average" or "15.2s 🔴 Slow" or "⏱️ Timeout"
    
    slow_10s_count = 0
    slow_5s_count = 0
    timeout_count = 0
    
    speed_col = df['⚡ Speed'].astype(str)
    
    for val in speed_col:
        if 'Timeout' in val or 'Offline' in val:
            timeout_count += 1
            # Timeouts are technically > 10s likely, but user asked for "load time > 10s"
            # It implies the site actually loaded but took long.
            # Timeout means it didn't complete.
            # I will separate them or include them? 
            # Usually Timeout > 15s (from configuration).
            # I will count them as > 10s for the "Problem" metric.
            slow_10s_count += 1
            slow_5s_count += 1
            continue
            
        # Parse "2.49s"
        match = re.search(r'([\d\.]+)s', val)
        if match:
            try:
                seconds = float(match.group(1))
                if seconds > 10.0:
                    slow_10s_count += 1
                if seconds > 5.0:
                    slow_5s_count += 1
            except ValueError:
                pass

    # 4. Outdated Design
    # Column: '🎨 Design'
    # Look for "⚠️" or "Outdated"
    outdated_count = 0
    if '🎨 Design' in df.columns:
         outdated_issues = df[df['🎨 Design'].astype(str).str.contains('⚠️|Outdated', regex=True, na=False)]
         outdated_count = len(outdated_issues)

    # 5. Lead Quality
    # Column: '🎯 Lead Quality'
    hot_lead_count = 0
    qualified_count = 0
    if '🎯 Lead Quality' in df.columns:
        hot_lead_count = len(df[df['🎯 Lead Quality'].astype(str).str.contains('🔥', na=False)])
        qualified_count = len(df[df['🎯 Lead Quality'].astype(str).str.contains('✅|Qualified', na=False)])

    print(f"Total Websites: {total}")
    print(f"- {ssl_count} без SSL (HTTP Only или ошибки сертификата).")
    print(f"- {mobile_count} без мобильной версии (Mobile Friendly Issues).")
    print(f"- {slow_10s_count} грузятся дольше 10 секунд (включая Timeouts).")
    print(f"- {outdated_count} имеют устаревший дизайн (Flash, jQuery 1.x, Tables).")
    print(f"- {hot_lead_count} горячих лидов (Hot Leads).")
    print(f"- {qualified_count} квалифицированных лидов (Qualified).")
    
    # Extra debug
    print(f"\nDebug Speed:")
    print(f"> 5s: {slow_5s_count}")
    print(f"Timeouts: {timeout_count}")

if __name__ == "__main__":
    analyze_audit_results()
