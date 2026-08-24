# 02 · 기술 아키텍처 (Godot 4)

## 1. 스택 선정 근거

| 항목 | 선택 | 이유 |
|---|---|---|
| 엔진 | **Godot 4.x (stable 최신)** | 무료·오픈소스, 로열티 0, Android/iOS/Windows/macOS/Linux 원스톱 익스포트, 2D 성능 충분 |
| 언어 | **GDScript** | 이 규모의 2D 게임에서 C# 대비 iOS 익스포트 리스크가 낮고 반복 속도가 빠름. 병목 발견 시 해당 부분만 GDExtension(C++)으로 교체 |
| 렌더 | 2D (Forward+ 또는 Mobile 렌더러) | 모바일 타깃이면 **Mobile 렌더러** 권장 |
| 테스트 | **GUT** (Godot Unit Test) | 족보 판정기·데미지 계산 등 순수 로직의 회귀 방지 |
| 버전 관리 | Git + Git LFS (아트 에셋) | |
| 아트 | **AI 생성 + 후처리 스크립트** | 1인 개발 전제. 9절 참조 |
| 결제 | Google Play Billing / StoreKit (Steam은 없음) | 10절 참조 |

> **주의:** Godot의 C# 빌드는 iOS 익스포트 파이프라인이 GDScript 대비 손이 더 갑니다.
> 팀에 강한 C# 선호가 없다면 GDScript로 시작하는 게 출시까지의 리스크가 낮습니다.

---

## 2. 프로젝트 구조

```
res://
├── autoload/                    # 싱글턴 (Project Settings > Autoload)
│   ├── GameState.gd             # 현재 스테이지/라운드/골드/라이프 등 런타임 상태
│   ├── EventBus.gd              # 전역 시그널 허브 (UI ↔ 게임로직 디커플링)
│   ├── SaveManager.gd           # user:// 세이브 로드/저장
│   ├── AudioManager.gd          # BGM/SFX 버스 관리
│   └── Rng.gd                   # 결정론적 RNG 스트림 관리
│
├── core/                        # ★ 엔진 비의존 순수 로직 (Node 상속 금지, RefCounted 기반)
│   ├── poker/
│   │   ├── Card.gd              # rank(2~14), suit(0~3), 값 객체
│   │   ├── Deck.gd              # 셔플, 딜, 제외 풀 관리
│   │   ├── HandRank.gd          # enum + 상수
│   │   └── HandEvaluator.gd     # 5장 → 족보 판정 (순수 함수) ★ 최우선 테스트 대상
│   ├── combat/
│   │   ├── Element.gd           # 4속성 + 상성 매트릭스
│   │   ├── TowerBuilder.gd      # 최종 5장 → TowerStats 변환
│   │   └── DamageCalc.gd        # 상성/방어력/치명타/보정 적용
│   ├── economy/
│   │   └── CostCurve.gd         # 건설 비용, 강화 비용, 보상 공식
│   └── sim/
│       └── HandSimulator.gd     # 몬테카를로 족보 확률 시뮬레이터 (M0 산출물)
│
├── data/                        # ★ 커스텀 Resource (.tres) — 밸런싱은 전부 여기서
│   ├── towers/                  # TowerDef.tres × 10 (족보별)
│   ├── enemies/                 # EnemyDef.tres
│   ├── waves/                   # WaveDef.tres
│   ├── stages/                  # StageDef.tres (라운드 수, 경로, 웨이브 목록, 컨셉)
│   ├── artifacts/               # ArtifactDef.tres
│   ├── characters/              # CharacterDef.tres
│   ├── equipment/               # EquipmentDef.tres
│   └── schema/                  # Resource 클래스 정의 (.gd)
│
├── scenes/
│   ├── game/
│   │   ├── GameScene.tscn       # 전투 씬 루트
│   │   ├── Board.tscn           # 타일 그리드 + 경로
│   │   ├── Tile.tscn
│   │   ├── Tower.tscn           # 데이터 주도 (TowerDef 주입)
│   │   ├── Enemy.tscn           # 데이터 주도
│   │   └── Projectile.tscn
│   ├── ui/
│   │   ├── HUD.tscn
│   │   ├── BuildSheet.tscn      # 카드 선택/리드로우 시트
│   │   ├── CardView.tscn
│   │   ├── TowerInspector.tscn  # 전술 강화 / 타겟팅 / 철거
│   │   ├── WavePreview.tscn
│   │   └── ArtifactPicker.tscn
│   └── meta/
│       ├── MainMenu.tscn
│       ├── StageSelect.tscn
│       ├── Collection.tscn      # 캐릭터/장비
│       └── Loadout.tscn         # 스테이지 진입 전 편성
│
├── systems/                     # 씬에 붙는 매니저 (Node 상속 O)
│   ├── WaveSpawner.gd
│   ├── PathService.gd
│   ├── TargetingGrid.gd         # 공간 분할 브로드페이즈
│   ├── ObjectPool.gd
│   └── RoundController.gd       # 라운드 시작/종료, 전술 강화 리셋
│
├── tests/                       # GUT
│   ├── test_hand_evaluator.gd
│   ├── test_damage_calc.gd
│   ├── test_cost_curve.gd
│   └── test_deck_exclusion.gd   # "버려진 카드 재출현 금지" 검증
│
└── assets/                      # art, audio, fonts (Git LFS)
```

