import streamlit as st
import datetime
import requests
from bs4 import BeautifulSoup

# ------------------------------
# 오늘 날짜 포맷
# ------------------------------
today = datetime.date.today().strftime("%Y년 %m월 %d일")

# ------------------------------
# 생일 → 별자리 계산 함수
# ------------------------------
def get_zodiac(month, day):
    zodiac_dates = [
        ((3,21),(4,19),"양자리"), ((4,20),(5,20),"황소자리"), ((5,21),(6,21),"쌍둥이자리"),
        ((6,22),(7,22),"게자리"), ((7,23),(8,22),"사자자리"), ((8,23),(9,22),"처녀자리"),
        ((9,23),(10,23),"천칭자리"), ((10,24),(11,22),"전갈자리"), ((11,23),(12,21),"사수자리"),
        ((12,22),(1,19),"염소자리"), ((1,20),(2,18),"물병자리"), ((2,19),(3,20),"물고기자리"),
    ]
    for start, end, name in zodiac_dates:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            return name
    return "알 수 없음"

# ------------------------------
# 웹 크롤링 함수 (예시)
# ------------------------------
def fetch_ohasa_rank():
    url = "https://www.asahi.co.jp/ohaasa/"  # 실제 운세 페이지 주소로 필요 시 변경
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    rankings = []  # 순위별 딕셔너리 리스트로 생성

    # 아래는 예시 구조, 실제 구조에 맞춰 CSS 선택자 조정 필요
    items = soup.select(".star-ranking-item")  # 페이지 구조에 맞게 변경
    for item in items:
        rank = item.select_one(".rank").text.strip()
        zodiac = item.select_one(".zodiac").text.strip()
        fortune = item.select_one(".fortune").text.strip()
        lucky = item.select_one(".lucky-tip").text.strip()
        rankings.append({
            "rank": rank,
            "zodiac": zodiac,
            "fortune": fortune,
            "lucky": lucky
        })
    return rankings

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="오하아사 별자리 운세", page_icon="🌅", layout="centered")
st.markdown(f"""<h1 style='text-align:center; color:#FF69B4;'>🌅 오늘의 오하아사 운세</h1>
<p style='text-align:center;'>오늘 날짜: {today}</p>""", unsafe_allow_html=True)

birthday = st.date_input("🎂 생일 입력", value=datetime.date(2000,1,1))
my_sign = get_zodiac(birthday.month, birthday.day)
st.markdown(f"### 당신의 별자리는 **{my_sign}** 입니다!")

# ------------------------------
# 운세 데이터 가져오기
# ------------------------------
with st.spinner("오늘의 운세를 불러오는 중..."):
    try:
        data = fetch_ohasa_rank()
    except Exception as e:
        st.error("오하아사 데이터를 가져오는 데 실패했어요… 인터넷 연결이나 크롤링 코드 구조를 확인해 주세요.")
        st.stop()

# ------------------------------
# 해당 별자리 데이터 찾기 및 카드 표시
# ------------------------------
found = next((d for d in data if my_sign in d["zodiac"]), None)

if found:
    st.markdown(f"""
    <div style="background-color:#FFF0F5; padding:20px; border-radius:20px;
                box-shadow:2px 4px 10px rgba(0,0,0,0.1); margin-top:20px;">
        <h2 style="color:#FF69B4;">🏆 오늘의 순위: {found['rank']}위</h2>
        <h3>⭐ {found['zodiac']} ⭐</h3>
        <p>{found['fortune']}</p>
        <p>👉 <b>행운 팁:</b> {found['lucky']}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("오늘 운세 데이터에 해당 별자리가 없어요… 다른 방법을 시도해볼까요?")
