import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="💞 이름+MBTI 궁합 보기", page_icon="✨", layout="centered")

st.title("✨💖 이름 + MBTI 궁합 보기 💖✨")
st.markdown(
    """
    두 사람의 **이름**과 **MBTI**로 궁합 점수를 계산해드려요! (｡♥‿♥｡)
    
    - 귀엽고 깜찍한 **러브 케미 테스트** 💕
    - MBTI 16가지 전 조합을 기반으로 계산 ✨
    - 이름으로 소소한 보너스 점수까지 추가 🎁
    
    👉 결과는 **0~100점** 사이이며, 귀여운 설명과 함께 나옵니다! 🐰
    """
)

# -----------------------------
# MBTI 기본 데이터
# -----------------------------
MBTI_TYPES = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP",
]

# -----------------------------
# 궁합 계산 함수
# -----------------------------
def mbti_pair_score(a: str, b: str):
    base = 50
    score = base
    reasons = []

    for i, (x, y) in enumerate(zip(a, b)):
        if x == y:
            score += 10
            reasons.append(f"{i+1}번째 글자가 같아서 두근두근 ✨")
        else:
            score += 5
            reasons.append(f"{i+1}번째 글자가 달라서 색다른 케미 🌈")

    return min(100, score), reasons

def name_bonus(n1: str, n2: str):
    bonus = 0
    reasons = []
    if n1 and n2:
        if n1[0] == n2[0]:
            bonus += 5
            reasons.append("첫 글자가 같아서 찌릿찌릿 ⚡")
        if n1[-1] == n2[-1]:
            bonus += 5
            reasons.append("끝 글자가 같아서 심쿵 💘")
    return bonus, reasons

def full_score(me_name, me_mbti, you_name, you_mbti):
    mbti_score, mbti_reasons = mbti_pair_score(me_mbti, you_mbti)
    n_bonus, n_reasons = name_bonus(me_name, you_name)
    total = min(100, mbti_score + n_bonus)

    if total >= 85:
        verdict = "💘💕 완전 찰떡궁합! 사랑 폭발 💕💘"
    elif total >= 70:
        verdict = "🌸💖 좋은 케미! 알콩달콩 사랑스러워요 💖🌸"
    elif total >= 55:
        verdict = "💛 무난무난~ 노력하면 더 귀여운 커플 💛"
    elif total >= 40:
        verdict = "💙 서로 다르지만 그게 또 매력! 💙"
    else:
        verdict = "💔 귀여운 티키타카 연습이 필요해요 💔"

    return total, verdict, mbti_reasons, n_reasons

# -----------------------------
# UI 입력
# -----------------------------
col1, col2 = st.columns(2)
with col1:
    me_name = st.text_input("내 이름 🐰", value="")
    me_mbti = st.selectbox("내 MBTI 🌸", MBTI_TYPES, index=7)
with col2:
    you_name = st.text_input("상대 이름 🐻", value="")
    you_mbti = st.selectbox("상대 MBTI 🌟", MBTI_TYPES, index=0)

if st.button("✨🔮 궁합 보기 🔮✨"):
    if me_mbti not in MBTI_TYPES or you_mbti not in MBTI_TYPES:
        st.error("MBTI 입력이 올바르지 않습니다.")
    else:
        total, verdict, mbti_reasons, n_reasons = full_score(me_name, me_mbti, you_name, you_mbti)

        st.subheader("💞 결과 💞")
        st.metric("최종 점수", f"{total}")
        st.success(verdict)

        with st.expander("🌈 궁합 설명 보기"):
            st.markdown("**💌 MBTI 근거**")
            for r in mbti_reasons:
                st.write("- ", r)
            if n_reasons:
                st.markdown("**🎀 이름 보너스**")
                for r in n_reasons:
                    st.write("- ", r)

# -----------------------------
# 전체 궁합표
# -----------------------------
with st.expander("📊 전체 16×16 MBTI 궁합표 보기"):
    data = np.zeros((16, 16), dtype=int)
    for i, a in enumerate(MBTI_TYPES):
        for j, b in enumerate(MBTI_TYPES):
            data[i, j] = mbti_pair_score(a, b)[0]
    df = pd.DataFrame(data, index=MBTI_TYPES, columns=MBTI_TYPES)

    st.dataframe(df)

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    im = ax.imshow(df.values, aspect='auto')
    ax.set_xticks(range(len(MBTI_TYPES)))
    ax.set_yticks(range(len(MBTI_TYPES)))
    ax.set_xticklabels(MBTI_TYPES, rotation=45, ha='right')
    ax.set_yticklabels(MBTI_TYPES)
    ax.set_title("🌸 MBTI 궁합표 🌸")
    plt.tight_layout()
    st.pyplot(fig)

    csv = df.to_csv(index=True).encode('utf-8-sig')
    st.download_button(
        label="⬇️ CSV 다운로드 🎀",
        data=csv,
        file_name="mbti_compatibility_table.csv",
        mime="text/csv",
    )

st.caption("※ 이 앱은 귀여운 오락/참고용이에요! 실제 관계는 소통과 사랑이 중요합니다 🐰💝")
