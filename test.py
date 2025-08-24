import streamlit as st
import datetime
from typing import List, Dict

# =============================
# 기본 설정
# =============================
st.set_page_config(page_title="오하아사 별자리 운세", page_icon="🌅", layout="centered")

# 파스텔 카드 스타일 (깜찍)
CARD_CSS = """
<style>
  .card {background:#FFF0F5; border-radius:20px; padding:20px; margin:12px 0; box-shadow:2px 4px 10px rgba(0,0,0,.08)}
  .gold {background:#FFE680; border-radius:20px; padding:20px; margin:12px 0; box-shadow:2px 4px 12px rgba(0,0,0,.12); font-weight:700}
  .muted {color:#555}
  .pill {display:inline-block; padding:4px 10px; border-radius:999px; background:#FFD6E7; font-weight:600}
</style>
"""
st.markdown(CARD_CSS, unsafe_allow_html=True)

TODAY_KR = datetime.date.today().strftime("%Y년 %m월 %d일")

# =============================
# 별자리 계산 & 유틸
# =============================
ZODIAC_ORDER = [
    (3,21, 4,19, "양자리"), (4,20, 5,20, "황소자리"), (5,21, 6,21, "쌍둥이자리"),
    (6,22, 7,22, "게자리"), (7,23, 8,22, "사자자리"), (8,23, 9,22, "처녀자리"),
    (9,23,10,23, "천칭자리"), (10,24,11,22, "전갈자리"), (11,23,12,21, "사수자리"),
    (12,22, 1,19, "염소자리"), (1,20, 2,18, "물병자리"), (2,19, 3,20, "물고기자리"),
]

ZODIAC_EMOJI = {
    "양자리":"♈", "황소자리":"♉", "쌍둥이자리":"♊", "게자리":"♋",
    "사자자리":"♌", "처녀자리":"♍", "천칭자리":"♎", "전갈자리":"♏",
    "사수자리":"♐", "염소자리":"♑", "물병자리":"♒", "물고기자리":"♓",
}

def get_zodiac(month:int, day:int) -> str:
    for sm, sd, em, ed, name in ZODIAC_ORDER:
        if (month == sm and day >= sd) or (month == em and day <= ed):
            return name
    return "알 수 없음"

# =============================
# 데이터 소스: 직접 붙여넣기 + 안전 파서
# =============================
SAMPLE_TEXT = """
1,쌍둥이자리,생각지도 못한 혜택이 있을지도! 쇼핑하러 나가보세요 🛍️,✨ 이마에 삼각형을 그려보세요
2,천칭자리,좋아하는 사람과 가까워질 기회 💕 공통의 관심사로 대화해보세요,✉️ 편지를 써보세요
3,물병자리,뜻밖의 행운이 찾아와요 🌈 지갑을 여유 있게 챙기세요,🥩 불고기를 먹어보세요
4,사수자리,활동적인 하루가 행운을 불러와요 🚴,📸 사진을 찍어보세요
5,사자자리,주위에서 응원이 따르는 날 💪,🌸 꽃 향기를 맡아보세요
6,게자리,마음이 따뜻해지는 하루 🍀,☕ 따뜻한 차를 마셔보세요
7,전갈자리,집중하면 좋은 성과가 있어요 📚,🖋️ 노트에 글을 적어보세요
8,물고기자리,소소한 즐거움이 찾아와요 🎶,🍫 달콤한 간식을 즐기세요
9,염소자리,조금 느리지만 안정적인 하루 🐢,🚶 산책을 해보세요
10,처녀자리,디테일을 놓치지 마세요 🔍,🧴 향수를 뿌려보세요
11,양자리,성급하면 실수가 생길지도 😵,🧘‍♀️ 잠시 명상해보세요
12,황소자리,조금 답답한 하루 💭 너무 무리하지 마세요,🛁 반신욕으로 휴식하세요
""".strip()

