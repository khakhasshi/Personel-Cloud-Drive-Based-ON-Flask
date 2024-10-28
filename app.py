import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 上传文件存放的路径
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 主页面，展示上传和下载功能
@app.route('/', methods=['GET', 'POST'])
def index():
    # 获取搜索关键字
    search_query = request.args.get('search', '')

    # 获取所有上传的文件
    files = os.listdir(app.config['UPLOAD_FOLDER'])

    # 根据搜索查询过滤文件
    if search_query:
        files = [f for f in files if search_query.lower() in f.lower()]

    return render_template('index.html', files=files, search_query=search_query)

# 上传文件的处理逻辑
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))
    return redirect(request.url)

# 多文件上传的处理逻辑
@app.route('/upload_multiple', methods=['POST'])
def upload_multiple_files():
    if 'files' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist('files')
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return redirect(url_for('index'))

# 提供下载文件的功能
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=80)
