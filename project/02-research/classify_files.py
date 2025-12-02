#!/usr/bin/env python3
import os
import json
import re
from pathlib import Path

RESEARCH_DIR = "/home/amanoops/paper-projects/anto/research"
OUTPUT_FILE = "classification_map.json"

# 분류 규칙 (우선순위 순)
RULES = [
    # S-시스템 (최신 정본)
    (r'^S00_', 'Chapter-0', ''),
    (r'^S01_', 'General', ''),
    (r'^S02_', 'Chapter-1', ''),
    (r'^S03_', 'Chapter-2', ''),
    (r'^S08_', 'Chapter-3', ''),  # S08 = 재무
    (r'^S04_', 'Chapter-4', ''),
    (r'^S05_', 'Chapter-5', ''),
    (r'^S06_', 'Chapter-6', ''),
    (r'^S07_', 'Chapter-6', ''),

    # 번호 기반 - Executive Summary
    (r'^00_Executive', 'Chapter-0', 'legacy'),
    (r'^01_Executive', 'Chapter-0', 'legacy'),

    # 번호 기반 - Chapter 1~8
    (r'^01_제안개요', 'General', 'legacy'),
    (r'^01_경쟁사', 'Chapter-4', ''),
    (r'^02_복제불가능', 'Chapter-1', ''),
    (r'^02_ANTO브랜드소개', 'Chapter-1', 'legacy'),
    (r'^02_브랜드', 'Chapter-1', 'legacy'),
    (r'^02_운영', 'Chapter-2', 'legacy'),
    (r'^02_포지셔닝', 'Chapter-4', ''),
    (r'^03_마케팅', 'Chapter-5', ''),
    (r'^03_시장', 'Chapter-4', 'legacy'),
    (r'^03_운영', 'Chapter-2', 'legacy'),
    (r'^04_재무', 'Chapter-3', 'legacy'),
    (r'^04_사업전략', 'Chapter-5', 'legacy'),
    (r'^04_시장', 'Chapter-4', 'legacy'),
    (r'^04_마케팅', 'Chapter-5', 'legacy'),
    (r'^04_운영', 'Chapter-5', ''),
    (r'^05_2026', 'Chapter-5', ''),
    (r'^05_마케팅', 'Chapter-5', 'legacy'),
    (r'^05_시장', 'Chapter-4', 'legacy'),
    (r'^05_시설', 'Chapter-2', 'legacy'),
    (r'^05_주요플랜', 'Chapter-6', 'legacy'),
    (r'^06_2026', 'Chapter-5', ''),
    (r'^06_재무', 'Chapter-3', 'legacy'),
    (r'^06_주요플랜', 'Chapter-6', 'legacy'),
    (r'^06_향후액션', 'Chapter-6', 'legacy'),
    (r'^07_재무', 'Chapter-3', 'legacy'),
    (r'^07_실행', 'Chapter-6', ''),
    (r'^07_향후계획', 'Chapter-6', 'legacy'),
    (r'^08_부서별', 'Chapter-7', ''),
    (r'^08_향후', 'Chapter-6', 'legacy'),
    (r'^08_결론', 'Chapter-8', 'legacy'),
    (r'^09_결론', 'Chapter-8', ''),

    # 명칭 기반
    (r'^딥 리서치 자료', 'Chapter-4', 'deep-research'),
    (r'^ANTO 딥리서치.*\.pdf$', 'Deep-Research-Archive', ''),
    (r'-News\.md$', 'News', 'articles'),
    (r'^ANTO Brand', 'Chapter-1', ''),
    (r'^ANTO_비전', 'Chapter-8', ''),
    (r'^ANTO_브랜드', 'Chapter-1', ''),
    (r'^ANTO_호텔', 'Chapter-7', ''),
    (r'^ANTO_슬라이드', 'General', ''),
    (r'^README\.md$', 'General', ''),
    (r'^ANTO_2026', 'General', ''),
    (r'^Appendix', 'Appendix', ''),
    (r'^ContentCreation', 'General', 'legacy'),
    (r'^CODEX_TODO', 'General', 'legacy'),
    (r'^PROMPT_TEMPLATES', 'General', 'legacy'),
    (r'^outline\.md$', 'General', ''),
    (r'^workflow\.md$', 'General', 'legacy'),
    (r'^scraping', 'General', 'legacy'),
    (r'^리서치-0', 'General', 'legacy'),
    (r'^대표님_보고', 'Chapter-7', ''),
    (r'^대내용', 'General', ''),
    (r'^안토_조직', 'Chapter-7', ''),
    (r'^안토_종합', 'General', ''),
    (r'^안토_인사팀', 'Chapter-7', ''),
    (r'benchmark', 'Chapter-4', ''),
    (r'paradisecity', 'Chapter-4', ''),
    (r'inspire', 'Chapter-4', ''),
    (r'네이버 지도', 'Chapter-4', ''),
    (r'^IV_사업전략', 'Chapter-5', ''),
]

def classify_file(filename):
    """파일명 기반 분류"""
    for pattern, chapter, subfolder in RULES:
        if re.search(pattern, filename, re.IGNORECASE):
            return {
                'filename': filename,
                'chapter': chapter,
                'subfolder': subfolder,
                'path': f"{chapter}/{subfolder}/{filename}".replace('//', '/')
            }

    # 미분류
    return {
        'filename': filename,
        'chapter': 'Unclassified',
        'subfolder': '',
        'path': f"Unclassified/{filename}"
    }

def main():
    results = []

    # research 폴더의 모든 파일 스캔
    for root, dirs, files in os.walk(RESEARCH_DIR):
        for file in files:
            # Zone.Identifier 제외
            if ':Zone.Identifier' in file:
                continue

            rel_path = os.path.relpath(os.path.join(root, file), RESEARCH_DIR)
            classification = classify_file(file)
            classification['original_path'] = rel_path
            results.append(classification)

    # JSON 저장
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 통계 출력
    stats = {}
    unclassified = []
    for item in results:
        chapter = item['chapter']
        stats[chapter] = stats.get(chapter, 0) + 1
        if chapter == 'Unclassified':
            unclassified.append(item['filename'])

    print("=== Classification Statistics ===")
    for chapter, count in sorted(stats.items()):
        print(f"{chapter}: {count} files")

    print(f"\n=== Unclassified Files ({len(unclassified)}) ===")
    for fname in unclassified:
        print(f"  - {fname}")

    print(f"\n✅ Classification map saved to: {OUTPUT_FILE}")
    print(f"Total files: {len(results)}")

    return len(unclassified)

if __name__ == '__main__':
    unclassified_count = main()
    exit(0 if unclassified_count < 10 else 1)
