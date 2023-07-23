#採用条件と自身の経験のマッチ度を測り、志望動機に組み込むか組み込まないかを決める。
#返り値　0:マッチしていない　1:一部マッチしている　2:マッチしている　3:エラー

import openai

openai.api_key = " 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"

#condition:採用条件　experience:自身の経験
def match_experience(condition, experience):
    prompt = "以下の採用条件と自身の経験はマッチしていますか。「マッチしている」「一部マッチしている」「マッチしていない」の3択で答えて下さい。\n採用条件：{condition}\n経験：{experience}".format(condition=condition, experience=experience)
    
    response = openai.ChatCompletion.create(
        #gpt4にすることも検討
        model="gpt-3.5-turbo",
        #temperatureは一旦0
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}, 
        ]
    )
    
    response = response["choices"][0]["message"]["content"]
    
    #if "1部マッチしている" in response:
    #    return 1
    if "マッチしている" in response:
        return 1
    
    elif "マッチしていない" in response:
        return 0
    
    #エラー処理はまた後で考える（もう一度判定させるのかどうか）
    else:
        return 3
    
if __name__=='__main__':
    condition = "プログラミング経験あり"
    experience = "漢字検定 準一級"
    result = match_experience(condition=condition, experience=experience)
    print(result)