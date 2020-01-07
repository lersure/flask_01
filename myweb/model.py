from exts import db
from myweb.ModelBase import ModelBase
import ast


# class DataSets(ModelBase, db.Model):
#     __tablename__ = 'datasets'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     configs = db.Column(db.Text)
#     path = db.Column(db.String(100))
#     flag = db.Column(db.Integer, default=0)
#
#     def __str__(self):
#         return self.path
#
#     @property
#     def serialize(self):
#         return {
#             "id": self.id,
#             'configs': self.configs,
#             'path': self.path,
#             'flag': self.flag
#         }

class DataSets(ModelBase, db.Model):
    __tablename__ = 'datasets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dataSets_id = db.Column(db.String(50), nullable=False)
    configs = db.relationship('Configs', backref='ds', lazy='dynamic')
    dsOrms = db.Column(db.Integer, default=1)

    @property
    def tojson(self):
        return {"id": self.dataSets_id, "configs": [x.config for x in self.configs], "dm": self.dsOrms}

    @property
    def configToJson(self):
        values = []
        for x in self.configs:
            temp_str = '{\"id\":%d,%s}' % (x.id, x.config)
            values.append(ast.literal_eval(temp_str))  # literal_eval函数可将字符串转换为json格式数据
        return values


class Configs(ModelBase, db.Model):
    def __init__(self, config):
        self.config = config

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    config = db.Column(db.Text)
    dataSets = db.Column(db.Integer, db.ForeignKey('datasets.id'))

    __tablename__ = 'configs'
