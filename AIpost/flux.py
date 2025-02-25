import requests
import random

def get_image(prompt, config):
    '''生成图像'''
    url = config.get('images_base_url')+'/images/generations'
    model = config.get('images_model')
    api_key = config.get('images_api_key')

    if not url or not model or not api_key:
        raise ValueError("图像生成配置不完整，请在设置中配置图像模型相关参数")

    payload = {
        "model": model,
        "prompt": prompt,
        "seed": random.randint(0, 1000000)
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.request("POST", url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()["images"][0]["url"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"图像生成请求失败: {str(e)}")
    except (KeyError, IndexError) as e:
        raise Exception(f"解析图像响应失败: {str(e)}")