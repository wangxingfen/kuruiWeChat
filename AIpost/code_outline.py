from openai import OpenAI

def code_outline(prompt, config):
    '''生成初步代码大纲提示词'''
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )
    
    messages = [
        {'role': 'system', 'content':"你是一个经验丰富的程序员，你的任务是将用户的指令准确具体地转换为条理清晰，步骤明确的代码提示词。"},
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
    
    prompts = completion.choices[0].message.content
    return prompts