from openai import OpenAI

def ai_respose(message, messageses, config):
    '''供日常聊天使用'''
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"],
        
    )
    
    messages = [
        {'role': 'system', 'content': config["system_prompt"]},
        {'role': 'user', 'content': str(messageses)+message},
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
    
    ai_respose = completion.choices[0].message.content
    context = []
    context.append({'role': 'user', 'content': message})
    context.append({'role': 'assistant', 'content': ai_respose})
    return ai_respose, context
