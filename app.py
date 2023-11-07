from flask import Flask, request, jsonify
from model import CodeGenerator
from collections import OrderedDict
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

app = Flask(__name__)

# 自定义错误
class ModelNotFoundError(Exception):
    pass

class ModelLoadingError(Exception):
    pass

# 使用有序字典来缓存模型实例
class ModelCache:
    def __init__(self, capacity=2):
        self.cache = OrderedDict()
        self.capacity = capacity

    def load_model(self, model_name):
        try:
            # 尝试从文件加载模型
            return CodeGenerator(model=model_name)
        except Exception as e:
            raise ModelLoadingError(f"An error occurred while loading the model: {e}")

    def get(self, model_name):
        if model_name not in self.cache:
            # 如果模型不在缓存中，尝试加载模型
            if len(self.cache) >= self.capacity:
                # 如果缓存已满，删除最先加入的
                self.cache.popitem(last=False)
            try:
                # 加载模型并加入缓存
                self.cache[model_name] = self.load_model(model_name)
            except ModelLoadingError as e:
                raise
        # 如果模型在缓存中，移动到最后表示最近使用
        self.cache.move_to_end(model_name)
        return self.cache[model_name]

# 初始化缓存对象
model_cache = ModelCache()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        text = data.get('text')
        max_length = int(data.get('max_length'))
        model_name = data.get('model', 'default-model')

        # 通过缓存管理类获取模型
        generator = model_cache.get(model_name)
        prediction = generator.predict(text, max_length)
        return jsonify({'prediction': prediction})
    except ModelNotFoundError:
        return jsonify({"error": "Model not found."}), 404
    except ModelLoadingError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8088, debug=True)
