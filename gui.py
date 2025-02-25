import tkinter as tk
from tkinter import ttk, scrolledtext
from GUI.config import load_config, save_config
from GUI.config import load_messageboxs, save_messageboxs
from wxauto import WeChat
import threading
import time
from openai import OpenAI
import tkinter.messagebox as messagebox
from AIpost.flux import get_image
import os
import uuid
import requests
from AIpost.image_prompt import image_prompt
from GUI.HelpDialog import HelpDialog
from AIpost.ai_respose import ai_respose
from code_mode import handle_code_request
from article_mode import article_mode

class EnhancedGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("酷睿微信助手")
        self.root.geometry("600x1000")
        
        # 显示主窗口
        self.root.deiconify()
        
        self.config = load_config()
        self.messageboxs = load_messageboxs()
        self.monitoring = False
        self.wx = WeChat()
        self.active_contacts = self.config.get("whitelist", [])
        self.available_models = []
        self.available_image_models = []

        # 添加顶部帮助按钮
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill='x', padx=5, pady=5)
        
        # 添加保存设置按钮
        save_button = ttk.Button(top_frame, text="保存设置", command=self.save_settings)
        save_button.pack(side='left')
        
        help_button = ttk.Button(top_frame, text="使用说明", command=self.show_help)
        help_button.pack(side='right')
        
        
        # 创建选项卡
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 设置选项卡
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text='设置')
        self.setup_settings_tab()
        
        # 监控选项卡
        self.monitor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.monitor_frame, text='监控')
        self.setup_monitor_tab()
        
        # 状态栏
        self.status_bar = tk.Label(self.root, text="就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 添加自动启动监控
        self.root.after(1000, self.start_monitoring)  # 程序启动1秒后开始监控

    def show_initial_help(self):
        """显示初始帮助对话框"""
        help_dialog = HelpDialog(self.root, is_initial=True)
        self.root.wait_window(help_dialog.dialog)

    def show_help(self):
        """显示常规帮助对话框"""
        HelpDialog(self.root, is_initial=False)

    def setup_settings_tab(self):
        # 创建主画布和滚动条
        canvas = tk.Canvas(self.settings_frame)
        scrollbar = ttk.Scrollbar(self.settings_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # 配置画布
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 将画布和滚动条放置在窗口中
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # API设置
        settings_frame = ttk.LabelFrame(scrollable_frame, text="API设置")
        settings_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(settings_frame, text="API Key:").pack(padx=5, pady=2)
        self.api_key = ttk.Entry(settings_frame, width=50)
        self.api_key.insert(0, self.config.get("api_key", ""))
        self.api_key.pack(padx=5, pady=2)
        
        ttk.Label(settings_frame, text="Base URL:").pack(padx=5, pady=2)
        self.base_url = ttk.Entry(settings_frame, width=50)
        self.base_url.insert(0, self.config.get("base_url", ""))
        self.base_url.pack(padx=5, pady=2)
        
        # 模型选择区域
        model_frame = ttk.Frame(settings_frame)
        model_frame.pack(fill='x', padx=5, pady=2)
        
        ttk.Label(model_frame, text="AI模型:").pack(side=tk.LEFT, padx=5)
        self.model_entry = ttk.Combobox(model_frame, width=40)
        self.model_entry.pack(side=tk.LEFT, padx=5)
        self.model_entry.insert(0, self.config.get("model", ""))
        
        ttk.Button(model_frame, text="加载可用模型", 
                  command=self.load_available_models).pack(side=tk.LEFT, padx=5)
        
        # 系统提示词
        prompt_frame = ttk.LabelFrame(scrollable_frame, text="系统提示词")
        prompt_frame.pack(fill='x', padx=5, pady=5)
        
        self.system_prompt = tk.Text(prompt_frame, height=4, width=50)
        self.system_prompt.insert("1.0", self.config.get("system_prompt", ""))
        self.system_prompt.pack(padx=5, pady=5)
        
        # 添加保存路径设置区域
        path_frame = ttk.LabelFrame(scrollable_frame, text="保存路径设置")
        path_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(path_frame, text="图片保存路径:").pack(padx=5, pady=2)
        self.image_path_entry = ttk.Entry(path_frame, width=50)
        self.image_path_entry.insert(0, self.config.get("image_save_path", os.path.join(os.path.dirname(__file__), 'images')))
        self.image_path_entry.pack(padx=5, pady=2)
        ttk.Button(path_frame, text="浏览", command=lambda: self.select_directory(self.image_path_entry)).pack(padx=5, pady=2)
        
        ttk.Label(path_frame, text="文本保存路径:").pack(padx=5, pady=2)
        self.text_path_entry = ttk.Entry(path_frame, width=50)
        self.text_path_entry.insert(0, self.config.get("text_save_path", os.path.dirname(__file__)))
        self.text_path_entry.pack(padx=5, pady=2)
        ttk.Button(path_frame, text="浏览", command=lambda: self.select_directory(self.text_path_entry)).pack(padx=5, pady=2)

        # 添加唤醒词设置区域（放在系统提示词之后）
        wake_frame = ttk.LabelFrame(scrollable_frame, text="唤醒词设置")
        wake_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(wake_frame, text="唤醒词:").pack(side=tk.LEFT, padx=5)
        self.wake_word_entry = ttk.Entry(wake_frame, width=20)
        self.wake_word_entry.insert(0, self.config.get("wake_word", "小王"))
        self.wake_word_entry.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Label(wake_frame, text="对话记忆轮数:").pack(side=tk.LEFT, pady=5)
        self.turns_limited = ttk.Entry(wake_frame, width=20)
        self.turns_limited.insert(0, self.config.get("turns_limited", "20"))
        self.turns_limited.pack(side=tk.LEFT,padx=5, pady=2)
        

        # 添加触发词设置区域（放在系统提示词之后）
        trigger_frame = ttk.LabelFrame(scrollable_frame, text="触发词设置")
        trigger_frame.pack(fill='x', padx=5, pady=5)
    
        # 画图触发词设置
        draw_frame = ttk.Frame(trigger_frame)
        draw_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(draw_frame, text="画图触发词:").pack(side=tk.LEFT, padx=5)
        self.draw_trigger_entry = ttk.Entry(draw_frame, width=20)
        self.draw_trigger_entry.insert(0, self.config.get("draw_trigger", "帮我画"))
        self.draw_trigger_entry.pack(side=tk.LEFT, padx=5)
        
        # 写作触发词设置
        write_frame = ttk.Frame(trigger_frame)
        write_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(write_frame, text="写作触发词:").pack(side=tk.LEFT, padx=5)
        self.write_trigger_entry = ttk.Entry(write_frame, width=20)
        self.write_trigger_entry.insert(0, self.config.get("write_trigger", "帮我写"))
        self.write_trigger_entry.pack(side=tk.LEFT, padx=5)

        
        # 联系人管理区域
        contacts_frame = ttk.LabelFrame(scrollable_frame, text="联系人管理")
        contacts_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # 已激活联系人列表
        active_frame = ttk.LabelFrame(contacts_frame, text="已激活的联系人")
        active_frame.pack(fill='x', padx=5, pady=5)
        
        self.active_listbox = tk.Listbox(active_frame, height=5)
        self.active_listbox.pack(side=tk.LEFT, fill='x', expand=True, padx=5, pady=5)
        for contact in self.active_contacts:
            self.active_listbox.insert(tk.END, contact)
        
        active_scroll = ttk.Scrollbar(active_frame, orient=tk.VERTICAL, command=self.active_listbox.yview)
        active_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.active_listbox.config(yscrollcommand=active_scroll.set)
        
        # 删除选中联系人按钮
        ttk.Button(active_frame, text="删除选中", command=self.remove_selected_contact).pack(side=tk.RIGHT, padx=5)

        # 手动添加区域
        manual_frame = ttk.LabelFrame(contacts_frame, text="手动添加联系人")
        manual_frame.pack(fill='x', padx=5, pady=5)
        
        self.manual_entry = ttk.Entry(manual_frame)
        self.manual_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=5, pady=5)
        
        ttk.Button(manual_frame, text="添加", command=self.add_manual_contact).pack(side=tk.RIGHT, padx=5)

        # 自动加载区域
        auto_frame = ttk.LabelFrame(contacts_frame, text="自动加载联系人")
        auto_frame.pack(fill='x', padx=5, pady=5)
        
        self.contact_listbox = tk.Listbox(auto_frame, selectmode=tk.MULTIPLE, height=8)
        self.contact_listbox.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)
        
        scroll = ttk.Scrollbar(auto_frame, orient=tk.VERTICAL, command=self.contact_listbox.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.contact_listbox.config(yscrollcommand=scroll.set)

        button_frame = ttk.Frame(auto_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="加载联系人", command=self.load_contacts).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="添加选中", command=self.add_selected_contacts).pack(side=tk.LEFT, padx=5)

        # 添加图像模型设置区域
        image_settings_frame = ttk.LabelFrame(scrollable_frame, text="图像生成设置")
        image_settings_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(image_settings_frame, text="图像API Key:").pack(padx=5, pady=2)
        self.image_api_key = ttk.Entry(image_settings_frame, width=50)
        self.image_api_key.insert(0, self.config.get("images_api_key", ""))
        self.image_api_key.pack(padx=5, pady=2)
        
        ttk.Label(image_settings_frame, text="图像API URL:").pack(padx=5, pady=2)
        self.image_base_url = ttk.Entry(image_settings_frame, width=50)
        self.image_base_url.insert(0, self.config.get("images_base_url", ""))
        self.image_base_url.pack(padx=5, pady=2)
        
        # 图像模型选择区域
        image_model_frame = ttk.Frame(image_settings_frame)
        image_model_frame.pack(fill='x', padx=5, pady=2)
        
        ttk.Label(image_model_frame, text="图像模型:").pack(side=tk.LEFT, padx=5)
        self.image_model_entry = ttk.Combobox(image_model_frame, width=40)
        self.image_model_entry.pack(side=tk.LEFT, padx=5)
        self.image_model_entry.insert(0, self.config.get("images_model", ""))
        
        ttk.Button(image_model_frame, text="加载图像模型", 
                  command=self.load_available_image_models).pack(side=tk.LEFT, padx=5)

        # 添加高级设置区域
        advanced_settings_frame = ttk.LabelFrame(scrollable_frame, text="高级设置")
        advanced_settings_frame.pack(fill='x', padx=5, pady=5)

        # max_tokens
        ttk.Label(advanced_settings_frame, text="Max Tokens:").pack(padx=5, pady=2)
        self.max_tokens_entry = ttk.Entry(advanced_settings_frame, width=50)
        self.max_tokens_entry.insert(0, self.config.get("max_tokens", ""))
        self.max_tokens_entry.pack(padx=5, pady=2)

        # temperature
        ttk.Label(advanced_settings_frame, text="Temperature:").pack(padx=5, pady=2)
        self.temperature_entry = ttk.Entry(advanced_settings_frame, width=50)
        self.temperature_entry.insert(0, self.config.get("temperature", ""))
        self.temperature_entry.pack(padx=5, pady=2)

        # top_p
        ttk.Label(advanced_settings_frame, text="Top P:").pack(padx=5, pady=2)
        self.top_p_entry = ttk.Entry(advanced_settings_frame, width=50)
        self.top_p_entry.insert(0, self.config.get("top_p", ""))
        self.top_p_entry.pack(padx=5, pady=2)

        # presence_penalty
        ttk.Label(advanced_settings_frame, text="Presence Penalty:").pack(padx=5, pady=2)
        self.presence_penalty_entry = ttk.Entry(advanced_settings_frame, width=50)
        self.presence_penalty_entry.insert(0, self.config.get("presence_penalty", ""))
        self.presence_penalty_entry.pack(padx=5, pady=2)

        # frequency_penalty
        ttk.Label(advanced_settings_frame, text="Frequency Penalty:").pack(padx=5, pady=2)
        self.frequency_penalty_entry = ttk.Entry(advanced_settings_frame, width=50)
        self.frequency_penalty_entry.insert(0, self.config.get("frequency_penalty", ""))
        self.frequency_penalty_entry.pack(padx=5, pady=2)

        # outline_tips
        outline_tips_frame = ttk.LabelFrame(scrollable_frame, text="大纲提示词")
        outline_tips_frame.pack(fill='x', padx=5, pady=5)
        self.outline_tips = tk.Text(outline_tips_frame, height=6, width=50)
        self.outline_tips.insert("1.0", self.config.get("outline_tips", ""))
        self.outline_tips.pack(padx=5, pady=5)

        # littleline_tips
        littleline_tips_frame = ttk.LabelFrame(scrollable_frame, text="小节提示词")
        littleline_tips_frame.pack(fill='x', padx=5, pady=5)
        self.littleline_tips = tk.Text(littleline_tips_frame, height=6, width=50)
        self.littleline_tips.insert("1.0", self.config.get("littleline_tips", ""))
        self.littleline_tips.pack(padx=5, pady=5)

        # image_prompt
        image_prompt_frame = ttk.LabelFrame(scrollable_frame, text="图像提示词")
        image_prompt_frame.pack(fill='x', padx=5, pady=5)
        self.image_prompt = tk.Text(image_prompt_frame, height=4, width=50)
        self.image_prompt.insert("1.0", self.config.get("image_prompt", ""))
        self.image_prompt.pack(padx=5, pady=5)

    def load_available_models(self):
        """从API加载可用模型列表"""
        self.load_models(self.api_key, self.base_url, self.model_entry, self.available_models, "AI模型")

    def load_available_image_models(self):
        """从API加载可用图像模型列表"""
        self.load_models(self.image_api_key, self.image_base_url, self.image_model_entry, self.available_image_models, "图像模型")

    def load_models(self, api_key_entry, base_url_entry, model_entry, available_models, model_type):
        try:
            api_key = api_key_entry.get().strip()
            base_url = base_url_entry.get().strip()
            
            if not api_key or not base_url:
                messagebox.showerror("错误", "请先填写API Key和Base URL")
                return
                
            client = OpenAI(api_key=api_key, base_url=base_url)
            models = client.models.list()
            
            # 获取所有模型ID
            available_models[:] = [model.id for model in models.data]
            model_entry['values'] = available_models
            
            # 如果当前选择的模型不在列表中，选择第一个模型
            current_model = model_entry.get()
            if (current_model not in available_models) and available_models:
                model_entry.set(available_models[0])
            
            messagebox.showinfo("成功", f"成功加载{len(available_models)}个{model_type}")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载{model_type}失败（请手动添加）: {str(e)}")

    def save_settings(self):
        self.config.update({
            "api_key": self.api_key.get(),
            "base_url": self.base_url.get(),
            "model": self.model_entry.get(),
            "system_prompt": self.system_prompt.get("1.0", tk.END).strip(),
            "whitelist": self.active_contacts,
            "images_api_key": self.image_api_key.get(),
            "images_base_url": self.image_base_url.get(),
            "images_model": self.image_model_entry.get(),
            "wake_word": self.wake_word_entry.get().strip(),
            "turns_limited": self.turns_limited.get().strip(),
            "draw_trigger": self.draw_trigger_entry.get().strip(),
            "write_trigger": self.write_trigger_entry.get().strip(),
            "image_save_path": self.image_path_entry.get().strip(),
            "text_save_path": self.text_path_entry.get().strip(),
            "max_tokens": self.max_tokens_entry.get().strip(),
            "temperature": self.temperature_entry.get().strip(),
            "top_p": self.top_p_entry.get().strip(),
            "presence_penalty": self.presence_penalty_entry.get().strip(),
            "frequency_penalty": self.frequency_penalty_entry.get().strip(),
            "outline_tips": self.outline_tips.get("1.0", tk.END).strip(),
            "littleline_tips": self.littleline_tips.get("1.0", tk.END).strip(),
            "image_prompt": self.image_prompt.get("1.0", tk.END).strip(),
        })
        save_config(self.config)
        self.log_message("设置已保存")
        
        # 停止当前监控
        if self.monitoring:
            self.stop_monitoring()
        
        # 重新开始监控以应用新设置
        self.start_monitoring()
        self.log_message("已重新开始监控")

    def setup_monitor_tab(self):
        # 控制按钮
        control_frame = ttk.Frame(self.monitor_frame)
        control_frame.pack(fill='x', padx=5, pady=5)
        
        self.start_button = ttk.Button(control_frame, text="开始监控", command=self.start_monitoring)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="停止监控", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # 添加一键清除日志按钮
        self.clear_log_button = ttk.Button(control_frame, text="清除日志", command=self.clear_log)
        self.clear_log_button.pack(side=tk.LEFT, padx=5)
        
        # 日志区域
        log_frame = ttk.LabelFrame(self.monitor_frame, text="监控日志")
        log_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=20)
        self.log_area.pack(fill='both', expand=True, padx=5, pady=5)
        
    def clear_log(self):
        """清除监控日志内容"""
        self.log_area.delete(1.0, tk.END)
        self.log_message("日志已清除")

    def add_manual_contact(self):
        contact = self.manual_entry.get().strip()
        if contact and contact not in self.active_contacts:
            self.active_contacts.append(contact)
            self.active_listbox.insert(tk.END, contact)
            self.manual_entry.delete(0, tk.END)
            self.log_message(f"手动添加联系人：{contact}")

    def remove_selected_contact(self):
        selection = self.active_listbox.curselection()
        if selection:
            contact = self.active_listbox.get(selection)
            self.active_contacts.remove(contact)
            self.active_listbox.delete(selection)
            self.log_message(f"删除联系人：{contact}")

    def add_selected_contacts(self):
        selected = [self.contact_listbox.get(idx) for idx in self.contact_listbox.curselection()]
        for contact in selected:
            if contact not in self.active_contacts:
                self.active_contacts.append(contact)
                self.active_listbox.insert(tk.END, contact)
        self.log_message(f"添加选中联系人：{', '.join(selected)}")

    def load_contacts(self):
        self.contact_listbox.delete(0, tk.END)
        try:
            wx = WeChat()
            contacts = wx.GetAllFriends()
            for contact in contacts:
                friend = contact["remark"] or contact["nickname"]
                if friend not in self.active_contacts:
                    self.contact_listbox.insert(tk.END, friend)
            self.log_message("已加载联系人列表")
        except Exception as e:
            self.log_message(f"加载联系人失败：{str(e)}")

    def log_message(self, message):
        formatted_message = self.format_log_message(message)
        self.log_area.insert(tk.END, formatted_message)
        self.log_area.see(tk.END)

    def format_log_message(self, message):
        return f"[{time.strftime('%H:%M:%S')}] {message}\n"

    def start_monitoring(self):
        self.monitoring = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_bar.config(text="正在监控中...")
        self.monitoring_thread = threading.Thread(target=self.monitor_messages)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

    def stop_monitoring(self):
        self.monitoring = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_bar.config(text="监控已停止")

    def download_image(self, chat,image_url):
        """下载图片，只尝试一次，并在失败时发送提示信息"""
        file_path = self.get_file_path(image_url, "jpg")
        try:
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                return file_path
            else:
                self.log_message(f"下载图片失败，状态码：{response.status_code}")
                chat.SendMsg("抱歉，图片下载失败")
        except Exception as e:
            self.log_message(f"下载图片失败：{str(e)}")
            chat.SendMsg("抱歉，图片下载失败")
        return None

    def send_file_with_retry(self, chat, file_path):
        """发送文件，只尝试一次，并在失败时发送提示信息"""
        try:
            chat.SendFiles(file_path)
        except Exception as e:
            self.log_message(f"发送文件失败：{str(e)}")
            chat.SendMsg("抱歉，文件发送失败")

    def get_file_path(self, url, extension):
        file_name = f"{uuid.uuid4()}.{extension}"
        return os.path.join(self.config.get("image_save_path"), file_name)

    def download_file(self, url, file_path):
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    return True
                else:
                    self.log_message(f"下载图片失败，状态码：{response.status_code}")
            except Exception as e:
                self.log_message(f"下载图片失败：{str(e)}")
            retry_count += 1
            time.sleep(1)  # 重试前等待1秒
        return False

    def retry_operation(self, operation, operation_name):
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                operation()
                return True
            except Exception as e:
                self.log_message(f"{operation_name}失败：{str(e)}，重试次数：{retry_count + 1}")
            retry_count += 1
            time.sleep(1)  # 重试前等待1秒
        return False
    def get_listen_content(self,wx):
        msgs = wx.GetListenMessage()
        for chats in msgs:
            whos = chats.who
            one_msgs = msgs.get(chats)
            for msg in one_msgs:
                contents = msg.content
                types = msg.type
                self.log_message(f"【{whos}】: {contents}") 

    def monitor_messages(self):
        '''监控微信消息'''
        wake_word = self.config.get("wake_word")
        code_word = self.config.get("code_word")
        draw_trigger = self.config.get("draw_trigger")
        write_trigger = self.config.get("write_trigger")
        for i in self.config["whitelist"]:
            self.wx.AddListenChat(who=i, savevoice=True)  # 改为保存图片
            if i not in self.messageboxs:  # 如果联系人不在 messageboxs 中，初始化空列表
                self.messageboxs[i] = []
            self.log_message(f"开始监控联系人: {i}")
    
        while self.monitoring:
            msgs = self.wx.GetListenMessage()
            for chat in msgs:
                who = chat.who
                one_msgs = msgs.get(chat)
                for msg in one_msgs:
                    content = msg.content
                    type = msg.type
                    self.log_message(f"【{who}】: {content}") 
                    if draw_trigger in content:
                        image_prompts = image_prompt(content, self.config)
                        image_url = get_image(image_prompts, self.config)
                        # 下载图片
                        local_image_path = self.download_image(chat,image_url)
                        if local_image_path:
                            time.sleep(0.5)
                            try:    
                                chat.SendFiles(local_image_path)
                                self.log_message(f"回复【{who}】图片：{local_image_path}")
                            except Exception as e:
                                chat.SendMsg(f"抱歉，发送图片失败，但保存在本地{local_image_path}")
                        else:
                            chat.SendMsg("抱歉，图片下载失败")
                    elif write_trigger in content:
                        try:
                            article_mode(self,chat,content,who)
                        except Exception as e:
                            chat.SendMsg("抱歉，文章生成失败")
    
                    elif code_word in content:
                        handle_code_request(self,chat, who)
                    elif (wake_word in content and type == "friend") or (who in content and type == "self"):
                        turns_limited = int(self.config.get("turns_limited"))
                        backtext = self.messageboxs[who][-turns_limited:] if turns_limited < len(self.messageboxs[who]) else self.messageboxs[who]
                        response, backtext = ai_respose(content.replace(who, ""), backtext, self.config)
                        chat.SendMsg(response.strip("\n"))
                        self.messageboxs[who].append(backtext)
                        save_messageboxs(self.messageboxs) # 保存 messageboxs 内容
                        self.log_message(f"回复【{who}】：{response}")
                    time.sleep(0.5)

    def select_directory(self, entry_widget):
        """打开文件浏览器选择目录，并更新输入框内容"""
        from tkinter import filedialog
        directory = filedialog.askdirectory()
        if directory:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, directory)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = EnhancedGUI()
    gui.run()