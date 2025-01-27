from langchain_core.output_parsers import CommaSeparatedListOutputParser

# パーサーのインスタンス作成
parser = CommaSeparatedListOutputParser()

# サンプルデータ（カンマ区切り文字列）
raw_data = "apple, banana, cherry"

# パース結果を取得
parsed_list = parser.parse(raw_data)

print(parsed_list)  # 出力: ['apple', 'banana', 'cherry']
