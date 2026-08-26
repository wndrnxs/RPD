#!/usr/bin/env python3
"""
RPD 경제 수지 모델 (M0)

"골드가 후반에 넘쳐난다"는 문제를 눈으로 확인하고 파라미터를 튜닝하기 위한 도구.

핵심 진단:
    수입은 라운드에 대해 2차식(웨이브 크기 ↑ × 마리당 골드 ↑)인데
    지출은 타워 개수에 대해 1차식이다. 그래서 후반에 반드시 넘친다.
    상수를 줄이는 걸로는 안 되고 곡선의 '모양'을 바꿔야 한다.

사용법:
    python3 tools/economy_sim.py                    # 현재값 vs 제안값 비교
    python3 tools/economy_sim.py --profile tuned    # 제안값만
"""
import argparse

ROUNDS = 30


class Profile:
    def __init__(self, name, **kw):
        self.name = name
        self.start_gold = kw.get("start_gold", 120)
        self.wave_base = kw.get("wave_base", 6)
        self.wave_slope = kw.get("wave_slope", 1.5)
        self.kill_base = kw.get("kill_base", 3.0)
        self.kill_slope = kw.get("kill_slope", 0.55)
        self.round_base = kw.get("round_base", 30)
        self.round_slope = kw.get("round_slope", 6)
        self.cost_first_free = kw.get("cost_first_free", True)
        self.cost_base = kw.get("cost_base", 50)
        self.cost_step = kw.get("cost_step", 10)
        self.cost_knee = kw.get("cost_knee", None)       # n이 이 값을 넘으면
        self.cost_step2 = kw.get("cost_step2", None)     # 증가폭을 이걸로
        self.boss_bonus = kw.get("boss_bonus", 1.0)

    def wave_size(self, r):
        if r % 10 == 0:
            return 1 + int(4 + r / 3)          # 보스 + 군집
        return self.wave_base + int(r * self.wave_slope)

    def kill_gold(self, r):
        return self.kill_base + r * self.kill_slope

    def round_reward(self, r):
        return self.round_base + r * self.round_slope

    def income(self, r):
        g = self.wave_size(r) * self.kill_gold(r)
        if r % 10 == 0:
            g += self.kill_gold(r) * 14 * self.boss_bonus   # 보스 처치 보상
        return g + self.round_reward(r)

    def cost(self, n):
        """n번째 타워 (0-indexed: n=0이 첫 타워)"""
        if n == 0 and self.cost_first_free:
            return 0
        i = n - 1 if self.cost_first_free else n
        if self.cost_knee is not None and i >= self.cost_knee:
            base = self.cost_base + (self.cost_knee - 1) * self.cost_step
            return round(base + (i - self.cost_knee + 1) * self.cost_step2)
        return round(self.cost_base + i * self.cost_step)

    def cum_tower_cost(self, n):
        return sum(self.cost(i) for i in range(n))


UP_COST = [60, 120, 240, 480, 960]


def upgrade_spend(levels_per_type):
    """예: [3,2,1] = 세 족보를 각각 Lv.3/2/1 까지"""
    return sum(sum(UP_COST[:lv]) for lv in levels_per_type)


def simulate(p, towers=25, upgrade_plan=(3, 3, 2, 2)):
    """
    타워를 towers개 짓고 upgrade_plan 만큼 강화했을 때의 라운드별 잔고.
    지출은 초반에 몰린다고 가정 (실제 플레이 패턴).
    """
    gold = p.start_gold
    tower_cost = [p.cost(i) for i in range(towers)]
    up_total = upgrade_spend(upgrade_plan)
    rows = []
    built = 0
    up_paid = 0
    for r in range(1, ROUNDS + 1):
        gold += p.income(r)
        # 초반 20라운드에 걸쳐 타워를 나눠 짓는다
        target_built = min(towers, round(towers * min(1.0, r / 20)))
        while built < target_built and gold >= tower_cost[built]:
            gold -= tower_cost[built]; built += 1
        # 강화는 여유 골드의 일부를 계속 투입
        want = up_total * min(1.0, r / 25)
        if up_paid < want and gold > 200:
            pay = min(want - up_paid, gold - 200)
            gold -= pay; up_paid += pay
        rows.append((r, round(p.income(r)), built, round(up_paid), round(gold)))
    return rows, sum(p.income(r) for r in range(1, ROUNDS + 1)), p.cum_tower_cost(towers), up_total


def report(p, towers=25, plan=(3, 3, 2, 2)):
    rows, total_in, tcost, upmax = simulate(p, towers, plan)
    print(f"\n{'='*66}")
    print(f"  {p.name}")
    print(f"{'='*66}")
    print(f"  {'R':>3} {'수입':>7} {'타워':>5} {'강화누적':>9} {'잔고':>9}")
    for r, inc, b, up, g in rows:
        if r % 3 == 0 or r in (1, 30):
            flag = "  ← 넘침" if g > 2500 else ("  ← 빠듯" if g < 120 else "")
            print(f"  {r:>3} {inc:>7} {b:>5} {up:>9} {g:>9}{flag}")
    end = rows[-1][4]
    print(f"  {'-'*60}")
    print(f"  30R 총수입      {round(total_in):>8}")
    print(f"  타워 {towers}개 비용  {tcost:>8}   (마지막 타워 {p.cost(towers-1)}G)")
    print(f"  강화 최대 투입   {upmax:>8}   (계획 {plan})")
    print(f"  최종 잔고       {end:>8}", end="")
    if end > 2500:
        print("   ✗ 넘침 — 후반에 쓸 곳이 없음")
    elif end < 0:
        print("   ✗ 부족 — 계획대로 못 지음")
    else:
        print("   ✓ 적정")
    peak = max(g for *_, g in rows)
    print(f"  최대 잔고       {peak:>8}", end="")
    print("   ✗ 중간에 넘침" if peak > 3000 else "   ✓")
    return end, peak


CURRENT = Profile("현재 (프로토타입)")

TUNED = Profile(
    "제안 (수입 곡선 평탄화 + 비용 무릎)",
    start_gold=90,
    kill_base=2.2, kill_slope=0.16,     # 마리당 골드 스케일링을 크게 약화
    round_base=26, round_slope=2.6,     # 라운드 보상도 완만하게
    cost_base=50, cost_step=10,
    cost_knee=15, cost_step2=26,        # 15번째 타워부터 증가폭 확대
    boss_bonus=1.0,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", choices=["current", "tuned", "both"], default="both")
    ap.add_argument("--towers", type=int, default=25)
    args = ap.parse_args()

    plan = (3, 3, 2, 2)
    if args.profile in ("current", "both"):
        report(CURRENT, args.towers, plan)
    if args.profile in ("tuned", "both"):
        report(TUNED, args.towers, plan)

    print(f"\n{'='*66}")
    print("  제안 프로파일의 비용 곡선")
    print(f"{'='*66}")
    print("   n  ", "".join(f"{i+1:>6}" for i in [0, 4, 9, 14, 19, 24, 29]))
    print("  비용", "".join(f"{TUNED.cost(i):>6}" for i in [0, 4, 9, 14, 19, 24, 29]))
    print(f"\n  누적: 10개 {TUNED.cum_tower_cost(10):,}G · "
          f"20개 {TUNED.cum_tower_cost(20):,}G · 25개 {TUNED.cum_tower_cost(25):,}G")


if __name__ == "__main__":
    main()
