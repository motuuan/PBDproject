from flask import Blueprint, request, redirect, url_for, session, render_template, flash, jsonify
import os
from werkzeug.utils import secure_filename
from Service.Users import User_operation

user = Blueprint('user', __name__)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@user.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.form
        Uid = data['Uid']
        Upassword = data['Upassword']
        Uname = data['Uname']
        Ugender = data['Ugender']
        Uphone = data['Uphone']
        confirmpassword = data['confirmpassword']

        if Upassword != confirmpassword:
            flash('确认密码与密码不一致，请重新输入!', 'error')
            return redirect(url_for('user.register'))

        Uheadshot = None
        if Uheadshot is None:
            with open('static/uploadusers/initialhead.png', 'rb') as f:
                Uheadshot = f.read()
        if 'Uheadshot' in request.files and request.files['Uheadshot'].filename != '':
            file = request.files['Uheadshot']
            if file and allowed_file(file.filename):
                file_data = file.read()  # 读取文件数据
                Uheadshot = file_data
            else:
                flash('上传的文件类型不被允许', 'error')
                return redirect(url_for('user.register'))

        u = User_operation()
        result = u.register(Uid, Uname, Uheadshot, Ugender, Uphone, Upassword)

        print(f"Debug: Register result: {result.json}")

        if result.json['code'] == 0:
            flash(result.json['message'], 'success')
            return redirect(url_for('user.login'))
        else:
            flash(result.json['message'], 'error')
            return redirect(url_for('user.register'))

    return render_template('register.html')


@user.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.form
        Uid = data['Uid']
        Upassword = data['Upassword']
        u = User_operation()
        result = u.login(Uid, Upassword)
        if result.json['code'] == 0:
            session['Uid'] = Uid
            return redirect(url_for('user.dashboard'))
        else:
            flash(result.json['message'], 'error')
            return redirect(url_for('user.login'))
    return render_template('login.html')


@user.route('/forgot_password', methods=['GET'])
def forgot_password():
    Uid = request.args.get('Uid')
    if not Uid:
        return jsonify({'code': -1, 'message': '用户名不能为空'})

    u = User_operation()
    result = u.forget_password(Uid)
    return result


@user.route('/update_info', methods=['POST', 'GET'])
def update_info():
    if request.method == 'POST':
        data = request.form
        Upassword = data['Upassword']
        Uname = data['Uname']
        Ugender = data['Ugender']
        Uphone = data['Uphone']

        Uid = session.get('Uid')

        default_avatar_path = 'static/uploadusers/initialhead.png'

        if 'Uheadshot' in request.files and request.files['Uheadshot'].filename != '' :
            file = request.files['Uheadshot']
            if file and allowed_file(file.filename):
                file_data = file.read()  # 读取文件数据
                Uheadshot = file_data
            else:
                flash('上传的文件类型不被允许', 'error')
                return redirect(url_for('user.update_info'))


        if not Uid:
            flash('请先登录！', 'error')
            return redirect(url_for('user.login'))

        u = User_operation()
        result = u.update_info(Uid, Uname, Uheadshot, Ugender, Uphone, Upassword)

        print(f"Debug: Update info result: {result.json}")  # 打印调试信息

        if result.json['code'] == 0:
            message = result.json['message']
            return redirect(url_for('user.dashboard', message=message))
        else:
            message = result.json['message']
            return redirect(url_for('user.update_info', message=message))

    Uid = session.get('Uid')
    if not Uid:
        flash('请先登录！', 'error')
        return redirect(url_for('user.login'))

    u = User_operation()
    user_info = u.get_user_info(Uid)
    return render_template('usercenter.html', user=user_info)


@user.route('/delete_account', methods=['POST', 'GET'])
def delete_account():
    if request.method == 'POST':
        Uid = session.get('Uid')
        if not Uid:
            flash('请先登录！', 'error')
            return redirect(url_for('user.login'))

        u = User_operation()
        result = u.delete_user(Uid)

        print(f"Debug: Delete account result: {result.json}")  # 打印调试信息

        if result.json['code'] == 0:
            session.pop('Uid', None)
            message = result.json['message']
            return redirect(url_for('user.login', message=message))
        else:
            message = result.json['message']
            return redirect(url_for('user.login', message=message))

    return render_template('usercenter.html')


@user.route('/logout')
def logout():
    session.pop('Uid', None)
    flash('您已成功退出登录！', 'success')
    return redirect(url_for('user.login'))


@user.route('/dashboard')
def dashboard():
    Uid = session.get('Uid')
    u = User_operation()
    user_info = u.get_user_info(Uid)

    return render_template('behavior.html', user=user_info)