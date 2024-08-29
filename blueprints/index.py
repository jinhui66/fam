from flask import Blueprint
from flask import Flask,request,render_template,session,redirect,url_for,jsonify
from sqlalchemy import text
from exts import db
import hashlib
import json
import os
import time

bp = Blueprint('index',__name__,url_prefix="/")

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
        else:
            sql = text('insert into USER_OUT(Uid,UImoney,Tid,UIdate,UIdetail) value(:user_id, :money, :type_id, :date, :detail)')
            db.session.execute(sql,{'user_id':user_id, 'money':money, 'type_id':type_id, 'date':date, 'detail':detail})
            db.session.commit()


