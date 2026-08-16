#!/usr/bin/env python3
# Jira 운영 방침 figure 3종 (정밀 SVG → chrome 렌더)
import html, os

FF = "Noto Sans CJK KR, Noto Sans CJK JP, sans-serif"
TMP = os.path.dirname(os.path.abspath(__file__))

INK, SUB = "#1F2933", "#5A6673"
BG, FRAME = "#FBFCFE", "#E6EAEF"
CARD_FILL, CARD_STROKE = "#FFFFFF", "#DBE1E8"
A_SOLID, A_DASH = "#3B4657", "#9AA6B6"

KEY  = ("#B7791F", "#FBF4E6")   # 강조 (에픽 · 진행 중)
OK   = ("#2F855A", "#EEF7F1")   # 도착 (스프린트 · 완료)
MUTE = ("#8A94A6", "#F2F4F7")   # 비활성 (백로그 · 타임라인)
BLUE = ("#2563A8", "#E9F2FD")   # 시각 · 단계


class Fig:
    def __init__(self, w, h):
        self.w, self.h, self.o = w, h, []
        self.add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                 f'viewBox="0 0 {w} {h}" font-family="{FF}">')
        self.add('<defs>')
        self.add('<filter id="sh" x="-20%" y="-20%" width="140%" height="140%">'
                 '<feDropShadow dx="0" dy="2" stdDeviation="3.2" flood-color="#1F2933" '
                 'flood-opacity="0.13"/></filter>')
        for name, col in (("shkey", KEY[0]), ("shok", OK[0]), ("shblue", BLUE[0])):
            self.add(f'<filter id="{name}" x="-30%" y="-30%" width="160%" height="160%">'
                     f'<feDropShadow dx="0" dy="4" stdDeviation="7" flood-color="{col}" '
                     f'flood-opacity="0.22"/></filter>')
        for mid, col in (('asolid', A_SOLID), ('adash', A_DASH), ('aok', OK[0]), ('amute', MUTE[0])):
            self.add(f'<marker id="{mid}" markerWidth="11" markerHeight="11" refX="8" refY="4" '
                     f'orient="auto" markerUnits="userSpaceOnUse">'
                     f'<path d="M0,0 L9,4 L0,8 z" fill="{col}"/></marker>')
        self.add('</defs>')
        self.add(f'<rect x="0" y="0" width="{w}" height="{h}" fill="{BG}"/>')
        self.add(f'<rect x="12" y="12" width="{w-24}" height="{h-24}" rx="20" fill="none" '
                 f'stroke="{FRAME}" stroke-width="1.5"/>')

    def add(self, s): self.o.append(s)

    @staticmethod
    def esc(s): return html.escape(str(s), quote=True)

    def title(self, x, y, text, sub=None, bar=BLUE[0], barw=150):
        self.add(f'<text x="{x}" y="{y}" font-size="29" font-weight="800" fill="{INK}">'
                 f'{self.esc(text)}</text>')
        self.add(f'<rect x="{x+2}" y="{y+10}" width="{barw}" height="5" rx="2.5" fill="{bar}"/>')
        if sub:
            self.add(f'<text x="{x}" y="{y+36}" font-size="15.5" fill="{SUB}">{self.esc(sub)}</text>')

    def card(self, x, y, w, h, title, subs=(), accent=None, hero=False, center=True,
             tsize=20, ssize=14, badge=None, dashed=False, shadow="sh"):
        """accent=(stroke,fill) 지정 시 강조 카드"""
        fill, stroke, sw = CARD_FILL, CARD_STROKE, 1.6
        tcol = INK
        if accent:
            stroke, fill = accent
            sw = 3 if hero else 2
            tcol = accent[0]
        f = f' filter="url(#{shadow})"' if shadow else ''
        da = ' stroke-dasharray="7 6"' if dashed else ''
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{sw}"{da}{f}/>')
        cx = x + w / 2
        anc, tx = ("middle", cx) if center else ("start", x + 20)
        ty = y + (34 if subs else h / 2 + 7)
        self.add(f'<text x="{tx}" y="{ty}" font-size="{tsize}" font-weight="700" '
                 f'fill="{tcol}" text-anchor="{anc}">{self.esc(title)}</text>')
        ty += 25
        for s in subs:
            self.add(f'<text x="{tx}" y="{ty}" font-size="{ssize}" fill="{SUB}" '
                     f'text-anchor="{anc}">{self.esc(s)}</text>')
            ty += 21
        if badge:
            bw = 22 + len(badge) * 13
            bc = accent[0] if accent else BLUE[0]
            self.add(f'<rect x="{x+w-bw-14}" y="{y-14}" width="{bw}" height="28" rx="14" fill="{bc}"/>')
            self.add(f'<text x="{x+w-bw/2-14}" y="{y+5}" font-size="13.5" font-weight="700" '
                     f'fill="#FFFFFF" text-anchor="middle">{self.esc(badge)}</text>')

    def chip(self, x, y, text, col):
        w = 24 + len(text) * 15
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="15" fill="{col}"/>')
        self.add(f'<text x="{x+w/2}" y="{y+20}" font-size="15" font-weight="700" '
                 f'fill="#FFFFFF" text-anchor="middle">{self.esc(text)}</text>')
        return w

    def arrow(self, x1, y1, x2, y2, label=None, dashed=False, color=None, mk=None, lw=7.6):
        color = color or (A_DASH if dashed else A_SOLID)
        mk = mk or ('adash' if dashed else 'asolid')
        da = ' stroke-dasharray="7 6"' if dashed else ''
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
                 f'stroke-width="{2.2 if dashed else 2.8}"{da} marker-end="url(#{mk})"/>')
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.lbl(mx, my, label, lw)

    def path(self, d, label=None, lx=0, ly=0, dashed=True, color=None, mk=None, lw=7.6):
        color = color or (A_DASH if dashed else A_SOLID)
        mk = mk or ('adash' if dashed else 'asolid')
        da = ' stroke-dasharray="7 6"' if dashed else ''
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="'
                 f'{2.2 if dashed else 2.8}"{da} marker-end="url(#{mk})"/>')
        if label:
            self.lbl(lx, ly, label, lw)

    def lbl(self, mx, my, text, lw=7.6):
        tw = len(text) * lw + 16
        self.add(f'<rect x="{mx-tw/2}" y="{my-14}" width="{tw}" height="23" rx="7" '
                 f'fill="{BG}" stroke="{FRAME}" stroke-width="1"/>')
        self.add(f'<text x="{mx}" y="{my+2}" font-size="13" fill="{INK}" '
                 f'text-anchor="middle">{self.esc(text)}</text>')

    def legend(self, x, y, w, items):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="54" rx="12" fill="#FFFFFF" '
                 f'stroke="#C3CCD8" stroke-width="1.6" filter="url(#sh)"/>')
        cx, cy = x + 26, y + 30
        for kind, col, text in items:
            if kind == "solid":
                self.add(f'<line x1="{cx}" y1="{cy}" x2="{cx+44}" y2="{cy}" stroke="{col}" '
                         f'stroke-width="2.8" marker-end="url(#asolid)"/>')
                cx += 56
            elif kind == "dash":
                self.add(f'<line x1="{cx}" y1="{cy}" x2="{cx+44}" y2="{cy}" stroke="{col}" '
                         f'stroke-width="2.2" stroke-dasharray="7 6" marker-end="url(#adash)"/>')
                cx += 56
            else:  # box
                self.add(f'<rect x="{cx}" y="{cy-13}" width="26" height="26" rx="7" '
                         f'fill="{kind}" stroke="{col}" stroke-width="2.4"/>')
                cx += 38
            self.add(f'<text x="{cx}" y="{cy+5}" font-size="14.5" fill="{INK}">{self.esc(text)}</text>')
            cx += len(text) * 14.8 + 34

    def save(self, name):
        self.add('</svg>')
        svg = '\n'.join(self.o)
        open(f'{TMP}/{name}.svg', 'w').write(svg)
        open(f'{TMP}/{name}.html', 'w').write(
            '<!doctype html><html><head><meta charset="utf-8">'
            f'<style>html,body{{margin:0;padding:0;background:{BG}}}svg{{display:block}}</style>'
            f'</head><body>{svg}</body></html>')
        print(f"  {name}  {self.w}x{self.h}")


