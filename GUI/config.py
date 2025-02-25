import json
import os

CONFIG_FILE = "settings.json"
MESSAGEBOX_FILE = "messageboxs.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default_config.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def save_messageboxs(messageboxs):
    with open(MESSAGEBOX_FILE, 'w', encoding='utf-8') as f:
        json.dump(messageboxs, f, ensure_ascii=False, indent=4)

def load_messageboxs():
    if os.path.exists(MESSAGEBOX_FILE):
        with open(MESSAGEBOX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

default_config = {
    "api_key": "请到https://cloud.siliconflow.cn/i/ByXrxmTh申请API Key",
    "base_url": "https://api.siliconflow.cn/v1",
    "model": "THUDM/glm-4-9b-chat",  # 默认模型
    "system_prompt": "你是一个助手，你的名字是小王，你的任务是帮助用户解决各种问题。",  # 默认系统提示
    "whitelist": ["文件传输助手"],
    "images_model": "black-forest-labs/FLUX.1-schnell",  # Will be populated from API
    "images_api_key": "请到https://cloud.siliconflow.cn/i/ByXrxmTh申请API Key",
    "images_base_url": "https://api.siliconflow.cn/v1",
    "wake_word": "小王",  # 默认唤醒词
    "code_word": "给我写",
    "draw_trigger": "帮我画",    # 添加画图触发词
    "write_trigger": "帮我写",   # 添加写作触发词
    "image_save_path": "d:",  # 默认图片保存路径
    "text_save_path": "d:",  # 默认文本保存路径
    "turns_limited":"20",
    "max_tokens": "4096",
    "temperature": "0.3",
    "top_p": "0.9",
    "presence_penalty": "0.2",#惩罚
    "frequency_penalty": "0.4",
    "n": "1",
    "outline_tips":"""你的任务是根据用户要求写出大纲，具体格式和要求如下：

标题：《{{y}}》（自拟标题，需体现核心冲突或意象） 
要求：【{{z}}】（一句话概括用户想要的主题，体裁，风格等） 
总章数：共{{x}}章（动态匹配用户进度，若用户指定1章则输出“共1章”）  
输出示例：
第1章：
第2章：
第3章：
第4章：
第5章：
第6章：
第7章：
第8章：
第9章：
第10章：
（具体章数根据用户指定决定）
注意：雕琢章名即可，无需写具体小节，更无需写具体内容"""
,
    "littleline_tips":"""输出示例：
第1章：（与用户提供的保持一致）
要求：（与用户提供的保持一致）
第一小节：
。。。。。。
（具体小节数根据内容决定）
"""
,
    "image_prompt":"请将用户的输入升华具有大师水准的准确且标准且丰富的的英文绘图提示词，以便绘图模型能够完美绘制。",
    "write_word": "给我写",  # 新增唤醒词
    "continue_word": "继续",  # 新增唤醒词
    "exit_word": "退出",  # 新增唤醒词
    "execute_code_word": "执行代码",  # 新增唤醒词
    "install_package_word": "安装包",  # 新增唤醒词
    "delete_file_word": "删除文件",  # 新增唤醒词
    "save_to_library_word": "保存入库",  # 新增唤醒词
    "code_explain_word": "代码解释",  # 新增唤醒词
    "open_code_library": "打开代码库",
    "execute_code_file": "执行库文件" , 
}