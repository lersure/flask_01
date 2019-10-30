from exts import db
from myweb.ModelBase import ModelBase


class DataSets(ModelBase, db.Model):
    __tablename__ = 'datasets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configs = db.Column(db.Text)
    path = db.Column(db.String(100))
    flag = db.Column(db.Integer, default=0)

    def __str__(self):
        return self.path

    @property
    def serialize(self):
        return {
            "id": self.id,
            'configs': self.configs,
            'path': self.path,
            'flag': self.flag
        }