# ══════════ figure 1 — 에픽 · 스토리 ══════════
f = Fig(1240, 786)
f.title(60, 56, "이슈 1건 = 에픽 1개", "스프린트에 담기는 단위는 에픽이 아니라 그 아래 스토리다", KEY[0], 190)

f.card(440, 108, 360, 76, "이슈 1건", ("고객 요청 · 결함 · 질의 · 내부 과제",), tsize=19)
f.arrow(620, 184, 620, 214)

f.card(370, 220, 500, 92, "에픽 1개", ("사이트명 · Triage · 기한 · 담당자",),
       accent=KEY, hero=True, tsize=23, ssize=15, shadow="shkey")
f.card(950, 220, 230, 92, "타임라인", ("에픽 단위로 표시", "스프린트엔 담기지 않는다"),
       accent=MUTE, dashed=True, tsize=18, ssize=13)
f.path("M 872 266 L 944 266", None, dashed=True, mk="amute", color=MUTE[0])

SY, SH, SW = 380, 128, 300
for i, (t, s1, s2) in enumerate([
        ("스토리 · 개발", "언제나 만든다", "쪼갤 게 없어도 최소 1개"),
        ("스토리 · 코드 리뷰", "다음 스프린트로", "넘어갈 때만 분리"),
        ("스토리 · 패치", "개발보다", "나중일 때만 분리")]):
    x = 120 + i * (SW + 50)
    f.card(x, SY, SW, SH, t, (s1, s2), tsize=19)
    f.arrow(620, 312, x + SW / 2, SY - 6)

DY = 596
f.card(160, DY, 520, 78, "스프린트에 담는다", ("한 스프린트 안에 닫을 수 있는 크기로",),
       accent=OK, hero=True, tsize=21, shadow="shok")
