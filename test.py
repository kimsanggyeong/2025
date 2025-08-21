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
# 오늘의 운세 데이터
# -------------------------
horoscope_data = {
    "물병자리": "새로운 아이디어가 떠오르는 하루! 💡",
    "물고기자리": "마음이 따뜻해지는 하루가 될 거예요. 🌊",
    "양자리": "도전정신이 빛나는 날! 🔥",
    "황소자리": "꾸준함이 큰 힘을 발휘해요. 🐂",
    "쌍둥이자리": "대화 속에서 행운이 숨어있어요. 💬",
    "게자리": "가족이나 친구와의 시간이 소중해요. 🦀",
    "사자자리": "자신감을 가지면 좋은 결과가 와요. 🦁",
    "처녀자리": "세심함이 당신을 빛나게 해요. 🌸",
    "천칭자리": "균형 잡힌 하루, 조화가 필요해요. ⚖️",
    "전갈자리": "집중력이 높아 성과가 커져요. 🦂",
    "사수자리": "여행이나 모험이 행운을 가져와요. 🏹",
    "염소자리": "성실함이 빛나는 하루예요. ⛰️"
}

lucky_items = ["🍎 사과", "☕ 커피", "📖 책", "🎧 이어폰", "🌂 우산", "🍀 네잎클로버", "🧸 인형", "💄 립밤", "🍫 초콜릿", "🕶️ 선글라스"]
good_things = ["친구에게 연락하기", "일찍 일어나기", "작은 선물하기", "산책하기", "좋아하는 음악 듣기", "웃는 얼굴 유지하기", "하루 계획 세우기"]

# -------------------------
# 오늘 날짜 기반 별자리 순위 (고정)
# -------------------------
today = datetime.date.today()
random.seed(today.toordinal())  # 날짜 기준 고정된 순위
zodiac_list = list(horoscope_data.keys())
random.shuffle(zodiac_list)

# -------------------------
# Streamlit 앱 UI
# -------------------------
st.set_page_config(page_title="오늘의 별자리 운세 (오하아사)", page_icon="✨", layout="centered")

st.markdown("<h1 style='text-align:center; color:#FF69B4;'>✨ 오늘의 별자리 운세 (오하아사) ✨</h1>", unsafe_allow_html=True)
st.write("생일을 입력하면 오늘의 별자리 운세와 순위를 확인할 수 있어요! 🎀")

birth = st.date_input("🎂 나의 생일을 입력하세요:", datetime.date(2000, 1, 1))

if birth:
    zodiac = get_zodiac(birth.month, birth.day)
    st.subheader(f"🌟 당신의 별자리는 **{zodiac}** 입니다! 🌟")

    # 운세 보여주기
    st.markdown(f"<h3 style='color:#FF82AB;'>🔮 오늘의 운세:</h3>", unsafe_allow_html=True)
    st.info(horoscope_data[zodiac])

    # 오늘의 순위
    rank = zodiac_list.index(zodiac) + 1
    st.markdown(f"<h3 style='color:#9370DB;'>🏆 오늘의 별자리 순위: {rank}위</h3>", unsafe_allow_html=True)

    # 행운 아이템 & 좋은 행동
    lucky_item = random.choice(lucky_items)
    good_thing = random.choice(good_things)

    st.success(f"🎁 행운의 아이템: {lucky_item}")
    st.warning(f"💡 오늘 하면 좋은 일: {good_thing}")
