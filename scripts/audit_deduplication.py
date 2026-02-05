# ============================================================================
# DATA DEDUPLICATION (v2.4)
# ============================================================================

import pandas as pd
from urllib.parse import urlparse



def deduplicate_data(df: pd.DataFrame, website_col: str) -> tuple:
    """
    Удаляет дубликаты из DataFrame перед аудитом.
    
    Стратегия:
    1. Группировка по НОРМАЛИЗОВАННОМУ Website (если URL ведут на один сайт)
    2. Проверка колонок до '⭐ Customer Rating' включительно
    3. Объединение конфликтующих значений через \n
    4. Строки без Website - сохраняются с warning
    
    Returns:
        tuple: (cleaned_df, dedup_log)
    """
    dedup_log = []
    original_count = len(df)
    
    # Определяем колонки для проверки (до Rating включительно)
    columns_to_check = []
    for col in df.columns:
        columns_to_check.append(col)
        if 'Rating' in col or col == '⭐ Customer Rating':
            break
    
    print(f"\n🔍 DEDUPLICATION:")
    print(f"   Checking columns: {', '.join(columns_to_check)}")
    
    # Step 1: Разделяем на строки с Website и без
    # Используем динамическое имя колонки
    df_with_website = df[df[website_col].notna() & (df[website_col] != '')].copy()
    df_no_website = df[~df.index.isin(df_with_website.index)].copy()
    
    # Создаем временную колонку для группировки (нормализованный URL)
    df_with_website['_normalized_url'] = df_with_website[website_col].apply(normalize_url_for_grouping)
    
    # Step 2: Group by NORMALIZED Website
    result_rows = []
    
    # Группируем по нормализованному URL, но сохраняем исходные данные
    for norm_url, group in df_with_website.groupby('_normalized_url'):
        if len(group) == 1:
            # Нет дубликатов
            row_data = group.iloc[0].to_dict()
            # Удаляем временную колонку если попала в dict
            if '_normalized_url' in row_data:
                del row_data['_normalized_url']
            result_rows.append(row_data)
        else:
            # Дубликаты найдены! (разные варианты написания одного сайта)
            merged_row = merge_duplicate_rows(group, columns_to_check, dedup_log, website_col)
            result_rows.append(merged_row)
    
    # Step 3: Add rows without Website (with warning)
    for idx, row in df_no_website.iterrows():
        row_dict = row.to_dict()
        row_dict['⚠️ Data Warning'] = 'No Website'
        result_rows.append(row_dict)
        dedup_log.append(f"⚠️ Row {idx}: No Website - kept with warning")
    
    # Create result DataFrame
    result_df = pd.DataFrame(result_rows)
    
    # Summary
    removed_count = original_count - len(result_df)
    
    print(f"   Original rows:  {original_count}")
    print(f"   After dedup:    {len(result_df)}")
    print(f"   Removed/Merged: {removed_count}")
    
    # Save log if any duplicates found
    if dedup_log:
        log_file = 'deduplication_log.txt'
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(dedup_log))
        print(f"   📝 Log saved: {log_file}")
    
    return result_df, dedup_log


def normalize_url_for_grouping(url: str) -> str:
    """Нормализует URL для сравнения (извлекает чистый домен)."""
    if not isinstance(url, str):
        return str(url)
    
    # 1. Добавляем http если нет схемы (для парсинга)
    url_clean = url.strip()
    if not url_clean.startswith(('http://', 'https://')):
        url_clean = 'http://' + url_clean
        
    try:
        parsed = urlparse(url_clean)
        # Получаем домен (netloc)
        domain = parsed.netloc.lower()
        
        # Удаляем www.
        if domain.startswith('www.'):
            domain = domain[4:]
            
        return domain
    except:
        # Fallback если парсинг не удался
        return url.strip().lower()




def merge_duplicate_rows(group: pd.DataFrame, columns_to_check: list, log: list, website_col: str) -> dict:
    """
    Объединяет дублирующиеся строки с одинаковым Website.
    
    Правила:
    - Заполняет пустые значения из других строк
    - Конфликтующие значения объединяет через \n
    - Проверяет только колонки до Rating включительно
    
    Returns:
        dict: Объединенная строка
    """
    merged = {}
    
    # Берем первый попавшийся URL как основной (или самый длинный/полный можно выбрать потом)
    first_row_idx = group.index[0]
    website = group.loc[first_row_idx, website_col]
    
    conflicts = []
    
    # Удаляем временную колонку перед слиянием
    cols = [c for c in group.columns if c != '_normalized_url']
    
    for col in cols:
        # Get all non-empty values for this column
        values = group[col].dropna()
        values = values[values != '']
        
        if len(values) == 0:
            # All empty
            merged[col] = ''
        elif len(values) == 1:
            # One value
            merged[col] = values.iloc[0]
        else:
            # Multiple values
            unique_values = values.unique()
            
            if len(unique_values) == 1:
                # Same value repeated
                merged[col] = unique_values[0]
            else:
                # CONFLICT! Different non-empty values
                if col in columns_to_check:
                    # Merge with newline separator (for columns we check)
                    merged[col] = '\n'.join(str(v) for v in unique_values)
                    conflicts.append(f"{col}: merged {len(unique_values)} values")
                else:
                    # For columns after Rating - just take first
                    merged[col] = values.iloc[0]
    
    # Log conflicts
    if conflicts:
        log.append(f"✅ Merged {len(group)} rows for {website}:")
        for conflict in conflicts:
            log.append(f"   - {conflict}")
    else:
        log.append(f"✅ Merged {len(group)} rows for {website} (no conflicts)")
    
    return merged
