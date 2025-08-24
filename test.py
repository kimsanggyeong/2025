import streamlit as st
import datetime

# -------------------------
# 오늘 날짜
# -------------------------
today = datetime.date.today().strftime("%Y년 %m월 %d일")

# -------------------------
# 오하아사 운세 데이터 (샘플)
# -------------------------
ohasa_data = [
    {"rank": 1, "zodiac": "쌍둥이자리", "fortune": "생각지도 못한 혜택이 있을지도! 쇼핑하러 나가보세요 🛍️", "lucky": "✨ 이마에 삼각형을 그려보세요"},
    {"rank": 2, "zodiac": "천칭자리", "fortune": "좋아하는 사람과 가까워질 기회 💕 공통의 관심사로 대화해보세요", "lucky": "✉️ 편지를 써보세요"},
    {"rank": 3, "zodiac": "물병자리", "fortune": "뜻밖의 행운이 찾아와요 🌈 지갑을 여유 있게 챙기세요", "lucky": "🥩 불고기를 먹어보세요"},
    {"rank": 4, "zodiac": "사수자리", "fortune": "활동적인 하루가 행운을 불러와요 🚴", "lucky": "📸 사진을 찍어보세요"},
    {"rank": 5, "zodiac": "사자자리", "fortune": "주위에서 응원이 따르는 날 💪", "lucky": "🌸 꽃 향기를 맡아보세요"},
    {"rank": 6, "zodiac": "게자리", "fortune": "마음이 따뜻해지는 하루 🍀", "lucky": "☕ 따뜻한 차를 마셔보세요"},
    {"rank": 7, "zodiac": "전갈자리", "fortune": "집중하면 좋은 성과가 있어요 📚", "lucky": "🖋️ 노트에 글을 적어보세요"},
    {"rank": 8, "zodiac": "물고기자리", "fortune": "소소한 즐거움이 찾아와요 🎶", "lucky": "🍫 달콤한 간식을 즐기세요"},
    {"rank": 9, "zodiac": "염소자리", "fortune": "조금 느리지만 안정적인 하루 🐢", "lucky": "🚶 산책을 해보세요"},
    {"rank": 10, "zodiac": "처녀자리", "fortune": "디테일을 놓치지 마세요 🔍", "lucky": "🧴 향수를 뿌려보세요"},
    {"rank": 11, "zodiac": "양자리", "fortune": "성급하면 실수가 생길지도 😵", "lucky": "🧘‍♀️ 잠시 명상해보세요"},
    {"rank": 12, "zodiac": "황소자리", "fortune": "조금 답답한 하루 💭 너무 무리하지 마세요", "lucky": "🛁 반신욕으로 휴식하세요"},
]

# -------------------------
# 생일 → 별자리 계산 함수
# -------------------------
def get_zodiac(month, day):
    zodiac_dates = [
        ((3,21),(4,19),"양자리"),
        ((4,20),(5,20),"황소자리"),
        ((5,21),(6,21),"쌍둥이자리"),
        ((6,22),(7,22),"게자리"),
        ((7,23),(8,22),"사자자리"),
        ((8,23),(9,22),"처녀자리"),
        ((9,23),(10,23),"천칭자리"),
        ((10,24),(11,22),"전갈자리"),
        ((11,23),(12,21),"사수자리"),
        ((12,22),(1,19),"염소자리"),
        ((1,20),(2,18),"물병자리"),
        ((2,19),(3,20),"물고기자리"),
    ]
    for start, end, sign in zodiac_dates:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            return sign
    return "알 수 없음"

# -------------------------
# Streamlit 앱 UI
# -------------------------
st.set_page_config(page_title="오하아사 별자리 운세", page_icon="🌅", layout="centered")

st.markdown(
    f"""
    <h1 style='text-align:center; color:#FF69B4;'>
        🌅 오늘의 오하아사 별자리 운세 🌅
    </h1>
    <p style='text-align:center; font-size:18px;'>
        오늘 날짜: {today}
    </p>
    """, unsafe_allow_html=True
)

# -------------------------
# 생일 입력
# -------------------------
birthday = st.date_input("🎂 생일을 입력하세요:", value=datetime.date(2000,1,1))
my_sign = get_zodiac(birthday.month, birthday.day)

st.markdown(f"### 🔮 당신의 별자리는 **{my_sign}** 입니다!")

# -------------------------
# 오늘의 운세 찾기
# -------------------------
my_fortune = None
for data in ohasa_data:
    if my_sign in data["zodiac"]:
        my_fortune = data
        break

if my_fortune:
    st.markdown(
        f"""
        <div style="background-color:#FFF0F5; padding:20px; border-radius:20px; 
                    box-shadow:2px 4px 10px rgba(0,0,0,0.1); margin-top:20px;">
            <h2 style="color:#FF69B4;">🏆 오늘의 순위: {my_fortune['rank']}위</h2>
            <h3>⭐ {my_fortune['zodiac']} ⭐</h3>
            <p>{my_fortune['fortune']}</p>
            <p>👉 <b>행운 팁:</b> {my_fortune['lucky']}</p>
        </div>
        """, unsafe_allow_html=True
    )
else:
    st.warning("해당 별자리의 운세 정보를 찾을 수 없어요 😢")
