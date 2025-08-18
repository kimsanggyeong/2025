import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List

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
# MBTI / Temperament Utilities
# -----------------------------
MBTI_TYPES = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP",
]

TEMPERAMENT = {
    # NT
    "INTJ":"NT","INTP":"NT","ENTJ":"NT","ENTP":"NT",
    # NF
    "INFJ":"NF","INFP":"NF","ENFJ":"NF","ENFP":"NF",
    # SJ
    "ISTJ":"SJ","ISFJ":"SJ","ESTJ":"SJ","ESFJ":"SJ",
    # SP
    "ISTP":"SP","ISFP":"SP","ESTP":"SP","ESFP":"SP",
}

def normalize_mbti(s: str) -> str:
    if not s:
        return ""
    s = s.strip().upper()
    valid = set(list("EISNTFJP"))
    if len(s) != 4 or any(ch not in valid for ch in s):
        return ""
    return s

# -----------------------------
# Scoring Logic
# -----------------------------

def mbti_pair_score(a: str, b: str) -> Tuple[int, List[str]]:
    a = normalize_mbti(a)
    b = normalize_mbti(b)
    assert a and b and a in MBTI_TYPES and b in MBTI_TYPES

    base = 50
    reasons = []

    pairs_bonus = 0
    for i, (x, y) in enumerate(zip(a, b)):
        if x == y:
            pairs_bonus += 12
            reasons.append(f"{i+1}번째 자리(\"{x}\")가 같아 두근두근✨")
        else:
            if i == 0:  # E/I
                pairs_bonus += 6
                reasons.append("E/I 보완으로 케미 뿜뿜 💫")
            elif i == 1:  # S/N
                pairs_bonus += 4
                reasons.append("S/N 차이가 시야 확장에 도움 🌈")
            elif i == 2:  # T/F
                pairs_bonus += 6
                reasons.append("T/F 보완으로 딱 맞는 하트💝")
            elif i == 3:  # J/P
                pairs_bonus += 6
                reasons.append("J/P 보완으로 생활 리듬 쿵짝짝 🎶")

    score = base + pairs_bonus

    ta, tb = TEMPERAMENT[a], TEMPERAMENT[b]
    if ta == tb:
        score += 6
        reasons.append(f"같은 기질({ta})라서 찰떡궁합 🍓")
    else:
        if {ta, tb} == {"NT", "NF"}:
            score += 4
            reasons.append("NT-NF 조합: 로맨틱한 비전 공유 🌟")
        if {ta, tb} == {"SJ", "SP"}:
            score += 4
            reasons.append("SJ-SP 조합: 알콩달콩 균형 ✨")

    if a == b:
        score -= 4
        reasons.append("너무 똑같아서 가끔 심심할 수도 있어요 🐻")

    score = int(max(0, min(100, score)))

    dedup = []
    for r in reasons:
        if r not in dedup:
            dedup.append(r)
    reasons = dedup[:4]

    return score, reasons


def name_bonus(n1: str, n2: str) -> Tuple[int, List[str]]:
    if not n1 or not n2:
        return 0, []
    a = n1.strip()
    b = n2.strip()
    if not a or not b:
        return 0, []
    bonus = 0
    reasons = []

    if a[0] == b[0]:
        bonus += 3
        reasons.append("첫 글자가 같아 찌릿찌릿 ⚡")
    if a[-1] == b[-1]:
        bonus += 4
        reasons.append("끝 글자가 같아 심쿵 💘")
    if (len(a) % 2) == (len(b) % 2):
        bonus += 2
        reasons.append("이름 길이 리듬이 맞아 귀여움 폭발 🐰")

    return bonus, reasons


def full_score_report(me_name: str, me_mbti: str, you_name: str, you_mbti: str):
    mbti_score, mbti_reasons = mbti_pair_score(me_mbti, you_mbti)
    n_bonus, n_reasons = name_bonus(me_name, you_name)
    total = int(max(0, min(100, mbti_score + n_bonus)))

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

    return {
        "mbti_score": mbti_score,
        "name_bonus": n_bonus,
        "total": total,
        "verdict": verdict,
        "mbti_reasons": mbti_reasons,
        "name_reasons": n_reasons,
    }

