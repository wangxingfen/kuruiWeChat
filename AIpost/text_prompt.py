from openai import OpenAI

def text_prompt(prompt, config):
    '''生成初步大纲提示词'''
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )
    
    messages = [
        {'role': 'system', 'content': config["outline_tips"]},
        {'role': 'user', 'content': prompt},
    ]
    
    completion = client.chat.completions.create(
        model=config['model'],
        messages=messages,
        temperature=eval(config['temperature']),
        max_tokens=eval(config['max_tokens']),
        frequency_penalty=eval(config['frequency_penalty']),
        presence_penalty=eval(config['presence_penalty']),
        top_p=eval(config['top_p']),
        n=1,
    )
    
    piece = completion.choices[0].message.content
    return piece