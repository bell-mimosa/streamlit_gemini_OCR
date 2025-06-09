import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

# Gemini APIキーの設定(環境変数も可)
api_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini APIキーが設定されていません。")
    st.stop()
genai.configure(api_key=api_key)

st.set_page_config(
    page_title="Gemini 簡易OCR",
)

st.title("Gemini文字認識アプリ")

st.write("画像の文字をGeminiが抽出します。")

# 画像アップロード
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

image = None
if uploaded_file is not None:
    # アップロードされた画像を表示
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた画像", use_container_width=True)
    st.success("画像が正常にアップロードされました。")

    # Geminiに渡す処理
    if st.button("Geminiで画像を処理"):
        if image is not None:
            with st.spinner("Geminiが画像を処理中..."):
                try:
                    # Geminiモデルの初期化
                    model = genai.GenerativeModel('gemini-1.5-flash')

                    # 画像とプロンプトをGeminiに渡す
                    # model.generate_content(["プロンプト",添付ファイル])
                    response = model.generate_content(["この画像の文字を抽出してください。適切にマークダウンして、結果のみを出力してください。画像内に文字がない場合は「画像から文字を抽出することができませんでした。文字を含む画像をアップロードしてください。」と返してください。", image])

                    # Geminiからのレスポンス表示
                    st.subheader("Geminiの処理結果:")
                    st.write(response.text)

                except Exception as e:
                    st.error(f"Geminiでの処理中にエラーが発生しました: {e}")
        else:
            st.warning("処理する画像がありません。画像をアップロードしてください。")

else:
    st.info("画像をアップロードしてください。")
