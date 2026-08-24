# 00 · 스타일 시트 (모든 생성의 기준)

> **이 문서를 먼저 확정하지 않고 개별 에셋을 만들면, 나중에 전부 다시 만들게 됩니다.**
> [03-roadmap.md](../../docs/03-roadmap.md) M-Art 트랙의 첫 번째 작업입니다.

---

## 1. 확정된 스타일

**아이소메트릭 픽셀아트.** 각 타워는 **자기 바닥판(base plate)을 포함**한 하나의 스프라이트입니다.

| 요소 | 기준 |
|---|---|
| 시점 | 아이소메트릭 (2:1 픽셀 비율, 약 45도) |
| 해상도 감각 | 16비트급. 픽셀이 굵고 또렷하며 안티에일리어싱 없음 |
| 팔레트 | **채도를 낮춘** 차가운 회색 석재 + 따뜻한 흙색. 강조색 1개만 채도 높게 |
| 조명 | 좌상단 키라이트 + 창문·룬에서 나오는 부드러운 발광 |
| 바닥판 | 다이아몬드형, **흙 단면이 보이는 두께**, 가장자리에 풀 |
| 소품 | 바닥에 작게 흩어진 오브젝트 (돌, 풀, 해골, 상자 등) — 컨셉을 말해주는 장치 |
| 배경 | 단색 세이지 그린 `#8a9a6b` (배경 제거를 쉽게 하기 위함) |
| 외곽선 | 구조물 둘레에 어두운 아웃라인 |

---

## 2. ⚠️ 무채색 방식은 폐기했습니다

**이전 결정:** 타워를 무채색으로 그리고 속성 4색을 셰이더로 전부 덮어씌운다 (10장 → 40조합)

**문제:** 이 방식은 지금 채택한 픽셀아트 스타일과 양립할 수 없습니다.
석재의 따뜻한 갈색, 이끼의 녹색, 흙의 황토색이 전부 속성색으로 물들어버리면
레퍼런스의 그 느낌이 사라집니다. 돌은 돌색이어야 합니다.

**새 방식: 발광부만 틴트합니다.**

| 부위 | 처리 |
|---|---|
| 석재·흙·풀·나무·소품 | **고정 색.** 절대 틴트하지 않음 |
| 창문·룬·수정·마법 이펙트 | **밝은 흰빛으로 생성** → 셰이더가 속성색으로 틴트 |

생성할 때 발광부를 **거의 흰색(pale white-cyan)** 으로 뽑으면,
셰이더가 휘도 임계값으로 그 픽셀만 골라내 ♠보라 / ♥적색 / ♦청색 / ♣초록으로 물들입니다.

```gdscript
// 발광부만 속성색으로 틴트 (무채색 전면 틴트를 대체)
shader_type canvas_item;
uniform vec4 element_color : source_color = vec4(1.0);
uniform float glow_threshold : hint_range(0.0, 1.0) = 0.72;
uniform float softness : hint_range(0.01, 0.5) = 0.12;

void fragment() {
    vec4 tex = texture(TEXTURE, UV);
    float luma = dot(tex.rgb, vec3(0.299, 0.587, 0.114));
    // 밝은 픽셀일수록 강하게 물듦. 어두운 석재는 그대로 남음
    float mask = smoothstep(glow_threshold - softness, glow_threshold + softness, luma);
    vec3 tinted = mix(tex.rgb, element_color.rgb * (0.6 + luma * 0.8), mask);
    COLOR = vec4(tinted, tex.a);
}
```

**절감 효과는 그대로입니다.** 10종 × 4속성 = 40장이 아니라 **10장**만 만들면 됩니다.
바뀐 건 "전체를 물들인다"에서 "빛나는 곳만 물들인다"로, 오히려 더 좋아 보입니다.

> **생성 시 반드시 지킬 것:** 창문·룬·수정을 **보라색이나 특정 색으로 뽑지 마세요.**
> 레퍼런스 이미지처럼 보라색으로 뽑으면 틴트가 보라 위에 덧칠되어 탁해집니다.
> **밝은 흰빛 / 아주 옅은 청백색**으로 생성해야 4속성이 모두 깨끗하게 나옵니다.

---

## 3. 세계관 프레이밍

**"마법사의 제단"이지 "카지노"가 아닙니다.** ([01 문서 8.5~8.6절](../../docs/01-game-design.md))

| 쓸 것 | 쓰지 말 것 |
|---|---|
| 룬, 마법진, 고대 문양, 오벨리스크 | 포커 칩, 룰렛, 카드 테이블 |
| 연금술 기구, 물약병, 촛대, 해골 | 딜러, 바카라, 슬롯머신, 주사위 |
| 이끼 낀 석조, 낡은 목재 | 카드 그 자체를 붙이는 것 |

