#!/bin/bash

echo "=== Checking Broken Links in project/02-research ==="
echo ""

broken_count=0
checked_count=0
cd /home/amanoops/paper-projects/anto/project/02-research

# 모든 .md 파일에서 상대 경로 링크 추출 및 검증
find . -name "*.md" -type f | while read file; do
    # [텍스트](./상대경로) 패턴 추출
    grep -oP '\[([^\]]+)\]\((\./[^\)]+)\)' "$file" 2>/dev/null | \
    sed 's/.*(\(\.\/[^)]*\))/\1/' | while read link; do
        checked_count=$((checked_count + 1))

        # URL 디코딩 (%20 -> 공백)
        decoded_link=$(echo "$link" | sed 's/%20/ /g')

        # 파일 디렉터리 기준으로 경로 해석
        link_dir=$(dirname "$file")
        full_path="$link_dir/$decoded_link"

        # 경로 정규화
        full_path=$(readlink -m "$full_path")

        if [ ! -f "$full_path" ] && [ ! -d "$full_path" ]; then
            echo "[BROKEN] $file"
            echo "  → Link: $link"
            echo "  → Resolved: $full_path"
            echo ""
            broken_count=$((broken_count + 1))
        fi
    done
done

echo ""
echo "=== Summary ==="
echo "Checked links: $checked_count"
echo "Broken links: $broken_count"

if [ $broken_count -eq 0 ]; then
    echo "✅ No broken links found"
    exit 0
else
    echo "❌ Found broken links"
    exit 1
fi
