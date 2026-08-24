#!/usr/bin/env python3
"""
RPD 족보 확률 시뮬레이터 (M0)

한국식 세븐포커 13족보 + 이 게임의 건설 룰(7장 딜 → 5장 선택 → 토큰 3개 리드로우)
아래에서 각 족보가 실제로 몇 %나 나오는지 몬테카를로로 측정한다.

GDD 2.3절의 추정치를 실측치로 대체하는 것이 목적.
검증이 끝나면 GDScript(core/sim/HandSimulator.gd)로 이식한다.

사용법:
    python3 tools/hand_sim.py [--trials 50000] [--tokens 3] [--deal 7]
"""
import random
import argparse
from collections import Counter
from itertools import combinations

RANKS = list(range(2, 15))          # 2..14 (A=14)
SUITS = [0, 1, 2, 3]                # ♠ ♥ ♦ ♣
DECK = [(r, s) for r in RANKS for s in SUITS]

HAND_NAMES = {
    13: "로열 스트레이트 플러시", 12: "백 스트레이트 플러시", 11: "스트레이트 플러시",
    10: "포 카드", 9: "풀 하우스", 8: "플러시", 7: "마운틴",
    6: "백 스트레이트", 5: "스트레이트", 4: "트리플", 3: "투 페어",
    2: "원 페어", 1: "탑",
}


def evaluate5(cards):
    """5장을 한국식 세븐포커 족보로 판정. 높을수록 강함 (1~13)."""
    ranks = sorted((c[0] for c in cards), reverse=True)
    suits = [c[1] for c in cards]
    is_flush = len(set(suits)) == 1

    uniq = sorted(set(ranks), reverse=True)
    is_mountain = uniq == [14, 13, 12, 11, 10]
    is_back = uniq == [14, 5, 4, 3, 2]
    is_normal_straight = (len(uniq) == 5 and uniq[0] - uniq[4] == 4)

    if is_flush:
        if is_mountain:
            return 13
        if is_back:
            return 12
        if is_normal_straight:
            return 11

    counts = sorted(Counter(ranks).values(), reverse=True)
    if counts[0] == 4:
        return 10
    if counts[0] == 3 and counts[1] == 2:
        return 9
    if is_flush:
        return 8
    if is_mountain:
        return 7
    if is_back:
        return 6
    if is_normal_straight:
        return 5
    if counts[0] == 3:
        return 4
    if counts[0] == 2 and counts[1] == 2:
        return 3
    if counts[0] == 2:
        return 2
    return 1


def best5_of(cards):
    """카드 묶음에서 최선의 5장 조합 등급을 반환."""
    if len(cards) == 5:
        return evaluate5(cards)
    return max(evaluate5(c) for c in combinations(cards, 5))


def straight_partners(ranks):
    """이 랭크 집합이 스트레이트로 갈 여지가 있는지 대략 평가 (연결된 최대 길이)."""
    u = sorted(set(ranks))
    if 14 in u:
        u = sorted(set(u + [1]))          # A를 낮은 쪽으로도 계산
    best = 1
    for i in range(len(u)):
        run = 1
        for j in range(i + 1, len(u)):
            if u[j] - u[j - 1] == 1:
                run += 1
            else:
                break
        best = max(best, run)
    # 갭이 하나 있는 경우(거트샷)도 약하게 인정
    for a, b in combinations(u, 2):
        if b - a == 4 and len([x for x in u if a <= x <= b]) >= 4:
            best = max(best, 4)
    return best


