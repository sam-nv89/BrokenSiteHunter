#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Создает тестовый Excel файл с популярными сайтами для тестирования скрипта аудита"""

import pandas as pd

# Создаем тестовые данные с разными типами сайтов
test_sites = [
    {
        'Name': 'Dentology Boston',
        'Website': 'www.dentologyboston.com',
        'Category': 'Dentist',
        'Rating': 4.5,
        'Phone': '(617) 555-0101',
        'Address': '123 Main St, Boston, MA'
    },
    {
        'Name': 'Example Domain',
        'Website': 'example.com',
        'Category': 'Test',
        'Rating': 5.0,
        'Phone': '',
        'Address': ''
    },
    {
        'Name': 'Google',
        'Website': 'google.com',
        'Category': 'Tech',
        'Rating': 5.0,
        'Phone': '',
        'Address': 'Mountain View, CA'
    },
    {
        'Name': 'BBC News',
        'Website': 'bbc.com',
        'Category': 'News',
        'Rating': 4.8,
        'Phone': '',
        'Address': 'London, UK'
    },
    {
        'Name': 'Wikipedia',
        'Website': 'wikipedia.org',
        'Category': 'Education',
        'Rating': 4.9,
        'Phone': '',
        'Address': 'San Francisco, CA'
    },
    {
        'Name': 'GitHub',
        'Website': 'github.com',
        'Category': 'Tech',
        'Rating': 4.9,
        'Phone': '',
        'Address': 'San Francisco, CA'
    },
    {
        'Name': 'Stack Overflow',
        'Website': 'stackoverflow.com',
        'Category': 'Tech',
        'Rating': 4.7,
        'Phone': '',
        'Address': 'New York, NY'
    },
    {
        'Name': 'Reddit',
        'Website': 'reddit.com',
        'Category': 'Social',
        'Rating': 4.6,
        'Phone': '',
        'Address': 'San Francisco, CA'
    },
    {
        'Name': 'Amazon',
        'Website': 'amazon.com',
        'Category': 'E-commerce',
        'Rating': 4.5,
        'Phone': '',
        'Address': 'Seattle, WA'
    },
    {
        'Name': 'YouTube',
        'Website': 'youtube.com',
        'Category': 'Video',
        'Rating': 4.8,
        'Phone': '',
        'Address': 'San Bruno, CA'
    }
]

# Создаем DataFrame
df = pd.DataFrame(test_sites)

# Сохраняем в Excel
output_file = 'data/test_sites.xlsx'
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"[OK] Создан файл: {output_file}")
print(f"[OK] Записано сайтов: {len(test_sites)}")
print("\nПример данных:")
print(df[['Name', 'Website', 'Rating']].head())
