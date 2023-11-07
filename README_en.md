# Large Language Models Code Generator API

## Introduction
This API provides an interface to various large language models for code generation. It's built using Flask and can dynamically load models as specified in the API requests.

## Prerequisites
- Python 3.x
- Flask
- Transformers library by Hugging Face
- PyTorch with CUDA support (if using a GPU)

Download the model files from Baidu Netdisk and place them in the specified directory before starting the API.

## Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/code-generator-api.git
cd code-generator-api
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the API with:
```bash
python app.py
```
Access the API at `http://0.0.0.0:8088`.

## Usage

To generate code, send a POST request to `/predict` with JSON data containing the `text`, `max_length`, and optionally, `model`:

```bash
curl -X POST http://0.0.0.0:8088/predict \
-H "Content-Type: application/json" \
-d '{"text": "Your prompt text", "max_length": 50, "model": "model-name"}'
```

You'll receive a JSON response with the prediction.

## License
This project is under the MIT License.

## Contact
Your Name - [@YourTwitter](https://twitter.com/YourTwitter)
