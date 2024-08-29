from flask import Blueprint
from flask import Flask,request,render_template,session,redirect,url_for,jsonify
from sqlalchemy import text
from exts import db
import hashlib
import json
import os
import time

bp = Blueprint('user',__name__,url_prefix="/")

@bp.route('/users', methods=['GET'])
def get_users():
    users = [
        {"时间": 1, "收入/支出": "收入", "类别": "生活", "子类别": "纸巾", "金额": 25, "备注": "666"},
        {"id": 2, "name": "李四", "age": 30},
        {"id": 3, "name": "王五", "age": 28}
        ]

    return jsonify(users)

@bp.route('/insert_user_action',methods=['GET','POST'])
def insert_user_action():
    if request.method == 'GET':
        pass
    else:
        data = request.get_json()

        money = data.get('money')
        type_id = data.get('type_id')
        date = data.get('date')
        detail = data.get('detail')

        user_id = session.get('user_id')

        is_out = data.get('is_out')
        if is_out:
            sql = text('insert into USER_OUT(Uid,UOmoney,Tid,UOdate,UOdetail) value(:user_id, :money, :type_id, :date, :detail)')
            db.session.execute(sql,{'user_id':user_id, 'money':money, 'type_id':type_id, 'date':date, 'detail':detail})
            db.session.commit()
            return
        else:
            sql = text('insert into USER_OUT(Uid,UImoney,Tid,UIdate,UIdetail) value(:user_id, :money, :type_id, :date, :detail)')
            db.session.execute(sql,{'user_id':user_id, 'money':money, 'type_id':type_id, 'date':date, 'detail':detail})
            db.session.commit()
            return


