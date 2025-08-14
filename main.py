import streamlit as st

# 제목
st.title("💖 MBTI 궁합 확인기")

# MBTI 리스트
mbti_list = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

# 궁합 데이터 (예시)
compatibility_data = {
    "ISTJ": {
        "best": "ESFP",
        "worst": "ENFP",
        "desc": {
            "ESFP": "ISTJ는 현실적이고 신중하며, ESFP는 자유롭고 사교적이라 서로 보완이 잘 됩니다.",
            "ENFP": "ISTJ는 계획적이고 ENFP는 즉흥적이라 충돌이 발생하기 쉽습니다."
        }
    },
    "ENFP": {
        "best": "INFJ",
        "worst": "ISTJ",
        "desc": {
            "INFJ": "ENFP의 에너지를 INFJ의 깊이 있는 성찰이 잘 받아줍니다.",
            "ISTJ": "ENFP의 자유분방함이 ISTJ의 규칙성에 부딪힐 수 있습니다."
        }
    },
    # 필요하면 여기서 나머지 MBTI 궁합도 채워 넣기
}

# 사용자가 MBTI 선택
my_mbti = st.selectbox("당신의 MBTI를 선택하세요", mbti_list)

# 궁합 결과 표시
if my_mbti in compatibility_data:
    best_match = compatibility_data[my_mbti]["best"]
    worst_match = compatibility_data[my_mbti]["worst"]
    st.subheader(f"💘 최고의 궁합: {best_match}")
    st.write(compatibility_data[my_mbti]["desc"][best_match])

    st.subheader(f"⚡ 최악의 궁합: {worst_match}")
    st.write(compatibility_data[my_mbti]["desc"][worst_match])
else:
    st.warning("이 MBTI의 궁합 데이터가 아직 준비되지 않았습니다.")

# 실행 방법 안내
st.markdown("---")
st.caption("이 앱은 예시 데이터이며, 실제 MBTI 궁합은 사람마다 다를 수 있습니다 😊")

