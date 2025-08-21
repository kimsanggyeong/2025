import streamlit as st
import datetime

# -------------------------
# 오늘 날짜 (샘플 데이터용)
# -------------------------
today = datetime.date.today().strftime("%Y년 %m월 %d일")

# -------------------------
# 오하아사 방송 스타일 운세 데이터 (예시)
# 실제라면 매일 크롤링/업데이트 필요
# -------------------------
ohasa_data = [
    {"rank": 1, "zodiac": "쌍둥이자리 ♊", "fortune": "생각지도 못한 혜택이 있을지도! 쇼핑하러 나가보세요 🛍️", "lucky": "✨ 이마에 삼각형을 그려보세요"},
    {"rank": 2, "zodiac": "천칭자리 ♎", "fortune": "좋아하는 사람과 가까워질 기회 💕 공통의 관심사로 대화해보세요", "lucky": "✉️ 편지를 써보세요"},
    {"rank": 3, "zodiac": "물병자리 ♒", "fortune": "뜻밖의 행운이 찾아와요 🌈 지갑을 여유 있게 챙기세요", "lucky": "🥩 불고기를 먹어보세요"},
    {"rank": 4, "zodiac": "사수자리 ♐", "fortune": "활동적인 하루가 행운을 불러와요 🚴", "lucky": "📸 사진을 찍어보세요"},
    {"rank": 5, "zodiac": "사자자리 ♌", "fortune": "주위에서 응원이 따르는 날 💪", "lucky": "🌸 꽃 향기를 맡아보세요"},
    {"rank": 6, "zodiac": "게자리 ♋", "fortune": "마음이 따뜻해지는 하루 🍀", "lucky": "☕ 따뜻한 차를 마셔보세요"},
    {"rank": 7, "zodiac": "전갈자리 ♏", "fortune": "집중하면 좋은 성과가 있어요 📚", "lucky": "🖋️ 노트에 글을 적어보세요"},
    {"rank": 8, "zodiac": "물고기자리 ♓", "fortune": "소소한 즐거움이 찾아와요 🎶", "lucky": "🍫 달콤한 간식을 즐기세요"},
    {"rank": 9, "zodiac": "염소자리 ♑", "fortune": "조금 느리지만 안정적인 하루 🐢", "lucky": "🚶 산책을 해보세요"},
    {"rank": 10, "zodiac": "처녀자리 ♍", "fortune": "디테일을 놓치지 마세요 🔍", "lucky": "🧴 향수를 뿌려보세요"},
    {"rank": 11, "zodiac": "양자리 ♈", "fortune": "성급하면 실수가 생길지도 😵", "lucky": "🧘‍♀️ 잠시 명상해보세요"},
    {"rank": 12, "zodiac": "황소자리 ♉", "fortune": "조금 답답한 하루 💭 너무 무리하지 마세요", "lucky": "🛁 반신욕으로 휴식하세요"},
]

# -------------------------
# Streamlit 앱 UI
# -------------------------
st.set_page_config(page_title="오하아사 별자리 운세", page_icon="🌅", layout="centered")

st.markdown(f"<h1 style='text-align:center; color:#FF69B4;'>🌅 오늘의 오하아사 🌅</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-size:18px;'><br>오늘 날짜: {today}</p>", unsafe_allow_html=True)

# -------------------------
# 내 별자리 입력
# -------------------------
my_sign = st.selectbox("🔮 나의 별자리를 선택하세요:", 
                       ["양자리 ♈","황소자리 ♉","쌍둥이자리 ♊","게자리 ♋",
                        "사자자리 ♌","처녀자리 ♍","천칭자리 ♎","전갈자리 ♏",
                        "사수자리 ♐","염소자리 ♑","물병자리 ♒","물고기자리 ♓"])

# -------------------------
# 순위 전체 표시
# -------------------------
st.markdown("## 🏆 오늘의 별자리 순위")
for data in ohasa_data:
    # 내 별자리 강조
    if my_sign in data["zodiac"]:
        st.success(f"✨ {data['rank']}위: {data['zodiac']} ✨\n\n{data['fortune']}\n\n👉 행운 팁: {data['lucky']}")
    else:
        st.write(f"**{data['rank']}위: {data['zodiac']}** — {data['fortune']} (행운팁: {data['lucky']})")