f.card(770, DY, 350, 78, "백로그에 둔다", ("패치 일정 확정 전까지",), accent=MUTE, tsize=19)
f.arrow(270, SY + SH, 330, DY - 6, None, mk="aok", color=OK[0])
f.arrow(620, SY + SH, 540, DY - 6, None, mk="aok", color=OK[0])
f.arrow(970, SY + SH, 945, DY - 6, None, mk="amute", color=MUTE[0])

f.legend(60, 700, 1120, [
    ("solid", A_SOLID, "만들면 스프린트에 잡힌다"),
    ("dash", MUTE[0], "잡히지 않는다"),
    (KEY[1], KEY[0], "에픽만 만들고 스토리가 없으면 그 일은 보드에 안 뜬다"),
])
f.save("epic_story")


# ══════════ figure 2 — 보드 컬럼 ══════════
f = Fig(1240, 442)
f.title(60, 56, "보드 컬럼 — 마지막 칸에 들어가면 완료",
        "팀이 손을 뗀 시점이 완료다. QA 검증을 기다리느라 미완료로 잡히지 않는다", OK[0], 210)

CW, CH, CY = 262, 116, 148
cols = [("해야 할 일", ["준비 완료 · 다시 열림"], None),
        ("진행 중", ["개발 · 수정 진행"], None),
        ("코드 리뷰", ["Merge request"], None),
        ("완료", ["QA test · Project Check", "RESOLVED · Complete"], OK)]
xs = []
for i, (t, subs, ac) in enumerate(cols):
    x = 60 + i * (CW + 28)
    xs.append(x)
    f.card(x, CY, CW, CH, t, subs, accent=ac, hero=bool(ac), tsize=21, ssize=13.5,
           shadow="shok" if ac else "sh", badge="여기부터 완료" if ac else None)
    if i:
        f.arrow(x - 26, CY + CH / 2, x - 4, CY + CH / 2)

f.path(f"M {xs[3]+CW/2} {CY+CH+6} L {xs[3]+CW/2} 318 L {xs[1]+CW/2} 318 L {xs[1]+CW/2} {CY+CH+8}",
       "QA 반려 시 되돌아온다", (xs[1] + xs[3] + CW) / 2, 318, dashed=True)
f.legend(60, 356, 1120, [
    (OK[1], OK[0], "이 칸에 들어간 카드가 스프린트 완료로 집계된다"),
    ("dash", A_DASH, "반려 시 진행 중으로 복귀"),
])
f.save("board")


# ══════════ figure 3 — 데일리 진행 순서 ══════════
f = Fig(1240, 534)
f.title(60, 56, "데일리 10분 — 오른쪽 컬럼부터",
        "보드 흐름과 반대로 본다. 우리가 약한 지점은 '시작'이 아니라 '마무리'이기 때문", BLUE[0], 200)

BARY = 146
f.add(f'<rect x="60" y="{BARY}" width="1120" height="6" rx="3" fill="{FRAME}"/>')
for lx, t in ((60, "10:15"), (1180, "10:25")):
    f.add(f'<circle cx="{lx}" cy="{BARY+3}" r="9" fill="{BLUE[0]}"/>')
    f.add(f'<text x="{lx}" y="{BARY-16}" font-size="16" font-weight="700" fill="{BLUE[0]}" '
          f'text-anchor="middle">{t}</text>')

SY, SH, SW = 190, 168, 340
steps = [("① 코드 리뷰", "3분", ['"이거 오늘 리뷰 볼 수 있나요?"', "리뷰 내용 얘기가 시작되면", "→ 끝나고 얘기하시죠"], None),
         ("② 진행 중", "5분", ["담당자가 티켓마다 세 줄", "어제 한 일 / 오늘 할 일", "/ 막히는 점"], KEY),
         ("③ 해야 할 일", "2분", ['"오늘 새로 시작할 것 있나요?"', '"보드에 없는데 하는 일 있나요?"', "→ 남을 사람만 정리"], None)]
for i, (t, mins, subs, ac) in enumerate(steps):
    x = 70 + i * (SW + 40)
    f.card(x, SY, SW, SH, f"{t} · {mins}", subs, accent=ac, hero=bool(ac),
           tsize=21, ssize=14, shadow="shkey" if ac else "sh",
           badge="여기가 본체" if ac else None)
    f.add(f'<line x1="{x+SW/2}" y1="{BARY+10}" x2="{x+SW/2}" y2="{SY-6}" '
          f'stroke="{FRAME}" stroke-width="2"/>')
    if i:
        f.arrow(x - 38, SY + SH / 2, x - 6, SY + SH / 2)

f.card(70, 386, 1100, 56, "완료 컬럼은 건너뛴다 — 이미 손을 뗀 일이라 매일 확인할 필요가 없다",
       (), accent=MUTE, dashed=True, tsize=17, shadow=None)
f.legend(60, 458, 1120, [
    (KEY[1], KEY[0], "10분 중 5분을 여기 쓴다"),
    ("solid", A_SOLID, "각 컬럼의 위에서 아래로"),
])
f.save("daily_flow")
