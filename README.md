# RPD — Royal Poker Defense (가제)

포커 족보로 타워를 만드는 1인용 싱글 타워 디펜스.
Godot 4 / 모바일 세로 우선 / Android · iOS · Steam 출시 목표.

> **▶ 플레이 가능한 프로토타입:** https://claude.ai/code/artifact/47ede4ca-002f-4fe0-801d-0257ccf37a78
> 브라우저에서 바로 돌아갑니다. ([prototype/README.md](prototype/README.md))
>
> **현재 상태: 기획 + M0 시뮬레이션 + 웹 프로토타입.**
> 게임 코드는 아직 없지만, 족보 확률 시뮬레이터(`tools/hand_sim.py`)는 동작하며
> 밸런싱의 기준이 되는 실측 분포가 [01 문서 2.3절](docs/01-game-design.md)에 들어가 있습니다.

## 한 줄 요약

타일을 탭해 타워를 지을 때마다 카드 7장을 받고, 그중 5장을 고른 뒤 리드로우 토큰으로 갈아끼운다.
최종 5장의 **족보가 타워의 종류**를, **무늬가 속성**을, **숫자가 미세 스탯**을 결정한다.
건설 비용은 짓는 개수에 따라 계속 오르지만 족보는 운이므로, 매 건설이 작은 도박이 된다.

## 확정된 설계 축

| 항목 | 결정 |
|---|---|
| 엔진 | Godot 4.x (GDScript) |
| 1차 타깃 | 모바일 세로 (720×1280 기준 해상도) |
| 맵 | 15×20 타일 그리드, 타일 48px, 고정 경로 |
| 포커 룰 | **5장 딜** → 리드로우 토큰 3개로 교체 (한국식 세븐포커 13족보) |
| 리드로우 | 토큰 1개 = 카드 1장. **토큰 교체된 슬롯은 광고로만 재교체**, 광고 교체분은 확정. 버려진 카드는 재출현 없음 |
| 무늬 | 무늬 = **속성**. 공격에 부가 효과만 붙음 (♠관통 · ♥화염 · ♦얼음 · ♣독). **상성 없음** |
| 건설 비용 | 첫 타워 무료, 50G부터 +10G, **15번째부터 +26G** |
| 아티팩트 | 스테이지 시작 시 1회 + 10라운드마다. 스테이지 종료 시 소멸 |
| 진행 구조 | 캠페인 (스테이지 셀렉트, 스테이지별 라운드 수 가변) |
| 보스 | 10라운드마다 미니보스, 스테이지 최종 라운드에 스테이지 보스 |
| 타워 강화 | **종류별 강화** — 원 페어를 올리면 모든 원 페어 타워의 공격력·공격속도가 오름. **승급은 없음**(원 페어가 투 페어가 되지 않음). 스테이지 종료 시 초기화 |
| 메타 성장 | 캐릭터 · 장비 = 콜렉션. 보상은 숫자가 아니라 **룰 변경**(토큰 +1 등) |
| 수익 모델 (v1.0) | 모바일 광고 중심 F2P (가챠 없음). Steam·성장 패스는 출시 후 |
| 개발 인원 | 1인, 아트는 AI 생성 |

## 문서

| 문서 | 내용 |
|---|---|
| [prototype/](prototype/) | 플레이 가능한 웹 프로토타입 (룰 검증용, 최종 코드 아님) |
| [tools/hand_sim.py](tools/hand_sim.py) | 족보 확률 시뮬레이터. `python3 tools/hand_sim.py` |
| [tools/sprite_check.py](tools/sprite_check.py) | AI 생성 스프라이트 검증·후처리. `python3 tools/sprite_check.py <이미지>` |
| [assets/_prompts/](assets/_prompts/) | AI 아트 프롬프트. 제미나이·ChatGPT는 [03-gemini.md](assets/_prompts/03-gemini.md), SD·Midjourney는 [02-ready-to-paste.md](assets/_prompts/02-ready-to-paste.md) |
| [01-game-design.md](docs/01-game-design.md) | 게임 디자인 문서 — 코어 루프, 포커 시스템, 타워/무늬 특성, 경제, 스테이지 구조, 메타 성장 |
| [02-tech-architecture.md](docs/02-tech-architecture.md) | Godot 4 프로젝트 구조, 데이터 스키마, 성능 예산, 플랫폼 익스포트 |
| [03-roadmap.md](docs/03-roadmap.md) | 마일스톤 M0~M7, 각 단계의 산출물과 완료 조건 |
| [04-open-questions.md](docs/04-open-questions.md) | 아직 결정되지 않은 사항과 선택지 |

## 다음 액션

1. **게임 제목 확정** ([04 B-1](docs/04-open-questions.md))
2. **M0 착수** — Godot 스캐폴딩 + 족보 판정기 + 몬테카를로 시뮬레이터
   → 토큰 개수와 실제 족보 분포를 숫자로 확정하는 것이 목표
3. M2 전까지 **아트 스타일 시트** 확정 ([04 B-2](docs/04-open-questions.md))

예상 기간: 전업 5~6개월 / 퇴근 후+주말 12~18개월 ([03 로드맵](docs/03-roadmap.md))