### 핵심 원칙: `core/`는 엔진에 의존하지 않는다

`core/` 안의 코드는 `Node`, `Scene`, `Viewport` 등을 절대 참조하지 않습니다.
`RefCounted` / `Resource`만 사용합니다. 그래서:

- **헤드리스로 테스트 가능** — `godot --headless` 로 CI에서 족보 판정 수천 케이스 검증
- **시뮬레이터 재사용 가능** — 같은 코드로 몬테카를로 밸런스 시뮬레이션 실행
- **엔진 교체 시 자산이 남음** — 만약 나중에 다른 엔진으로 옮기더라도 룰 정의는 그대로 이식

---

## 3. 데이터 스키마

밸런싱을 **코드 수정 없이** 하려면 모든 수치가 Resource여야 합니다.

```gdscript
# data/schema/tower_def.gd
class_name TowerDef extends Resource

@export var hand_rank: int              # HandRank enum
@export var display_name: String
@export var base_dps: float
@export var range_tiles: float
@export var attack_pattern: int         # SINGLE / MULTI / BURST / PIERCE / AOE / OMNI / GLOBAL
@export var targets_per_shot: int = 1
@export var projectile_scene: PackedScene
@export var sprite: Texture2D
```

```gdscript
# data/schema/stage_def.gd
class_name StageDef extends Resource

@export var stage_id: String
@export var display_name: String
@export var round_count: int                    # ★ 스테이지마다 가변
@export var path_points: PackedVector2Array     # 타일 좌표 기준 경로
@export var blocked_tiles: PackedVector2Array   # 건설 금지 구역
@export var waves: Array[WaveDef]
@export var miniboss_rounds: PackedInt32Array   # 기본 [10, 20, ...]
@export var boss_wave: WaveDef                  # 최종 라운드
@export var star_conditions: Array[StarCondition]
@export var starting_gold: int = 200
@export var starting_life: int = 20
```

```gdscript
# data/schema/enemy_def.gd
class_name EnemyDef extends Resource

@export var enemy_type: int      # NORMAL / ARMORED / SWIFT / SWARM / REGEN / STEALTH / BOSS
@export var element: int         # SPADE / CLUB / HEART / DIAMOND
@export var base_hp: float
@export var armor: float
@export var move_speed: float    # 타일/초
@export var gold_reward: int
@export var life_damage: int = 1
```

**밸런스 데이터 워크플로 제안:** `.tres`를 직접 손으로 편집하는 건 고통스럽습니다.
`balance/*.csv` → `.tres` 임포트 스크립트를 두면 스프레드시트에서 밸런싱하고
한 번에 반영할 수 있습니다. (M2 즈음 도입 권장)

---

## 4. 결정론적 RNG

```gdscript
# autoload/Rng.gd — 스트림 분리가 중요합니다
var _streams: Dictionary = {}   # "cards" / "waves" / "artifacts" / "crit"

func stream(name: String) -> RandomNumberGenerator
```

