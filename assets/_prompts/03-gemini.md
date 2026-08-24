# 03 · 제미나이 / ChatGPT / Claude 용 프롬프트

> **네거티브 입력란이 없는 대화형 툴 전용입니다.**
> Stable Diffusion·Leonardo·Midjourney를 쓰신다면 [02-ready-to-paste.md](02-ready-to-paste.md)를 보세요.

## ⚠️ 헷갈리기 쉬운 점

**이 파일과 02번 파일은 "순서"가 아니라 "선택"입니다.** 둘 다 넣으면 안 됩니다.

| 쓰는 툴 | 쓸 파일 |
|---|---|
| 제미나이, ChatGPT, Claude | **이 파일** (03) |
| SD 계열, Leonardo, NightCafe | [02-ready-to-paste.md](02-ready-to-paste.md) |
| Midjourney | [02-ready-to-paste.md](02-ready-to-paste.md) 의 `--no` 방식 |

## 입력 방법

제미나이는 입력창이 **채팅 하나뿐**입니다. 아래 프롬프트를 **통째로 복사해서 그 창에 붙여넣으면** 됩니다.
네거티브 프롬프트를 따로 넣을 곳은 없습니다 — 제약이 `CRITICAL CONSTRAINTS`에 문장으로 들어가 있습니다.

## 순서

```
STEP 0   스타일 시트          ← 이걸로 스타일을 고정
STEP 1   ① 감시 초소 (최약체)
STEP 2   ⑩ 왕좌 (최강체)      ← 격차를 먼저 확정
STEP 3~  나머지 8종
```

**STEP 1부터는 STEP 0에서 채택한 이미지를 채팅에 첨부하고**
프롬프트 맨 앞에 아래 한 줄을 추가하세요.

```
Match the exact art style, palette, pixel scale, and base plate design of the attached reference image.
```

이걸 빼면 10종이 각각 다른 게임처럼 보입니다. **AI 아트 프로젝트가 실패하는 가장 흔한 이유입니다.**

---


## STEP 0 · 스타일 시트 (가장 먼저)

```
Create a single isometric pixel art game asset for a tower defense game.

STYLE: Detailed 16-bit isometric pixel art, 45 degree projection with 2:1 pixel ratio.
Chunky readable pixels with crisp hard edges and a visible pixel grid. Use subtle dithering
for shading. Muted, desaturated palette: cool grey weathered stone with warm earth and
moss tones. Top-left key light with a dark outline around the structure. The structure sits
on a diamond-shaped base plate showing a layered soil cross-section with a grass edge.

SUBJECT: A modest stone wizard watchtower - a single round tower with a conical slate
roof, one glowing window, and cracked mossy masonry. Scatter a few small rocks and weed
tufts on the base plate of dry earth and sparse grass.

CRITICAL CONSTRAINTS:
- All glowing parts (windows, runes, crystals, magic light) must be PALE WHITE or very
  light cyan-white. They must NOT be purple, blue, orange, or any saturated color.
  This is essential - the glow gets recolored later in the game engine.
- Exactly ONE structure, centered in frame, fully visible and not cropped.
- Flat solid sage green background (#8a9a6b). No sky, no scenery, no horizon.
- No text, letters, numbers, watermarks, logos, or UI elements anywhere.
- Strictly 2D pixel art. Not a 3D render, not smooth or blurry, no anti-aliasing.
- Arcane fantasy theme only. No casino, gambling, playing card, or dice imagery.

Output as a square image.
```

**마음에 들 때까지 반복하세요.** 여기서 채택한 이미지가 나머지 9종의 기준이 됩니다.
채택하면 `python3 tools/sprite_check.py`로 검증한 뒤 다음으로 넘어가세요.

---


## STEP 1 · 1. 감시 초소 (탑 / High Card)

