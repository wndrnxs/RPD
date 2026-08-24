# 00 · 스타일 시트 (모든 생성의 기준)

> **이 문서를 먼저 확정하지 않고 개별 에셋을 만들면, 나중에 전부 다시 만들게 됩니다.**
> [03-roadmap.md](../../docs/03-roadmap.md) M-Art 트랙의 첫 번째 작업입니다.

---

## 1. 핵심 제약 (타협 불가)

| 제약 | 이유 |
|---|---|
| **무채색(그레이스케일)로 생성** | 속성 4색은 런타임 셰이더로 입힙니다. 10종 × 4속성 = 40장을 **10장으로** 줄이는 핵심 장치 ([02 문서 9.2절](../../docs/02-tech-architecture.md)) |
| **48px에서 실루엣이 구분될 것** | 보드 타일이 48px입니다. 축소해서 안 보이면 그 디자인은 실패입니다 |
| **카지노 이미지 전면 금지** | 연령 등급 리스크 ([01 문서 8.5~8.6절](../../docs/01-game-design.md)). 칩·룰렛·딜러 테이블·슬롯머신 절대 금지 |
| **정지 이미지만** | 애니메이션은 Godot 트윈/셰이더로 처리합니다. AI에게 프레임 애니메이션을 시키지 마세요 |

---

## 2. 세계관 프레이밍

**"마법사의 제단"이지 "카지노"가 아닙니다.**

| 쓸 것 | 쓰지 말 것 |
|---|---|
| 룬, 마법진, 고대 문양, 오벨리스크 | 포커 칩, 룰렛, 카드 테이블 |
| 부유하는 수정, 각인된 석판 | 딜러, 바카라, 슬롯머신 |
| 연금술 기구, 아케인 장치 | "잭팟", "올인" 등 도박 용어 |

카드 무늬(♠♥♦♣)는 **마법 문양처럼** 각인된 형태로만 등장시킵니다.
카드 그 자체를 타워에 붙이지 마세요 — 그게 카지노 연상의 주범입니다.

---

## 3. 공통 프롬프트 블록

**모든 타워 생성 시 아래를 그대로 앞에 붙입니다.** 뒤에 개별 타워 설명을 이어씁니다.

```
arcane stone tower game asset, 3/4 top-down isometric view,
grayscale monochrome only, no color, matte stone and dark metal,
carved runes and glowing arcane sigils, fantasy alchemy device,
strong readable silhouette, centered single object, isolated on plain flat background,
soft top-left key light, subtle ambient occlusion at base,
clean edges, high contrast between form and background,
game sprite, orthographic feel, no perspective distortion
```

**네거티브 프롬프트 (필수)**

```
color, colored, saturated, casino, poker chips, playing cards, gambling,
roulette, slot machine, dealer table, dice, money, coins,
text, letters, numbers, watermark, signature, logo,
busy background, scenery, landscape, multiple objects, cropped, cut off,
blurry, low contrast, flat lighting, photorealistic, human figure
```

---

## 4. 실루엣이 족보를 말하게 한다 ⭐

**이 프로젝트의 아트 설계 원칙입니다.**

플레이어는 보드를 내려다보며 "저기 투 페어가 몇 개 있지?"를 판단해야 합니다
([01 문서 3.1절](../../docs/01-game-design.md)의 타워 강화 때문에 이 판단이 매우 중요해졌습니다).
그러니 **타워의 형태가 족보를 직접 드러내야** 합니다.

| 족보 | 실루엣이 말하는 것 |
|---|---|
| 탑 | **1개**의 요소 |
| 원 페어 | **2개**가 나란히 (쌍) |
| 투 페어 | **2 + 2** (두 쌍이 교차) |
| 트리플 | **3개**가 삼각형 |
| 스트레이트 | **5개**가 계단처럼 오름차순 |
| 플러시 | **하나의 무늬**가 반복 (통일성) |
| 풀 하우스 | **3 + 2** (큰 셋 위에 작은 둘) |
| 포 카드 | **4개**가 사방으로 |
| 스트레이트 플러시 | 계단 + 통일된 무늬 |
| 로열 | **왕관**, 압도적 높이 |

개수를 셀 수 있게 만들면, 플레이어는 색과 무관하게 족보를 읽습니다.
속성 색은 셰이더로 덮어씌워지므로 **색에 의존한 구분은 애초에 불가능**합니다.

---

## 5. 생성 워크플로

```
1. 스타일 시트 확정   → 대표 3~5장을 먼저 뽑아 스타일을 고정
2. 개별 생성          → 1024×1024, 스타일 레퍼런스를 항상 첨부
3. 실루엣 검증 ★      → 48px로 축소 → 눈을 가늘게 뜨고 봤을 때 구분되는가?
4. 배경 제거          → rembg 등
5. 그레이스케일 정규화 → 히스토그램을 맞춰 밝기 편차 제거
6. 다운스케일         → 타일용은 nearest, UI는 lanczos
7. 아틀라스 패킹
```

**3번에서 실패하면 되돌아가세요.** 여기서 타협하면 게임 플레이가 망가집니다.

---

## 6. 스타일 시트 생성용 프롬프트

**가장 먼저 이것부터 뽑으세요.** 마음에 드는 결과가 나올 때까지 반복하고,
채택한 이미지를 이후 모든 생성의 레퍼런스로 씁니다.

```
[공통 프롬프트 블록]
+
a simple arcane stone watchtower, single tall obelisk with one glowing rune,
weathered granite, thin metal bands, small floating crystal above the tip
```

채택 후 기록할 것: **모델명 / 시드 / 최종 프롬프트 / 생성 날짜**
