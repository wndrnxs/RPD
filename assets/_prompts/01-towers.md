# 01 · 타워 10종 프롬프트

> 사용 전 [00-style-sheet.md](00-style-sheet.md)를 먼저 읽으세요.
> 아래 모든 프롬프트는 **공통 블록 뒤에 이어 붙이는 부분**만 적혀 있습니다.

## 사용법

```
[00-style-sheet.md의 공통 프롬프트 블록]
,
[아래 개별 타워 프롬프트]
```

네거티브 프롬프트는 공통 블록의 것을 그대로 씁니다.

**순서대로 만들지 마세요.** ① 감시 초소 → ② 왕좌를 먼저 만들어
**최약체와 최강체의 격차**를 확정한 뒤, 나머지를 그 사이에 배치하는 것이 효율적입니다.

---

## 1. 감시 초소 (탑 / High Card)

**실루엣: 요소 1개.** 가장 단순하고 낮아야 합니다. 다른 9종의 기준점입니다.

```
a single slender stone obelisk, one small glowing rune carved near the top,
one tiny floating crystal shard hovering above, plain square base,
humble and minimal, shortest tower of the set, weathered granite
```

> **주의:** 이게 "꽝"으로 보이되 초라해선 안 됩니다. 9%나 나오는 결과물입니다.
> 낡았지만 단단해 보이게.

---

## 2. 쌍열 포탑 (원 페어 / One Pair)

**실루엣: 나란한 2개.** 대칭이 핵심입니다.

```
two identical stone pillars standing side by side on a shared base,
twin matching runes glowing on each pillar, perfectly symmetrical pair,
two small crystals hovering at equal height, connected by a thin arcane arc
```

---

## 3. 교차 포대 (투 페어 / Two Pair)

**실루엣: 2 + 2, 서로 다른 높이의 두 쌍.**

```
four stone pillars arranged as two distinct pairs, one pair taller than the other,
the two pairs crossing at different angles, four runes in two matching styles,
X-shaped crossing arcane beams connecting each pair, layered stepped base
```

---

## 4. 삼연장포 (트리플 / Triple)

**실루엣: 삼각 배치 3개.**

```
three identical stone barrels arranged in a triangular cluster,
three matching runes forming a triangle pattern, tri-fold symmetry,
one larger crystal suspended in the center of the three, hexagonal base
```

---

## 5. 레일 랜스 (스트레이트 / Straight · 백스트레이트 · 마운틴)

**실루엣: 5개가 계단처럼 오름차순.** 직선 관통 무기라 길고 낮게.

```
a long horizontal rail cannon on a stone platform,
five ascending stepped segments increasing in height along the rail,
a single long focused beam channel running the full length,
carved sequence of five runes ascending in size, elongated low profile
```

> **변종 처리:** 백 스트레이트와 마운틴은 **같은 스프라이트**를 씁니다
> ([01 문서 2.5절](../../docs/01-game-design.md)). 차이는 랭크 합에 따른 스탯과 연출로만 표현합니다.

---

## 6. 원소 증폭탑 (플러시 / Flush)

**실루엣: 하나의 무늬가 반복되는 통일감.** 속성 효과가 강조되는 타워입니다.

```
a tall spire ringed by five identical floating crystals orbiting in a circle,
all five crystals cut in the exact same shape, unified repeating motif,
concentric circular rings carved into the base, radiating amplifier antenna,
one large central sigil repeated five times around the ring
```

---

## 7. 중력 제단 (풀 하우스 / Full House)

**실루엣: 큰 3개 위에 작은 2개.** 3+2 구조가 보여야 합니다.

```
a heavy altar with three thick stone columns supporting a platform,
two smaller pillars standing on top of that platform,
a dark heavy orb suspended in the center pulling everything inward,
downward gravitational distortion rings, massive and grounded, three-plus-two structure
```

---

## 8. 사방 요새 (포 카드 / Four Card)

**실루엣: 4방향 대칭.** 위에서 봤을 때 십자.

```
a fortified square keep with four identical cannon barrels facing
north south east and west, perfect four-fold radial symmetry,
four matching runes on each face, thick fortress walls, crenellated top,
cross-shaped footprint when seen from above
```

---

## 9. 프리즘 랜스 (스트레이트 플러시 / Straight Flush · 백스플)

**실루엣: 레일 랜스의 계단 구조 + 원소 증폭탑의 통일 무늬.** 두 타워의 언어를 합칩니다.

```
an elongated crystalline rail lance, five ascending prism segments in a row,
all five prisms identical in cut and facet pattern, refracting arcane light,
a continuous beam channel splitting into a spectrum along its length,
elevated stone platform with carved sequential sigils, sleek and precise
```

> 5번(레일 랜스)과 6번(원소 증폭탑)을 **먼저 확정한 뒤에** 만드세요.
> 두 타워의 시각 요소를 조합한 것이라는 게 보여야 합니다.

---

## 10. 왕좌 (로열 스트레이트 플러시 / Royal)

**실루엣: 왕관. 압도적 높이.** 세트에서 가장 높고 화려해야 합니다.

```
a colossal crowned throne of arcane stone, towering above all others,
five tall crown spires rising in a regal arc, ornate carved filigree,
a massive central sigil radiating authority, floating rings of runes orbiting the crown,
grand tiered pedestal base, tallest and most elaborate structure of the set
```

> 이건 한 스테이지에 한 번 볼까 말까 한 결과물입니다
> ([01 문서 2.3절](../../docs/01-game-design.md) 확률표 참조).
> **아낌없이 화려하게** 만들어도 됩니다.

---

## 검증 체크리스트

생성 후 10종을 **한 화면에 나란히 놓고** 확인하세요.

- [ ] 48px로 축소했을 때 10종이 서로 구분되는가
- [ ] 눈을 가늘게 뜨고 봐도 개수(1/2/2+2/3/5/4/3+2)가 읽히는가
- [ ] 높이 순서가 족보 서열과 대략 일치하는가 (감시 초소 최저 → 왕좌 최고)
- [ ] 전부 무채색인가 (색이 남아 있으면 셰이더 틴트가 오염됩니다)
- [ ] 카지노를 연상시키는 요소가 하나도 없는가
- [ ] 조명 방향이 10종 모두 동일한가 (좌상단)
- [ ] 바닥 접지면 높이가 일정한가 (타일에 올렸을 때 들뜨거나 파묻히면 안 됨)

---

## 생성 기록

| 타워 | 모델 | 시드 | 날짜 | 비고 |
|---|---|---|---|---|
| 1. 감시 초소 | | | | |
| 2. 쌍열 포탑 | | | | |
| 3. 교차 포대 | | | | |
| 4. 삼연장포 | | | | |
| 5. 레일 랜스 | | | | |
| 6. 원소 증폭탑 | | | | |
| 7. 중력 제단 | | | | |
| 8. 사방 요새 | | | | |
| 9. 프리즘 랜스 | | | | |
| 10. 왕좌 | | | | |