```
Match the exact art style, palette, pixel scale, and base plate design of the attached reference image.

Create a single isometric pixel art game asset for a tower defense game.

STYLE: Detailed 16-bit isometric pixel art, 45 degree projection with 2:1 pixel ratio.
Chunky readable pixels with crisp hard edges and a visible pixel grid. Use subtle dithering
for shading. Muted, desaturated palette: cool grey weathered stone with warm earth and
moss tones. Top-left key light with a dark outline around the structure. The structure sits
on a diamond-shaped base plate showing a layered soil cross-section with a grass edge.

SUBJECT: a small crude stone watchpost, single short square tower with a plain wooden roof, one narrow pale glowing slit window, cracked weathered masonry, a rickety wooden ladder leaning on the side, base plate of dry cracked earth with sparse dead weeds, a few loose rocks and a broken wooden signpost scattered around

CRITICAL CONSTRAINTS:
- All glowing parts (windows, runes, crystals, magic light) must be PALE WHITE or very
  light cyan-white. They must NOT be purple, blue, orange, or any saturated color.
  This is essential - the glow gets recolored later in the game engine.
- Exactly ONE structure, centered in frame, fully visible and not cropped.
- Flat solid sage green background (#8a9a6b). No sky, no scenery, no horizon.
- No text, letters, numbers, watermarks, logos, or UI elements anywhere.
- Strictly 2D pixel art. Not a 3D render, not smooth or blurry, no anti-aliasing.
- Arcane fantasy theme only. No casino, gambling, playing card, or dice imagery.

Output as a square image.
```


## STEP 2 · 10. 왕좌 (로열 스트레이트 플러시 / Royal)

```
Match the exact art style, palette, pixel scale, and base plate design of the attached reference image.

Create a single isometric pixel art game asset for a tower defense game.

STYLE: Detailed 16-bit isometric pixel art, 45 degree projection with 2:1 pixel ratio.
Chunky readable pixels with crisp hard edges and a visible pixel grid. Use subtle dithering
for shading. Muted, desaturated palette: cool grey weathered stone with warm earth and
moss tones. Top-left key light with a dark outline around the structure. The structure sits
on a diamond-shaped base plate showing a layered soil cross-section with a grass edge.

SUBJECT: a colossal crowned throne of pale marble and dark stone, towering far above all others, five tall crown spires rising in a regal arc, ornate carved filigree and gold trim, a massive central sigil radiating brilliant white authority, floating rings of runes orbiting the crown, grand and imposing, base plate of polished white marble steps with a deep red carpet leading up, golden ornamental patterns inlaid in the marble, two ceremonial braziers flanking the stairs

CRITICAL CONSTRAINTS:
- All glowing parts (windows, runes, crystals, magic light) must be PALE WHITE or very
  light cyan-white. They must NOT be purple, blue, orange, or any saturated color.
  This is essential - the glow gets recolored later in the game engine.
- Exactly ONE structure, centered in frame, fully visible and not cropped.
- Flat solid sage green background (#8a9a6b). No sky, no scenery, no horizon.
- No text, letters, numbers, watermarks, logos, or UI elements anywhere.
- Strictly 2D pixel art. Not a 3D render, not smooth or blurry, no anti-aliasing.
- Arcane fantasy theme only. No casino, gambling, playing card, or dice imagery.

Output as a square image.
```


## STEP 3 · 2. 쌍열 포탑 (원 페어 / One Pair)

```
Match the exact art style, palette, pixel scale, and base plate design of the attached reference image.

Create a single isometric pixel art game asset for a tower defense game.

STYLE: Detailed 16-bit isometric pixel art, 45 degree projection with 2:1 pixel ratio.
Chunky readable pixels with crisp hard edges and a visible pixel grid. Use subtle dithering
for shading. Muted, desaturated palette: cool grey weathered stone with warm earth and
moss tones. Top-left key light with a dark outline around the structure. The structure sits
on a diamond-shaped base plate showing a layered soil cross-section with a grass edge.

SUBJECT: two identical narrow stone towers standing side by side on one shared foundation, each with a matching pale glowing rune window at the same height, a thin arcane arc of white light connecting the two tops, base plate of packed dirt and short grass, two matching upright rune stones planted symmetrically at the front corners

CRITICAL CONSTRAINTS:
- All glowing parts (windows, runes, crystals, magic light) must be PALE WHITE or very
  light cyan-white. They must NOT be purple, blue, orange, or any saturated color.
  This is essential - the glow gets recolored later in the game engine.
- Exactly ONE structure, centered in frame, fully visible and not cropped.
- Flat solid sage green background (#8a9a6b). No sky, no scenery, no horizon.
- No text, letters, numbers, watermarks, logos, or UI elements anywhere.
- Strictly 2D pixel art. Not a 3D render, not smooth or blurry, no anti-aliasing.
- Arcane fantasy theme only. No casino, gambling, playing card, or dice imagery.

Output as a square image.
```


