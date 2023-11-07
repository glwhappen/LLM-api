from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

class CodeGenerator:
    def __init__(self, model='Salesforce/codegen-2B-mono'):
        print("加载模型")
        base_path = "./models"
        path = os.path.join(base_path, model)
        
        # 检查CUDA是否可用并设置设备
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("启动模式", self.device)

        self.tokenizer = AutoTokenizer.from_pretrained(model, cache_dir=os.path.join(path, 'config'), local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(model, cache_dir=os.path.join(path, 'models'), local_files_only=True)

        # 将模型放到设备上
        self.model.to(self.device)

    def predict(self, text, max_length=5):
        print('进行补全', text)
        # 确保输入张量也在正确的设备上
        input_ids = self.tokenizer(text, return_tensors="pt").input_ids.to(self.device)
        generated_ids = self.model.generate(input_ids, max_length=input_ids.shape[1] + max_length)
        generated_tokens = generated_ids[0][-max_length:]
        
        # 在返回之前将生成的张量转回CPU
        return self.tokenizer.decode(generated_tokens.cpu(), skip_special_tokens=True)
