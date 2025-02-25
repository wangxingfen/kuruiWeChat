from openai import OpenAI
def ai_counter(bigline,config,thechapter):
    '''计算每章的小节数'''
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )
    messages = [
        {'role': 'system', 'content':"数出用户提供大纲的第"+thechapter+"章共有几小节，输出阿拉伯数字。输出示例：【共有3小节】。请以具体情况为准！"},
        {'role': 'user', 'content':bigline},
    ]
    
    completion = client.chat.completions.create(
        model=config['model'],
        messages=messages,
        temperature=0.2,
    )
    
    count = completion.choices[0].message.content
    return count