## STEP 4 · 3. 교차 포대 (투 페어 / Two Pair)

```
Match the exact art style, palette, pixel scale, and base plate design of the attached reference image.

Create a single isometric pixel art game asset for a tower defense game.

STYLE: Detailed 16-bit isometric pixel art, 45 degree projection with 2:1 pixel ratio.
Chunky readable pixels with crisp hard edges and a visible pixel grid. Use subtle dithering
for shading. Muted, desaturated palette: cool grey weathered stone with warm earth and
moss tones. Top-left key light with a dark outline around the structure. The structure sits
on a diamond-shaped base plate showing a layered soil cross-section with a grass edge.

SUBJECT: four stone pillars arranged as two distinct pairs, one pair clearly taller than the other, the two pairs crossing at right angles, pale glowing runes in two matching styles, crossed white arcane beams linking each pair, base plate with cross shaped cobblestone paving splitting the ground into four quadrants, small stacked stone cairns at the four corners

CRITICAL CONSTRAINTS:
- All glowing parts (windows, runes, crystals, magic light) must be PALE WHITE or very
  light cyan-white. They must NOT be purple, blue, orange, or any saturated color.
  This is essential - the glow gets recolored later in the game engine.
- Exactly ONE structure, centered in frame, fully visible and not cropped.
- Flat solid sage green background (#8a9a6b). No sky, no scenery, no horizon.
- No text, letters, numbers, watermarks, logos, or UI elements anywhere.
- Strictly 2D pixel art. Not a 3D render, not smooth or blurry, no anti-aliasing.
- Arcane fantasy theme only. No casino, gambling, playing card, or dice imagery.

Output as a square image.
```


## STEP 5 · 4. 삼연장포 (트리플 / Triple)

```
Match the exact art style, palette, pixel scale, and base plate design of the attached reference image.

Create a single isometric pixel art game asset for a tower defense game.

STYLE: Detailed 16-bit isometric pixel art, 45 degree projection with 2:1 pixel ratio.
Chunky readable pixels with crisp hard edges and a visible pixel grid. Use subtle dithering
for shading. Muted, desaturated palette: cool grey weathered stone with warm earth and
moss tones. Top-left key light with a dark outline around the structure. The structure sits
on a diamond-shaped base plate showing a layered soil cross-section with a grass edge.

SUBJECT: three identical stone cannon barrels clustered in a triangular formation on a round tower, three matching pale glowing runes forming a triangle, tri-fold symmetry, one larger white crystal suspended in the center between the three, base plate with a carved triangular magic circle glowing faintly white, three iron candlesticks with lit candles at the triangle points

CRITICAL CONSTRAINTS:
- All glowing parts (windows, runes, crystals, magic light) must be PALE WHITE or very
  light cyan-white. They must NOT be purple, blue, orange, or any saturated color.
  This is essential - the glow gets recolored later in the game engine.
- Exactly ONE structure, centered in frame, fully visible and not cropped.
- Flat solid sage green background (#8a9a6b). No sky, no scenery, no horizon.
- No text, letters, numbers, watermarks, logos, or UI elements anywhere.
- Strictly 2D pixel art. Not a 3D render, not smooth or blurry, no anti-aliasing.
- Arcane fantasy theme only. No casino, gambling, playing card, or dice imagery.

Output as a square image.
```


## STEP 6 · 5. 레일 랜스 (스트레이트 / Straight · 백스트레이트 · 마운틴)

