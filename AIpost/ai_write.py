from openai import OpenAI

def ai_write(outlines,config,chapters,piece):
    '''执行具体写作任务'''
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )
    tippieces=f'你是一个伟大且热烈的作家，现在根据如下第{chapters}章大纲全神贯注写其中第{piece}小节的内容。'
    messages = [
        {'role': 'system', 'content':tippieces},
        {'role': 'user', 'content':outlines},
    ]
    
    completion = client.chat.completions.create(
        model=config['model'],
        messages=messages,
        temperature=eval(config['temperature']),
        max_tokens=eval(config['max_tokens']),
        frequency_penalty=eval(config['frequency_penalty']),
        presence_penalty=eval(config['presence_penalty']),
        top_p=eval(config['top_p']),
    )
    
    piece = completion.choices[0].message.content
    return piece
