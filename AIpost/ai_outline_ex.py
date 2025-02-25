from openai import OpenAI
def ai_outline_ex(outlines,outlinebox,config,chapters):
    """生成大纲的具体化扩展版本"""
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )
    tippieces=f'现在根据[{outlines}]全神贯注丰富其中第{chapters}章的大纲，参考资料为用户输入，你的输出格式为{config["littleline_tips"].encode('utf-8').decode('utf-8')}'
    messages = [
        {'role': 'system', 'content':tippieces},
        {'role': 'user', 'content': outlinebox},
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