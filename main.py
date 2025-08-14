import streamlit as st
import pandas as pd
import altair as alt
from functools import lru_cache

st.set_page_config(page_title="MBTI 궁합 계산기", page_icon="💞", layout="wide")

# -----------------------------
# 기본 데이터
# -----------------------------
MBTIS = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP",
]

# 기질(temperament)
TEMPERAMENT = {
    "SP": {"letters": ["ESTP","ESFP","ISTP","ISFP"], "label": "SP (실용/경험)"},
    "SJ": {"letters": ["ESTJ","ESFJ","ISTJ","ISFJ"], "label": "SJ (책임/안정)"},
    "NT": {"letters": ["ENTJ","ENTP","INTJ","INTP"], "label": "NT (전략/이성)"},
    "NF": {"letters": ["ENFJ","ENFP","INFJ","INFP"], "label": "NF (의미/가치)"},
}

TYPE_TO_TEMP = {}
for k, v in TEMPERAMENT.items():
    for t in v["letters"]:
        TYPE_TO_TEMP[t] = k

# 각 차원에 대한 간단 설명
DIM_DESC = {
    "E": "E(외향): 자극·사람과의 상호작용에서 에너지 충전",
    "I": "I(내향): 고요·깊은 집중에서 에너지 충전",
    "S": "S(감각): 사실·경험·구체성 선호",
    "N": "N(직관): 가능성·패턴·추상성 선호",
    "T": "T(사고): 논리·분석 기반 의사결정",
    "F": "F(감정): 가치·관계 기반 의사결정",
    "J": "J(판단): 계획·구조·마감 선호",
    "P": "P(인식): 자율·융통성·탐색 선호",
}

# -----------------------------
# 점수 알고리즘
# -----------------------------
# 가중치: 직관/감각, 사고/감정(0.3), 외향/내향, 판단/인식(0.2)
WEIGHTS = {"EI": 0.2, "SN": 0.3, "TF": 0.3, "JP": 0.2}

@lru_cache(maxsize=None)
def split_dims(t: str):
    t = t.upper()
    return dict(EI=t[0], SN=t[1], TF=t[2], JP=t[3])

@lru_cache(maxsize=None)
def temperament(t: str) -> str:
    return TYPE_TO_TEMP[t.upper()]

@lru_cache(maxsize=None)
def pair_score(a: str, b: str) -> dict:
    A, B = split_dims(a), split_dims(b)
    # 일치 여부(같으면 1, 다르면 0). 일부 차원은 차이가 상호보완으로 작동하므로 보정
    matches = {
        "EI": 1.0 if A["EI"] == B["EI"] else 0.0,
        "SN": 1.0 if A["SN"] == B["SN"] else 0.0,
        "TF": 1.0 if A["TF"] == B["TF"] else 0.0,
        "JP": 1.0 if A["JP"] == B["JP"] else 0.0,
    }

    # 상호보완 보정: EI, JP는 다르면 약간의 보너스(자극/균형)
    complement_bonus = 0.0
    if A["EI"] != B["EI"]:
        complement_bonus += 0.06  # 6점
    if A["JP"] != B["JP"]:
        complement_bonus += 0.06

    # 기질 보너스: 같은 기질이면 +0.06, NF↔NT / SJ↔SP 인접 기질은 +0.03
    ta, tb = temperament(a), temperament(b)
    if ta == tb:
        complement_bonus += 0.06
    else:
        neighbor = {"NF": {"NT"}, "NT": {"NF"}, "SJ": {"SP"}, "SP": {"SJ"}}
        if tb in neighbor.get(ta, set()):
            complement_bonus += 0.03

    # 원점수(0~1)
    base = sum(matches[d] * WEIGHTS[d] for d in WEIGHTS)
    raw = min(1.0, base + complement_bonus)
    score = int(round(raw * 100))  # 0~100

    # 등급
    if score >= 85:
        tier = "환상적 (S+)"
    elif score >= 75:
        tier = "아주 좋음 (A)"
    elif score >= 65:
        tier = "양호 (B)"
    elif score >= 55:
        tier = "보통 (C)"
    else:
        tier = "도전적 (D)"

    details = {
        "EI": ("에너지 스타일", "같음" if matches["EI"] else "다름"),
        "SN": ("정보 처리", "같음" if matches["SN"] else "다름"),
        "TF": ("의사결정", "같음" if matches["TF"] else "다름"),
        "JP": ("생활 리듬", "같음" if matches["JP"] else "다름"),
        "temperament": ("기질", f"{TEMPERAMENT[ta]['label']} ↔ {TEMPERAMENT[tb]['label']}")
    }

    return {
        "score": score,
        "tier": tier,
        "matches": matches,
        "details": details,
        "bonus": round(complement_bonus * 100),
    }

# 설명 생성기
BLURBS = {
    "EI_same": "둘 다 에너지를 비슷한 방식으로 충전해 사회적 리듬이 잘 맞습니다.",
    "EI_diff": "한쪽은 활동/자극, 다른 한쪽은 고요/회복을 원해 리듬 조율이 필요합니다.",
    "SN_same": "현실 대화 또는 아이디어 대화 중 하나로 일치하여 오해가 적습니다.",
    "SN_diff": "구체와 가능성의 초점이 달라, 설명·예시를 충분히 주고받으면 시너지가 납니다.",
    "TF_same": "의사결정 기준이 유사해 갈등 조정이 수월합니다.",
    "TF_diff": "논리와 배려의 균형을 합의해야 하며, 서로의 강점을 인정하면 좋습니다.",
    "JP_same": "생활 템포가 비슷하여 일정/변경 관리가 편합니다.",
    "JP_diff": "한쪽은 계획, 한쪽은 융통성을 선호해 경계·자유도를 명확히 하면 좋습니다.",
}

