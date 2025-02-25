from openai import OpenAI

def code_explainer(prompt,code,config):
    '''执行解释代码任务'''
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )
    tippieces=f'你是一个伟大且热烈的程序员，现在根据以下代码按照用户要求给出相应解释。'
    messages = [
        {'role': 'system', 'content':tippieces},
        {'role': 'user', 'content':code+prompt},
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
    
    explanin = completion.choices[0].message.content
    return explanin
