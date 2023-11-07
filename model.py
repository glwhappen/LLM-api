from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
import logging

class CodeGenerator:
    def __init__(self, model=None):
        # 配置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # 确定基础路径和使用的模型
        base_path = os.getenv('MODEL_BASE_PATH', './models')
        model_name = model if model is not None else os.getenv('MODEL_NAME', 'Salesforce/codegen-2B-mono')

        self.logger.info(f"正在加载模型: {model_name}")

        model_path = os.path.join(base_path, model_name)
        
        # 检查CUDA是否可用，并设置设备
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.logger.info(f"设备设置为 {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=os.path.join(model_path, 'config'), local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=os.path.join(model_path, 'models'), local_files_only=True)

        # 将模型移动到适当的设备上
        self.model.to(self.device)

        # 确保模型处于评估模式
        self.model.eval()

    def predict(self, text, max_length=5):
        self.logger.info(f"为以下文本生成补全: {text}")
        try:
            # 禁用梯度计算
            with torch.no_grad():
                input_ids = self.tokenizer(text, return_tensors="pt").input_ids.to(self.device)
                generated_ids = self.model.generate(input_ids, max_length=input_ids.shape[1] + max_length)
            generated_tokens = generated_ids[0][-max_length:]
            return self.tokenizer.decode(generated_tokens.cpu(), skip_special_tokens=True)
        except RuntimeError as e:
            if "CUDA out of memory" in str(e):
                self.logger.error("CUDA内存不足：您可能需要减少批量大小或序列长度。")
                raise RuntimeError("CUDA内存不足：您可能需要减少批量大小或序列长度。") from e
            else:
                raise e

# 使用示例
# generator = CodeGenerator()
# prediction = generator.predict("快速的棕色狐狸", max_length=50)