def gen_explainer(a: str, b: str, res: dict) -> str:
    A, B = split_dims(a), split_dims(b)
    lines = []
    lines.append(f"• EI: {BLURBS['EI_same' if A['EI']==B['EI'] else 'EI_diff']}")
    lines.append(f"• S/N: {BLURBS['SN_same' if A['SN']==B['SN'] else 'SN_diff']}")
    lines.append(f"• T/F: {BLURBS['TF_same' if A['TF']==B['TF'] else 'TF_diff']}")
    lines.append(f"• J/P: {BLURBS['JP_same' if A['JP']==B['JP'] else 'JP_diff']}")
    lines.append("• 기질 관점: " + res["details"]["temperament"][1])
    return "\n".join(lines)

# 개선 팁 추천
TIP_POOL = {
    "EI_diff": [
        "주말 중 절반은 외부 활동, 절반은 휴식으로 합의",
        "행사 전·후 ‘재충전 시간’ 예약하기",
    ],
    "SN_diff": [
        "아이디어는 사례로, 사실은 의도를 함께 설명하기",
        "회의는 ‘큰그림→세부’ 순서로 진행",
    ],
    "TF_diff": [
        "의사결정 전에 ‘사실/영향/가치’를 분리해 논의",
        "갈등 시 감정 확인→근거 정리→선택 기준 합의",
    ],
    "JP_diff": [
        "고정 마감과 유연 범위를 문서로 명시",
        "캘린더 공유·변경 규칙 만들기",
    ],
}

def suggest_tips(a: str, b: str) -> list:
    A, B = split_dims(a), split_dims(b)
    tips = []
    if A['EI'] != B['EI']:
        tips += TIP_POOL['EI_diff']
    if A['SN'] != B['SN']:
        tips += TIP_POOL['SN_diff']
    if A['TF'] != B['TF']:
        tips += TIP_POOL['TF_diff']
    if A['JP'] != B['JP']:
        tips += TIP_POOL['JP_diff']
    if not tips:
        tips = [
            "공통 강점을 프로젝트·가사에 분담해 ‘역할 시너지’를 만드세요.",
            "정기 1:1 체크인으로 작은 오해를 초기에 해소하세요.",
        ]
    return tips[:4]

# 256 조합 행렬 생성
@lru_cache(maxsize=None)
def compatibility_matrix() -> pd.DataFrame:
    data = []
    for a in MBTIS:
        row = []
        for b in MBTIS:
            row.append(pair_score(a, b)["score"])
        data.append(row)
    return pd.DataFrame(data, index=MBTIS, columns=MBTIS)

# -----------------------------
# UI
# -----------------------------
st.title("💞 MBTI 궁합 계산기 (256 조합)")
st.caption("두 MBTI를 선택하면 점수·등급·설명·실전 팁을 제공합니다. 아래에는 16×16 전체 궁합 열지도와 상위 매칭이 함께 표시됩니다.")

left, right = st.columns(2)
with left:
    a = st.selectbox("당신(또는 A)의 MBTI", MBTIS, index=MBTIS.index("ENFP") if "ENFP" in MBTIS else 0)
with right:
    b = st.selectbox("상대(또는 B)의 MBTI", MBTIS, index=MBTIS.index("INTJ") if "INTJ" in MBTIS else 1)

res = pair_score(a, b)

st.subheader(f"{a} ↔ {b} : {res['score']}점 · {res['tier']}")
st.markdown(
    f"""
**세부요소**  
- 에너지(E/I): {res['details']['EI'][1]}  
- 정보(S/N): {res['details']['SN'][1]}  
- 판단(T/F): {res['details']['TF'][1]}  
- 생활(J/P): {res['details']['JP'][1]}  
- 보너스: +{res['bonus']}  
"""
)

with st.expander("🔎 관계 해설"):
    st.text(gen_explainer(a, b, res))

with st.expander("🧰 함께 쓰는 실전 팁"):
    for tip in suggest_tips(a, b):
        st.markdown(f"- {tip}")

st.markdown("---")

# 열지도
st.subheader("전체 256 조합 열지도")
mat = compatibility_matrix().copy()
mat_df = mat.reset_index().melt(id_vars="index", var_name="B", value_name="점수").rename(columns={"index": "A"})

heat = (
    alt.Chart(mat_df)
    .mark_rect()
    .encode(
        x=alt.X("B:N", sort=MBTIS, title="상대 B"),
        y=alt.Y("A:N", sort=MBTIS, title="당신 A"),
        color=alt.Color("점수:Q", scale=alt.Scale(domain=[0,100])),
        tooltip=["A","B","점수"]
    )
    .properties(height=420)
)

text = (
    alt.Chart(mat_df)
    .mark_text(baseline='middle')
    .encode(x="B:N", y="A:N", text=alt.Text("점수:Q", format=".0f"))
)

st.altair_chart(heat + text, use_container_width=True)

# 특정 타입의 상위 궁합
st.markdown("---")
st.subheader("타입별 상위 궁합 추천")
col1, col2 = st.columns(2)
with col1:
    pick = st.selectbox("타입 선택", MBTIS, key="pick")
    scores = mat.loc[pick].sort_values(ascending=False)
    top5 = scores.head(5)
    st.table(pd.DataFrame({"상대 타입": top5.index, "점수": top5.values}))
with col2:
    # CSV 다운로드
    csv = mat.to_csv().encode('utf-8-sig')
    st.download_button("📥 전체 매트릭스 CSV 다운로드", data=csv, file_name="mbti_compatibility_256.csv", mime="text/csv")

st.caption("※ 본 도구는 MBTI 선호 차이를 바탕으로 한 비공식 가이드입니다. 상호 존중과 소통이 무엇보다 중요합니다.")
