import os
from flask import Flask, render_template, request

app = Flask(__name__)
# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 允许上传的文件类型，添加 'docx' 和 'doc'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/one_page')
def one_page():
    return render_template('one_page.html')

@app.route('/second_page')
def second_page():
    return render_template('second_page.html')

@app.route('/question_page')
def question_page():
    return render_template('question_page.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # 检查请求中是否包含文件
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # 检查用户是否选择了文件
        if file.filename == '':
            return 'No selected file'
        # 检查文件类型是否允许
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded successfully'
        else:
            return 'Invalid file type. Only PDF, DOCX and DOC files are allowed.'
    return render_template('upload.html')

if __name__ == '__main__':
    # 创建上传文件夹
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

# 用于Vercel的无服务器函数
def handler(event, context):
    return app(event, context)