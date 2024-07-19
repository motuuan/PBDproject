from Model.Users import Users
from flask import jsonify
from PBD_config import db_init as db

class User_operation():
    def __init__(self):
        super().__init__()

    def login(self, Uid, Upassword):
        u = Users.query.filter_by(Uid=Uid).first()
        if u is None:
            return jsonify({'code': -1, 'message': '用户不存在', 'data': {}})

        u_dict = u.to_dict()
        if u_dict['Upassword'] != Upassword:
            return jsonify({'code': -2, 'message': '密码错误', 'data': {}})

        return jsonify({'code': 0, 'message': '登录成功', 'data': u_dict})

    def register(self, Uid, Uname, Uheadshot, Ugender, Uphone, Upassword):
        existing_id = Users.query.filter_by(Uid=Uid).first()
        existing_phone = Users.query.filter_by(Uphone=Uphone).first()

        if existing_id:
            print(f"Debug: Existing user ID: {existing_id}")
            return jsonify({'code': -1, 'message': '账号已存在！', 'data': {}})

        if existing_phone:
            print(f"Debug: Existing phone: {existing_phone}")
            return jsonify({'code': -2, 'message': '手机号已被使用', 'data': {}})

        new_user = Users(
            Uid=Uid,
            Uname=Uname,
            Uheadshot=Uheadshot,
            Ugender=Ugender,
            Uphone=Uphone,
            Upassword=Upassword,
        )
        db.session.add(new_user)
        db.session.commit()

        print(f"Debug: New user registered: {new_user.to_dict()}")

        return jsonify({'code': 0, 'message': '注册成功！', 'data': new_user.to_dict()})

    def update_info(self, Uid, Uname, Uheadshot, Ugender, Uphone, Upassword):
        user = Users.query.filter_by(Uid=Uid).first()
        if not user:
            return jsonify({'code': -1, 'message': '用户不存在！', 'data': {}})
        user.Uname = Uname
        if Uheadshot:
            user.Uheadshot = Uheadshot
        user.Ugender = Ugender
        user.Uphone = Uphone
        if Upassword:
            user.Upassword = Upassword
        db.session.commit()

        return jsonify({'code': 0, 'message': '信息更新成功！', 'data': user.to_dict()})

    def delete_user(self, Uid):
        user = Users.query.filter_by(Uid=Uid).first()
        if not user:
            return jsonify({'code': -1, 'message': '用户不存在！', 'data': {}})
        db.session.delete(user)
        db.session.commit()
        return jsonify({'code': 0, 'message': '用户账号删除成功！', 'data': {}})

    def get_user_info(self, Uid):
        user = Users.query.filter_by(Uid=Uid).first()
        if not user:
            return None
        return user.to_dict()

    def get_user_uid(self, Uid):
        user = Users.query.filter_by(Uid=Uid).first()
        if not user:
            return None
        return user.Uid