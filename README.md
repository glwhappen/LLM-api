# 快速部署大语言模型

## 简介
这个项目可以快速部署 huggingface上 的模型，并提供一个 API 接口，可以访问多种大型语言模型进行代码生成。它使用 Flask 构建，并可以根据 API 请求中指定的模型动态加载。此外，API 实现了一个简单的模型缓存机制，每次只保留最近使用的两个模型实例。

目前只针对代码生成的模型做了接口，其他的模型可能还需要稍微修改代码，这个项目旨在提供一个思路。

## 前提条件
- Python 3.x
- Flask
- Hugging Face 的 Transformers 库
- 支持 CUDA 的 PyTorch（如果使用 GPU）

在启动 API 之前，请从百度网盘下载模型文件并放置在指定目录。

## 安装

克隆仓库：
```bash
git clone https://github.com/glwhappen/LLM-api.git
cd code-generator-api
```

安装依赖项：
```bash
Flask==2.2.5
torch==1.13.0+cu117
transformers==4.27.0.dev0

得根据自己的实际环境来
```

## 运行 API

使用以下命令启动 API：
```bash
python app.py
```
在 `http://127.0.0.1:5000` 访问 API。

## 使用方法

要生成代码，请发送包含 `text`、`max_length` 和可选的 `model` 字段的 JSON 数据到 `/predict` 的 POST 请求：

```bash
curl --location 'http://127.0.0.1:5000/predict' \
--header 'Content-Type: application/json' \
--data '{
    "text": "print(",
    "max_length": 50,
    "model": "Salesforce/codegen-350M-mono"
}'
```

您将收到包含预测内容的 JSON 响应。

## 模型列表

为了移动模型方便，我把相同的模型的 config 和 models 放到了一起，在网络比较好的情况下，会自动的进行模型的下载，如果网络不好，可以在其他地方下载好以后，用百度网盘或者其他工具上传一下

> 为了方便使用，可以直接从我提供的百度网盘下载
链接：https://pan.baidu.com/s/1KFUlXBqzQfZtmGLq6QUKIw?pwd=6666 
提取码：6666 

- Salesforce/codegen-350M-mono
- Salesforce/codegen-2B-mono
- Salesforce/codegen-16B-mono

模型存放的位置

![](https://raw.githubusercontent.com/glwhappen/images/main/img/202312041543561.png)


## 模型缓存和删除策略

API 使用一个有序缓存机制来存储最近使用的两个模型实例。如果新的模型请求到来，并且缓存已满，那么最不常用的模型实例将会被从缓存中删除以释放空间给新模型。

## 许可证
该项目遵循 MIT 许可证。
