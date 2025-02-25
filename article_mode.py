from AIpost.text_prompt import text_prompt
from AIpost.ai_counter import ai_counter
from AIpost.ai_outline_ex import ai_outline_ex
from AIpost.ai_write import ai_write
import re
import os
import time
def article_mode(self,chat,content,who):
        textbox = ""
        outline = text_prompt(content, self.config)
        self.log_message(f"回复【{who}】：{outline}")
        chapters = int(re.search(r'共(\d+)章', outline).group(1)) if re.search(r'共(\d+)章', outline) else 1
        outline_box = ""
        for i in range(1, chapters + 1):
            littleoutline = ai_outline_ex(outline, outline_box, self.config, str(i))
            outline_box += littleoutline + "\n"
            self.log_message(f"回复【{who}】：{littleoutline}")
            counter = ai_counter(outline_box, self.config, str(i))
            counter_num = re.search(r'(\d+)小节', counter)
            real_count = int(counter_num.group(1)) if counter_num else 1
            for j in range(1, real_count + 1):
                part = ai_write(littleoutline, self.config, str(i), j)
                self.log_message(f"回复【{who}】：{part}")
                textbox += part + "\n"

        # Generate unique filename and save text content
        title = re.search(r'《([^》]+)》', outline)
        file_name = f"{title.group(1)}.txt" if title else "未命名.txt"
        file_path = os.path.join(self.config["text_save_path"], file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(textbox)
        time.sleep(0.5)
        # Send file and cleanup
        if chat.SendFiles(file_path):
            chat.SendMsg("已为您生成文章，请查看附件。")