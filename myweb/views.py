from flask import render_template, request, jsonify, Blueprint, redirect, url_for
import os, subprocess, time
from exts import db
import json
from myweb.model import DataSets, Configs
from myweb import util

admin = Blueprint('admin', __name__)


@admin.route('/testPage', methods=['GET', 'POST'])
def testPage():
    return render_template('myweb/test.html')


# 添加数据集模型及配置到数据库
@admin.route('/saveConfigs', methods=['post'])
def saveConfigs():
    global dm
    try:
        dm = request.form.get('dm')
        ds = DataSets()
        c1 = Configs("'wqz':123,'qaz':'qqq'")
        c2 = Configs("'aaa':345,'zzz':'5655'")
        ds.configs = [c1, c2]
        ds.dsOrms = 1
        ds.dataSets_id = '654321'
        ds.save()
        info = "保存成功！"
        print("保存成功！")
    except:
        info = "保存失败！"
        print("保存失败！")
    return render_template('myweb/index.html', name=dm, info=info)
    # try:
    #     filepath = request.form.get('filepath')
    #     configs = request.form.get('json')
    #     dm = request.form.get('dm')
    #     ds.path = filepath
    #     ds.configs = configs
    #     ds.flag = 1 if dm == 'dataSets' else 0
    #     ds.save()
    #     print("保存成功...")
    #     info = "保存成功！"
    # except:
    #     info = "保存失败！"
    # return render_template('myweb/index.html', name=dm, info=info)


# 查询保存的数据集及配置
@admin.route('/query/<name>', methods=['post', 'get'])
def queryAll(name=None):
    if name is None or name == '':
        return None
    dsOrms = 1 if name == 'dataSets' else 0
    data = DataSets.query.filter_by(dsOrms=dsOrms)
    # for x in data:
    #     print(x.tojson)
    print(util.querysetToJson(data))

    try:
        jsonValue = {
            "code": 0,
            "msg": "",
            "count": 10,
            "data": util.querysetToJson(data)

        }
    except Exception as e:
        jsonValue = {
            "code": -1,
            "msg": e,
            "count": 0,
            "data": ""
        }
    return jsonValue


# 将queryset数据转换成json格式


@admin.route('/queryData/<name>', methods=['post', 'get'])
def queryData(name=None):
    if name is None or name == '':
        return None
    dsOrms = 1 if name == 'dataSets' else 0
    data = DataSets.query.filter_by(dsOrms=dsOrms)
    for d in data:
        i = d.dataSets_id.rfind('/')
        d.dataSets_id = d.dataSets_id[i + 1:]
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
                        {'code': 0, 'filename': timeTmp, 'msg': 'upload successful'})  # 返回上传成功的响应值
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


@admin.route('/train_1', methods=['GET', 'POST'])
def train1():
    return render_template('myweb/train_1.html')


@admin.route('/del', methods=['GET', 'POST'])
def delConfs():
    id = request.args.get("id")
    dsOrms = request.args.get("dsOrms")
    ds = 'dataSets' if dsOrms == '1' else 'models'
    c = Configs.query.get(id)
    c.delete()
    return redirect(url_for('admin.queryAll', name=ds))


@admin.route('/test', methods=['GET', 'POST'])
def testCommand():
    # 这里接收参数
    f = subprocess.Popen("test.sh %s %s %s" % (arg1, arg2, arg3), shell=True, stdout=subprocess.PIPE)
    f.wait()
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

    # 进入编辑页面并返回数据

# @admin.route("/edit<p>/<id>", methods=['POST', 'GET'])
# def editPage(p=None, id=None):
#     # 如果是编辑数据集配置页面
#
#     dsOrMs = p
#     configId = id
