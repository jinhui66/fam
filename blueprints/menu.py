from flask import Blueprint
from flask import Flask,request,render_template,session,redirect,url_for,jsonify
from sqlalchemy import text
from exts import db
import hashlib
import json
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

# 登录操作
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
        # 使用原生SQL查询数据
        sql = text('SELECT * FROM USER WHERE Uaccount = :account')
        get_user = db.session.execute(sql, {'account': account}).fetchone()
        print(2)
        if get_user is not None:
            session['user_id'] = get_user.Uid
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
        name = data.get('name')
        password = data.get('password')
        password2 = data.get('password2')
        captcha = data.get('captcha')

        if not account or not password or not password2 or not captcha or not name:
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
            with db.engine.connect() as connection:
            # 调用存储过程
                connection.execute(text("CALL COMPARE_CAPTCHA(:account, :captcha, @result);"), {'account':account, 'captcha':captcha})
                # 检查会话变量 @is_true
                captcha_model = connection.execute(text("SELECT @result;")).fetchone()
                print(captcha_model[0])

                if captcha_model[0] == 0:
                    return jsonify({'status': '', 'message': '验证码错误'})
                connection.commit()

            sql = text('insert into USER(Uaccount,Upassword,Uname) value(:account, :password, :name)')
            db.session.execute(sql, {'account': account, 'password':password, 'name':name})
            db.session.commit()
            return jsonify({'status': 'success', 'message': '注册成功'})


@bp.route('/forget',methods=['GET','POST'])
def forget():
    return render_template('forget.html')

@bp.route('/forget_action',methods=['GET','POST'])
def forget_action():
    if request.method == 'GET':
        pass
    else: # post
        data = request.get_json()
        account = data.get('account')
        password = data.get('password')
        password2 = data.get('password2')
        captcha = data.get('captcha')

        if not account or not password or not password2 or not captcha:
            return jsonify({'status':'', 'message':'请填写完整'})
        # 条件判断
        sql = text('select * from USER where Uaccount = :account')
        is_same = db.session.execute(sql, {'account': account}).fetchone()
        if not is_same:
            return jsonify({'status': '', 'message': '账号未注册'})
        elif password != password2:
            return jsonify({'status': '', 'message': '两次密码不一致'})
        else:
            # 调用存储过程
            with db.engine.connect() as connection:
            # 调用存储过程
                connection.execute(text("call COMPARE_CAPTCHA(:account, :captcha, @is_true);"), {'account':account, 'captcha':captcha})
                # 检查会话变量 @is_true
                captcha_model = connection.execute(text("SELECT @is_true;")).fetchone()
                # print(captcha_model[0])

                if captcha_model[0] == 0:
                    return jsonify({'status': '', 'message': '验证码错误'})

                connection.execute(text('update USER set Upassword = :password where Uaccount = :account'), {'password': password, 'account':account})

                connection.commit()


        session.clear()
        return jsonify({'status':'success', 'message':'修改成功'})
