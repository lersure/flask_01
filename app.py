from flask import Flask, render_template
from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager
from exts import db
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from myweb.views import admin
from myweb.model import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # mysql://root:root@127.0.0.1/
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS  # 关闭对模型修改的监控
db.init_app(app)

manage = Manager(app)
Migrate(app, db)
manage.add_command('db', MigrateCommand)
# app.config['SECRET_KEY'] = '123456'

# 模型 -> 迁移文件 ->表
# init migrate upgrade


if __name__ == '__main__':
    # app.debug = True  # 在run方法开始之前启动debug模式
    # app.run()  # 通过调用此方法来启动程序
    manage.run()
    app.run(debug=True)


@app.route('/', methods=['GET', 'POST'])  # 可以添加
def hello_world():
    return render_template("myweb/mainPage.html")


@app.route('/addDataSets/<name>', methods=['GET', 'POST'])  # 可以添加
def addDataSets(name=None):
    return render_template("myweb/index.html", name=name, info=None)


@app.route('/train', methods=['get', 'post'])
def train():
    return render_template("myweb/train.html")


# 自定义一个过滤器
def my_filter(e):
    s = str(e)
    index = s.rfind('/')  # 找出从右往左第一个/
    return s[index + 1:]


app.add_template_filter(my_filter, 'my_filter')
app.register_blueprint(admin)  # app.register_blueprint(admin)#

# 判断是否是以指定格式上传文件
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENTIONS

# {
#   "code": 0
#   ,"msg": ""
#   ,"data": {
#     "src": "http://cdn.layui.com/123.jpg"
#   }
# }
# 数据库的模型，需要继承自db.Model
# class Role(db.Model):
#     # 定义表名
#     __tablename__ = "roles"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(16), unique=True)
#
#
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(16), unique=True)
#     age = db.Column(db.Integer, nullable=True)
#     # 外键
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#
#     def __repr__(self):
#         return 'Author:%s' % self.name


#################################################################################
# 在路由中添加参数
# @app.route("/hello/<name>")
# def hello(name):
#     return "hello,%s" % name


# 在路由中可以添加int，float，path三种类型的参数
# @app.route('/blog/<int:id>')
# def show_blog(id):
#     return 'blog number %d' % id


# 1、如何返回一个网页（模板）
# 2、如何给模板填充数据
# @app.route('/index')
# def index():
#     # 比如需要传入网址
#     url_str = 'http://www.baidu.com'
#     my_list = [1, 3, 4, 6, 8]
#     my_dict = {
#         'name': "西电一名优秀的研究生",
#         'url': url_str
#     }
#     return render_template("myweb/index.html", url_str=url_str, my_list=my_list, my_dict=my_dict)


# app.secret_key = 'wqz'
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def hello_world():
#     if request.method == 'POST':
#         print("post传输。。。。")
#         username = request.form.get('username')
#         password = request.form.get('password')
#         password1 = request.form.get('password1')
#         # 校验参数的完整性
#         if not all([username, password, password1]):
#             flash(u'参数不完整')
#         # 校验密码
#         elif password != password1:
#             flash(u"密码不一致")
#         else:
#             print("username", username)
#             return 'success'
#     return render_template('myweb/login.html')

# class LoginForm(FlaskForm):
#     username = StringField(u'用户名', validators=[DataRequired()])
#     password = PasswordField('密码', validators=[DataRequired()])
#     password1 = PasswordField("确认密码", validators=[DataRequired(), EqualTo('', '密码填写不一致')])
#     submit = SubmitField('提交')

# @app.route('/form', methods=['GET', 'POST'])
# def login():
#     login_form = LoginForm()
#     if request.method == 'POST':
#         # 验证参数，WTF可以一句话实现所有的校验
#         if login_form.validate_on_submit():
#             return 'success'
#         else:
#             flash('参数有误！')
#     return render_template('myweb/index.html', login_form=login_form)
