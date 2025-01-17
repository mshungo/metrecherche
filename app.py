
import pandas as pd
import streamlit as st

# タイトル
st.title("韻文検索ツール（高速版）")

# CSVファイルのパス
CSV_FILE = "data.csv"

# 検索用ジェネレーター関数
def search_generator(file_path, keywords, search_mode):
    with open(file_path, "r", encoding="utf-8") as f:
        header = f.readline().strip().split("\t")  # ヘッダー
        yield header  # ヘッダーを最初に返す
        for line in f:
            line_lower = line.lower()
            if search_mode == "AND":
                if all(keyword.lower() in line_lower for keyword in keywords):
                    yield line.strip().split("\t")
            elif search_mode == "OR":
                if any(keyword.lower() in line_lower for keyword in keywords):
                    yield line.strip().split("\t")

# キーワード入力
keyword_input = st.text_input("検索キーワードを入力してください（スペース区切りで複数入力可能）")
search_mode = st.radio("検索モードを選択してください", options=["AND", "OR"], horizontal=True)

if keyword_input:
    keywords = keyword_input.split()  # キーワードをスペース区切りで分割
    results = list(search_generator(CSV_FILE, keywords, search_mode))  # 結果をリスト化

    if len(results) > 1:  # 結果が存在する場合
        st.write(f"検索結果 ({len(results) - 1}件):")
        header = results[0]
        data = results[1:]
        df = pd.DataFrame(data, columns=header)  # データフレーム作成

        # 表示サイズを広げる設定
        st.markdown(
            """
            <style>
            .dataframe table {
                width: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # データフレームを表示
        st.dataframe(df, use_container_width=True)  # 表を全幅で表示
    else:
        st.warning("該当する韻文が見つかりませんでした。")

