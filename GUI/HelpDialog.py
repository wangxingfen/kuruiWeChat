import tkinter as tk
from tkinter import ttk, scrolledtext

class HelpDialog:
    '''应用使用说明书'''
    def __init__(self, parent, is_initial=False):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("使用说明")
        self.dialog.geometry("600x800")
        
        # 创建滚动文本区域
        self.text_area = scrolledtext.ScrolledText(self.dialog, wrap=tk.WORD, width=70, height=40)
        self.text_area.pack(padx=10, pady=10, fill='both', expand=True)
        
        # 使用说明内容
        self.help_text = """
佩奇微信助手使用说明书

1. 基础设置（设置选项卡）
   ---------------
   1.1 API设置
   • API Key: 填入您的API密钥
   • Base URL: 填入API基础地址
   • AI模型: 选择或输入要使用的AI模型
   • "加载可用模型"按钮可以自动获取可用的模型列表
   
   1.2 系统配置
   • 系统提示词: 设置AI助手的基础人设和行为模式
   • 唤醒词: 设置触发AI回复的关键词（默认为"小王"）
   • 画图触发词: 设置触发画图功能的关键词（默认为"帮我画"）
   • 写作触发词: 设置触发写作功能的关键词（默认为"帮我写"）
   
   1.3 图像生成设置
   • 图像API Key: 填入用于图像生成的API密钥
   • 图像API URL: 填入图像生成服务的地址
   • 图像模型: 选择用于生成图像的模型
   
2. 联系人管理
   ---------------
   • 已激活的联系人: 显示当前启用自动回复的联系人列表
   • 手动添加: 直接输入联系人名称添加
   • 自动加载: 从微信获取联系人列表，可多选添加
   
3. 功能使用说明
   ---------------
   3.1 AI对话功能
   • 在与AI对话时，需要使用设定的唤醒词
   • 例如: "小王，今天天气怎么样？"
   
   3.2 AI绘图功能
   • 使用画图触发词来生成图片
   • 例如: "帮我画一只可爱的猫咪"
   • 生成的图片会自动发送给对应联系人
   
   3.3 AI写作功能
   • 使用写作触发词来生成文章
   • 例如: "帮我写一篇关于春天的文章"
   • 生成的文章将以文本文件形式发送
   
4. 监控面板（监控选项卡）
   ---------------
   • 开始监控: 启动自动回复功能
   • 停止监控: 暂停自动回复功能
   • 监控日志: 显示所有消息和回复记录
   
5. 注意事项
   ---------------
   • 使用前请确保已正确配置所有API相关设置
   • 建议先进行小范围测试后再大规模使用
   • 监控开启后请勿关闭程序窗口
   • 定期检查日志确保功能正常运行
   
6. 常见问题解决
   ---------------
   • 如果无法连接API，请检查网络和API配置
   • 如果图片生成失败，请检查图像API设置
   • 如果联系人加载失败，请确保微信已正确登录
   • 如果需要更新配置，请停止监控后再修改设置
        """
        
        self.text_area.insert('1.0', self.help_text)
        self.text_area.config(state='disabled')  # 设置为只读
        
        # 根据是否是初始化对话框显示不同的按钮
        if is_initial:
            ttk.Button(self.dialog, text="开始使用", command=self.dialog.destroy).pack(pady=10)
            self.dialog.protocol("WM_DELETE_WINDOW", self.dialog.destroy)
            self.dialog.transient(parent)  # 设置为主窗口的临时窗口
            self.dialog.grab_set()  # 模态对话框
        else:
            ttk.Button(self.dialog, text="关闭", command=self.dialog.destroy).pack(pady=10)
