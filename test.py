import streamlit as st
import datetime

# -------------------------
# 별자리 계산 함수
# -------------------------
def get_zodiac(month, day):
    zodiac_dates = [
        ("물병자리 ♒", (1,20), (2,18)),
        ("물고기자리 ♓", (2,19), (3,20)),
        ("양자리 ♈", (3,21), (4,19)),
        ("황소자리 ♉", (4,20), (5,20)),
        ("쌍둥이자리 ♊", (5,21), (6,21)),
        ("게자리 ♋", (6,22), (7,22)),
        ("사자자리 ♌", (7,23), (8,22)),
        ("처녀자리 ♍", (8,23), (9,22)),
        ("천칭자리 ♎", (9,23), (10,23)),
        ("전갈자리 ♏", (10,24), (11,22)),
        ("사수자리 ♐", (11,23), (12,21)),
        ("염소자리 ♑", (12,22), (1,19)),
    ]

    for sign, (sm, sd), (em, ed) in zodiac_dates:
        if (month == sm and day >= sd) or (month == em and day <= ed):
            return sign
    return "알 수 없음"

# -------------------------
# 오늘의 운세 데이터 (오하아사 느낌)
# -------------------------
ohasa_data = {
    "쌍둥이자리 ♊": {"rank":1, "fortune":"생각지도 못한 혜택이 있을지도! 🛍️", "lucky":"✨ 이마에 삼각형을 그려보세요"},
    "천칭자리 ♎": {"rank":2, "fortune":"좋아하는 사람과 가까워질 기회 💕", "lucky":"✉️ 편지를 써보세요"},
    "물병자리 ♒": {"rank":3, "fortune":"뜻밖의 행운이 찾아와요 🌈", "lucky":"🥩 불고기를 먹어보세요"},
    "사수자리 ♐": {"rank":4, "fortune":"활동적인 하루가 행운을 불러와요 🚴", "lucky":"📸 사진을 찍어보세요"},
    "사자자리 ♌": {"rank":5, "fortune":"주위에서 응원이 따르는 날 💪", "lucky":"🌸 꽃 향기를 맡아보세요"},
    "게자리 ♋": {"rank":6, "fortune":"마음이 따뜻해지는 하루 🍀", "lucky":"☕ 따뜻한 차를 마셔보세요"},
    "전갈자리 ♏": {"rank":7, "fortune":"집중하면 좋은 성과가 있어요 📚", "lucky":"🖋️ 노트에 글을 적어보세요"},
    "물고기자리 ♓": {"rank":8, "fortune":"소소한 즐거움이 찾아와요 🎶", "lucky":"🍫 달콤한 간식을 즐기세요"},
    "염소자리 ♑": {"rank":9, "fortune":"조금 느리지만 안정적인 하루 🐢", "lucky":"🚶 산책을 해보세요"},
    "처녀자리 ♍": {"rank":10,"fortune":"디테일을 놓치지 마세요 🔍", "lucky":"🧴 향수를 뿌려보세요"},
    "양자리 ♈": {"rank":11,"fortune":"성급하면 실수가 생길지도 😵", "lucky":"🧘‍♀️ 잠시 명상해보세요"},
    "황소자리 ♉": {"rank":12,"fortune":"조금 답답한 하루 💭", "lucky":"🛁 반신욕으로 휴식하세요"},
}

# -------------------------
# Streamlit 앱 UI
# -------------------------
st.set_page_config(page_title="오하아사 별자리 운세", page_icon="🌅", layout="centered")

st.markdown(
    "<h1 style='text-align:center; color:#FF69B4;'>🌅 오늘의 오하아사 별자리 운세 🌅</h1>",
    unsafe_allow_html=True
)

# 생일 입력 받기
birthday = st.date_input("🎂 생일을 입력하세요", datetime.date(2000,1,1))

if birthday:
    zodiac = get_zodiac(birthday.month, birthday.day)
    st.markdown(f"## ✨ 당신의 별자리는 {zodiac} 입니다!")

    if zodiac in ohasa_data:
        data = ohasa_data[zodiac]

        st.markdown(
            f"""
            <div style='background:#FFF0F5; border-radius:20px; padding:25px; text-align:center; 
                        box-shadow:2px 4px 12px rgba(0,0,0,0.15); margin-top:20px;'>
                <h2 style='color:#FF69B4;'>🏆 오늘의 순위: {data['rank']}위</h2>
                <p style='font-size:18px;'>🔮 운세: {data['fortune']}</p>
                <p style='font-size:18px;'>🍀 행운 팁: {data['lucky']}</p>
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.warning("오늘은 별자리 운세 데이터가 없어요 😢")
