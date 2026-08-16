#!/usr/bin/env python3
"""SVG(HTML wrap) → Chrome headless PNG 렌더 + 정확한 크롭.

Chrome headless는 뷰포트 높이 == 문서 높이일 때 하단 ~106px을 잘라먹는다.
넉넉한 뷰포트로 찍고 원하는 높이만큼 크롭한다.
"""
import subprocess, sys, os, zlib, struct

PAD = 200  # 뷰포트 여유


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
