#!/usr/bin/env python3
"""SVG(HTML wrap) → Chrome headless PNG 렌더 + 정확한 크롭.

Chrome headless 뷰포트에는 두 방향 모두 함정이 있다.

높이 — 뷰포트 높이 == 문서 높이면 하단 ~106px을 잘라먹는다.
       넉넉한 뷰포트로 찍고 원하는 높이만큼 크롭한다(PAD).

폭   — `--window-size` 폭에 **하한**이 있다. 그보다 좁게 주면 스크린샷 캔버스만
       요청 폭으로 나오고 **레이아웃은 하한 폭으로 잡혀**, 하한과 요청 폭 사이의
       내용이 소리 없이 잘린다. 높이 함정과 달리 에러도 경고도 없고, 결과가
       "가로로 넘친 페이지"와 픽셀 단위로 구별되지 않는다 —
       실제로 2026-08-21 에 멀쩡한 페이지를 390px 로 찍고 가로 넘침으로 오진했다.

       하한은 머신·Chrome 버전 종속이므로 상수를 믿지 말고 재측정한다:
           <div style="width:100%;border-right:6px solid red">
       를 여러 --window-size 로 찍어, 빨간 보더가 캔버스 안에 보이기 시작하는
       폭이 하한이다(그 미만에서는 보더가 캔버스 밖으로 밀려 안 보인다).
       2026-08-21 private_cloud host 실측 = 495px.

       하한보다 좁은 뷰포트가 **정말 필요하면**(모바일 반응형 점검 등)
       하한 이상 창 안에 그 폭의 <iframe> 을 띄운다 — iframe 은 독립 레이아웃
       뷰포트를 가지므로 390px 등을 정확히 재현한다.
"""
import subprocess, sys, os, zlib, struct

PAD = 200      # 뷰포트 높이 여유
MIN_W = 495    # --window-size 폭 하한 (실측값 — 위 docstring 의 재측정법 참조)


def decode_png(path):
    d = open(path, 'rb').read()
    i, idat, ct = 8, b'', 0
    w = h = 0
    while i < len(d):
        ln = struct.unpack('>I', d[i:i+4])[0]
        t = d[i+4:i+8]
        if t == b'IHDR':
            w, h = struct.unpack('>II', d[i+8:i+16]); ct = d[i+8+9]
        elif t == b'IDAT':
            idat += d[i+8:i+8+ln]
        i += 12 + ln
    bpp = {0: 1, 2: 3, 4: 2, 6: 4}[ct]
    raw = zlib.decompress(idat)
    stride = w * bpp + 1
    prev = bytearray(w * bpp)
    rows = []
    for y in range(h):
        f = raw[y*stride]
        line = bytearray(raw[y*stride+1:(y+1)*stride])
        for x in range(len(line)):
            a = line[x-bpp] if x >= bpp else 0
            b = prev[x]
            c = prev[x-bpp] if x >= bpp else 0
            if f == 1:   line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                pp = a + b - c
                pa, pb, pc = abs(pp-a), abs(pp-b), abs(pp-c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        rows.append(bytes(line)); prev = line
    return w, h, bpp, ct, rows


def encode_png(path, w, rows, bpp, ct):
    raw = b''.join(b'\x00' + r for r in rows)
    comp = zlib.compress(raw, 9)
    def chunk(tag, data):
        return (struct.pack('>I', len(data)) + tag + data
                + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff))
    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', w, len(rows), 8, ct, 0, 0, 0))
           + chunk(b'IDAT', comp) + chunk(b'IEND', b''))
    open(path, 'wb').write(png)


def render(name, w, h, scale=2, cwd='.'):
    html = os.path.abspath(os.path.join(cwd, name + '.html'))
    tmp = os.path.join(cwd, name + '.raw.png')
    out = os.path.join(cwd, name + '.png')
    if w < MIN_W:
        raise SystemExit(
            f"{name}: window 폭 {w} < 하한 {MIN_W} — 레이아웃이 {MIN_W} 로 잡혀 "
            f"{w}~{MIN_W} 구간이 조용히 잘린다. 폭을 {MIN_W} 이상으로 올리거나, "
            f"좁은 뷰포트가 목적이면 iframe 방식을 쓴다(docstring 참조).")
    subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--no-sandbox',
                    '--hide-scrollbars', f'--force-device-scale-factor={scale}',
                    f'--window-size={w},{h+PAD}', f'--screenshot={tmp}', 'file://' + html],
                   check=True, capture_output=True)
    W, H, bpp, ct, rows = decode_png(tmp)
    keep = h * scale
    if H < keep:
        raise SystemExit(f"{name}: 렌더 높이 부족 {H} < {keep}")
    encode_png(out, W, rows[:keep], bpp, ct)
    os.remove(tmp)
    print(f"  {name:12} {W}x{keep}")


if __name__ == '__main__':
    cwd = os.path.dirname(os.path.abspath(__file__))
    for spec in sys.argv[1:]:
        n, w, h = spec.split(':')
        render(n, int(w), int(h), cwd=cwd)