```
Match the exact art style, palette, pixel scale, and base plate design of the attached reference image.

Create a single isometric pixel art game asset for a tower defense game.

STYLE: Detailed 16-bit isometric pixel art, 45 degree projection with 2:1 pixel ratio.
Chunky readable pixels with crisp hard edges and a visible pixel grid. Use subtle dithering
for shading. Muted, desaturated palette: cool grey weathered stone with warm earth and
moss tones. Top-left key light with a dark outline around the structure. The structure sits
on a diamond-shaped base plate showing a layered soil cross-section with a grass edge.

SUBJECT: a long horizontal rail cannon mounted on a low stone platform, five stepped segments ascending in height along the rail from back to front, a single long focused beam channel with pale white light running its length, five carved runes ascending in size along the side, base plate with iron rails and wooden sleepers embedded in gravel, scattered mechanical parts, a rusted lever and a coil of chain

CRITICAL CONSTRAINTS:
- All glowing parts (windows, runes, crystals, magic light) must be PALE WHITE or very
  light cyan-white. They must NOT be purple, blue, orange, or any saturated color.
  This is essential - the glow gets recolored later in the game engine.
- Exactly ONE structure, centered in frame, fully visible and not cropped.
- Flat solid sage green background (#8a9a6b). No sky, no scenery, no horizon.
- No text, letters, numbers, watermarks, logos, or UI elements anywhere.
- Strictly 2D pixel art. Not a 3D render, not smooth or blurry, no anti-aliasing.
- Arcane fantasy theme only. No casino, gambling, playing card, or dice imagery.

Output as a square image.
```


## STEP 7 · 6. 원소 증폭탑 (플러시 / Flush)

```
Match the exact art style, palette, pixel scale, and base plate design of the attached reference image.

Create a single isometric pixel art game asset for a tower defense game.

STYLE: Detailed 16-bit isometric pixel art, 45 degree projection with 2:1 pixel ratio.
Chunky readable pixels with crisp hard edges and a visible pixel grid. Use subtle dithering
for shading. Muted, desaturated palette: cool grey weathered stone with warm earth and
moss tones. Top-left key light with a dark outline around the structure. The structure sits
on a diamond-shaped base plate showing a layered soil cross-section with a grass edge.

SUBJECT: a slender spire ringed by five identical floating crystals orbiting in a circle, all five crystals cut in the exact same shape, glowing pale white, unified repeating motif, concentric rings carved into the tower body, amplifier antenna at the top, base plate with a large circular magic circle, the same sigil repeated five times around it, small white crystal shards growing from the ground at the circle edge

CRITICAL CONSTRAINTS:
- All glowing parts (windows, runes, crystals, magic light) must be PALE WHITE or very
  light cyan-white. They must NOT be purple, blue, orange, or any saturated color.
  This is essential - the glow gets recolored later in the game engine.
- Exactly ONE structure, centered in frame, fully visible and not cropped.
- Flat solid sage green background (#8a9a6b). No sky, no scenery, no horizon.
- No text, letters, numbers, watermarks, logos, or UI elements anywhere.
- Strictly 2D pixel art. Not a 3D render, not smooth or blurry, no anti-aliasing.
- Arcane fantasy theme only. No casino, gambling, playing card, or dice imagery.

Output as a square image.
```


## STEP 8 · 7. 중력 제단 (풀 하우스 / Full House)

```
Match the exact art style, palette, pixel scale, and base plate design of the attached reference image.

Create a single isometric pixel art game asset for a tower defense game.

STYLE: Detailed 16-bit isometric pixel art, 45 degree projection with 2:1 pixel ratio.
Chunky readable pixels with crisp hard edges and a visible pixel grid. Use subtle dithering
for shading. Muted, desaturated palette: cool grey weathered stone with warm earth and
moss tones. Top-left key light with a dark outline around the structure. The structure sits
on a diamond-shaped base plate showing a layered soil cross-section with a grass edge.

SUBJECT: a heavy stone altar with three thick columns supporting a raised platform, two smaller pillars standing on top of that platform, a dark heavy orb suspended in the center emitting pale white gravitational rings, massive and grounded, three-plus-two tiered structure, base plate with the ground cracked and pulled inward toward the center, small rocks and pebbles floating in mid-air above the cracks

CRITICAL CONSTRAINTS:
- All glowing parts (windows, runes, crystals, magic light) must be PALE WHITE or very
  light cyan-white. They must NOT be purple, blue, orange, or any saturated color.
  This is essential - the glow gets recolored later in the game engine.
- Exactly ONE structure, centered in frame, fully visible and not cropped.
- Flat solid sage green background (#8a9a6b). No sky, no scenery, no horizon.
- No text, letters, numbers, watermarks, logos, or UI elements anywhere.
- Strictly 2D pixel art. Not a 3D render, not smooth or blurry, no anti-aliasing.
- Arcane fantasy theme only. No casino, gambling, playing card, or dice imagery.

Output as a square image.
```


