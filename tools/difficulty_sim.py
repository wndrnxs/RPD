#!/usr/bin/env python3
"""
RPD 난이도 모델 (M0)

"타워 2개로 4라운드까지 클리어된다"는 문제를 수치로 잡기 위한 도구.

실제 경로 기하를 그대로 써서 타일별 '경로 커버리지'(그 타일에 타워를 세우면
몬스터가 사거리 안에 머무는 경로 길이)를 계산하고, 라운드별로 필요한 타워 수를 낸다.

사용법:
    python3 tools/difficulty_sim.py
    python3 tools/difficulty_sim.py --hp 125,69,3.15
"""
import argparse
import math

COLS, ROWS = 11, 15
WP = [(5,-1),(5,2),(1,2),(1,5),(9,5),(9,8),(1,8),(1,11),(9,11),(9,13),(5,13),(5,15)]
SPEED_SCALE = 1.35

# 5장 딜 + 토큰3 실측 분포 (hand_sim.py) → 타워별 확률
DIST = [   # (족보, 확률%, 설계 DPS, rate)
    ("탑",            27.80, 10,  .90),
    ("원 페어",       49.12, 18,  .75),
    ("투 페어",       12.10, 26,  .70),
    ("트리플",         6.99, 40,  .65),
    ("스트레이트 계열", 1.26, 55,  .85),
    ("플러시",         1.39, 70,  .72),
    ("풀 하우스",      1.17, 95,  .80),
    ("포 카드",        0.18, 130, .55),
    ("스플 계열",      0.02, 180, .90),
    ("로열",           0.00, 300, 1.0),
]
# 몬스터 유형: (HP배율, 속도배율, 방어력)
MTYPES = {
    "normal":(1.0, 1.00, 0.00), "armor":(1.5, 0.72, 0.45),
    "swift":(0.55,1.85, 0.00), "swarm":(0.32,1.15, 0.00),
    "regen": (1.2, 0.90, 0.10), "boss":(None,0.55, 0.35),
}
PIERCE_AVG = 0.10          # ♠ 관통이 방어력을 깎아주는 기대값


def path_points(step=0.05):
    """경로를 촘촘한 점으로 샘플링. (좌표, 누적거리)"""
    pts, total = [], 0.0
    for i in range(len(WP)-1):
        (ax,ay),(bx,by) = WP[i], WP[i+1]
        L = math.hypot(bx-ax, by-ay)
        n = max(1, int(L/step))
        for k in range(n):
            u = k/n
            pts.append((ax+(bx-ax)*u, ay+(by-ay)*u, total + L*u))
        total += L
    return pts, total


PTS, PLEN = path_points()
PATH_CELLS = set()
for i in range(len(WP)-1):
    (ax,ay),(bx,by) = WP[i], WP[i+1]
    dx, dy = (bx>ax)-(bx<ax), (by>ay)-(by<ay)
    x, y = ax, ay
    while True:
        if 0 <= y < ROWS: PATH_CELLS.add((x,y))
        if (x,y) == (bx,by): break
        x, y = x+dx, y+dy


def coverage(tx, ty, rng, step=0.05):
    """타일(tx,ty)에 사거리 rng 타워를 세웠을 때 사거리 안에 들어오는 경로 길이"""
    cx, cy = tx+0.5, ty+0.5
    n = sum(1 for (px,py,_) in PTS if (px+0.5-cx)**2 + (py+0.5-cy)**2 <= rng*rng)
    return n*step