- 스테이지 진입 시 마스터 시드 1개 생성 → 각 스트림은 `hash(master_seed + name)`으로 초기화
- **왜 스트림을 분리하나:** 치명타 판정이 카드 셔플 RNG를 소모하면, 전투 결과가 카드 결과를
  바꿔버려 재현이 불가능해집니다. 버그 리포트("이 시드에서 이상한 카드가 나와요")를
  재현하려면 반드시 분리해야 합니다.
- 세이브에 마스터 시드를 기록 → 재현 가능한 버그 리포트, 나중에 리플레이/일일 챌린지 확장 여지

---

## 5. 성능 예산 (모바일 기준)

목표: **중급 안드로이드 기기에서 60fps**, 배속 3× 상태에서도 유지.

| 항목 | 예산 |
|---|---|
| 동시 몬스터 | 80체 (군집 웨이브 기준) |
| 동시 투사체 | 200개 |
| 타워 | 40기 |
| 드로우콜 | < 100 |

**필수 최적화 4가지**

1. **오브젝트 풀링** — 몬스터/투사체/데미지 숫자는 절대 런타임 `instantiate()` 하지 않습니다.
   씬 시작 시 예산만큼 미리 생성해두고 `visible` + 활성 플래그로 재사용.
2. **물리 엔진 미사용** — `Area2D`/`CharacterBody2D` 대신 직접 위치 계산.
   타워 사거리 판정은 **제곱 거리 비교** (`sqrt` 호출 제거).
3. **그리드 브로드페이즈** — 타워마다 전체 몬스터를 순회하면 40×80 = 3200회/프레임.
   맵을 4×4타일 셀로 나눠 몬스터를 등록하고, 타워는 사거리에 걸치는 셀만 조회.
4. **타겟 재탐색 주기 제한** — 매 프레임이 아니라 **0.1초마다** 또는 현재 타겟이
   죽거나 사거리를 벗어날 때만 재탐색.

**추가:**
- 몬스터 이동은 `Path2D` + `PathFollow2D` 대신 **경로 포인트 배열 + 수동 보간**이 더 빠르고 제어가 쉽습니다.
- 배속 구현은 `Engine.time_scale`이 아니라 **자체 `game_speed` 배수를 delta에 곱하는 방식**으로.
  (`time_scale`은 UI 애니메이션과 트윈까지 같이 빨라져서 조작감이 망가집니다.)
- 텍스처 아틀라스로 묶어 드로우콜 억제.

---

## 6. 세이브 데이터

- 위치: `user://save_v1.json` (플랫폼별 경로는 Godot이 처리)
- 내용: 캠페인 진행도, 별점, 보유 캐릭터/장비 및 강화 수치, 설정, 통계
- **전투 중 세이브는 라운드 경계에서만** — 라운드 중간 상태 직렬화는 복잡도 대비 이득이 적습니다.
  앱이 백그라운드로 가면 자동 일시정지 후 "라운드 재시작" 옵션 제공.
- 버전 필드 + 마이그레이션 함수를 **처음부터** 넣습니다. 나중에 넣으면 이미 늦습니다.
- 무결성: 단순 체크섬. 싱글 플레이 게임이므로 강한 안티치트는 투자 대비 효용이 낮습니다.

---

## 7. 플랫폼 익스포트

| 플랫폼 | 필요 사항 | 주의 |
|---|---|---|
| **Android** | Godot Android Build Template, JDK, Android SDK, 키스토어 | Play 스토어는 **AAB** 필수. 타깃 API 레벨 정책이 매년 오르므로 출시 시점 확인 |
| **iOS** | **macOS 머신 + Xcode 필수**, Apple Developer 계정(연 $99) | Godot에서 Xcode 프로젝트를 뽑고 Xcode에서 아카이브. 원격 빌드 서비스로 우회 가능하나 디버깅이 어려움 |
| **Steam (Win/Mac/Linux)** | Steamworks 파트너 등록(작품당 $100), **GodotSteam** 또는 Steamworks GDExtension | 업적/클라우드 세이브 쓸 거면 GodotSteam. 안 쓸 거면 순정 Godot 빌드로도 출시 가능 |

**입력 대응 (Steam 대비)**
모바일 세로 우선이지만 Steam 출시를 하려면 처음부터 대비해야 합니다:
- 입력을 **Godot InputMap 액션**으로 추상화 (직접 `InputEventScreenTouch` 처리 금지)
- 마우스 = 탭, 키보드 단축키(배속, 다음 라운드, 카드 1~8 선택) 추가
- 게임패드는 커서 이동 방식으로 지원 (Steam Deck 검증 노림)
- 가로 화면에서는 보드를 중앙에 두고 좌우에 패널 배치 — **레이아웃을 처음부터 컨테이너 기반으로**

