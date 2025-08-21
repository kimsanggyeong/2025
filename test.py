import streamlit as st
import datetime
import random

# -------------------------
# 별자리 계산 함수
# -------------------------
def get_zodiac(month, day):
    zodiac_dates = [
        ("물병자리", (1, 20), (2, 18)),
        ("물고기자리", (2, 19), (3, 20)),
        ("양자리", (3, 21), (4, 19)),
        ("황소자리", (4, 20), (5, 20)),
        ("쌍둥이자리", (5, 21), (6, 21)),
        ("게자리", (6, 22), (7, 22)),
        ("사자자리", (7, 23), (8, 22)),
        ("처녀자리", (8, 23), (9, 22)),
        ("천칭자리", (9, 23), (10, 22)),
        ("전갈자리", (10, 23), (11, 22)),
        ("사수자리", (11, 23), (12, 21)),
        ("염소자리", (12, 22), (1, 19)),
    ]
    for sign, start, end in zodiac_dates:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            return sign
    return "알 수 없음"

# -------------------------
# 오늘의 운세 데이터 (여러 개 준비 → 매일 다르게)
# -------------------------
horoscope_data = {
    "물병자리": [
        "새로운 아이디어가 떠오르는 하루! 💡",
        "좋은 소식을 듣게 될 거예요 📩",
        "주변 사람에게 친절하게 대하면 행운이 와요 🌈"
    ],
    "물고기자리": [
        "마음이 따뜻해지는 하루가 될 거예요 🌊",
        "작은 배려가 큰 기쁨을 가져와요 🌟",
        "오늘은 직감이 놀랍도록 잘 맞아요 🔮"
    ],
    "양자리": [
        "도전정신이 빛나는 날! 🔥",
        "용기를 내면 좋은 일이 생겨요 💪",
        "새로운 시작이 좋은 결과로 이어져요 🌱"
    ],
    # (다른 별자리들도 3개씩 넣어주면 좋아요)
}

# 행운 아이템 + 사용법
lucky_items = {
    "🍎 사과": "오늘은 사과를 먹으면 활력이 넘쳐나요!",
    "☕ 커피": "새로운 사람과 커피를 마시면 좋은 일이 생겨요!",
    "📖 책": "책에서 영감을 얻어보세요, 좋은 아이디어가 떠오를 거예요!",
    "🎧 이어폰": "좋아하는 음악을 들으면 기분이 한층 밝아져요!",
    "🌂 우산": "비가 오지 않아도 우산을 챙기면 뜻밖의 행운이 와요!",
    "🍀 네잎클로버": "지갑에 넣어두면 하루가 반짝 빛날 거예요!",
    "🧸 인형": "인형과 함께 있으면 마음이 따뜻해져요!",
    "💄 립밤": "립밤을 바르면 좋은 인연이 다가와요!",
    "🍫 초콜릿": "친구에게 나눠주면 행복이 두 배가 돼요!",
    "🕶️ 선글라스": "햇살 아래에서 자신감이 빛나요!"
}

# -------------------------
# 오늘 날짜 기반 랜덤 고정
# -------------------------
today = datetime.date.today()
random.seed(today.toordinal())  # 날짜 기준 고정

zodiac_list = list(horoscope_data.keys())
random.shuffle(zodiac_list)

# -------------------------
# Streamlit 앱 UI
# -------------------------
st.set_page_config(page_title="오늘의 별자리 운세 (오하아사)", page_icon="✨", layout="centered")

st.markdown("<h1 style='text-align:center; color:#FF69B4;'>✨ 오늘의 오하아사 ✨</h1>", unsafe_allow_html=True)
st.write("생일을 입력하면 오늘의 별자리 운세와 순위를 확인할 수 있어요! 🎀")

birth = st.date_input("🎂 나의 생일을 입력하세요:", datetime.date(2000, 1, 1))

if birth:
    zodiac = get_zodiac(birth.month, birth.day)
    st.subheader(f"🌟 당신의 별자리는 **{zodiac}** 입니다! 🌟")

    # 오늘의 운세 (여러 개 중 랜덤)
    if zodiac in horoscope_data:
        daily_fortune = random.choice(horoscope_data[zodiac])
    else:
        daily_fortune = "오늘은 특별한 하루가 될 거예요 ✨"
    
    st.markdown(f"<h3 style='color:#FF82AB;'>🔮 오늘의 운세:</h3>", unsafe_allow_html=True)
    st.info(daily_fortune)

    # 오늘의 순위
    rank = zodiac_list.index(zodiac) + 1
    st.markdown(f"<h3 style='color:#9370DB;'>🏆 오늘의 별자리 순위: {rank}위</h3>", unsafe_allow_html=True)

    # 오늘의 행운 아이템
    lucky_item, usage = random.choice(list(lucky_items.items()))
    st.success(f"🎁 오늘의 행운 아이템: {lucky_item}")
    st.warning(f"✨ 행운을 부르는 사용법: {usage}")
