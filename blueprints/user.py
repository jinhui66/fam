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
    sql = text('select * from USER_IN;')
    result = db.session.execute(sql).fetchall()
    list = []
    for row in result:
        sql = text('select T.Tname, C.Cname from TYPE T join CATEGORY C on C.Cid = T.Cid where T.Tid = :Tid')
        zhonglei = db.session.execute(sql,{'Tid':row[3]}).fetchone()
        type = zhonglei[0]
        category = zhonglei[1]

        list.append({
            "time": row[4],
            "is_out": row[0],
            "category": category,
            "type": type,# type
            "money": row[2],
            "detail": row[5]
        })
    print(list)

    return jsonify(list)

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


