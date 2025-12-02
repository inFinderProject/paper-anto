#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path

PROJECT_DIR = "/home/amanoops/paper-projects/anto/project"
LINK_MAPPING_FILE = "/home/amanoops/paper-projects/anto/project/02-research/link_mapping.json"

def update_links_in_file(filepath, link_mapping, dry_run=True):
    """파일 내 링크 업데이트"""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes_made = []

    # 링크 패턴: [텍스트](../../research/파일명.md) 또는 ../../research/파일명.md
    for old_link, new_link in link_mapping.items():
        # URL 인코딩 처리
        old_link_encoded = old_link.replace(' ', '%20')

        # 마크다운 링크 형식 [텍스트](../../research/xxx)
        if old_link in content:
            content = content.replace(old_link, new_link)
            changes_made.append(f"  - {old_link} → {new_link}")

        # URL 인코딩된 버전도 처리
        if old_link_encoded in content and old_link_encoded != old_link:
            content = content.replace(old_link_encoded, new_link.replace(' ', '%20'))
            changes_made.append(f"  - {old_link_encoded} → {new_link.replace(' ', '%20')}")

    if content != original_content:
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {os.path.relpath(filepath, PROJECT_DIR)}")
        else:
            print(f"[DRY-RUN] Would update: {os.path.relpath(filepath, PROJECT_DIR)}")

        # 변경사항 출력
        for change in changes_made[:3]:  # 처음 3개만 출력
            print(change)
        if len(changes_made) > 3:
            print(f"  ... and {len(changes_made) - 3} more changes")

        return len(changes_made)

    return 0

def main(dry_run=True):
    # link_mapping.json 로드
    with open(LINK_MAPPING_FILE, 'r', encoding='utf-8') as f:
        link_mapping = json.load(f)

    print(f"Loaded {len(link_mapping)} link mappings")
    print("")

    updated_files = 0
    total_changes = 0

    # project/ 내 모든 .md 파일 스캔
    for root, dirs, files in os.walk(PROJECT_DIR):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                changes = update_links_in_file(filepath, link_mapping, dry_run)
                if changes > 0:
                    updated_files += 1
                    total_changes += changes

    print("")
    print("=== Summary ===")
    print(f"Updated files: {updated_files}")
    print(f"Total link changes: {total_changes}")

    return updated_files

if __name__ == '__main__':
    import sys

    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    execute = '--execute' in sys.argv or '-e' in sys.argv

    if execute:
        dry_run = False

    mode = "DRY-RUN" if dry_run else "EXECUTE"
    print(f"=== Link Update Mode: {mode} ===")
    print("")

    updated = main(dry_run=dry_run)

    if dry_run and updated > 0:
        print("")
        print("⚠️  This was a DRY-RUN. No files were modified.")
        print("   Run with --execute to apply changes.")

    exit(0 if updated >= 0 else 1)
