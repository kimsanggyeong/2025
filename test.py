import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="✨ 오하아사 별자리 운세 💖", page_icon="🌟", layout="centered")

st.markdown("""
# 🌸 오늘의 오하아사 🌸
생일을 입력하면 오늘의 귀엽고 깜찍한 운세를 확인할 수 있어요! 🐰💫
""")

# -----------------------------
# 별자리 계산
# -----------------------------
def get_zodiac(month, day):
    zodiac = [
        ("염소자리", (12, 22), (1, 19)),
        ("물병자리", (1, 20), (2, 18)),
        ("물고기자리", (2, 19), (3, 20)),
        ("양자리", (3, 21), (4, 19)),
        ("황소자리", (4, 20), (5, 20)),
        ("쌍둥이자리", (5, 21), (6, 20)),
        ("게자리", (6, 21), (7, 22)),
        ("사자자리", (7, 23), (8, 22)),
        ("처녀자리", (8, 23), (9, 22)),
        ("천칭자리", (9, 23), (10, 22)),
        ("전갈자리", (10, 23), (11, 21)),
        ("사수자리", (11, 22), (12, 21)),
    ]
    for name, start, end in zodiac:
        start_month, start_day = start
        end_month, end_day = end
        if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
            return name
    return "염소자리"

# -----------------------------
# 운세 생성
# -----------------------------
def generate_fortune(zodiac):
    total_texts = [
        f"{zodiac}님, 오늘 하루는 귀여운 일들로 가득해요! 🌸😊",
        f"작은 행복을 발견할 수 있는 날이에요 💖✨",
        f"오늘은 마음이 두근두근 설레는 일이 있을지도 몰라요 🐰💕",
        f"{zodiac}의 매력이 반짝이는 하루가 될 거예요 🌟💗"
    ]
    love_texts = [
        "💌 연애운: 오늘은 솔직한 마음 표현이 통하는 날이에요 💖",
        "💘 썸타기 좋은 기운! 귀여운 메시지를 보내보세요 🐰💌",
        "💞 마음이 통하는 순간이 찾아올 거예요 💕",
        "💖 친구와의 우정도 사랑으로 느껴질 수 있어요 ✨"
    ]
    money_texts = [
        "💰 금전운: 소소한 행운이 찾아오는 날! 🍀",
        "💵 작은 저축이 큰 기쁨으로 돌아올 거예요 💖",
        "🪙 지출은 신중하게, 행운은 가까이에 있어요 ✨",
        "💳 계획적인 소비가 기분까지 행복하게 만들어요 🐰"
    ]
    health_texts = [
        "🍀 건강운: 활기찬 하루! 가벼운 산책 추천 🌸",
        "🏃‍♀️ 운동하면 스트레스가 훨씬 줄어들어요 💪",
        "🥗 균형 잡힌 식사와 충분한 수면이 중요해요 😴",
        "💪 기운 충전! 작은 운동이나 스트레칭으로 하루를 시작하세요 🐰"
    ]
    items = [
        ("⭐ 행운의 별", "오늘은 이 별을 가방에 넣고 다니며 소원을 빌어보세요 🌟"),
        ("🍓 딸기", "딸기 그림이나 사진을 보면 귀여운 기운이 늘어나요 🍓💖"),
        ("🧸 작은 인형", "작은 인형을 손에 쥐고 하루를 보내면 안정감이 생겨요 🐻"),
        ("🎀 리본", "옷이나 소지품에 리본을 달고 다니며 기분을 업! 🎀"),
        ("💎 반짝이는 보석", "반짝이는 물건을 바라보며 자신감을 충전하세요 💎✨")
    ]
    
    return {
        "총운": random.choice(total_texts),
        "사랑운": random.choice(love_texts),
        "금전운": random.choice(money_texts),
        "건강운": random.choice(health_texts),
        "행운아이템": random.choice(items)
    }

# -----------------------------
# 오하아사 순위 생성 (오늘 날짜 기준 고정)
# -----------------------------
def generate_rankings():
    zodiacs = ["양자리","황소자리","쌍둥이자리","게자리","사자자리","처녀자리","천칭자리",
               "전갈자리","사수자리","염소자리","물병자리","물고기자리"]
    random.shuffle(zodiacs)
    rankings = {i+1: z for i, z in enumerate(zodiacs)}
    return rankings

# -----------------------------
# UI 입력
# -----------------------------
birth_date = st.date_input("🎂 생일을 입력해주세요", value=datetime(2000,1,1))
month = birth_date.month
day = birth_date.day
zodiac = get_zodiac(month, day)
st.subheader(f"🌟 당신의 별자리: {zodiac} 🌟")

# 오늘 날짜로 랜덤 시드 고정 (순위 고정용)
today = datetime.today().strftime("%Y-%m-%d")
random.seed(today)

# 운세 생성
fortune = generate_fortune(zodiac)
st.markdown(f"**총운:** {fortune['총운']}")
st.markdown(f"**사랑운:** {fortune['사랑운']}")
st.markdown(f"**금전운:** {fortune['금전운']}")
st.markdown(f"**건강운:** {fortune['건강운']}")

# 행운 아이템
item_name, item_tip = fortune['행운아이템']
st.markdown(f"**오늘의 행운아이템:** {item_name} 🎀")
st.markdown(f"💡 활용 팁: {item_tip}")

# -----------------------------
# 오하아사 순위 표시
# -----------------------------
st.subheader("🏆 오늘의 오하아사 별자리 순위 🏆")
rankings = generate_rankings()
for rank, z in rankings.items():
    medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "✨"
    st.markdown(f"{medal} {rank}위: {z}")

# -----------------------------
# 별자리 이미지
# -----------------------------
zodiac_images = {
    "양자리": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Aries_symbol.svg",
    "황소자리": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Taurus_symbol.svg",
    "쌍둥이자리": "https://upload.wikimedia.org/wikipedia/commons/2/2a/Gemini_symbol.svg",
    "게자리": "https://upload.wikimedia.org/wikipedia/commons/8/8b/Cancer_symbol.svg",
    "사자자리": "https://upload.wikimedia.org/wikipedia/commons/9/9f/Leo_symbol.svg",
    "처녀자리": "https://upload.wikimedia.org/wikipedia/commons/6/64/Virgo_symbol.svg",
    "천칭자리": "https://upload.wikimedia.org/wikipedia/commons/e/e6/Libra_symbol.svg",
    "전갈자리": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Scorpio_symbol.svg",
    "사수자리": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Sagittarius_symbol.svg",
    "염소자리": "https://upload.wikimedia.org/wikipedia/commons/7/76/Capricorn_symbol.svg",
    "물병자리": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Aquarius_symbol.svg",
    "물고기자리": "https://upload.wikimedia.org/wikipedia/commons/3/36/Pisces_symbol.svg",
}
st.image(zodiac_images[zodiac], width=150, caption=f"{zodiac} 이미지 🐰✨")

st.caption("※ 이 운세는 재미로 보는 오하아사 스타일 운세입니다 💖")
