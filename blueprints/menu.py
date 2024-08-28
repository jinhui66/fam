from flask import Blueprint
from flask import Flask,request,render_template,session,redirect,url_for,jsonify
from sqlalchemy import text
from exts import db
import hashlib
import json
from models.forms import RegisterForm,LoginForm,ForgotForm
# from models.table import User, Admin
import os
import time

bp = Blueprint('menu',__name__,url_prefix="/")

@bp.route('/',methods=['GET','POST'])
def menu():
    print(session.get('user_id'))
    if not session.get('user_id'):
        return redirect('login')
    else:
        return render_template('index.html')

@bp.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')

@bp.route('/login_action',methods=['GET','POST'])
def login_action():

    if request.method == 'GET':
        pass
    else:
        data = request.get_json()
        account = data.get('account')
        password = data.get('password')
        if not account or not password:
            return jsonify({'status':'', 'message':'请填写完整'})
        # print(type(account),"ddddddd")
        # print(account,password,1221212)
        # get_user = User.query.filter_by(email=email).first()
        # 使用原生SQL查询数据
        sql = text('SELECT * FROM USER WHERE Uaccount = :account')
        get_user = db.session.execute(sql, {'account': account}).fetchone()
        print(2)
        if get_user is not None:
            session['user_id'] = get_user.Uid
            # password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            print(password)
            if(get_user.Upassword == password):
                print('success')
                return jsonify({'status':'success', 'message':''})
        return jsonify({'status':'', 'message':'账号或密码错误'})


@bp.route('/out',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect('/login')

@bp.route('/register',methods=['GET','POST'])
def register():
    return render_template('register.html')

@bp.route('/register_action',methods=['GET','POST'])
def register_action():
    if request.method == 'GET':
        pass
    else:
        data = request.get_json()
        account = data.get('account')
        password = data.get('password')
        password2 = data.get('password2')
        captcha = data.get('captcha')

        if not account or not password or not password2:
            return jsonify({'status':'', 'message':'请填写完整'})
        # 条件判断
        sql = text('select * from USER where Uaccount = :account')
        is_same = db.session.execute(sql, {'account': account}).fetchone()
        if is_same:
            return jsonify({'status': '', 'message': '账号已被注册'})
        elif password != password2:
            return jsonify({'status': '', 'message': '两次密码不一致'})
        else:
            # 调用存储过程

            sql = text('insert into USER(Uaccount,Upassword) value(:account, :password)')
            db.session.execute(sql, {'account': account, 'password':password})
            db.session.commit()
            return jsonify({'status': 'success', 'message': '注册成功'})


@bp.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    return render_template('menu/forgot_password.html')

@bp.route('/forgot_password_action',methods=['GET','POST'])
def forgot_password_action():
    if request.method == 'GET':
        pass
    else: # post
        form = ForgotForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            sql_user = text('SELECT * FROM User WHERE email = :email')
            get_user = db.session.execute(sql_user, {'email': email}).fetchone()

            sql_admin = text('SELECT * FROM Admin WHERE email = :email')
            get_admin = db.session.execute(sql_admin, {'email': email}).fetchone()

            if get_user:
                # get_user = User.query.filter_by(email=email).first()
                # get_user.user_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                sql = text('update User set user_password = :user_password where email = :email')
                db.session.execute(sql, {'user_password':hashlib.sha256(password.encode('utf-8')).hexdigest(), 'email': email})
                db.session.commit()
            elif get_admin:
                # get_user = Admin.query.filter_by(email=email).first()
                # get_user.admin_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                sql = text('update Admin set admin_password = :admin_password where email = :email')
                db.session.execute(sql, {'admin_password':hashlib.sha256(password.encode('utf-8')).hexdigest(), 'email': email})
                db.session.commit()

            session.clear()
            return jsonify({'status':'success', 'message':''})
        else:
            for field, errors in form.errors.items():
                # errors 是一个列表，包含该字段的所有错误消息
                if errors:
                #     # 打印第一个错误消息
                    error = errors[0]
                    print(f"{field} 的第一个错误是: {errors[0]}")
                    break
                print(error)
            return jsonify({'status': '','message':error})
