import openai
from generate_text.match_experience import match_experience

openai.api_key = "" #前述で発行したAPIをKeyに置き換えてください

def generate_text(occupation, condition, experience, business_content, purpose, lower_limit, upper_limit):
    
    #採用条件とマッチする経験を取得
    matched_experience = match_experience(condition, experience)
    
    if matched_experience == 1:
        prompt = "###指示###新卒の就活生の立場で、サマーインターンの志望動機を考えてください。企業理念はそのまま使わないでください。\n###応募職種###：{occupation}\n###自身の強み###{matched_experience}\n###会社の事業内容###{business_content}\n###企業理念###{purpose}\n###文字数の下限###{lower_limit}\n###文字数の上限###{upper_limit}".format(occupation=occupation, matched_experience=experience, business_content=business_content, purpose=purpose, lower_limit=lower_limit, upper_limit=upper_limit)
        
        #prompt = "新卒就活の志望動機を、以下の情報を踏まえて考えてください。#応募職種：{occupation}\n自身の強み{matched_experience}\n会社の事業内容{business_content}\nまた、出力は、次の文字数の範囲に納めてください。文字数の下限：{lower_limit}, 上限：{upper_limit}".format(occupation=occupation, matched_experience=experience, business_content=business_content, lower_limit=lower_limit, upper_limit=upper_limit)
    else:
        prompt = "###指示###新卒の就活生の立場で、サマーインターンの志望動機を考えてください。企業理念はそのまま使わないでください。\n###応募職種###：{occupation}\n###会社の事業内容###{business_content}\n###企業理念###{purpose}\n###文字数の下限###{lower_limit}\n###文字数の上限###{upper_limit}".format(occupation=occupation, matched_experience=experience, business_content=business_content, purpose=purpose, lower_limit=lower_limit, upper_limit=upper_limit)
        #prompt = "新卒就活の志望動機を、以下の情報を踏まえて考えてください。\n応募職種：{occupation}\n会社の事業内容{business_content}\nまた、出力は、次の文字数の範囲に納めてください。文字数の下限：{lower_limit}, 上限：{upper_limit}".format(occupation=occupation, business_content=business_content, lower_limit=lower_limit, upper_limit=upper_limit)

    # 対話の初期化
    chat_history = []

    i = 0
    flag = False

    while flag == False:
        if i == 10:
            return "10回以内に文字数の範囲内に収まる文章を生成できませんでした。"
        
        if len(chat_history) > 4:
            #配列の先頭から要素を削除
            chat_history.pop(2)
            chat_history.pop(2)
        
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
        model_response = model_response.replace("GPTモデル: ", "")
        
        # チャット履歴にモデルの返答を追加
        chat_history.append(f"GPTモデル: {model_response}")
        
        
        # モデルの返答を出力
        print(model_response)
        print("文字数：", len(model_response))
        # print(type(len(model_response)), type(lower_limit), type(upper_limit))
        
        if lower_limit <= len(model_response) <= upper_limit:
            flag = True
            return model_response
        elif len(model_response) < lower_limit:
            difference = lower_limit - len(model_response)
            prompt = "文字数が少ないです。{difference}文字程度追加して、書き直してください。".format(difference=difference - 10)
        elif len(model_response) > upper_limit:
            difference = len(model_response) - upper_limit
            prompt = "文字数が多いです。{difference}文字程度削除して、書き直してください。".format(difference=difference + 10)
        
        i += 1
        """if i == 10:
            return "10回以内に文字数の範囲内に収まる文章を生成できませんでした。"""
        
if __name__=='__main__':
    occupation = "プログラマー"
    condition = "プログラミング経験あり"
    experience = "Python 3年"
    business_content = "ECシステム運用・構築など" 
    lower_limit = 360
    upper_limit = 400
    output = generate_text(occupation, condition, experience, business_content, lower_limit, upper_limit)
    print("--------------------")
    print(output)
    print(len(output))