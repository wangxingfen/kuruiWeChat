from openai import OpenAI

def ai_coder(code_prompt,old_code,config):
    '''执行具体写代码任务'''
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )
    tippieces=f'你是一个伟大且热烈的python程序员，拒绝写非python代码，现在根据如下内容写代码。直接输出代码即可。'
    messages = [
        {'role': 'system', 'content':tippieces},
        {'role': 'user', 'content':old_code+code_prompt},
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
    
    last_code = completion.choices[0].message.content
    return last_code
