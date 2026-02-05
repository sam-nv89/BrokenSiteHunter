#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт сравнения результатов v2.1 vs v2.2
"""
import sys
import pandas as pd

# Настройка UTF-8
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Читаем результаты
v21 = pd.read_excel('data/dentists_test_20_results.xlsx')
v22 = pd.read_excel('data/dentists_test_20_results_v2.2.xlsx')

print("=" * 80)
print("📊 СРАВНЕНИЕ РЕЗУЛЬТАТОВ v2.1 vs v2.2")
print("=" * 80)
print()

print(f"Записей обработано:")
print(f"  v2.1: {len(v21)} сайтов")
print(f"  v2.2: {len(v22)} сайтов")
print()

# Сравнение Lead Quality
print("=" * 80)
print("🎯 LEAD QUALITY")
print("=" * 80)
print("\nv2.1:")
lq_v21 = v21['🎯 Lead Quality'].value_counts()
for quality, count in lq_v21.items():
    print(f"  {quality}: {count} сайтов")

print("\nv2.2:")
lq_v22 = v22['🎯 Lead Quality'].value_counts()
for quality, count in lq_v22.items():
    print(f"  {quality}: {count} сайтов")

print("\n📈 ИЗМЕНЕНИЯ:")
all_qualities = set(list(lq_v21.index) + list(lq_v22.index))
for quality in ['🔥 HOT LEAD', '🟠 QUALIFIED', '🟡 POTENTIAL', '⚪ SKIP']:
    if quality in all_qualities:
        old_count = lq_v21.get(quality, 0)
        new_count = lq_v22.get(quality, 0)
        diff = new_count - old_count
        if diff > 0:
            print(f"  {quality}: {old_count} → {new_count} (+{diff})")
        elif diff < 0:
            print(f"  {quality}: {old_count} → {new_count} ({diff})")
        else:
            print(f"  {quality}: {old_count} → {new_count} (без изменений)")

# Сравнение Website Status
print("\n" + "=" * 80)
print("🌐 WEBSITE STATUS")
print("=" * 80)
print("\nv2.1:")
ws_v21 = v21['🌐 Website Status'].value_counts()
for status, count in ws_v21.items():
    print(f"  {status}: {count} сайтов")

print("\nv2.2:")
ws_v22 = v22['🌐 Website Status'].value_counts()
for status, count in ws_v22.items():
    print(f"  {status}: {count} сайтов")

print("\n📈 ИЗМЕНЕНИЯ:")
all_statuses = set(list(ws_v21.index) + list(ws_v22.index))
for status in ['✅ Online', '⚠️ Protected', '❌ Offline', '⏱️ Timeout']:
    if status in all_statuses:
        old_count = ws_v21.get(status, 0)
        new_count = ws_v22.get(status, 0)
        diff = new_count - old_count
        if diff > 0:
            print(f"  {status}: {old_count} → {new_count} (+{diff})")
        elif diff < 0:
            print(f"  {status}: {old_count} → {new_count} ({diff})")

# Детальное сравнение сайтов с изменениями
print("\n" + "=" * 80)
print("🔍 ДЕТАЛЬНЫЕ ИЗМЕНЕНИЯ ПО САЙТАМ")
print("=" * 80)

changes = []
for idx in range(len(v21)):
    website = v21.loc[idx, 'Website']
    old_status = v21.loc[idx, '🌐 Website Status']
    new_status = v22.loc[idx, '🌐 Website Status']
    old_quality = v21.loc[idx, '🎯 Lead Quality']
    new_quality = v22.loc[idx, '🎯 Lead Quality']
    
    if old_status != new_status or old_quality != new_quality:
        changes.append({
            'website': website,
            'old_status': old_status,
            'new_status': new_status,
            'old_quality': old_quality,
            'new_quality': new_quality
        })

if changes:
    for i, change in enumerate(changes, 1):
        print(f"\n{i}. {change['website']}")
        if change['old_status'] != change['new_status']:
            print(f"   Status: {change['old_status']} → {change['new_status']}")
        if change['old_quality'] != change['new_quality']:
            print(f"   Quality: {change['old_quality']} → {change['new_quality']}")
else:
    print("\nНет изменений!")

print("\n" + "=" * 80)
print("✅ СРАВНЕНИЕ ЗАВЕРШЕНО")
print("=" * 80)
