
import pandas as pd
import streamlit as st
import re

# タイトル
st.title("韻文検索ツール（高速版）")

# CSVファイルのパス
CSV_FILE = "data.csv"

# 検索用ジェネレーター関数
def search_generator(file_path, keywords, search_mode):
    with open(file_path, "r", encoding="utf-8") as f:
        header = f.readline().strip().split("\t")  # ヘッダー
        yield header  # ヘッダーを最初に返す
        # VERS列のインデックスを特定
        try:
            vers_index = header.index("VERS")
        except ValueError:
            raise ValueError("CSVファイルに 'VERS' 列が存在しません。")

        for line in f:
            columns = line.strip().split("\t")
            if len(columns) <= vers_index:
                continue  # 行が不完全な場合はスキップ

            vers_content = columns[vers_index].lower()  # VERS列の内容を取得
            if search_mode == "AND":
                if all(keyword.lower() in vers_content for keyword in keywords):
                    yield columns
            elif search_mode == "OR":
                if any(keyword.lower() in vers_content for keyword in keywords):
                    yield columns

# 大文字小文字を区別しないハイライト関数
def highlight_keywords(text, keywords):
    def highlight(match):
        return f'<span style="color: black; background-color: yellow; font-weight: bold;">{match.group(0)}</span>'

    for keyword in keywords:
        # re.IGNORECASE を指定して大文字小文字を区別せずに検索
        text = re.sub(
            keyword, highlight, text, flags=re.IGNORECASE
        )
    return text

# キーワード入力
keyword_input = st.text_input("検索キーワードを入力してください（スペース区切りで複数入力可能）")
search_mode = st.radio("検索モードを選択してください", options=["AND", "OR"], horizontal=True)

if keyword_input:
    keywords = keyword_input.split()  # キーワードをスペース区切りで分割
    try:
        results = list(search_generator(CSV_FILE, keywords, search_mode))  # 結果をリスト化

        if len(results) > 1:  # 結果が存在する場合
            st.write(f"検索結果 ({len(results) - 1}件):")
            header = results[0]
            data = results[1:]
            df = pd.DataFrame(data, columns=header)  # データフレーム作成

            # VERS列にハイライトを適用
            vers_index = header.index("VERS")
            df["VERS"] = df["VERS"].apply(
                lambda x: highlight_keywords(x, keywords)
            )

            # 列幅を調整するCSS
            st.markdown(
                """
                <style>
                table {
                    width: 100%;
                }
                th, td {
                    padding: 8px 12px;
                    text-align: left;
                }
                th:first-child, td:first-child {
                    width: 5%;
                }
                th:nth-child(2), td:nth-child(2) {
                    width: 60%;
                }
                th:nth-child(3), td:nth-child(3) {
                    width: 20%;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            # データフレームを表示（HTMLでハイライトを反映）
            st.write(
                df.to_html(escape=False, index=False), unsafe_allow_html=True
            )
        else:
            st.warning("該当する韻文が見つかりませんでした。")
    except ValueError as e:
        st.error(str(e))

