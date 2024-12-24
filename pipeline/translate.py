import json
import openai
import requests

# 配置 OpenAI API 密钥
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyYW5mT09vckloTWZ4eFk3WHM2eFZCdkVHcHciLCJleHAiOjE3MzUwNDQ0NTMsIm5iZiI6MTczNDk1ODA0OH0.4EZC9erAykbyjfFFRKNFbnUKupqM-SyfZaK0dhyyaNc'

# 输入和输出文件路径
input_file = 'persona.jsonl'
output_file = 'persona_cn.jsonl'

def request(key, prompt, img_path):
    url = 'https://api.sensenova.cn/v1/llm/chat-completions'
    prompt = prompt + "\n将此句话翻译为中文"
    if img_path:
        content = [{
            'image_base64': image_to_base64(img_path),
            'image_file_id': '',
            'image_url': '',
            'text': '',
            'text': '',
            'type': 'image_base64'
        }]

        content.append({
            'image_base64': '',
            'image_file_id': '',
            'image_url': '',
            'text': prompt,
            'type': 'text'
        })
    else:
        content = [{
            'image_base64': '',
            'image_file_id': '',
            'image_url': '',
            'text': prompt,
            'type': 'text'
        }]
    message = [{'content': content, 'role': 'user'}]

    data = {
        'messages': message,
        # 'max_new_tokens': max_new_tokens, # 
        'temperature':0,
        "top_k": 0, 
        "top_p": 0.99, 
        'repetition_penalty':1.05,
        'model': "SenseChat-5-Vision",
        'stream': False,
    }
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + key
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
    )
    
    response = response.json()['data']['choices'][0]['message'].strip()
    print(response)
    return response

def translate_text(text):
    """使用 OpenAI API 将文本翻译为目标语言"""
    return request(api_key, text, None)


def translate_jsonl(input_path, output_path):
    """读取 JSONL 文件并翻译其内容"""
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
           
            # 解析每一行的 JSON 数据
            record = json.loads(line)

            # 翻译每个字段的值
            translated_record = {
                key: translate_text(value) if isinstance(value, str) else value
                for key, value in record.items()
            }

            # 写入翻译后的数据到输出文件
            outfile.write(json.dumps(translated_record, ensure_ascii=False) + '\n')
            

# 调用函数进行翻译
translate_jsonl(input_file, output_file)

print("Translation completed. Translated content saved to", output_file)
