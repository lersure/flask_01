from flask import render_template, request, jsonify, Blueprint
import os, subprocess, time
import json
from exts import db
from myweb.model import DataSets

admin = Blueprint('admin', __name__)


@admin.route('/testPage', methods=['GET', 'POST'])
def testPage():
    return render_template('myweb/test.html')


# 添加数据集模型及配置到数据库
@admin.route('/saveConfigs', methods=['post'])
def saveConfigs():
    global dm
    ds = DataSets()
    try:
        filepath = request.form.get('filepath')
        configs = request.form.get('json')
        dm = request.form.get('dm')
        ds.path = filepath
        ds.configs = configs
        ds.flag = 1 if dm == 'dataSets' else 0
        ds.save()
        print("保存成功...")
        info = "保存成功！"
    except:
        info = "保存失败！"
    return render_template('myweb/index.html', name=dm, info=info)


# 查询保存的数据集及配置
@admin.route('/query/<name>', methods=['post', 'get'])
def queryAll(name=None):
    print("name=", name)
    if name is None or name == '':
        return None
    flag = 1 if name == 'dataSets' else 0
    data = DataSets.query.filter_by(flag=flag)
    print(data)
    return render_template('myweb/configsPage.html', data=data)


@admin.route('/queryData/<name>', methods=['post', 'get'])
def queryData(name=None):
    if name is None or name == '':
        return None
    flag = 1 if name == 'dataSets' else 0
    data = DataSets.query.filter_by(flag=flag)
    for d in data:
        i = d.path.rfind('/')
        d.path = d.path[i + 1:]
    return jsonify({"code": 0, "data": [i.serialize for i in data]})


upload_path = "file/upload"


@admin.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # 检查post请求是否有file这个属性
        if 'file' not in request.files:
            return jsonify({'code': -1, 'msg': '', 'data': 'No file part'})
        file = request.files['file']
        # 选择的文件名不能为空
        if file.filename == '':
            return jsonify({'code': -1, 'filename': '', 'msg': 'No selected file'})
        else:
            try:
                if file:  # 如果上传的文件存在
                    origin_file_name = file.filename
                    print('filename is %s' % origin_file_name)
                    filename = origin_file_name
                    timeTmp = str(int(time.time()))
                    upload_path = "%s/%s" % ("file/upload", timeTmp)
                    if os.path.exists(upload_path):  # 如果此路径存在了，则不用创建此路径了，否则创建
                        pass
                    else:
                        os.makedirs(upload_path)
                    file.save(os.path.join(upload_path, filename))  # 将上传的文件保存在此路径下
                    print('%s save successfully' % filename)
                    return jsonify(
                        {'code': 0, 'filepath': upload_path + '/' + filename, 'msg': 'upload successful'})  # 返回上传成功的响应值
                else:
                    print('%s not allowed' % file.filename)
                    return jsonify({'code': -1, 'filename': '', 'msg': 'File not allowed'})
            except Exception as e:
                print('upload file exception: %s' % e)
                return jsonify({'code': -1, 'filename': '', 'msg': 'Error occurred'})
    return jsonify({'code': -1, 'msg': '', 'data': 'Method not allowed'})


@admin.route('/getData', methods=['POST'])
def getdata():
    global allContents, f_read
    arg1 = request.args.get('quiz1')
    arg2 = request.args.get('quiz2')
    arg3 = request.args.get('quiz3')
    # f = os.popen("test.sh %s %s %s" % (arg1, arg2, arg3))
    f = subprocess.Popen("test.sh %s %s %s" % (arg1, arg2, arg3), shell=True, stdout=subprocess.PIPE)
    f.wait()
    # print("执行结束")
    f.stdout.close()
    try:
        f_read = open('data.txt', 'r', encoding='utf-8')
        allContents = f_read.read()
        print(allContents)
    except IOError:
        print("文件读取异常！")
    finally:
        f_read.close()
    return jsonify(allContents)