@st.cache_data(show_spinner=False)
def parse_rank_text(raw:str) -> List[Dict]:
    """입력 텍스트를 안전하게 파싱해서 [{'rank':int,'zodiac':str,'fortune':str,'lucky':str}] 반환.
       구분자는 콤마(,) 또는 탭(\t) 허용. 잘못된 줄은 자동 건너뜀."""
    out = []
    if not raw:
        return out
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    for ln in lines:
        # 탭 우선, 없으면 콤마
        parts = [p.strip() for p in (ln.split('\t') if '\t' in ln else ln.split(','))]
        if len(parts) < 4:
            continue
        try:
            rank = int(parts[0])
        except Exception:
            continue
        zodiac = parts[1].replace(" ♈","" ).replace(" ♉","" ).replace(" ♊","" ).replace(" ♋","" )\
                          .replace(" ♌","" ).replace(" ♍","" ).replace(" ♎","" ).replace(" ♏","" )\
                          .replace(" ♐","" ).replace(" ♑","" ).replace(" ♒","" ).replace(" ♓","" )
        fortune = parts[2]
        lucky = parts[3]
        if zodiac in ZODIAC_EMOJI:
            out.append({"rank":rank, "zodiac":zodiac, "fortune":fortune, "lucky":lucky})
    # 순위 기준 정렬 & 중복 제거(최초 등장 우선)
    uniq = {}
    for item in sorted(out, key=lambda x: x["rank"]):
        if item["zodiac"] not in uniq:
            uniq[item["zodiac"]] = item
    return list(uniq.values())

# =============================
# 헤더
# =============================
st.markdown(
    f"""
    <h1 style='text-align:center; color:#FF69B4;'>🌅 오늘의 오하아사 별자리 운세</h1>
    <p style='text-align:center;' class='muted'>오늘 날짜: {TODAY_KR}</p>
    """, unsafe_allow_html=True
)

# =============================
# 사이드바: 데이터 입력 방식
# =============================
with st.sidebar:
    st.markdown("### 📥 오늘 방송 순위 붙여넣기")
    st.caption("형식: rank,별자리,운세,행운팁 — 12줄. 탭/콤마 모두 가능")
    raw = st.text_area("예: 1,쌍둥이자리,내용,팁", value=SAMPLE_TEXT, height=260)
    show_table = st.checkbox("전체 순위표도 본문에 보여주기", value=False)

rank_data = parse_rank_text(raw)

if len(rank_data) < 12:
    st.warning("⚠️ 12개 별자리가 모두 입력되지 않았어요. 우선 입력된 항목만 사용할게요.")

# =============================
# 본문: 생일 입력 → 내 별자리 운세 카드
# =============================
birthday = st.date_input("🎂 생일을 입력하세요", value=datetime.date(2000,1,1))
my_sign = get_zodiac(birthday.month, birthday.day)

st.markdown(f"<div class='pill'>내 별자리: {ZODIAC_EMOJI.get(my_sign,'')} {my_sign}</div>", unsafe_allow_html=True)

# 내 별자리 찾기
mine = next((d for d in rank_data if d["zodiac"] == my_sign), None)

if mine:
    st.markdown(
        f"""
        <div class='gold'>
            <h2>🏆 오늘의 순위: {mine['rank']}위</h2>
            <h3>⭐ {ZODIAC_EMOJI.get(my_sign,'')} {my_sign}</h3>
            <p>{mine['fortune']}</p>
            <p>👉 <b>행운 팁:</b> {mine['lucky']}</p>
        </div>
        """, unsafe_allow_html=True
    )
else:
    st.info("오늘 입력된 방송 데이터에 내 별자리가 없어요. 사이드바에 순위를 붙여넣어 주세요!")

# =============================
# 옵션: 전체 순위표(카드 리스트)
# =============================
if show_table and rank_data:
    st.markdown("## 🗒️ 오늘의 전체 순위")
    for item in sorted(rank_data, key=lambda x: x["rank"]):
        cls = "gold" if item["zodiac"] == my_sign else "card"
        st.markdown(
            f"""
            <div class='{cls}'>
                <h3>{item['rank']}위 — {ZODIAC_EMOJI.get(item['zodiac'],'')} {item['zodiac']}</h3>
                <p>{item['fortune']}</p>
                <p class='muted'>행운 팁: {item['lucky']}</p>
            </div>
            """, unsafe_allow_html=True
        )

# =============================
# 푸터
# =============================
st.caption("※ 방송과 동일한 내용을 원하시면, 아침에 본 순위를 그대로 붙여넣으면 앱이 그 내용으로 바로 동작해요 ✨")
