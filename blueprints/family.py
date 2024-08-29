from flask import Blueprint
from flask import Flask,request,render_template,session,redirect,url_for,jsonify
from sqlalchemy import text
from exts import db
import hashlib
import json
import os
import time

bp = Blueprint('family',__name__,url_prefix="/")

@bp.route('/invite_family_action',methods=['GET','POST'])
def invite_family_action():
    if request.method == 'GET':
        pass
    else:
        data = request.get_json()

        account = data.get('account')
        exist = data.get('exist')
        user_id = session.get(user_id)

        with db.engine.connect() as connection:

            if exist:   #家庭已存在
                调用存储过程
                connection.execute('',{})
            else:       #新组建家庭
                connection.execute('',{})

            connection.commit()



# 增加公共收支部分
@bp.route('/insert_family_action',methods=['GET','POST'])
def insert_family_action():
    if request.method == 'GET':
        pass
    else:
        data = request.get_json()

        family_id = data.get('family_id')
        money = data.get('money')
        type_id = data.get('type_id')
        date = data.get('date')
        detail = data.get('detail')

        user_id = session.get('user_id')

        is_out = data.get('is_out')
        if is_out:
            sql = text('insert into FAMILY_OUT(Fid,Uid,FOmoney,Tid,FOdate,FOdetail) value(:family_id, :user_id, :money, :type_id, :date, :detail)')
            db.session.execute(sql,{'family_id':family_id, 'user_id':user_id, 'money':money, 'type_id':type_id, 'date':date, 'detail':detail})
            db.session.commit()
        else:
            sql = text('insert into FAMILY_IN(Fid,Uid,FImoney,Tid,FIdate,FIdetail) value(:family_id, :user_id, :money, :type_id, :date, :detail)')
            db.session.execute(sql,{'family_id':family_id, 'user_id':user_id, 'money':money, 'type_id':type_id, 'date':date, 'detail':detail})
            db.session.commit()
