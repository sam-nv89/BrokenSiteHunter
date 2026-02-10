import pandas as pd
import sys
import os

# Add local directory to path to allow import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from apply_styles import apply_excel_formatting

# Настройка UTF-8 для Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def create_marketing_sample():
    full_file = 'data/dentists_results_final_v2.8.xlsx'
    
    try:
        # Read the Excel file
        df = pd.read_excel(full_file)
        
        # Select best examples for marketing
        # We want: 
        # 1. Some with Mobile issues
        # 2. Some with SSL issues
        # 3. Some Hot Leads
        # Instead of just head(15), let's sort or pick interesting ones.
        
        # Filter for issues
        mobile_issues = df[df['📱 Mobile'].astype(str).str.contains('❌', na=False)].head(5)
        ssl_issues = df[df['🔒 Security'].astype(str).str.contains('❌|⚠️', na=False)].head(5)
        hot_leads = df[df['🎯 Lead Quality'].astype(str).str.contains('🔥', na=False)].head(5)
        
        # Combine and deduplicate
        sample_df = pd.concat([mobile_issues, ssl_issues, hot_leads]).drop_duplicates().head(20)
        
        # If we have less than 5, just take head
        if len(sample_df) < 5:
            sample_df = df.head(15)
            
        # Sort by Lead Quality to show Hot first? No, keep mix.
        
        # Save to new Excel file
        output_file = 'data/marketing_sample_v2.8.xlsx'
        
        sample_df.to_excel(output_file, index=False)
        print(f"✅ Created marketing sample data: {output_file}")
        
        # Apply formatting
        print("🎨 Applying visual styles...")
        apply_excel_formatting(output_file)
        
        print(f"✅ Marketing sample ready: {output_file}")
        print(f"Contains {len(sample_df)} rows of 'broken' sites.")
        
    except FileNotFoundError:
        print(f"❌ File not found: {full_file}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_marketing_sample()
