import openai
# OpenAI APIの設定
openai.api_key = ''  # 自分のAPIキーに置き換えてください

#gptへの支持
theme = "gptへの指示をここに入力してください。"
#文字数上限
upper_limit = 400
#下限
lower_limit = 360

#ループ回数
i = 0

def character_limit(theme, upper_limit, lower_limit):

    flag = False

    prompt = "{theme}\n 出力は、次の文字数の範囲に納めてください。文字数の下限：{lower_limit}, 上限：{upper_limit}".format(theme=theme, upper_limit=upper_limit, lower_limit=lower_limit)


    # 対話の初期化
    chat_history = []

    while flag == False:
        chat_history.append(f"ユーザー: {prompt}")
        
        input_text = prompt='\n'.join(chat_history)
        
        # OpenAI APIを使用して応答を生成
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "user", "content": input_text},
        ]
    )

        
        # 応答からモデルの返答を取得
        model_response = response["choices"][0]["message"]["content"]
        
        # チャット履歴にモデルの返答を追加
        chat_history.append(f"GPTモデル: {model_response}")
        
        
        if lower_limit <= len(model_response) <= upper_limit:
            #一応
            flag = True
            return model_response
        elif len(model_response) < lower_limit:
            difference = 360 - len(model_response)
            prompt = "文字数が少ないです。{difference}文字以上追加してください。".format(difference=difference + 10)
        elif len(model_response) > upper_limit:
            difference = len(model_response) - 400
            prompt = "文字数が多いです。{difference}文字以上削除してください。".format(difference=difference - 10)  
            
        if i == 10:
            flag = True
            return "10回以内に文字数の範囲内に収まる文章を生成できませんでした。"
