import openai
from match_experience import match_experience

openai.api_key = "" #前述で発行したAPIをKeyに置き換えてください

def generate_text(occupation, condition, experience, business_content, lower_limit, upper_limit):
    
    #採用条件とマッチする経験を取得
    matched_experience = match_experience(condition, experience)
    
    if matched_experience == 1:
        prompt = "新卒就活の志望動機を、以下の情報を踏まえて考えてください。\n応募職種：{occupation}\n自身の強み{matched_experience}\n会社の事業内容{business_content}\nまた、出力は、次の文字数の範囲に納めてください。文字数の下限：{lower_limit}, 上限：{upper_limit}".format(occupation=occupation, matched_experience=experience, business_content=business_content, lower_limit=lower_limit, upper_limit=upper_limit)
    else:
        prompt = "新卒就活の志望動機を、以下の情報を踏まえて考えてください。\n応募職種：{occupation}\n会社の事業内容{business_content}\nまた、出力は、次の文字数の範囲に納めてください。文字数の下限：{lower_limit}, 上限：{upper_limit}".format(occupation=occupation, business_content=business_content, lower_limit=lower_limit, upper_limit=upper_limit)

    # 対話の初期化
    chat_history = []

    i = 0
    flag = False

    while flag == False:
        if i == 10:
            return "10回以内に文字数の範囲内に収まる文章を生成できませんでした。"
        
        chat_history.append(f"ユーザー: {prompt}")
        
        input_text = prompt='\n'.join(chat_history)
        
        # OpenAI APIを使用して応答を生成
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            messages=[
                {"role": "user", "content": input_text},
            ]
        )

        
        # 応答からモデルの返答を取得
        model_response = response["choices"][0]["message"]["content"]
        
        # チャット履歴にモデルの返答を追加
        chat_history.append(f"GPTモデル: {model_response}")
        
        
        # モデルの返答を出力
        print("GPTモデル:", model_response)
        print("文字数：", len(model_response))
        
        if lower_limit <= len(model_response) <= upper_limit:
            flag = True
            return model_response
        elif len(model_response) < lower_limit:
            difference = lower_limit - len(model_response)
            prompt = "文字数が少ないです。{difference}文字程度追加してください。".format(difference=difference - 10)
        elif len(model_response) > upper_limit:
            difference = len(model_response) - upper_limit
            prompt = "文字数が多いです。{difference}文字程度削除してください。".format(difference=difference + 10)
        
        i += 1
        """if i == 10:
            return "10回以内に文字数の範囲内に収まる文章を生成できませんでした。"""