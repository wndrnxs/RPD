# 02 · 바로 복사해서 쓰는 프롬프트

> **네거티브 프롬프트 입력란이 있는 툴 전용입니다** (Stable Diffusion 계열, Leonardo, Midjourney 등).
> 제미나이·ChatGPT·Claude를 쓰신다면 → **[03-gemini.md](03-gemini.md)** 를 보세요.
>
> 설계 의도와 검증 기준은 [00-style-sheet.md](00-style-sheet.md) · [01-towers.md](01-towers.md) 참조.

## 순서

```
STEP 0  스타일 시트 2~3장을 먼저 뽑아 고정   ← 여기부터
STEP 1  ① 감시 초소 (최약체)
STEP 2  ⑩ 왕좌 (최강체)          ← 격차를 먼저 확정
STEP 3  나머지 8종을 그 사이에 배치
```

**STEP 1부터는 STEP 0에서 채택한 이미지를 스타일 레퍼런스로 반드시 첨부하세요.**
안 그러면 10종이 각각 다른 게임처럼 보입니다.

---

## 공통 네거티브 프롬프트

**모든 생성에 동일하게 넣습니다.** 아래 프롬프트에는 포함되어 있지 않으니 별도 입력란에 넣으세요.

```
3d render, smooth gradients, anti-aliasing, blurry, soft focus, photorealistic, painterly, purple glow, colored light, saturated neon, rainbow, oversaturated, text, letters, numbers, watermark, signature, logo, ui elements, health bar, multiple buildings, cluttered background, scenery, sky, clouds, horizon, casino, poker chips, playing cards, gambling, roulette, slot machine, dice, money, human figure, character, creature, cropped, cut off, tilted
```

---

## ⚠️ 네거티브 프롬프트를 어디에 넣는가

**본문 프롬프트와 절대 이어붙이지 마세요.** 툴에 따라 넣는 위치가 다릅니다.

| 툴 | 방법 |
|---|---|
| Stable Diffusion 계열 (A1111 · ComfyUI · Forge), Leonardo, NightCafe, Krea | **Negative prompt 입력란**에 따로 붙여넣기 |
| Midjourney | 본문 끝에 `--no` 를 붙이고 그 뒤에 나열 |
| ChatGPT(DALL·E · GPT Image), Gemini(Nano Banana), Claude | **네거티브 입력란이 없음** → 아래 "통합 버전" 사용 |

**Midjourney 예시**

```
[STEP 0 본문] --no 3d render, smooth gradients, anti-aliasing, photorealistic, purple glow, colored light, oversaturated, text, watermark, ui elements, multiple buildings, cluttered background, sky, casino, poker chips, playing cards, gambling, dice, human figure, cropped
```

추가로 `--ar 1:1 --stylize 250` 정도를 권장합니다.

---

## 제미나이 · ChatGPT · Claude를 쓰신다면

네거티브 입력란이 없으므로 **[03-gemini.md](03-gemini.md)** 의 프롬프트를 쓰세요.
제약이 자연어 문장으로 재구성되어 있고, 10종 전부 변환되어 있습니다.

**이 파일과 03번 파일을 둘 다 넣으면 안 됩니다. 툴에 맞는 하나만 고르세요.**

---

## STEP 0 · 스타일 시트 (가장 먼저)

```
isometric pixel art game asset, 45 degree isometric projection, 2:1 pixel ratio, detailed 16-bit pixel art style, chunky readable pixels, crisp hard edges, no anti-aliasing, muted desaturated palette, cool grey weathered stone, warm earth and moss tones, pale white-cyan glowing windows and runes as the only bright accent, diamond shaped base plate with visible layered soil cross-section and grass edge, small scattered props on the base plate telling the concept, single centered structure, flat solid sage green background, strong readable silhouette, high value contrast, subtle dithering for shading, top-left key light, dark outline around the structure, soft ambient occlusion at base, a modest stone wizard watchtower, single round tower with a conical slate roof, one pale glowing window, cracked masonry with moss, standing on a diamond base plate of dry earth and sparse grass, a few small rocks and weed tufts scattered around the base
```

**마음에 들 때까지 반복하세요.** 여기서 나온 이미지가 나머지 전부의 기준이 됩니다.
채택하면 시드와 모델명을 [01-towers.md](01-towers.md) 하단 표에 기록하세요.

---


## STEP 1 · 1. 감시 초소 (탑 / High Card)

```
isometric pixel art game asset, 45 degree isometric projection, 2:1 pixel ratio, detailed 16-bit pixel art style, chunky readable pixels, crisp hard edges, no anti-aliasing, muted desaturated palette, cool grey weathered stone, warm earth and moss tones, pale white-cyan glowing windows and runes as the only bright accent, diamond shaped base plate with visible layered soil cross-section and grass edge, small scattered props on the base plate telling the concept, single centered structure, flat solid sage green background, strong readable silhouette, high value contrast, subtle dithering for shading, top-left key light, dark outline around the structure, soft ambient occlusion at base, a small crude stone watchpost, single short square tower with a plain wooden roof, one narrow pale glowing slit window, cracked weathered masonry, a rickety wooden ladder leaning on the side, base plate of dry cracked earth with sparse dead weeds, a few loose rocks and a broken wooden signpost scattered around
```


