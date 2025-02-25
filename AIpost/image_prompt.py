from openai import OpenAI
def image_prompt(prompt,config):
    '''生成图像提示词'''
    image_prompts=config["image_prompt"]
    client = OpenAI(
    # 请用知识引擎原子能力API Key将下行替换为：api_key="sk-xxx",
    api_key=config["api_key"], # 如何获取API Key：https://cloud.tencent.com/document/product/1772/115970
    base_url=config["base_url"],
)
    completion = client.chat.completions.create(
        model=config['model'],  # 此处以 deepseek-r1 为例，可按需更换模型名称。
        messages=[
            {'role': 'system', 'content':image_prompts}
            , {'role': 'user', 'content': prompt}
            ]
)
    img_prompt=completion.choices[0].message.content
    return img_prompt
