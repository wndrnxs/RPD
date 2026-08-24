#!/usr/bin/env python3
"""
생성된 AI 픽셀아트를 게임에 쓸 수 있는지 검증하고 후처리한다.

AI가 만든 "픽셀아트"는 1024px에서는 그럴싸해 보여도 실제 타일 크기로 줄이면
뭉개지는 경우가 대부분이다. 이 스크립트는 그걸 생성 직후에 걸러낸다.

하는 일:
  1. 배경(세이지 그린) 제거 → 투명 PNG
  2. 실루엣만 남긴 이미지 출력 (형태가 읽히는지 확인용)
  3. 여러 타일 크기로 nearest 축소한 미리보기 시트 생성
  4. 발광부 마스크 추출 (셰이더 틴트가 잡아낼 픽셀이 맞는지 확인)
  5. 색상 수 · 발광부 비율 등 수치 리포트

사용법:
    python3 tools/sprite_check.py <이미지경로> [--out 출력디렉터리]
    python3 tools/sprite_check.py tower_01.png --bg 8a9a6b --tol 30
"""
import argparse
import os
from collections import Counter

from PIL import Image

PREVIEW_HEIGHTS = [48, 64, 96, 128]   # 검증용 축소 크기 (스프라이트 세로 기준)
GLOW_THRESHOLD = 0.72                 # 00-style-sheet.md 의 셰이더 임계값과 동일


def luma(px):
    return (0.299 * px[0] + 0.587 * px[1] + 0.114 * px[2]) / 255.0


def remove_background(img, bg_hex, tol):
    """지정한 배경색과 가까운 픽셀을 투명하게. 워터마크가 배경 위에 있으면 같이 사라진다."""
    bg = tuple(int(bg_hex[i:i + 2], 16) for i in (0, 2, 4))
    img = img.convert("RGBA")
    out = img.copy()
    px = out.load()
    w, h = out.size
    removed = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if abs(r - bg[0]) <= tol and abs(g - bg[1]) <= tol and abs(b - bg[2]) <= tol:
                px[x, y] = (0, 0, 0, 0)
                removed += 1
    return out, removed / (w * h)


def autocrop(img):
    bbox = img.getbbox()
    return img.crop(bbox) if bbox else img


def silhouette(img):
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sp, dp = img.load(), out.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if sp[x, y][3] > 128:
                dp[x, y] = (20, 20, 25, 255)
    return out


def glow_mask(img):
    """셰이더가 속성색으로 물들일 픽셀만 남긴다."""
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sp, dp = img.load(), out.load()
    count = 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = sp[x, y]
            if a > 128 and luma((r, g, b)) >= GLOW_THRESHOLD:
                dp[x, y] = (255, 255, 255, 255)
                count += 1
            elif a > 128:
                dp[x, y] = (30, 30, 35, 255)
    return out, count


def downscale_sheet(img, heights):
    """여러 크기로 nearest 축소해 나란히 붙인 미리보기."""
    scaled = []
    for h in heights:
        w = max(1, round(img.size[0] * h / img.size[1]))
        scaled.append((h, img.resize((w, h), Image.NEAREST)))

    pad, label = 12, 16
    total_w = sum(s.size[0] for _, s in scaled) + pad * (len(scaled) + 1)
    max_h = max(s.size[1] for _, s in scaled) + pad * 2 + label
    sheet = Image.new("RGBA", (total_w, max_h), (138, 154, 107, 255))
    x = pad
    for h, s in scaled:
        sheet.paste(s, (x, max_h - pad - s.size[1]), s)
        x += s.size[0] + pad
    return sheet, scaled


def report(img, scaled, bg_ratio, glow_px):
    w, h = img.size
    px = img.load()
    colors = Counter()
    opaque = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 128:
                colors[(r, g, b)] += 1
                opaque += 1

    print("\n" + "=" * 58)
    print("  스프라이트 검증 리포트")
    print("=" * 58)
    print(f"  크롭 후 크기      {w} × {h}")
    print(f"  배경 제거 비율    {bg_ratio * 100:.1f}%")
    print(f"  고유 색상 수      {len(colors):,}")
    print(f"  발광 픽셀 비율    {glow_px / max(opaque,1) * 100:.2f}%  (임계값 {GLOW_THRESHOLD})")

    print("\n  판정")
    ok = True
    if len(colors) > 4000:
        print(f"  ✗ 색상이 {len(colors):,}개로 너무 많습니다.")
        print("    진짜 픽셀아트가 아니라 '픽셀아트 풍 일러스트'일 가능성이 높습니다.")
        print("    → 축소 후 팔레트를 32~64색으로 양자화하세요.")
        ok = False
    else:
        print(f"  ✓ 색상 수 {len(colors):,} — 픽셀아트 범위")

    if glow_px == 0:
        print("  ✗ 발광부가 하나도 검출되지 않았습니다. 셰이더 틴트가 작동하지 않습니다.")
        print("    → 창문·룬을 더 밝게 다시 생성하세요.")
        ok = False
    elif glow_px / max(opaque, 1) < 0.005:
        print(f"  △ 발광부가 {glow_px / max(opaque,1) * 100:.2f}%로 매우 작습니다.")
        print("    속성색이 거의 안 보일 수 있습니다. 육안으로 glow.png를 확인하세요.")
    else:
        print(f"  ✓ 발광부 {glow_px:,}px — 셰이더가 잡아낼 수 있습니다")

    if bg_ratio < 0.05:
        print("  △ 배경이 거의 제거되지 않았습니다. --bg 색상값을 확인하세요.")

    print("\n  ★ 사람이 직접 봐야 하는 것")
    print("    preview.png 에서 가장 작은 크기를 보세요.")
    print("    - 형태가 뭉개지지 않고 남아 있는가?")
    print("    - silhouette.png 에서 무엇인지 알아볼 수 있는가?")
    print("    이 둘이 통과해야 나머지 9종을 같은 스타일로 생성할 수 있습니다.")
    print("=" * 58 + "\n")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--out", default=None, help="출력 디렉터리 (기본: <이미지명>_check)")
    ap.add_argument("--bg", default="8a9a6b", help="배경색 hex (기본 세이지 그린)")
    ap.add_argument("--tol", type=int, default=32, help="배경색 허용 오차")
    args = ap.parse_args()

    out_dir = args.out or os.path.splitext(args.image)[0] + "_check"
    os.makedirs(out_dir, exist_ok=True)

    src = Image.open(args.image)
    print(f"입력: {args.image}  ({src.size[0]}×{src.size[1]})")

    cut, bg_ratio = remove_background(src, args.bg, args.tol)
    cut = autocrop(cut)
    cut.save(os.path.join(out_dir, "cutout.png"))

    sil = silhouette(cut)
    sil.save(os.path.join(out_dir, "silhouette.png"))

    glow, glow_px = glow_mask(cut)
    glow.save(os.path.join(out_dir, "glow.png"))

    sheet, scaled = downscale_sheet(cut, PREVIEW_HEIGHTS)
    sheet.save(os.path.join(out_dir, "preview.png"))
    for h, s in scaled:
        s.save(os.path.join(out_dir, f"scaled_{h}px.png"))

    sil_sheet, _ = downscale_sheet(sil, PREVIEW_HEIGHTS)
    sil_sheet.save(os.path.join(out_dir, "preview_silhouette.png"))

    report(cut, scaled, bg_ratio, glow_px)
    print(f"출력 디렉터리: {out_dir}/")
    for f in sorted(os.listdir(out_dir)):
        print(f"  {f}")


if __name__ == "__main__":
    main()