def coverage_stats(rng):
    """건설 가능 타일 전체의 커버리지 분포"""
    vals = [coverage(x,y,rng) for y in range(ROWS) for x in range(COLS)
            if (x,y) not in PATH_CELLS]
    vals.sort()
    return {"max":vals[-1], "p90":vals[int(len(vals)*.90)],
            "p75":vals[int(len(vals)*.75)], "median":vals[len(vals)//2]}


def avg_dps(fix_bug=True):
    """실측 족보 분포로 가중한 타워 평균 DPS"""
    tot = 0
    for _, p, dps, rate in DIST:
        eff = dps if fix_bug else dps*rate     # 버그 시 실효 DPS = dps × rate
        tot += p/100 * eff
    return tot


def wave_size(R):
    if R % 10 == 0: return 1 + int(4 + R/3)
    return 6 + int(R*1.5)


def wave_window(R):
    """웨이브가 살아있는 시간 = 스폰 시간 + 마지막 몬스터 주파 시간"""
    gap = max(.30, .85 - R*.016)
    return wave_size(R)*gap + PLEN/SPEED_SCALE


def wave_mix(R):
    """makeWave() 와 동일한 유형 구성 (기대값)"""
    if R % 10 == 0:
        return [("boss",1)] + [("swarm", int(4+R/3))]
    n = wave_size(R)
    mix = []
    p_arm  = .22 if R>=3 else 0
    p_swf  = (.42-.22) if R>=4 else 0
    p_swm  = (.62-.42) if R>=2 else 0
    p_rgn  = (.74-.62) if R>=6 else 0
    p_nrm  = 1 - (p_arm+p_swf+p_swm+p_rgn)
    for k,pr in (("armor",p_arm),("swift",p_swf),("swarm",p_swm),
                 ("regen",p_rgn),("normal",p_nrm)):
        if pr > 0: mix.append((k, n*pr))
    return mix


def required_towers(R, hp_coef, cov, dps, upg, boss_mult):
    base = hp_coef[0] + hp_coef[1]*R + hp_coef[2]*R*R
    u = upg(R)
    need_kill, total_hp = 0.0, 0.0
    for kind, cnt in wave_mix(R):
        hpm, spm, arm = MTYPES[kind]
        hp = base*(boss_mult if kind=="boss" else hpm)
        eff_arm = max(0.0, arm - PIERCE_AVG)
        # 이 몬스터가 사거리 안에 머무는 시간
        expose = cov / (spm * SPEED_SCALE)
        per_tower = dps * u * expose * (1-eff_arm)
        need_kill = max(need_kill, hp/per_tower)      # 가장 단단한 놈 기준
        total_hp += hp*cnt*(1/(1-eff_arm))
    # 처리량 제약: 웨이브 전체 HP를 웨이브 지속시간 안에 녹여야 함
    need_thru = total_hp / (dps*u*wave_window(R))
    return max(need_kill, need_thru)


def upg_curve(R):
    """라운드별 평균 강화 배수 (점진 투자 가정)"""
    return 1 + min(2.2, R*0.05)


def report(name, hp_coef, fix_bug=True, cov=None, target=None, boss_mult=16):
    dps = avg_dps(fix_bug)
    cs = coverage_stats(2.6)          # 초중반 주력 사거리
    c = cov if cov else cs["p75"]
    print(f"\n{'='*62}\n  {name}\n{'='*62}")
    print(f"  평균 타워 DPS {dps:.1f}"
          f"{'' if fix_bug else '  ← rate² 버그 적용값'}"
          f"   커버리지 p75 {c:.1f}타일 (최대 {cs['max']:.1f})")
    print(f"  {'R':>3} {'몹HP':>7} {'웨이브HP':>9} {'필요타워':>9} {'목표':>7}")
    bad = 0
    for R in range(1, 31):
        need = required_towers(R, hp_coef, c, dps, upg_curve, boss_mult)
        tgt = target(R) if target else None
        if R <= 6 or R % 5 == 0:
            hp = hp_coef[0]+hp_coef[1]*R+hp_coef[2]*R*R
            flag = ""
            if tgt:
                if need < tgt*0.65: flag = "  ← 너무 쉬움"; bad += 1
                elif need > tgt*1.6: flag = "  ← 너무 어려움"; bad += 1
            tag = " 보스" if R%10==0 else ""
            print(f"  {R:>3} {hp:>7.0f} {wave_size(R)*hp:>9.0f}"
                  f" {need:>9.1f} {tgt if tgt else '-':>7}{flag}{tag}")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hp", default=None, help="a,b,c  (HP = a + b·R + c·R²)")
    args = ap.parse_args()

    # 목표: 라운드 R에 이 정도 타워를 요구한다
    target = lambda R: round(1.5 + R*0.75, 1)

    print(f"경로 길이 {PLEN:.1f}타일 · 주파 시간 {PLEN/SPEED_SCALE:.1f}초")
    print("\n사거리별 경로 커버리지 (건설 가능 타일 기준)")
    for rng in (2.4, 2.6, 3.0, 3.4, 4.3):
        s = coverage_stats(rng)
        print(f"  사거리 {rng}: 최대 {s['max']:5.1f} · p90 {s['p90']:5.1f}"
              f" · p75 {s['p75']:5.1f} · 중앙 {s['median']:5.1f}")

    if args.hp:
        c = [float(x) for x in args.hp.split(",")]
        report(f"지정값 HP = {c[0]} + {c[1]}·R + {c[2]}·R²", c, True, target=target)
        return

    report("현재값 (rate² 버그 포함) HP = 14 + 7.5R + 0.92R²",
           (14,7.5,.92), False, target=target, boss_mult=16)

    # HP 계수와 보스 배율을 목표 곡선에 맞게 탐색
    dps, c = avg_dps(True), coverage_stats(2.6)["p75"]
    best, bestErr = None, 1e18
    for a in range(40, 260, 10):
        for b in range(20, 130, 5):
            for cc in [x/4 for x in range(0, 30)]:
                err = 0
                for R in range(1, 31):
                    if R % 10 == 0: continue
                    n = required_towers(R,(a,b,cc),c,dps,upg_curve,4)
                    err += (n - target(R))**2
                if err < bestErr: bestErr, best = err, (a,b,cc)
    a,b,cc = best
    # 보스 배율 탐색 (보스 라운드는 일반 라운드의 1.35배를 요구하도록)
    bm, bmErr = 4, 1e18
    for m in [x/4 for x in range(4, 80)]:
        e = sum((required_towers(R,(a,b,cc),c,dps,upg_curve,m) - target(R)*1.35)**2
                for R in (10,20,30))
        if e < bmErr: bmErr, bm = e, m
    print(f"\n탐색 결과: HP = {a} + {b}·R + {cc}·R²   보스 배율 ×{bm}")
    report(f"제안 HP = {a} + {b}R + {cc}R² · 보스 ×{bm}",
           (a,b,cc), True, target=target, boss_mult=bm)


if __name__ == "__main__":
    main()
