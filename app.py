import streamlit as st
from openai import OpenAI

# =========================
# ページ設定
# =========================
st.set_page_config(
    page_title="癒しの占いアプリ",
    page_icon="🔮",
    layout="centered"
)

# =========================
# APIキー確認
# =========================
if "OPENAI_API_KEY" not in st.secrets:
    st.error("APIキーが設定されていません")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# =========================
# カスタムCSS（上欠け対策込み）
# =========================
st.markdown("""
<style>

/* 背景 */
.stApp {
    background: linear-gradient(180deg, #f8f4ff 0%, #fdfaf6 50%, #f3ecff 100%);
}

/* 上余白（ここ重要！！） */
.block-container {
    padding-top: 3.5rem;
    padding-bottom: 2rem;
    max-width: 820px;
}

/* タイトル */
.main-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 700;
    color: #5b4b7a;
    margin-top: 1rem;
    margin-bottom: 0.3rem;
    letter-spacing: 0.03em;
}

/* サブタイトル */
.sub-title {
    text-align: center;
    font-size: 1.05rem;
    color: #7a6a93;
    margin-bottom: 1.2rem;
    line-height: 1.8;
}

/* 見出し */
.section-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #6b4ca0;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}

/* 結果タイトル */
.result-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #6b4ca0;
    margin-bottom: 0.7rem;
}

/* 履歴タイトル */
.history-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #6b4ca0;
    margin-top: 1.5rem;
    margin-bottom: 0.8rem;
    text-align: center;
}

/* 入力欄 */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {
    border-radius: 16px !important;
    border: 1px solid #d8caee !important;
    background-color: rgba(255, 255, 255, 0.95) !important;
}

/* フォーカス */
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #b99de8 !important;
    box-shadow: 0 0 0 1px #c7b0ef !important;
}

/* ボタン */
.stButton > button {
    background: linear-gradient(90deg, #caa8ff 0%, #f1c6e7 100%);
    color: #4d3d68;
    border: none;
    border-radius: 999px;
    padding: 0.7rem 1.6rem;
    font-size: 1rem;
    font-weight: 700;
    box-shadow: 0 6px 18px rgba(182, 145, 231, 0.28);
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 22px rgba(182, 145, 231, 0.34);
}

/* expander */
.streamlit-expanderHeader {
    font-weight: 600;
    color: #5f4f7a;
}

/* コード表示 */
.stCodeBlock {
    border-radius: 16px;
}

/* アラート */
div[data-testid="stAlert"] {
    border-radius: 16px;
}

/* 区切り線 */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(
        90deg,
        rgba(0,0,0,0),
        rgba(186,160,219,0.8),
        rgba(0,0,0,0)
    );
    margin-top: 2rem;
    margin-bottom: 1.2rem;
}

</style>
""", unsafe_allow_html=True)

# =========================
# セッション状態
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# ヘッダー
# =========================
st.markdown('<div class="main-title">🔮 癒しの占いアプリ</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">ふっと心をゆるめながら、今のあなたに必要なメッセージを受け取ってみましょう。<br>やさしく、でも芯のある言葉で鑑定します。</div>',
    unsafe_allow_html=True
)

# =========================
# 入力エリア
# =========================
st.markdown('<div class="section-title">🌙 あなたの情報を入力してください</div>', unsafe_allow_html=True)

birthday = st.text_input("生年月日", placeholder="例：1990/01/01")

category = st.selectbox(
    "占いの種類",
    ["総合", "恋愛", "仕事", "金運", "人間関係", "健康"]
)

user_input = st.text_area(
    "相談内容",
    height=150,
    placeholder="例：2026年の全体運をみてください"
)

# =========================
# 鑑定ボタン
# =========================
if st.button("鑑定する"):
    if not birthday or not user_input:
        st.warning("生年月日と相談内容の両方を入力してください。")
    else:
        with st.spinner("🔮 静かにエネルギーを読み取っています…"):
            prompt = f"""
相談者の生年月日は {birthday} です。
相談ジャンルは {category} です。
相談内容は以下です。
「{user_input}」

相談者に寄り添いながら、占い歴15年の実力派占い師として自然で人間らしい言葉で鑑定してください。
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "あなたは占い歴15年の実力派占い師です。優しく寄り添ってください。"},
                    {"role": "user", "content": prompt}
                ]
            )

            result = response.choices[0].message.content

            st.session_state.history.insert(0, result)

            st.markdown("### 🌸 鑑定結果")
            st.write(result)
            st.code(result)

# =========================
# 履歴
# =========================
if st.session_state.history:
    st.markdown("---")
    st.markdown('<div class="history-title">🕊 鑑定履歴</div>', unsafe_allow_html=True)

    for i, h in enumerate(st.session_state.history):
        with st.expander(f"{i+1}件目"):
            st.write(h)

# =========================
# 履歴削除
# =========================
if st.session_state.history:
    if st.button("履歴を手放す"):
        st.session_state.history = []
        st.success("履歴を削除しました")
