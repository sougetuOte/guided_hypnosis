import os
import sys
import configparser
import time
import anthropic
import re

# 設定ファイルを読み込む
config = configparser.ConfigParser()
config.read('config.ini')

# APIキーを設定ファイルから取得し、環境変数にセット
api_key = config.get('anthropic', 'api_key')
os.environ["ANTHROPIC_API_KEY"] = api_key

# システムプロンプトを設定ファイルから読み込む
with open(config.get('system_prompt', 'system_prompt'), 'r') as f:
    system_prompt = f.read()

# Anthropic APIクライアントを初期化  
client = anthropic.Anthropic()

# チャットループ
while True:
    try:
        # ユーザーからの入力を取得
        user_input = input("あなた: ")
        
        # APIにリクエストを送信
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_input}
            ]
        )

        # Claude3 Opusからの応答を表示
        response_text = ''.join(block.text for block in response.content)
        print(f"Claude3: {response_text}")
        # スクリプト開始と終了の確認
        if "(スクリプト開始)" in response_text:
            # ユーザーに確認を求める
            confirmation = input("このスクリプトで良いですか？ (yes/no): ")
            if confirmation.lower() in ["yes","y"]:
                # スクリプトの開始と終了の位置を取得
                start_index = response_text.index("(スクリプト開始)") + len("(スクリプト開始)")
                end_index = response_text.index("(スクリプト終了)")
                
                # スクリプトをトリミングして保存
                trimmed_script = response_text[start_index:end_index]
                # ファイルを生成
                with open(f"script_{time.strftime('%Y%m%d%H%M%S')}.txt", 'w') as script_file:
                    script_file.write(response_text)
                print("スクリプトを生成しました。\nプログラムを終了します。")
                break  # ループを終了
            elif confirmation.lower() in ["no","n"]:
                print("スクリプトの生成を中止しました。")
            else:
                print("無効な入力です。yes(y)またはno(n)を入力してください。")
    except KeyboardInterrupt:
        print("\nCtrl+Cが押されました。プログラムを終了します。")
        sys.exit()