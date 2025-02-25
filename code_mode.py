import os
import re
import subprocess
import time
import shutil
from AIpost.ai_coder import ai_coder
from AIpost.code_explainer import code_explainer
from AIpost.title_name import title_name
from AIpost.code_outline import code_outline
def handle_code_request(self,chat,who):
    """远程控制生成代码"""

    def write_code(code_last,type):
        title = title_name(code_last, self.config).replace("\n", "").strip()
        file_name = title + type
        file_path = os.path.join("./py_temp/", file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code_last)
        return file_path

    # 确保 ex_library 和 py_temp 文件夹存在
    os.makedirs("./ex_library/", exist_ok=True)
    os.makedirs("./py_temp/", exist_ok=True)
    
    help=f"""已进入代码模式，请选择：
                    1 {self.config.get("write_word")}
                    2 {self.config.get("continue_word")}
                    3 {self.config.get("code_explain_word")}
                    4 {self.config.get("exit_word")}
                    5 {self.config.get("execute_code_word")}
                    6 {self.config.get("install_package_word")}
                    7 {self.config.get("save_to_library_word")}
                    8 打开代码库
                    9 执行代码库文件
                    10 打开帮助"""
    help_text=write_code(help,".txt")
    chat.SendFiles(help_text)
    X = 1
    while X == 1:
        time.sleep(1)
        msgs = self.wx.GetListenMessage()
        for chat in msgs:
            who = chat.who
            one_msgs = msgs.get(chat)
            for msg in one_msgs:
                content = msg.content
                #type = msg.type
                if self.config.get("write_word") in content:
                    try:
                        code_prompt = code_outline(content, self.config)
                        self.log_message(f"收到【{who}】的请求：{code_prompt}")
                        old_code = ""
                        code = ai_coder(code_prompt, old_code, self.config)
                        self.log_message(f"回复【{who}】：{code}")
                        code_last = re.search(r'```python\n([^`]+)```', code).group(1)
                        self.log_message(f"回复【{who}】：{code_last}")
                        file_path = write_code(code_last,".txt")
                        try:
                            chat.SendFiles(file_path)
                            os.remove(file_path)
                            self.log_message(f"回复【{who}】：{code}")
                        except TimeoutError as e:
                            self.log_message(f"发送文件超时：{e}")
                            save_path = "./py_temp/"
                            shutil.move(file_path, save_path)
                            chat.SendMsg(f"文件发送超时，已保存到路径：{save_path}")
                            self.log_message(f"文件已保存到路径：{save_path}")
                    except Exception as e:
                        self.log_message(f"发生错误：{e}")
                        chat.SendMsg(f"发生错误：{e}")


                elif self.config.get("continue_word") in content:
                    try:
                        code_prompt = code_outline(content, self.config)
                        self.log_message(f"收到【{who}】的请求：{code_prompt}")
                        old_code = code_last
                        code = ai_coder(code_prompt, old_code, self.config)
                        self.log_message(f"回复【{who}】：{code_last}")
                        code_last = re.search(r'```python\n([^`]+)```', code).group(1)
                        file_path = write_code(code_last,".txt")
                        try:
                            chat.SendFiles(file_path)
                            os.remove(file_path)
                            self.log_message(f"回复【{who}】：{code_last}")
                        except TimeoutError as e:
                            self.log_message(f"发送文件超时：{e}")
                            save_path = "./timeout_files/"
                            os.makedirs(save_path, exist_ok=True)
                            shutil.move(file_path, save_path)
                            chat.SendMsg(f"文件发送超时，已保存到路径：{save_path}")
                            self.log_message(f"文件已保存到路径：{save_path}")
                    except Exception as e:
                        self.log_message(f"发生错误：{e}")
                        chat.SendMsg(f"发生错误：{e}")
                elif self.config.get("exit_word") in content:
                    chat.SendMsg("已退出代码生成模式")
                    X = 0
                elif self.config.get("execute_code_word") in content:
                    
                    try:
                        file_path = write_code(code_last,".py")
                        result = subprocess.run(['./venv/Scripts/python.exe', file_path], capture_output=True, text=True, check=True)
                        chat.SendMsg(f"代码执行成功，输出如下：\n{result.stdout}")
                        os.remove(file_path)
                        self.log_message(f"代码执行成功，输出如下：\n{result.stdout}")
                    except subprocess.CalledProcessError as e:
                        chat.SendMsg(f"代码执行出错：\n{e.stderr}")
                        self.log_message(f"代码执行出错：\n{e.stderr}")
                elif self.config.get("install_package_word") in content:
                    try:
                        subprocess.run(['pip', 'install', content.replace(self.config.get("install_package_word"), "")], check=True)
                        chat.SendMsg(f"安装成功：{content.replace(self.config.get('install_package_word'), '')}")
                    except subprocess.CalledProcessError as e:
                        chat.SendMsg(f"安装出错：\n{e.stderr}")
                        self.log_message(f"安装出错：\n{e.stderr}")
                elif self.config.get("delete_file_word") in content:
                    try:
                        file_name = content.replace(self.config.get("delete_file_word"), "").strip()
                        file_path = os.path.join("./ex_library/", file_name)
                        os.remove(file_path)
                        chat.SendMsg(f"文件已删除：{file_path}")
                    except OSError as e:
                        chat.SendMsg(f"删除文件出错：\n{e}")
                        self.log_message(f"删除文件出错：\n{e}")
                elif self.config.get("save_to_library_word") in content:
                    try:
                        file_path = write_code(code_last,".py")
                        save_path = "./ex_library/"
                        shutil.move(file_path, save_path)
                        chat.SendMsg(f"文件已保存到路径：{save_path}")
                    except OSError as e:
                        chat.SendMsg(f"保存文件出错：\n{e}")
                        self.log_message(f"保存文件出错：\n{e}")
                elif self.config.get("code_explain_word") in content:
                    try:
                        code_explain = code_explainer(content, code_last, self.config).replace("代码解释", "")
                        chat.SendMsg(f"{code_explain}")
                    except Exception as e:
                        chat.SendMsg(f"代码解释出错：\n{e}")
                        self.log_message(f"代码解释出错：\n{e}")
                # 新增功能：列出 ex_library 文件夹中的所有 Python 文件
                elif self.config.get("open_code_library") in content:
                    ex_library_path = "./ex_library/"
                    python_files = [f for f in os.listdir(ex_library_path) if f.endswith('.py')]
                    if python_files:
                        file_list = "\n".join(python_files)
                        chat.SendMsg(f"ex_library 文件夹中的 Python 文件：\n{file_list}")
                    else:
                        chat.SendMsg("ex_library 文件夹中没有 Python 文件。")
                elif self.config.get("execute_code_file") in content:
                    file_name = content.replace(self.config.get("execute_code_file"), "").strip()
                    file_path = os.path.join(ex_library_path, file_name)
                    with open(file_path, 'r',encoding="utf-8") as f:
                        code_last = f.read()
                    try:
                        result = subprocess.run(['./venv/Scripts/python.exe', file_path], capture_output=True, text=True, check=True)
                        chat.SendMsg(f"代码执行成功，输出如下：\n{result.stdout}")
                        self.log_message(f"代码执行成功，输出如下：\n{result.stdout}")
                    except subprocess.CalledProcessError as e:
                        chat.SendMsg(f"代码执行出错：\n{e.stderr}")
                        self.log_message(f"代码执行出错：\n{e.stderr}")
                elif "打开帮助" in content:
                    chat.SendFiles(help_text)