# run.py
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # TODO: 调用你的LM模型处理图像并生成 metadata
    # 示例占位代码:
    print(f"Received file: {filepath}")

    # 返回处理中的页面或重定向到结果展示页
    return 'Processing... (This will be replaced with loading and preview)'

if __name__ == '__main__':
    app.run(debug=True)