카드 무늬(♠♥♦♣)는 **바닥 마법진에 각인된 문양**으로만 등장시킵니다.

---

## 4. 공통 프롬프트 블록

**모든 타워 생성 시 아래를 그대로 앞에 붙입니다.**

```
isometric pixel art game asset, 45 degree isometric projection, 2:1 pixel ratio,
detailed 16-bit pixel art style, chunky readable pixels, crisp hard edges, no anti-aliasing,
muted desaturated palette, cool grey weathered stone, warm earth and moss tones,
pale white-cyan glowing windows and runes as the only bright accent,
diamond shaped base plate with visible layered soil cross-section and grass edge,
small scattered props on the base plate telling the concept,
single centered structure, flat solid sage green background,
strong readable silhouette, high value contrast, subtle dithering for shading,
top-left key light, dark outline around the structure, soft ambient occlusion at base
```

**네거티브 프롬프트 (필수)**

```
3d render, smooth gradients, anti-aliasing, blurry, soft focus, photorealistic, painterly,
purple glow, colored light, saturated neon, rainbow, oversaturated,
text, letters, numbers, watermark, signature, logo, ui elements, health bar,
multiple buildings, cluttered background, scenery, sky, clouds, horizon,
casino, poker chips, playing cards, gambling, roulette, slot machine, dice, money,
human figure, character, creature, cropped, cut off, tilted
```

---

## 5. 실루엣이 족보를 말하게 한다 ⭐

**이 프로젝트의 아트 설계 원칙입니다.**

플레이어는 보드를 내려다보며 "저기 투 페어가 몇 개 있지?"를 판단해야 합니다
([01 문서 3.1절](../../docs/01-game-design.md)의 타워 강화 때문에 이 판단이 매우 중요합니다).
그러니 **형태가 족보를 직접 드러내야** 합니다.

| 족보 | 구조가 말하는 것 | 바닥이 말하는 것 |
|---|---|---|
| 탑 | **1개**의 요소 | 메마른 흙, 잡초 — 가장 초라 |
| 원 페어 | 나란한 **2개** | 대칭으로 박힌 룬석 2개 |
| 투 페어 | **2 + 2** 교차 | 십자로 갈라진 포석 |
| 트리플 | 삼각 **3개** | 삼각 마법진, 촛대 3개 |
| 스트레이트 | **5단** 오름차순 | 레일과 침목 |
| 플러시 | **동일 요소 5개** 원형 | 원형 마법진, 같은 수정 5개 |
| 풀 하우스 | 큰 **3** + 작은 **2** | 중력으로 갈라진 바닥, 떠 있는 돌 |
| 포 카드 | **4방향** 대칭 | 사방으로 뻗은 성벽 기초 |
| 스트레이트 플러시 | 5단 + 통일 무늬 | 수정이 박힌 레일 |
| 로열 | **왕관**, 최고 높이 | 대리석 계단, 황금 문양 |

발광색은 셰이더가 덮으므로 **색으로는 족보를 구분할 수 없습니다.**
개수와 형태, 그리고 바닥 컨셉이 유일한 단서입니다.

---

## 6. 생성 워크플로

```
1. 스타일 시트 확정   → 7절의 프롬프트로 대표 2~3장을 먼저 뽑아 고정
2. 개별 생성          → 1024×1024, 스타일 레퍼런스를 항상 첨부
3. 실루엣 검증 ★      → 타일 크기로 축소 → 눈을 가늘게 뜨고 봤을 때 구분되는가?
4. 배경 제거          → 세이지 그린을 키컬러로 제거 (rembg 또는 색상 키)
5. 발광부 확인 ★      → 창문·룬이 충분히 밝은가? (셰이더 마스크가 잡아내야 함)
6. 다운스케일         → nearest neighbor 고정. lanczos 쓰면 픽셀아트가 뭉개짐
7. 아틀라스 패킹
```

**3번과 5번에서 실패하면 되돌아가세요.** 여기서 타협하면 게임 플레이가 망가집니다.

---

## 7. 스타일 시트 생성용 프롬프트

**가장 먼저 이것부터 뽑으세요.** 마음에 들 때까지 반복하고,
채택한 이미지를 이후 모든 생성의 레퍼런스로 씁니다.

```
[4절 공통 프롬프트 블록]
,
a modest stone wizard watchtower, single round tower with a conical slate roof,
one pale glowing window, cracked masonry with moss,
standing on a diamond base plate of dry earth and sparse grass,
a few small rocks and weed tufts scattered around the base
```

**채택 후 반드시 기록:** 모델명 / 시드 / 최종 프롬프트 / 생성 날짜 / 파라미터