def candidate_keepsets(hand, max_draw, novice=False):
    """
    7장에서 '남길 카드'(keep set) 후보를 생성한다.
    최종 5장 = keep + 리드로우. keep 크기는 5-max_draw .. 5.
    실제 드로우 포커 전략을 따른 후보만 추린다 (전수 112개는 느리고 비현실적).
    """
    lo = 5 - max_draw
    cands = set()
    ranks = [c[0] for c in hand]
    suits = [c[1] for c in hand]
    rc, sc = Counter(ranks), Counter(suits)

    # 1) 현재 만들어진 최선의 5장 (드로우 0)
    best = max(combinations(hand, 5), key=evaluate5)
    cands.add(tuple(sorted(best)))

    # 2) 같은 숫자 묶음 유지 (포카드/트리플/투페어/원페어)
    groups = [r for r, v in rc.items() if v >= 2]
    if groups:
        pair_cards = [c for c in hand if rc[c[0]] >= 2]
        for size in range(max(lo, 2), min(len(pair_cards), 5) + 1):
            for combo in combinations(pair_cards, size):
                cands.add(tuple(sorted(combo)))
        # 최고 페어 + 킥커
        top = max(groups)
        core = [c for c in hand if c[0] == top][:2]
        others = sorted((c for c in hand if c[0] != top), key=lambda c: -c[0])
        for extra in range(0, min(3, 5 - len(core)) + 1):
            k = tuple(sorted(core + others[:extra]))
            if len(k) >= lo:
                cands.add(k)

    if not novice:
        # 3) 플러시 드로우 (같은 무늬 3장 이상 유지)
        for suit, n in sc.items():
            if n >= 3:
                same = sorted((c for c in hand if c[1] == suit), key=lambda c: -c[0])
                for size in range(max(lo, 3), min(n, 5) + 1):
                    cands.add(tuple(sorted(same[:size])))

        # 4) 스트레이트 드로우 (연결된 카드 유지)
        u = sorted(set(ranks), reverse=True)
        for size in range(max(lo, 3), min(len(u), 5) + 1):
            for combo in combinations(u, size):
                if straight_partners(combo) >= size - 1:
                    picked = []
                    for r in combo:
                        picked.append(next(c for c in hand if c[0] == r))
                    cands.add(tuple(sorted(picked)))

    # 5) 하이카드 유지 (최후 수단)
    high = sorted(hand, key=lambda c: -c[0])
    if lo <= 2:
        cands.add(tuple(sorted(high[:2])))
    cands.add(tuple(sorted(high[:max(lo, 2)])))

    return [list(k) for k in cands if lo <= len(k) <= 5]


def simulate_one(rng, deal=7, tokens=3, samples=40, novice=False):
    deck = DECK[:]
    rng.shuffle(deck)
    hand = deck[:deal]
    rest = deck[deal:]          # 아직 공개되지 않은 카드 (폐기 카드는 재출현 불가)

    best_score, best_keep = -1.0, None
    for keep in candidate_keepsets(hand, tokens, novice):
        need = 5 - len(keep)
        if need == 0:
            val = float(evaluate5(keep))
        else:
            total = 0
            for _ in range(samples):
                drawn = rng.sample(rest, need)
                total += evaluate5(list(keep) + drawn)
            val = total / samples
        if val > best_score:
            best_score, best_keep = val, keep

    need = 5 - len(best_keep)
    final = list(best_keep) + (rng.sample(rest, need) if need else [])
    return evaluate5(final)


def run(trials, deal, tokens, samples, novice, seed=12345):
    rng = random.Random(seed)
    counts = Counter()
    for _ in range(trials):
        counts[simulate_one(rng, deal, tokens, samples, novice)] += 1
    return counts


def baseline_no_redraw(trials, deal, seed=999):
    """리드로우 없이 '7장 중 최선 5장'만 했을 때의 분포 (비교 기준선)."""
    rng = random.Random(seed)
    counts = Counter()
    for _ in range(trials):
        deck = DECK[:]
        rng.shuffle(deck)
        counts[best5_of(deck[:deal])] += 1
    return counts


def show(title, counts, trials):
    print(f"\n{title}")
    print("-" * 52)
    for h in range(13, 0, -1):
        pct = counts.get(h, 0) / trials * 100
        bar = "█" * int(pct / 2)
        print(f"  {HAND_NAMES[h]:<16} {pct:7.3f}%  {bar}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--deal", type=int, default=7)
    ap.add_argument("--tokens", type=int, default=3)
    ap.add_argument("--samples", type=int, default=40, help="keep set 평가용 내부 표본 수")
    args = ap.parse_args()

    print(f"딜 {args.deal}장 / 토큰 {args.tokens}개 / {args.trials:,}회")

    base = baseline_no_redraw(args.trials, args.deal)
    show(f"[기준선] {args.deal}장 중 최선 5장 (리드로우 없음)", base, args.trials)

    nov = run(args.trials, args.deal, args.tokens, args.samples, novice=True)
    show(f"[초보] 딜 {args.deal} + 토큰 {args.tokens}", nov, args.trials)

    avg = run(args.trials, args.deal, args.tokens, args.samples, novice=False)
    show(f"[평균] 딜 {args.deal} + 토큰 {args.tokens}", avg, args.trials)


if __name__ == "__main__":
    main()
