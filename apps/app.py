from flask import Flask, flash, request, redirect, url_for, render_template, redirect, send_from_directory
from werkzeug.utils import secure_filename
import configparser, os
from broadcast import TG

# Loading Config From File
config=configparser.ConfigParser()
config.read('config.ini')

# To dict
CHAT_ID=dict(config.items('CHAT_ID'))

# Document Folder
FILE_DIR=config.get('UPLOAD','UPLOAD_FOLDER')

# Flask Config
app=Flask(__name__)
app.config['SECRET_KEY']=config['UPLOAD']['SECRET_KEY']
app.config['UPLOAD_FOLDER']=config['UPLOAD']['UPLOAD_FOLDER']
app.config['MAX_CONTENT_LENGTH']=16*1024*1024 # 16MB

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in config['UPLOAD']['ALLOWED_EXT']

@app.route('/', methods=['GET', 'POST'])
def index():
    # get option list
    chat_id = list(CHAT_ID.keys())
    if request.method == 'POST':
        # send one group
        if request.values['submit'] == 'Send':
            content=request.values['s_content']
            if content == '':
                flash('未輸入訊息...')
                return redirect('/')
            else:
                select = request.form.get('chat_id')
                TG(content, CHAT_ID.get(str(select))).send_message()
                return redirect('/')
        # send all group
        elif request.values['submit'] == 'Send_All':
            content=request.values['a_content']
            if content == '':
                flash('未輸入訊息...')
                return redirect('/')
            else:
                TG(content).send_message_all()
                return redirect('/')
        # send one group img
        elif request.values['submit'] == 'Send_File':
            file_name=request.values['file_name']
            if file_name == '':
                flash('未輸入訊息...')
                return redirect('/')
            else:
                try:
                    select = request.form.get('chat_id')
                    content=request.values['caption']
                    TG(id=CHAT_ID.get(str(select)), content=content, file='files/'+file_name).send_img_file()
                    return redirect('/')
                except:
                    flash('找不到檔案')
                    return redirect('/')
                # send one group img
        elif request.values['submit'] == 'Send_All_File':
            file_name=request.values['files_name']
            if file_name == '':
                flash('未輸入訊息...')
                return redirect('/')
            else:
                try:
                    content=request.values['captions']
                    TG(content=content, file='files/'+file_name).send_img_file_all()
                    return redirect('/')
                except:
                    flash('找不到檔案')
                    return redirect('/')
    # send frontend list options
    return render_template('index.html', chat_id = chat_id )

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file=request.files['file']
        # check file format or empty
        if allowed_file(file.filename) == False:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            else:
                flash('Format fail')
                return redirect(request.url)
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return render_template('upload_file.html')

@app.route('/file_list')
def file_list():
    files=os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('file_list.html', files=files)

@app.route('/file_list/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run( host='0.0.0.0', port=80, debug=True)