## STEP 2 · 10. 왕좌 (로열 스트레이트 플러시 / Royal)

```
isometric pixel art game asset, 45 degree isometric projection, 2:1 pixel ratio, detailed 16-bit pixel art style, chunky readable pixels, crisp hard edges, no anti-aliasing, muted desaturated palette, cool grey weathered stone, warm earth and moss tones, pale white-cyan glowing windows and runes as the only bright accent, diamond shaped base plate with visible layered soil cross-section and grass edge, small scattered props on the base plate telling the concept, single centered structure, flat solid sage green background, strong readable silhouette, high value contrast, subtle dithering for shading, top-left key light, dark outline around the structure, soft ambient occlusion at base, a colossal crowned throne of pale marble and dark stone, towering far above all others, five tall crown spires rising in a regal arc, ornate carved filigree and gold trim, a massive central sigil radiating brilliant white authority, floating rings of runes orbiting the crown, grand and imposing, base plate of polished white marble steps with a deep red carpet leading up, golden ornamental patterns inlaid in the marble, two ceremonial braziers flanking the stairs
```


## STEP 3 · 2. 쌍열 포탑 (원 페어 / One Pair)

```
isometric pixel art game asset, 45 degree isometric projection, 2:1 pixel ratio, detailed 16-bit pixel art style, chunky readable pixels, crisp hard edges, no anti-aliasing, muted desaturated palette, cool grey weathered stone, warm earth and moss tones, pale white-cyan glowing windows and runes as the only bright accent, diamond shaped base plate with visible layered soil cross-section and grass edge, small scattered props on the base plate telling the concept, single centered structure, flat solid sage green background, strong readable silhouette, high value contrast, subtle dithering for shading, top-left key light, dark outline around the structure, soft ambient occlusion at base, two identical narrow stone towers standing side by side on one shared foundation, each with a matching pale glowing rune window at the same height, a thin arcane arc of white light connecting the two tops, base plate of packed dirt and short grass, two matching upright rune stones planted symmetrically at the front corners
```


## STEP 4 · 3. 교차 포대 (투 페어 / Two Pair)

```
isometric pixel art game asset, 45 degree isometric projection, 2:1 pixel ratio, detailed 16-bit pixel art style, chunky readable pixels, crisp hard edges, no anti-aliasing, muted desaturated palette, cool grey weathered stone, warm earth and moss tones, pale white-cyan glowing windows and runes as the only bright accent, diamond shaped base plate with visible layered soil cross-section and grass edge, small scattered props on the base plate telling the concept, single centered structure, flat solid sage green background, strong readable silhouette, high value contrast, subtle dithering for shading, top-left key light, dark outline around the structure, soft ambient occlusion at base, four stone pillars arranged as two distinct pairs, one pair clearly taller than the other, the two pairs crossing at right angles, pale glowing runes in two matching styles, crossed white arcane beams linking each pair, base plate with cross shaped cobblestone paving splitting the ground into four quadrants, small stacked stone cairns at the four corners
```


## STEP 5 · 4. 삼연장포 (트리플 / Triple)

```
isometric pixel art game asset, 45 degree isometric projection, 2:1 pixel ratio, detailed 16-bit pixel art style, chunky readable pixels, crisp hard edges, no anti-aliasing, muted desaturated palette, cool grey weathered stone, warm earth and moss tones, pale white-cyan glowing windows and runes as the only bright accent, diamond shaped base plate with visible layered soil cross-section and grass edge, small scattered props on the base plate telling the concept, single centered structure, flat solid sage green background, strong readable silhouette, high value contrast, subtle dithering for shading, top-left key light, dark outline around the structure, soft ambient occlusion at base, three identical stone cannon barrels clustered in a triangular formation on a round tower, three matching pale glowing runes forming a triangle, tri-fold symmetry, one larger white crystal suspended in the center between the three, base plate with a carved triangular magic circle glowing faintly white, three iron candlesticks with lit candles at the triangle points
```


## STEP 6 · 5. 레일 랜스 (스트레이트 / Straight · 백스트레이트 · 마운틴)

```
isometric pixel art game asset, 45 degree isometric projection, 2:1 pixel ratio, detailed 16-bit pixel art style, chunky readable pixels, crisp hard edges, no anti-aliasing, muted desaturated palette, cool grey weathered stone, warm earth and moss tones, pale white-cyan glowing windows and runes as the only bright accent, diamond shaped base plate with visible layered soil cross-section and grass edge, small scattered props on the base plate telling the concept, single centered structure, flat solid sage green background, strong readable silhouette, high value contrast, subtle dithering for shading, top-left key light, dark outline around the structure, soft ambient occlusion at base, a long horizontal rail cannon mounted on a low stone platform, five stepped segments ascending in height along the rail from back to front, a single long focused beam channel with pale white light running its length, five carved runes ascending in size along the side, base plate with iron rails and wooden sleepers embedded in gravel, scattered mechanical parts, a rusted lever and a coil of chain
```