## STEP 9 · 8. 사방 요새 (포 카드 / Four Card)

```
Match the exact art style, palette, pixel scale, and base plate design of the attached reference image.

Create a single isometric pixel art game asset for a tower defense game.

STYLE: Detailed 16-bit isometric pixel art, 45 degree projection with 2:1 pixel ratio.
Chunky readable pixels with crisp hard edges and a visible pixel grid. Use subtle dithering
for shading. Muted, desaturated palette: cool grey weathered stone with warm earth and
moss tones. Top-left key light with a dark outline around the structure. The structure sits
on a diamond-shaped base plate showing a layered soil cross-section with a grass edge.

SUBJECT: a fortified square keep with four identical cannon barrels facing north south east and west, perfect four-fold radial symmetry, crenellated battlements, thick fortress walls, four matching pale glowing runes one on each face, base plate with stone rampart foundations extending toward all four corners, a small dry moat around the keep, four iron braziers burning white flame

CRITICAL CONSTRAINTS:
- All glowing parts (windows, runes, crystals, magic light) must be PALE WHITE or very
  light cyan-white. They must NOT be purple, blue, orange, or any saturated color.
  This is essential - the glow gets recolored later in the game engine.
- Exactly ONE structure, centered in frame, fully visible and not cropped.
- Flat solid sage green background (#8a9a6b). No sky, no scenery, no horizon.
- No text, letters, numbers, watermarks, logos, or UI elements anywhere.
- Strictly 2D pixel art. Not a 3D render, not smooth or blurry, no anti-aliasing.
- Arcane fantasy theme only. No casino, gambling, playing card, or dice imagery.

Output as a square image.
```


## STEP 10 · 9. 프리즘 랜스 (스트레이트 플러시 / Straight Flush · 백스플)

```
Match the exact art style, palette, pixel scale, and base plate design of the attached reference image.

Create a single isometric pixel art game asset for a tower defense game.

STYLE: Detailed 16-bit isometric pixel art, 45 degree projection with 2:1 pixel ratio.
Chunky readable pixels with crisp hard edges and a visible pixel grid. Use subtle dithering
for shading. Muted, desaturated palette: cool grey weathered stone with warm earth and
moss tones. Top-left key light with a dark outline around the structure. The structure sits
on a diamond-shaped base plate showing a layered soil cross-section with a grass edge.

SUBJECT: an elongated crystalline rail lance, five ascending prism segments in a row, all five prisms identical in cut and facet pattern, refracting pale white light into a spectrum, a continuous beam channel splitting along its length, sleek and precise, elevated polished stone platform with sequential carved sigils, base plate with rails inlaid with embedded white crystals, glowing prism shards jutting from the ground alongside the track

CRITICAL CONSTRAINTS:
- All glowing parts (windows, runes, crystals, magic light) must be PALE WHITE or very
  light cyan-white. They must NOT be purple, blue, orange, or any saturated color.
  This is essential - the glow gets recolored later in the game engine.
- Exactly ONE structure, centered in frame, fully visible and not cropped.
- Flat solid sage green background (#8a9a6b). No sky, no scenery, no horizon.
- No text, letters, numbers, watermarks, logos, or UI elements anywhere.
- Strictly 2D pixel art. Not a 3D render, not smooth or blurry, no anti-aliasing.
- Arcane fantasy theme only. No casino, gambling, playing card, or dice imagery.

Output as a square image.
```


---

## 생성 후 매번 할 것

```bash
python3 tools/sprite_check.py <이미지경로>
```

두 가지만 확인하면 됩니다.

1. **발광부가 흰빛인가** — `glow.png`에 창문·룬이 잡히는가
2. **축소해도 형태가 남는가** — `preview.png`의 48px 버전

나머지 검증 항목은 [01-towers.md](01-towers.md)의 체크리스트를 쓰세요.