**현지화**
- 처음부터 `tr()` + CSV 번역 파일. 한국어/영어 2개로 시작.
- 하드코딩된 문자열이 코드에 섞이면 나중에 뽑아내는 비용이 큽니다.

---

## 8. CI (선택, 권장)

GitHub Actions에서:
1. `godot --headless --script tests/run_tests.gd` → GUT 유닛 테스트
2. `gdlint` / `gdformat` (godot-gdscript-toolkit)
3. (선택) 태그 푸시 시 Android APK 빌드 아티팩트 업로드

족보 판정기 하나만 깨져도 게임 전체가 무너지므로, **테스트 자동화는 사치가 아니라 필수**입니다.

---

## 9. AI 아트 파이프라인 (1인 개발 전제)

AI 생성은 **잘하는 것과 못하는 것이 명확히 갈립니다.** 못하는 영역에 시간을 쓰면
일정이 통째로 날아갑니다.

| AI가 잘하는 것 | AI가 못하는 것 |
|---|---|
| 배경 일러스트, 스테이지 아트 | **일관된 스프라이트 시트** |
| UI 프레임, 아이콘, 버튼 | **프레임 애니메이션** |
| 몬스터 · 캐릭터 정지 일러스트 | **타일링되는 지형 타일** |
| 아티팩트 · 장비 아이콘 | 48px에서 구분되는 소형 스프라이트 |
| 스토어 프로모션 아트 | 여러 장에 걸친 캐릭터 동일성 |

### 9.1 일관성 확보 — 가장 큰 함정

AI 아트 프로젝트가 실패하는 이유의 대부분은 **스타일이 조금씩 흘러가서**
나중에 보면 같은 게임 같지 않다는 것입니다.

1. **스타일 시트를 먼저 만듭니다.** 대표 이미지 3~5장을 뽑아 확정하고,
   이후 모든 생성에 그 이미지를 레퍼런스로 넣습니다.
2. **프롬프트를 파일로 관리합니다.** `assets/_prompts/` 에 에셋별 프롬프트와 시드를
   텍스트로 저장 → 나중에 재생성/수정이 가능해집니다. 이걸 안 하면 6개월 뒤
   "이 이미지를 어떻게 만들었더라"가 됩니다.
3. **색 팔레트를 고정합니다.** 생성 후 팔레트 강제 적용 스크립트를 한 번 짜두면
   출처가 다른 이미지들이 같은 세계관으로 묶입니다.

### 9.2 ★ 무채색 스프라이트 + 셰이더 틴트

**이 프로젝트에서 가장 큰 절약 지점입니다.**

타워는 족보 10종 × 속성 4종 = **40가지 조합**입니다. 이걸 전부 그리면 AI 일관성이
반드시 무너집니다. 대신:

1. 타워 스프라이트를 **무채색(회색조)으로 10장만** 만듭니다
2. 속성 색은 **런타임 셰이더로 틴트**합니다

```gdscript
# 간단한 틴트 셰이더 — 무채색 스프라이트에 속성 색을 입힘
shader_type canvas_item;
uniform vec4 element_color : source_color;
uniform float tint_strength : hint_range(0.0, 1.0) = 0.85;

void fragment() {
    vec4 tex = texture(TEXTURE, UV);
    float luma = dot(tex.rgb, vec3(0.299, 0.587, 0.114));
    COLOR = vec4(mix(tex.rgb, element_color.rgb * luma * 2.0, tint_strength), tex.a);
}
```

**효과: 40장 → 10장.** 작업량이 1/4로 줄고, 일관성 문제가 발생할 표면적도 1/4이 됩니다.
같은 기법을 몬스터(유형 7종 × 속성 4종 = 28 → 7장)에도 적용합니다.

### 9.3 애니메이션은 AI가 아니라 코드로

AI는 프레임 애니메이션을 만들지 못합니다. 대신 Godot에서:

