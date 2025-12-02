#!/usr/bin/env python3
import os
import json
import subprocess
from pathlib import Path

RESEARCH_DIR = "/home/amanoops/paper-projects/anto/research"
TARGET_DIR = "/home/amanoops/paper-projects/anto/project/02-research"
CLASSIFICATION_MAP = "classification_map.json"
LINK_MAPPING_FILE = "link_mapping.json"

def execute_git_mv(src, dst, dry_run=False):
    """git mv 실행 (히스토리 보존)"""
    # 목적지 디렉터리 생성
    dst_dir = os.path.dirname(dst)
    if not dry_run:
        os.makedirs(dst_dir, exist_ok=True)

    cmd = ['git', 'mv', src, dst]

    if dry_run:
        print(f"[DRY-RUN] {' '.join(cmd)}")
        return True
    else:
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, cwd="/home/amanoops/paper-projects/anto")
            print(f"✅ Moved: {os.path.basename(src)} → {os.path.relpath(dst, TARGET_DIR)}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error moving {os.path.basename(src)}: {e.stderr.decode().strip()}")
            return False

def main(dry_run=True, filter_chapter=None):
    # classification_map.json 로드
    with open(CLASSIFICATION_MAP, 'r', encoding='utf-8') as f:
        classifications = json.load(f)

    link_mapping = {}
    success_count = 0
    fail_count = 0

    for item in classifications:
        chapter = item['chapter']

        # 필터 적용
        if filter_chapter and chapter != filter_chapter:
            continue

        # Unclassified 스킵
        if chapter == 'Unclassified':
            continue

        # 경로 구성
        src = os.path.join(RESEARCH_DIR, item['original_path'])
        dst = os.path.join(TARGET_DIR, item['path'])

        # 파일 존재 확인
        if not os.path.exists(src):
            print(f"⚠️  파일 없음: {src}")
            fail_count += 1
            continue

        # git mv 실행
        if execute_git_mv(src, dst, dry_run):
            success_count += 1
            # 링크 매핑 기록
            old_link = f"../../research/{item['filename']}"
            new_link = f"./{item['path']}"
            link_mapping[old_link] = new_link
        else:
            fail_count += 1

    # 링크 매핑 저장
    if not dry_run:
        with open(LINK_MAPPING_FILE, 'w', encoding='utf-8') as f:
            json.dump(link_mapping, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Link mapping saved to: {LINK_MAPPING_FILE}")

    print(f"\n=== Summary ===")
    print(f"Success: {success_count}")
    print(f"Fail: {fail_count}")
    print(f"Total: {success_count + fail_count}")

    return success_count, fail_count

if __name__ == '__main__':
    import sys

    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    execute = '--execute' in sys.argv or '-e' in sys.argv
    filter_chapter = None

    for arg in sys.argv[1:]:
        if arg.startswith('--filter='):
            filter_chapter = arg.split('=')[1]

    if execute:
        dry_run = False
    else:
        dry_run = True

    mode = "DRY-RUN" if dry_run else "EXECUTE"
    print(f"=== Migration Mode: {mode} ===")
    if filter_chapter:
        print(f"Filter: {filter_chapter}")

    success, fail = main(dry_run=dry_run, filter_chapter=filter_chapter)
    exit(0 if fail == 0 else 1)
