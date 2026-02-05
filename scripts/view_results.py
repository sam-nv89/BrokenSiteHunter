#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Просмотр результатов аудита с поддержкой UTF-8
"""
import sys
import pandas as pd

# Настройка UTF-8 для Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    # Читаем результаты
    df = pd.read_excel('data/dentists_test_20_results.xlsx')
    
    print("=" * 80)
    print("📊 РЕЗУЛЬТАТЫ АУДИТА (20 сайтов)")
    print("=" * 80)
    print()
    
    # Основные колонки для отображения
    display_cols = ['#', 'Name', 'Website', '🌐 Website Status', '🔒 Security', 
                    '⚡ Speed', '📱 Mobile', '🎨 Design', '🎯 Lead Quality']
    
    # Фильтруем существующие колонки
    available_cols = [col for col in display_cols if col in df.columns]
    
    # Показываем результаты
    for idx, row in df.iterrows():
        print(f"\n{'─' * 80}")
        print(f"#{idx+1} | {row.get('Name', 'N/A')}")
        print(f"{'─' * 80}")
        print(f"🌐 Website:        {row.get('Website', 'N/A')}")
        print(f"📍 Status:         {row.get('🌐 Website Status', 'N/A')}")
        print(f"🔒 Security:       {row.get('🔒 Security', 'N/A')}")
        print(f"⚡ Speed:          {row.get('⚡ Speed', 'N/A')}")
        print(f"📱 Mobile:         {row.get('📱 Mobile', 'N/A')}")
        print(f"🎨 Design:         {row.get('🎨 Design', 'N/A')}")
        print(f"🎯 Lead Quality:   {row.get('🎯 Lead Quality', 'N/A')}")
    
    print(f"\n{'=' * 80}")
    print("📈 СТАТИСТИКА")
    print("=" * 80)
    
    # Подсчет по Lead Quality
    if '🎯 Lead Quality' in df.columns:
        quality_counts = df['🎯 Lead Quality'].value_counts()
        for quality, count in quality_counts.items():
            print(f"{quality}: {count} сайтов")
    
    print(f"\n✅ Всего обработано: {len(df)} сайтов")
    print(f"📄 Файл: data/dentists_test_20_results.xlsx")

if __name__ == '__main__':
    main()