| 표현 | 방법 |
|---|---|
| 타워 발사 | `Tween`으로 스케일 펀치 + 총구 섬광 스프라이트 |
| 몬스터 걷기 | 스프라이트를 위아래로 살짝 바운스 + 좌우 기울임 |
| 피격 | 셰이더 화이트 플래시 + 넉백 트윈 |
| 카드 뒤집기 | `scale.x`를 1 → 0 → 1로 트윈하며 중간에 텍스처 교체 |
| 보스 | `Skeleton2D` 로 파츠 분리 후 리깅 (정지 이미지 1장에서 파츠만 잘라내면 됨) |

**정지 이미지 1장 + 코드 움직임**이 이 프로젝트의 기본 원칙입니다.
프레임 애니메이션은 보스 등장 연출 정도에만 예외적으로 씁니다.

### 9.4 후처리 스크립트화

생성 → 사용 사이의 수작업을 스크립트로 만들어두면 반복 비용이 사라집니다.

```
1. 생성 (고해상도, 예: 1024×1024)
2. 배경 제거 (rembg 등)
3. 팔레트 강제 적용
4. 다운스케일 (48px 타일용은 nearest, UI는 lanczos)
5. 아틀라스 패킹
```

4번의 다운스케일 방식이 중요합니다. 48px 스프라이트를 부드럽게 축소하면 뭉개져서
실루엣 구분이 사라집니다. **축소 후 반드시 실제 크기로 확인**하세요.

### 9.5 법적 · 정책 사항 ⚠️

| 항목 | 내용 |
|---|---|
| **Steam** | AI 생성 콘텐츠 **공시 의무**가 있습니다. 스토어 등록 시 어떤 AI를 어디에 썼는지 신고해야 하며, 누락 시 심사 지연/거부 사유가 됩니다 |
| **Google Play / App Store** | 정책이 계속 갱신 중입니다. 출시 시점에 반드시 최신 정책을 확인하세요 |
| **저작권** | 순수 AI 생성물은 저작권 보호를 받지 못할 수 있습니다(미국 저작권청 입장). 상업 출시 자체에는 문제가 없지만, **에셋 도용에 대한 법적 대응이 어려울 수 있습니다** |
| **생성 툴 약관** | 사용하는 서비스의 상업적 이용 허용 여부와 조건을 출시 전에 확인하세요. 유료 플랜에서만 상업 이용을 허용하는 경우가 많습니다 |
| **음악** | AI 생성 음악은 이미지보다 정책 리스크가 큽니다. 라이선스 에셋 구매를 권장합니다 |

---

## 10. 인앱 결제 (IAP)

[01 문서 8.4절](01-game-design.md)의 수익 모델을 구현하기 위한 기술 사항입니다.

### 10.1 플랫폼별 구현

| 플랫폼 | 방식 | 리스크 |
|---|---|---|
| Android | Google Play Billing (Godot Android 플러그인) | 플러그인이 Godot 버전에 종속. 엔진 업그레이드 시 깨질 수 있음 |
| iOS | StoreKit (Godot iOS 플러그인) | 위와 동일 + macOS 빌드 환경 필요 |
| Steam | **IAP 없음** — 단품 판매 | 해당 없음 |

> Godot의 IAP 플러그인 생태계는 Unity만큼 성숙하지 않습니다.
> **일정에 최소 1주 이상의 버퍼**를 두세요. 여기서 예상보다 오래 걸리는 경우가 흔합니다.

### 10.2 구현 원칙

- **`monetization_profile` 플래그**로 모바일/Steam 빌드를 분기합니다.
  Steam 빌드는 패스 보상이 처음부터 전부 해금된 상태로 시작합니다.
- **구매 복원(Restore Purchases)** 은 iOS 심사 필수입니다. 빼먹으면 반려됩니다.
- 영수증 검증은 **로컬 검증으로 시작**합니다. 싱글 플레이 게임이라 서버 검증의
  투자 대비 효용이 낮습니다. 매출이 의미 있게 나오면 그때 서버를 붙입니다.
- 구매 상태는 세이브가 아니라 **스토어에서 복원**하는 것이 원칙입니다.
  세이브 파일이 날아가도 구매한 것은 살아있어야 합니다.
- 결제 실패/취소/중복 경로를 전부 처리하세요. 여기서 버그가 나면 환불과 악평이 직결됩니다.
