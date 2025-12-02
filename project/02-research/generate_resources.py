#!/usr/bin/env python3
import os
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

TARGET_DIR = "/home/amanoops/paper-projects/anto/project/02-research"
CLASSIFICATION_MAP = "classification_map.json"

# Chapter 한글 이름 매핑
CHAPTER_NAMES = {
    'Chapter-0': 'Executive Summary',
    'Chapter-1': '복제 불가능한 자연 자산 & 브랜드',
    'Chapter-2': '운영 현황',
    'Chapter-3': '재무 목표 및 시나리오',
    'Chapter-4': '시장 분석 및 포지셔닝',
    'Chapter-5': '2026년 실행 전략',
    'Chapter-6': '실행 과제 및 리스크 관리',
    'Chapter-7': '부서별 실행 과제',
    'Chapter-8': '결론 및 비전',
    'General': '프로젝트 전반',
    'Deep-Research-Archive': '딥리서치 PDF 보고서',
    'News': '뉴스 기사',
    'Appendix': '부록'
}

def generate_resources_md(chapter, files_by_subfolder):
    """각 Chapter의 resources.md 생성"""

    chapter_name = CHAPTER_NAMES.get(chapter, chapter)
    current_date = datetime.now().strftime('%Y-%m-%d')

    # 파일 분류
    primary = files_by_subfolder.get('', [])
    legacy = files_by_subfolder.get('legacy', [])
    deep_research = files_by_subfolder.get('deep-research', [])
    articles = files_by_subfolder.get('articles', [])

    # 총 파일 개수
    total_files = sum(len(files) for files in files_by_subfolder.values())

    content = f"""---
type: resource-index
chapter: {chapter}
chapter_name: {chapter_name}
updated: {current_date}
total_files: {total_files}
---

# {chapter} Resources

> **{chapter_name}** 관련 리서치 자료 인덱스

"""

    # Primary Files (최신 정본)
    if primary:
        content += "## 📄 Primary Files (최신 정본)\n\n"
        content += f"> 현재 사용 중인 최신 버전 ({len(primary)}개)\n\n"
        for item in sorted(primary, key=lambda x: x['filename']):
            filename = item['filename']
            # S-시스템 파일 강조
            if filename.startswith('S0'):
                content += f"- **[{filename}](./{filename})** ⭐ (System Version)\n"
            else:
                content += f"- [{filename}](./{filename})\n"
        content += "\n"

    # Deep Research (딥리서치)
    if deep_research:
        content += "## 🔍 Deep Research (딥리서치)\n\n"
        content += f"> 상세 경쟁사 분석 및 시장 조사 ({len(deep_research)}개)\n\n"
        for item in sorted(deep_research, key=lambda x: x['filename']):
            content += f"- [{item['filename']}](./deep-research/{item['filename']})\n"
        content += "\n"

    # News Articles
    if articles:
        content += "## 📰 News Articles (뉴스 기사)\n\n"
        content += f"> 관련 뉴스 및 기사 ({len(articles)}개)\n\n"
        for item in sorted(articles, key=lambda x: x['filename']):
            content += f"- [{item['filename']}](./articles/{item['filename']})\n"
        content += "\n"

    # Legacy Files (구 버전)
    if legacy:
        content += "## 📦 Legacy Files (구 버전)\n\n"
        content += f"> 참고용 이전 버전 및 외부 보고서 ({len(legacy)}개)\n\n"
        content += "<details>\n<summary>펼치기/접기</summary>\n\n"
        for item in sorted(legacy, key=lambda x: x['filename']):
            content += f"- [{item['filename']}](./legacy/{item['filename']})\n"
        content += "\n</details>\n\n"

    # 네비게이션 링크
    content += "---\n\n"
    content += "## 📂 Navigation\n\n"
    content += "- [← README로 돌아가기](../README.md)\n"
    content += "- [↑ 프로젝트 루트](../../)\n"
    content += f"- [📊 전체 진행 상황](../RESEARCH-STATUS.md)\n\n"

    # 푸터
    content += "---\n\n"
    content += f"**Total Files**: {total_files} | "
    content += f"**Last Updated**: {current_date}\n"

    return content

def main():
    # classification_map.json 로드
    with open(CLASSIFICATION_MAP, 'r', encoding='utf-8') as f:
        classifications = json.load(f)

    # Chapter별, subfolder별 그룹화
    by_chapter = defaultdict(lambda: defaultdict(list))
    for item in classifications:
        chapter = item['chapter']
        subfolder = item['subfolder']
        by_chapter[chapter][subfolder].append(item)

    # 각 Chapter의 resources.md 생성
    created_count = 0
    for chapter, files_by_subfolder in sorted(by_chapter.items()):
        resources_md = generate_resources_md(chapter, files_by_subfolder)

        output_path = os.path.join(TARGET_DIR, chapter, 'resources.md')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(resources_md)

        total_files = sum(len(files) for files in files_by_subfolder.values())
        print(f"✅ Generated: {chapter}/resources.md ({total_files} files)")
        created_count += 1

    print(f"\n✅ All resources.md files generated ({created_count} chapters)")
    return created_count

if __name__ == '__main__':
    count = main()
    exit(0 if count > 0 else 1)
