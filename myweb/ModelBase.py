from exts import db


class ModelBase:
    # 添加一条数据
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()

    # 添加多条数据
    @staticmethod  # 将查询所有方法设置成静态较为方便
    def saveAll(*args):
        try:
            db.session.add_all(args)
            db.session.commit()
        except:
            db.session.rollback()

    # 删除数据
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
