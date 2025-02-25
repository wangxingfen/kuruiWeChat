import torch
from torch.utils.data import DataLoader, Dataset
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AdamW

class TextDataset(Dataset):
    def __init__(self, texts, tokenizer, max_length=512):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            return_tensors='pt',
            padding='max_length',
            truncation=True
        )
        return encoding['input_ids'], encoding['attention_mask']

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

texts = ["This is a sample text.", "Another example text.", "Yet another text."]
dataset = TextDataset(texts, tokenizer)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

optimizer = AdamW(model.parameters(), lr=5e-5)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

model.train()
for epoch in range(3):
    for batch in dataloader:
        input_ids, attention_mask = batch
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=input_ids)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    print(f"Epoch {epoch+1} finished")

model.save_pretrained('my_gpt_model')

# 1. 确保安装了transformers库
# pip install transformers

# 2. 设置自定义的Hugging Face镜像地址
from transformers import AutoModel
import os

# 定义一个函数来加载模型，使用自定义的镜像地址
def load_model_from_mirror(model_name, mirror_url):
    # 设置环境变量，指向自定义的镜像地址
    os.environ["HF_HUB_MODEL_REPOS"] = mirror_url
    
    # 加载模型
    model = AutoModel.from_pretrained(model_name)
    return model

# 3. 使用自定义镜像地址加载模型
# 假设你的模型名称是 "distilbert-base-uncased"
model_name = "distilbert-base-uncased"
mirror_url = "https://huggingface.co/datasets"  # 你的自定义镜像地址

# 加载模型
model = load_model_from_mirror(model_name, mirror_url)

# 现在你可以使用model变量来访问你的模型了
