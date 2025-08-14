import streamlit as st

st.set_page_config(page_title="MBTI 궁합 테스트", page_icon="💖", layout="centered")

st.title("💖 MBTI 궁합 테스트")
st.write("자신과 상대방의 MBTI를 선택하고 궁합을 확인하세요!")

# MBTI 리스트
mbti_list = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

# 궁합 데이터 (간단 예시 - 실제로는 세부 분석 가능)
# 데이터 구조: compatibility_data[내MBTI][상대MBTI] = {"score": int, "desc": str}
compatibility_data = {
    "ISTJ": {
        "ISTJ": {"score": 70, "desc": "비슷한 성향이라 안정감 있지만 지루할 수 있음."},
        "ISFJ": {"score": 85, "desc": "서로 배려하며 안정적인 관계 가능."},
        "INFJ": {"score": 80, "desc": "서로 조용하지만 가치관이 맞으면 깊은 관계 형성."},
        "INTJ": {"score": 75, "desc": "계획적이고 목표지향적인 점에서 궁합이 좋음."},
        "ISTP": {"score": 65, "desc": "실용적이지만 감정 교류 부족 가능."},
        "ISFP": {"score": 78, "desc": "서로 조용하고 차분한 성향으로 잘 맞음."},
        "INFP": {"score": 60, "desc": "가치관 차이가 있어 이해가 필요."},
        "INTP": {"score": 68, "desc": "논리적이지만 생활 패턴이 다를 수 있음."},
        "ESTP": {"score": 82, "desc": "서로 보완하며 활기찬 관계 가능."},
        "ESFP": {"score": 90, "desc": "서로의 부족한 부분을 채워줌."},
        "ENFP": {"score": 55, "desc": "성향 차이가 커서 갈등 가능."},
        "ENTP": {"score": 60, "desc": "서로 다른 생활방식으로 마찰 가능."},
        "ESTJ": {"score": 88, "desc": "실용적이고 목표지향적으로 잘 맞음."},
        "ESFJ": {"score": 85, "desc": "서로 배려하며 안정적."},
        "ENFJ": {"score": 72, "desc": "목표를 공유하면 좋은 시너지."},
        "ENTJ": {"score": 80, "desc": "계획적이고 강한 추진력으로 잘 맞음."},
    },
    # 여기서 나머지 15개 MBTI도 동일 구조로 채우면 완성
}

# 두 사람 MBTI 선택
col1, col2 = st.columns(2)
with col1:
    my_mbti = st.selectbox("당신의 MBTI", mbti_list)
with col2:
    partner_mbti = st.selectbox("상대방의 MBTI", mbti_list)

# 결과 표시
if my_mbti in compatibility_data and partner_mbti in compatibility_data[my_mbti]:
    score = compatibility_data[my_mbti][partner_mbti]["score"]
    desc = compatibility_data[my_mbti][partner_mbti]["desc"]

    st.markdown(f"### 💘 궁합 점수: **{score} / 100**")
    st.progress(score / 100)
    st.write(desc)
else:
    st.warning("아직 해당 MBTI 조합의 데이터가 준비되지 않았습니다.")

st.caption("⚠️ 이 결과는 참고용이며, 실제 관계의 성공 여부는 사람마다 다를 수 있습니다.")