# -----------------------------
# UI – Inputs
# -----------------------------
col1, col2 = st.columns(2)
with col1:
    me_name = st.text_input("내 이름 🐰", value="")
    me_mbti = st.selectbox("내 MBTI 🌸", MBTI_TYPES, index=7)
with col2:
    you_name = st.text_input("상대 이름 🐻", value="")
    you_mbti = st.selectbox("상대 MBTI 🌟", MBTI_TYPES, index=0)

st.markdown("—")
run = st.button("✨🔮 궁합 보기 🔮✨")

# -----------------------------
# Validation
# -----------------------------
if run:
    if not (me_mbti in MBTI_TYPES and you_mbti in MBTI_TYPES):
        st.error("MBTI 입력이 올바르지 않습니다. 예: ENFP, ISTJ …")
    else:
        report = full_score_report(me_name, me_mbti, you_name, you_mbti)
        st.subheader("💞 결과 💞")
        c1, c2, c3 = st.columns(3)
        c1.metric("MBTI 점수", f"{report['mbti_score']}")
        c2.metric("이름 보너스", f"+{report['name_bonus']}")
        c3.metric("최종 점수", f"{report['total']}")
        st.success(report["verdict"])        

        with st.expander("🌈 궁합 설명 보기"):
            st.markdown("**💌 MBTI 근거**")
            for r in report["mbti_reasons"]:
                st.write("- ", r)
            if report["name_reasons"]:
                st.markdown("**🎀 이름 보너스**")
                for r in report["name_reasons"]:
                    st.write("- ", r)

        with st.expander("💡 러브 팁"):
            tips = []
            a, b = me_mbti, you_mbti
            if a[0] != b[0]:
                tips.append("에너지 충전 방식(E/I)이 달라요 🌞🌙 균형 잡기!")
            if a[1] != b[1]:
                tips.append("정보 처리(S/N)가 달라요 🔍🌌 다양하게 공유!")
            if a[2] != b[2]:
                tips.append("의사결정(T/F)이 달라요 🧠💗 함께 고려!")
            if a[3] != b[3]:
                tips.append("생활 템포(J/P)가 달라요 📅🎉 유연하게!")
            if not tips:
                tips.append("둘이 닮아 있어서 귀엽고 푹 빠질 조합! 💕")
            for t in tips:
                st.write("- ", t)

# -----------------------------
# Full 16×16 Compatibility Table
# -----------------------------
with st.expander("📊 전체 16×16 MBTI 궁합표 보기"):
    data = np.zeros((16, 16), dtype=int)
    for i, a in enumerate(MBTI_TYPES):
        for j, b in enumerate(MBTI_TYPES):
            data[i, j] = mbti_pair_score(a, b)[0]
    df = pd.DataFrame(data, index=MBTI_TYPES, columns=MBTI_TYPES)

    st.dataframe(df.style.format("{}"))

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    im = ax.imshow(df.values, aspect='auto')
    ax.set_xticks(range(len(MBTI_TYPES)))
    ax.set_yticks(range(len(MBTI_TYPES)))
    ax.set_xticklabels(MBTI_TYPES, rotation=45, ha='right')
    ax.set_yticklabels(MBTI_TYPES)
    ax.set_title("🌸 MBTI 궁합표 (이름 보너스 제외) 🌸")
    plt.tight_layout()
    st.pyplot(fig)

    csv = df.to_csv(index=True).encode('utf-8-sig')
    st.download_button(
        label="⬇️ 귀여운 CSV 다운로드 🎀",
        data=csv,
        file_name="mbti_compatibility_table.csv",
        mime="text/csv",
    )

st.caption("※ 이 앱은 귀여운 오락/참고용이에요! 실제 관계는 소통과 사랑이 중요합니다 🐰💝")

