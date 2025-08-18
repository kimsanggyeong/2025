import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="✨ 오하아사 별자리 운세 💖", page_icon="🌟", layout="centered")

st.title("🌸 오늘의 오하아사 별자리 운세 🌸")
st.markdown("생일을 입력하면 오늘의 귀엽고 깜찍한 운세를 알려드려요! 🐰💫")

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
# 귀여운 운세 생성
# -----------------------------
def cute_ohasa_fortune(zodiac):
    fortunes = ["💖 대박 행운!", "💛 기분 좋은 하루!", "💚 작은 행복 가득!", "💜 오늘은 집중 💫", "💙 사랑이 넘치는 하루!"]
    love = ["💌 연애운 상승!", "💘 썸타기 좋은 날!", "💞 마음이 통하는 하루!", "💖 귀여운 티키타카 💖", "💓 혼자만의 시간도 즐거워요"]
    money = ["💰 용돈 벌기 좋은 날!", "💵 알뜰하게!", "💎 쇼핑은 신중하게", "🪙 행운의 재물", "💳 카드 사용 조심!"]
    health = ["🍀 활기찬 하루!", "🏃‍♀️ 운동 추천!", "🥗 건강식 챙기기", "😴 충분한 휴식 필요", "💪 기운 충전!"]
    items = ["⭐ 행운의 별", "🍓 딸기", "🧸 작은 인형", "🎀 리본", "💎 반짝이는 보석"]

    return {
        "총운": random.choice(fortunes),
        "사랑운": random.choice(love),
        "금전운": random.choice(money),
        "건강운": random.choice(health),
        "행운아이템": random.choice(items)
    }

# -----------------------------
# UI 입력
# -----------------------------
birth_date = st.date_input("🎂 생일을 입력해주세요", value=datetime(2000,1,1))

month = birth_date.month
day = birth_date.day
zodiac = get_zodiac(month, day)
st.subheader(f"🌟 당신의 별자리: {zodiac} 🌟")

fortune = cute_ohasa_fortune(zodiac)
st.markdown(f"**총운:** {fortune['총운']}")
st.markdown(f"**사랑운:** {fortune['사랑운']}")
st.markdown(f"**금전운:** {fortune['금전운']}")
st.markdown(f"**건강운:** {fortune['건강운']}")
st.markdown(f"**오늘의 행운아이템:** {fortune['행운아이템']} 🎀")

# -----------------------------
# 귀여운 별자리 이미지
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