## STEP 7 · 6. 원소 증폭탑 (플러시 / Flush)

```
isometric pixel art game asset, 45 degree isometric projection, 2:1 pixel ratio, detailed 16-bit pixel art style, chunky readable pixels, crisp hard edges, no anti-aliasing, muted desaturated palette, cool grey weathered stone, warm earth and moss tones, pale white-cyan glowing windows and runes as the only bright accent, diamond shaped base plate with visible layered soil cross-section and grass edge, small scattered props on the base plate telling the concept, single centered structure, flat solid sage green background, strong readable silhouette, high value contrast, subtle dithering for shading, top-left key light, dark outline around the structure, soft ambient occlusion at base, a slender spire ringed by five identical floating crystals orbiting in a circle, all five crystals cut in the exact same shape, glowing pale white, unified repeating motif, concentric rings carved into the tower body, amplifier antenna at the top, base plate with a large circular magic circle, the same sigil repeated five times around it, small white crystal shards growing from the ground at the circle edge
```


## STEP 8 · 7. 중력 제단 (풀 하우스 / Full House)

```
isometric pixel art game asset, 45 degree isometric projection, 2:1 pixel ratio, detailed 16-bit pixel art style, chunky readable pixels, crisp hard edges, no anti-aliasing, muted desaturated palette, cool grey weathered stone, warm earth and moss tones, pale white-cyan glowing windows and runes as the only bright accent, diamond shaped base plate with visible layered soil cross-section and grass edge, small scattered props on the base plate telling the concept, single centered structure, flat solid sage green background, strong readable silhouette, high value contrast, subtle dithering for shading, top-left key light, dark outline around the structure, soft ambient occlusion at base, a heavy stone altar with three thick columns supporting a raised platform, two smaller pillars standing on top of that platform, a dark heavy orb suspended in the center emitting pale white gravitational rings, massive and grounded, three-plus-two tiered structure, base plate with the ground cracked and pulled inward toward the center, small rocks and pebbles floating in mid-air above the cracks
```


## STEP 9 · 8. 사방 요새 (포 카드 / Four Card)

```
isometric pixel art game asset, 45 degree isometric projection, 2:1 pixel ratio, detailed 16-bit pixel art style, chunky readable pixels, crisp hard edges, no anti-aliasing, muted desaturated palette, cool grey weathered stone, warm earth and moss tones, pale white-cyan glowing windows and runes as the only bright accent, diamond shaped base plate with visible layered soil cross-section and grass edge, small scattered props on the base plate telling the concept, single centered structure, flat solid sage green background, strong readable silhouette, high value contrast, subtle dithering for shading, top-left key light, dark outline around the structure, soft ambient occlusion at base, a fortified square keep with four identical cannon barrels facing north south east and west, perfect four-fold radial symmetry, crenellated battlements, thick fortress walls, four matching pale glowing runes one on each face, base plate with stone rampart foundations extending toward all four corners, a small dry moat around the keep, four iron braziers burning white flame
```


## STEP 10 · 9. 프리즘 랜스 (스트레이트 플러시 / Straight Flush · 백스플)

```
isometric pixel art game asset, 45 degree isometric projection, 2:1 pixel ratio, detailed 16-bit pixel art style, chunky readable pixels, crisp hard edges, no anti-aliasing, muted desaturated palette, cool grey weathered stone, warm earth and moss tones, pale white-cyan glowing windows and runes as the only bright accent, diamond shaped base plate with visible layered soil cross-section and grass edge, small scattered props on the base plate telling the concept, single centered structure, flat solid sage green background, strong readable silhouette, high value contrast, subtle dithering for shading, top-left key light, dark outline around the structure, soft ambient occlusion at base, an elongated crystalline rail lance, five ascending prism segments in a row, all five prisms identical in cut and facet pattern, refracting pale white light into a spectrum, a continuous beam channel splitting along its length, sleek and precise, elevated polished stone platform with sequential carved sigils, base plate with rails inlaid with embedded white crystals, glowing prism shards jutting from the ground alongside the track
```


---

## 생성 파라미터 권장값

| 항목 | 값 | 비고 |
|---|---|---|
| 해상도 | 1024 × 1024 | 정사각. 축소는 나중에 |
| 스타일 강도 | 중~강 | 레퍼런스 이미지를 첨부했을 때 |
| 시드 | **고정해서 기록** | 나중에 수정하려면 반드시 필요 |

## 생성 후 반드시 확인할 것 2가지

1. **발광부가 흰빛인가** — 보라·청색으로 나왔으면 재생성하세요.
   셰이더 틴트가 그 위에 덧칠되어 4속성이 전부 탁해집니다.
2. **타일 크기로 축소해도 구분되는가** — 1024px에서 멋있어도 축소하면 뭉개지는 경우가 대부분입니다.
   nearest neighbor로 축소해서 눈을 가늘게 뜨고 확인하세요.

나머지 검증 항목은 [01-towers.md](01-towers.md)의 체크리스트를 쓰세요.
