# import time

def generate(input_text, input_text2, input_text3):
    print(input_text, input_text2, input_text3)
    # time.sleep(30) # debug: delay 30 seconds
    
    text = input_text + input_text2 + input_text3 + "を生成しました"
    
    return text