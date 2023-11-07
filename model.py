from transformers import AutoTokenizer, AutoModelForCausalLM
import os

class CodeGenerator:
    def __init__(self, model = 'Salesforce/codegen-2B-mono'):
        print("加载模型")
        base_path = "./models"
        path = os.path.join(base_path, model)
        self.tokenizer = AutoTokenizer.from_pretrained(model, cache_dir=os.path.join(path, 'config'), local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(model, cache_dir=os.path.join(path, 'models'), local_files_only=True)

    def predict(self, text, max_length = 5):
        print('进行补全', text)
        input_ids = self.tokenizer(text, return_tensors="pt").input_ids
        generated_ids = self.model.generate(input_ids, max_length=input_ids.shape[1] + max_length)
        generated_tokens = generated_ids[0][-max_length:]
        return self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
