---
description: 인하대병원 퀴즈노스 프로젝트용 PPT 워크플로(00~03 단계)를 세션에 세팅하고, 현재까지 산출물을 요약한 뒤 다음 할 일을 제안합니다.
model: claude-3.5-sonnet
argument-hint: "[project-path]"
---

아래는 이 레포에서 사용하는 PPT 워크플로입니다.

- 00 인테이크 → 01 1차 목차 구성 → 02 리서치(R1~R6) → 03 리서치 요약·브리프 압축 → 04 2차 목차 구성

이번 명령은 **projects/project-quiznote-inha-hospital**를 기본 대상으로 합니다.
필요하면 인자로 다른 프로젝트 경로를 넘길 수 있습니다.

## 1. 프로젝트 기본 컨텍스트

프로젝트 루트는 기본적으로 `projects/project-quiznote-inha-hospital`로 가정합니다.
필요 시 사용자가 인자로 전달한 경로를 우선합니다.

프로젝트 구조:
- 브리프: @projects/project-quiznote-inha-hospital/00-intake/brief.md
- 1차 목차: @projects/project-quiznote-inha-hospital/01-outline-first/outline-v1.md
- 리서치 결과:
  - R1: @projects/project-quiznote-inha-hospital/02-research/R1-hospital-fnb-strategy.md
  - R2: @projects/project-quiznote-inha-hospital/02-research/R2-quiznos-brand-strategy.md
  - R3: @projects/project-quiznote-inha-hospital/02-research/R3-customer-segments-strategy.md
  - R4: @projects/project-quiznote-inha-hospital/02-research/R4-competition-benchmark.md
  - R5: @projects/project-quiznote-inha-hospital/02-research/R5-evidence-insights.md
  - R6: @projects/project-quiznote-inha-hospital/02-research/R6-storyline-outline.md
- 리서치 요약(03 단계 초안): @projects/project-quiznote-inha-hospital/03-synthesis/00-research-synthesis.md

## 2. 너의 작업

1. 위 파일들을 읽고, 현재까지의 **00~02 단계 인풋 + R1~R6 리서치 결과**를 한눈에 이해할 수 있도록 요약해 주세요.
   - 프로젝트 목표, 성공 기준
   - 상권·고객, 경쟁 구도, 타깃 세그먼트 요약
   - 퀴즈노스 브랜드/메뉴 강점 요약
   - 주요 숫자/증거(필요한 것만) 정리
2. @projects/project-quiznote-inha-hospital/03-synthesis/00-research-synthesis.md 파일의
   각 섹션을 채우기 위한 내용을 제안해 주세요.
   - 1. 요약 브리프 (5~7줄)
   - 2. 리서치 참조 맵에서 틀린 부분이 있으면 수정 제안
   - 3. R1~R6별 핵심 인사이트 3~5개씩 체크리스트 형태로 정리
3. 마지막으로, 04 단계(2차 목차 구성)를 시작할 때
   - 어떤 순서로 목차를 다듬을지
   - 어느 섹션에 어떤 리서치 결과를 우선 연결해야 할지
   를 3~5단계 정도의 TODO 리스트로 정리해 주세요.

## 3. 출력 형식

- 섹션 A: 프로젝트 요약 (3~5문단)
- 섹션 B: `00-research-synthesis.md`에 채워 넣을 제안 텍스트
  - 1. 요약 브리프
  - 3. R코드별 핵심 인사이트 목록
- 섹션 C: 04 2차 목차 구성을 위한 다음 단계 TODO 3~5개

