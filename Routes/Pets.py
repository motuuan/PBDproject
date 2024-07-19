from flask import Blueprint, request, redirect, url_for, session, render_template, flash, jsonify
import os
from werkzeug.utils import secure_filename
from Service.Pets import Pet_operation
from Service.Users import User_operation
pet = Blueprint('pet', __name__)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@pet.route('/pet_register', methods=['POST', 'GET'])
def pet_register():
    if request.method == 'POST':
        data = request.form
        Pname = data['Pname']
        Pgender = data['Pgender']
        Pvariety = data['Pvariety']
        Pbirth_year = data['Pbirth_year']
        Pbirth_month = data['Pbirth_month']
        Pbirth_day = data['Pbirth_day']
        Pbirth = f"{Pbirth_year}-{Pbirth_month}-{Pbirth_day}"
        Uid = session.get('Uid')  # 获取当前登录用户的 Uid

        if not Uid:
            flash('请先登录！', 'error')
            return redirect(url_for('user.login'))

        Pimage = None
        if 'Pimage' in request.files and request.files['Pimage'].filename != '':
            file = request.files['Pimage']
            if file and allowed_file(file.filename):
                file_data = file.read()  # 读取文件数据
                Pimage = file_data
            else:
                flash('上传的文件类型不被允许', 'error')
                return redirect(url_for('pet.pet_register'))

        u = User_operation()  # 创建用户操作实例
        Powner = u.get_user_uid(Uid)  # 根据 Uid 获取用户的唯一标识

        p = Pet_operation()
        result = p.register_pet(Pname, Powner, Pimage, Pgender, Pvariety, Pbirth)

        if result.json['code'] == 0:
            flash(result.json['message'], 'success')
            return redirect(url_for('user.dashboard', Pno=result.json['data']['Pno']))
        else:
            flash(result.json['message'], 'error')
            return redirect(url_for('pet.pet_register'))

    return render_template('addpets.html')





@pet.route('/view_pet', methods=['GET'])
def view_pet():
    powner = session.get('Uid')
    if not powner:
        flash('请先登录！', 'error')
        return redirect(url_for('user.login'))
    p = Pet_operation()
    pet_info = p.get_pet_info(powner)
    if pet_info.json['code'] == -1:
        message = pet_info.json['message']
        return redirect(url_for('user.login', message=message))
    print(pet_info.json['data'])
    return render_template('pets_info.html', pets=pet_info.json['data'])



@pet.route('/updatepets', methods=['POST', 'GET'])
def update_pet():
    powner = session.get('Uid')
    if not powner:
        flash('请先登录！', 'error')
        return redirect(url_for('user.login'))
    p = Pet_operation()
    pet_info = p.get_pet_info(powner)
    if request.method == 'POST':
        data = request.form
        Pname = data['Pname']
        Pgender = data['Pgender']
        Pvariety = data['Pvariety']
        Pbrith = data['Pbrith']
        Pimage = None

        if 'Pimage' in request.files and request.files['Pimage'].filename != '' and allowed_file(request.files['Pimage'].filename):
            file = request.files['Pimage']
            filename = secure_filename(file.filename)
            upload_path = os.path.join('static/uploads', filename)
            file.save(upload_path)
            Pimage = upload_path

        result = p.update_pet(Pname, Pimage, Pgender, Pvariety, Pbrith)

        if result.json['code'] == 0:
            flash(result.json['message'], 'success')
            return redirect(url_for('pet.view_pet'))
        else:
            flash(result.json['message'], 'error')
            return redirect(url_for('pet.update_pet'))

    if not pet_info:
        flash('宠物不存在', 'error')
        return redirect(url_for('user.dashboard'))

    return render_template('update_pet.html', pet=pet_info)


@pet.route('/deletepet', methods=['POST', 'GET'])
def delete_pet(Pno):
    p = Pet_operation()
    result = p.delete_pet(Pno)
    if result.json['code'] == 0:
        flash(result.json['message'], 'success')
    else:
        flash(result.json['message'], 'error')
    return redirect(url_for('user.dashboard'))