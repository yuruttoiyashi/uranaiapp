# =========================
# ページ設定
# =========================
st.set_page_config(
    page_title="癒しの占いアプリ",
    page_icon="🔮",
    layout="centered"
)

# =========================
# カスタムCSS
# =========================
st.markdown("""
<style>
/* 全体背景 */
.stApp {
    background: linear-gradient(180deg, #f8f4ff 0%, #fdfaf6 50%, #f3ecff 100%);
}

/* メイン全体の余白 */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 820px;
}

/* タイトル */
.main-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
    color: #5b4b7a;
    margin-bottom: 0.3rem;
    letter-spacing: 0.03em;
}

/* サブタイトル */
.sub-title {
    text-align: center;
    font-size: 1.05rem;
    color: #7a6a93;
    margin-bottom: 2rem;
    line-height: 1.8;
}

/* カード風コンテナ */
.soft-card {
    background: rgba(255, 255, 255, 0.72);
    border: 1px solid rgba(180, 160, 220, 0.35);
    border-radius: 24px;
    padding: 1.4rem 1.2rem 1.2rem 1.2rem;
    box-shadow: 0 8px 24px rgba(125, 103, 168, 0.10);
    backdrop-filter: blur(6px);
    margin-bottom: 1.2rem;
}

/* ラベル風テキスト */
.section-label {
    font-size: 1rem;
    font-weight: 600;
    color: #6a5a84;
    margin-bottom: 0.4rem;
}

/* 結果見出し */
.result-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #6b4ca0;
    margin-bottom: 0.7rem;
}

/* 小見出し */
.history-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #6b4ca0;
    margin-top: 1.2rem;
    margin-bottom: 0.8rem;
    text-align: center;
}

/* 入力欄 */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
    border-radius: 16px !important;
    border: 1px solid #d8caee !important;
    background-color: rgba(255, 255, 255, 0.92) !important;
}

/* 入力中 */
.stTextInput input:focus, .stTextArea textarea:focus {
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

/* メッセージ系 */
div[data-testid="stAlert"] {
    border-radius: 16px;
}

/* 区切り線 */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, rgba(0,0,0,0), rgba(186,160,219,0.8), rgba(0,0,0,0));
    margin-top: 2rem;
    margin-bottom: 1.2rem;
}
</style>
""", unsafe_allow_html=True)

if "OPENAI_API_KEY" not in st.secrets:
    st.error("APIキーが設定されていません")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# =========================
# セッション状態の初期化
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
st.markdown("### 🌙 あなたの情報を入力してください")

birthday = st.text_input("生年月日", placeholder="例：1986/12/03")

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
芸能人や経営者も密かに通う人気占い師のような、信頼感のある語り口にしてください。
恋愛、仕事、人間関係、金運、健康運など幅広く見られる占い師として答えてください。

条件:
- 最初に相談者の気持ちにやさしく共感する
- テンプレっぽい古いAI口調は使わない
- ふわっとしすぎず、具体性を入れる
- 読みやすく、やわらかい文章にする
- 最後は前向きになれる言葉で締める
- 少しスピリチュアルで安心感のある雰囲気にする
- 日本語で回答する
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "あなたは占い歴15年の実力派占い師です。"
                                "芸能人や経営者も密かに通う人気鑑定士で、"
                                "恋愛、仕事、人間関係、金運、健康運など幅広く鑑定できます。"
                                "優しく寄り添いながらも、曖昧な表現は避け、"
                                "現実的で具体的なアドバイスをしてください。"
                                "テンプレ的な占い表現や古いAIっぽい言い回しは使わず、"
                                "自然な会話のような口調で話してください。"
                                "相談者は少し不安を抱えている女性です。"
                                "最初に気持ちに共感し、その後に鑑定を行い、"
                                "最後は前向きになれる言葉で締めてください。"
                                "文章は読みやすく、やわらかく、でもプロらしい深みを感じる内容にしてください。"
                                "全体の雰囲気は、癒し・安心感・やさしいスピリチュアルさを大切にしてください。"
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                result = response.choices[0].message.content

                st.session_state.history.insert(
                    0,
                    {
                        "birthday": birthday,
                        "category": category,
                        "question": user_input,
                        "result": result
                    }
                )

                st.markdown('<div class="soft-card">', unsafe_allow_html=True)
                st.markdown('<div class="result-title">🌸 鑑定結果</div>', unsafe_allow_html=True)
                st.write(result)
                st.markdown("### 📋 コピー用")
                st.code(result)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error("エラーが発生しました。")
                st.code(str(e))

# =========================
# 履歴表示
# =========================
if st.session_state.history:
    st.markdown("---")
    st.markdown('<div class="history-title">🕊 これまでの鑑定</div>', unsafe_allow_html=True)

    for i, item in enumerate(st.session_state.history, start=1):
        with st.expander(f"{i}. {item['category']}｜{item['birthday']}"):
            st.write(f"**相談内容**：{item['question']}")
            st.write("**鑑定結果**：")
            st.write(item["result"])
            st.code(item["result"])

# =========================
# 履歴削除
# =========================
if st.session_state.history:
    if st.button("履歴を手放す"):
        st.session_state.history = []
        st.success("履歴を削除しました。")