from openai import OpenAI

def title_name(code,config):
    '''执行给代码取名的任务'''
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )
    tippieces=f'你是一个取名的专家，现在根据以下代码给出一个标题，输出不超过二十个字。不带任何标点符号。'
    messages = [
        {'role': 'system', 'content':tippieces},
        {'role': 'user', 'content':code},
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
    
    title = completion.choices[0].message.content
    return title