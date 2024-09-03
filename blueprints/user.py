from flask import Blueprint
from flask import Flask,request,render_template,session,redirect,url_for,jsonify
from sqlalchemy import text
from exts import db
import hashlib
import json
import os
import time
import plotly.graph_objects as go
from datetime import datetime


bp = Blueprint('user',__name__,url_prefix="/")

@bp.route('/users', methods=['GET'])
def get_users():
    user_id = session.get('user_id')
    sql = text('select * from USER_INOUT where Uid = :user_id ORDER BY UIid DESC;')
    result = db.session.execute(sql,{'user_id':user_id}).fetchall()
    list = []
    for row in result:
        sql = text('select T.Tname, C.Cname from TYPE T join CATEGORY C on C.Cid = T.Cid where T.Tid = :Tid')
        zhonglei = db.session.execute(sql,{'Tid':row[3]}).fetchone()
        type = zhonglei[0]
        category = zhonglei[1]

        if row[6] == 0:
            is_in = '支出'
        else:
            is_in = '收入'

        python_datetime = datetime.strptime(str(row[4]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')


        list.append({
            "id": row[0],
            "time": python_datetime,
            "is_in": is_in,
            "category": category,
            "type": type,# type
            "money": row[2],
            "detail": row[5]
        })
    # print(list)

    response = {
        "code": 0,  # 成功状态码
        "msg": "",  # 消息字段
        "count": len(list),  # 数据总数
        "data": list  # 数据列表
    }

    return jsonify(response)

@bp.route('/users_in', methods=['GET'])
def users_in():
    user_id = session.get('user_id')
    sql = text('select * from USER_INOUT where Uid = :user_id and UIisin = 1 ORDER BY UIid DESC;')
    result = db.session.execute(sql,{'user_id':user_id}).fetchall()
    list = []
    for row in result:
        sql = text('select T.Tname, C.Cname from TYPE T join CATEGORY C on C.Cid = T.Cid where T.Tid = :Tid')
        zhonglei = db.session.execute(sql,{'Tid':row[3]}).fetchone()
        type = zhonglei[0]
        category = zhonglei[1]

        if row[6] == 0:
            is_in = '支出'
        else:
            is_in = '收入'

        python_datetime = datetime.strptime(str(row[4]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

        list.append({
            "id": row[0],
            "time": python_datetime,
            "is_in": is_in,
            "category": category,
            "type": type,# type
            "money": row[2],
            "detail": row[5]
        })
    # print(list)

    response = {
        "code": 0,  # 成功状态码
        "msg": "",  # 消息字段
        "count": len(list),  # 数据总数
        "data": list  # 数据列表
    }

    return jsonify(response)



@bp.route('/users_out', methods=['GET'])
def users_out():
    user_id = session.get('user_id')
    sql = text('select * from USER_INOUT where Uid = :user_id and UIisin = 0 ORDER BY UIid DESC;')
    result = db.session.execute(sql,{'user_id':user_id}).fetchall()
    list = []
    for row in result:
        sql = text('select T.Tname, C.Cname from TYPE T join CATEGORY C on C.Cid = T.Cid where T.Tid = :Tid')
        zhonglei = db.session.execute(sql,{'Tid':row[3]}).fetchone()
        type = zhonglei[0]
        category = zhonglei[1]

        if row[6] == 0:
            is_in = '支出'
        else:
            is_in = '收入'

        python_datetime = datetime.strptime(str(row[4]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

        list.append({
            "id": row[0],
            "time": python_datetime,
            "is_in": is_in,
            "category": category,
            "type": type,# type
            "money": row[2],
            "detail": row[5]
        })
    # print(list)
    # print('user_out')
    response = {
        "code": 0,  # 成功状态码
        "msg": "",  # 消息字段
        "count": len(list),  # 数据总数
        "data": list  # 数据列表
    }

    return jsonify(response)


@bp.route('/select_category',methods=['POST','get'])
def select_category():
    cata = [{
            'id': 'all',
            'title': '全部'}
            ]

    sql = text('select * from CATEGORY')
    category = db.session.execute(sql).fetchall()
    # print(category)
    for row in category:
        # print(row)
        cata.append({
            'id': row[0],
            'title': row[1]
        })

    return jsonify(cata)

@bp.route('/select_type/<output>',methods=['POST','get'])
def select_type(output):
    if output == 'all':
        cata = [{
            'id': 'allall',
            'title': '全部'}
            ]
    else:
        cata = [{
            'id': 'all',
            'title': '全部'}
            ]
    # print('output',output)
    sql = text('select * from TYPE T where T.Cid = :output')
    category = db.session.execute(sql,{'output':output}).fetchall()
    # print(category)
    for row in category:
        # print(row)
        cata.append({
            'id': row[0],
            'title': row[1]
        })

    return jsonify(cata)

@bp.route('/change',methods=['POST','get'])
def change():
    data = request.get_json()
    money = data.get('money')
    detail = data.get('detail')
    id = data.get('id')

    sql = text('update USER_INOUT set UImoney=:money,UIdetail=:detail where UIid = :id')
    db.session.execute(sql,{'money':money,'detail':detail,'id':id})
    db.session.commit()
    return jsonify({'status':'success'})

# 按照类别进行筛选
@bp.route('/type/<output>',methods=['POST','get'])
def type(output):
    user_id = session.get('user_id')
    sql = text('select * from USER_INOUT UI join TYPE T on T.Tid = UI.Tid where :output = T.Tid and UI.Uid = :user_id ORDER BY UIid DESC;')
    result = db.session.execute(sql,{'output':output,'user_id':user_id}).fetchall()
    list = []
    for row in result:
        sql = text('select T.Tname, C.Cname from TYPE T join CATEGORY C on C.Cid = T.Cid where T.Tid = :Tid')
        zhonglei = db.session.execute(sql,{'Tid':row[3]}).fetchone()
        type = zhonglei[0]
        category = zhonglei[1]
        if row[6] == 0:
            is_in = '支出'
        else:
            is_in = '收入'

        python_datetime = datetime.strptime(str(row[4]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

        list.append({
            "id": row[0],
            "time": python_datetime,
            "is_in": is_in,
            "category": category,
            "type": type,# type
            "money": row[2],
            "detail": row[5]
        })
    response = {
        "code": 0,  # 成功状态码
        "msg": "",  # 消息字段
        "count": len(list),  # 数据总数
        "data": list  # 数据列表
    }


    return jsonify(response)

@bp.route('/type_in/<output>',methods=['POST','get'])
def type_in(output):
        # print(output)
    user_id = session.get('user_id')
    sql = text('select * from USER_INOUT UI join TYPE T on T.Tid = UI.Tid where :output = T.Tid and UI.Uid = :user_id and UI.UIisin = 1 ORDER BY UIid DESC;')
    result = db.session.execute(sql,{'output':output,'user_id':user_id}).fetchall()
    list = []
    for row in result:
        sql = text('select T.Tname, C.Cname from TYPE T join CATEGORY C on C.Cid = T.Cid where T.Tid = :Tid')
        zhonglei = db.session.execute(sql,{'Tid':row[3]}).fetchone()
        type = zhonglei[0]
        category = zhonglei[1]

        if row[6] == 0:
            is_in = '支出'
        else:
            is_in = '收入'

        python_datetime = datetime.strptime(str(row[4]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

        list.append({
            "id": row[0],
            "time": python_datetime,
            "is_in": is_in,
            "category": category,
            "type": type,# type
            "money": row[2],
            "detail": row[5]
        })
    # print(list)

    response = {
        "code": 0,  # 成功状态码
        "msg": "",  # 消息字段
        "count": len(list),  # 数据总数
        "data": list  # 数据列表
    }


    return jsonify(response)

@bp.route('/type_out/<output>',methods=['POST','get'])
def type_out(output):
        # print(output)
    user_id = session.get('user_id')
    sql = text('select * from USER_INOUT UI join TYPE T on T.Tid = UI.Tid where :output = T.Tid and UI.Uid = :user_id and UI.UIisin = 0 ORDER BY UIid DESC;')
    result = db.session.execute(sql,{'output':output,'user_id':user_id}).fetchall()
    list = []
    for row in result:
        sql = text('select T.Tname, C.Cname from TYPE T join CATEGORY C on C.Cid = T.Cid where T.Tid = :Tid')
        zhonglei = db.session.execute(sql,{'Tid':row[3]}).fetchone()
        type = zhonglei[0]
        category = zhonglei[1]

        if row[6] == 0:
            is_in = '支出'
        else:
            is_in = '收入'

        python_datetime = datetime.strptime(str(row[4]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

        list.append({
            "id": row[0],
            "time": python_datetime,
            "is_in": is_in,
            "category": category,
            "type": type,# type
            "money": row[2],
            "detail": row[5]
        })
    # print(list)

    response = {
        "code": 0,  # 成功状态码
        "msg": "",  # 消息字段
        "count": len(list),  # 数据总数
        "data": list  # 数据列表
    }


    return jsonify(response)

@bp.route('/category/<output>',methods=['POST','get'])
def category(output):
    # print(output)
    user_id = session.get('user_id')
    sql = text('select * from USER_INOUT UI join TYPE T on T.Tid = UI.Tid join CATEGORY C on C.Cid = T.Cid where :output = C.Cid and UI.Uid = :user_id ORDER BY UIid DESC;')
    result = db.session.execute(sql,{'output':output,'user_id':user_id}).fetchall()
    list = []
    for row in result:
        sql = text('select T.Tname, C.Cname from TYPE T join CATEGORY C on C.Cid = T.Cid where T.Tid = :Tid')
        zhonglei = db.session.execute(sql,{'Tid':row[3]}).fetchone()
        type = zhonglei[0]
        category = zhonglei[1]

        if row[6] == 0:
            is_in = '支出'
        else:
            is_in = '收入'

        python_datetime = datetime.strptime(str(row[4]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

        list.append({
            "id": row[0],
            "time": python_datetime,
            "is_in": is_in,
            "category": category,
            "type": type,# type
            "money": row[2],
            "detail": row[5]
        })
    # print(list)

    response = {
        "code": 0,  # 成功状态码
        "msg": "",  # 消息字段
        "count": len(list),  # 数据总数
        "data": list  # 数据列表
    }

    return jsonify(response)

@bp.route('/category_in/<output>',methods=['POST','get'])
def category_in(output):
    # print(output)
    user_id = session.get('user_id')
    sql = text('select * from USER_INOUT UI join TYPE T on T.Tid = UI.Tid join CATEGORY C on C.Cid = T.Cid where :output = C.Cid and UI.Uid = :user_id and UIisin = 1 ORDER BY UIid DESC;')
    result = db.session.execute(sql,{'output':output,'user_id':user_id}).fetchall()
    list = []
    for row in result:
        sql = text('select T.Tname, C.Cname from TYPE T join CATEGORY C on C.Cid = T.Cid where T.Tid = :Tid')
        zhonglei = db.session.execute(sql,{'Tid':row[3]}).fetchone()
        type = zhonglei[0]
        category = zhonglei[1]

        if row[6] == 0:
            is_in = '支出'
        else:
            is_in = '收入'

        python_datetime = datetime.strptime(str(row[4]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

        list.append({
            "id": row[0],
            "time": python_datetime,
            "is_in": is_in,
            "category": category,
            "type": type,# type
            "money": row[2],
            "detail": row[5]
        })
    # print(list)

    response = {
        "code": 0,  # 成功状态码
        "msg": "",  # 消息字段
        "count": len(list),  # 数据总数
        "data": list  # 数据列表
    }

    return jsonify(response)

@bp.route('/category_out/<output>',methods=['POST','get'])
def category_out(output):

    user_id = session.get('user_id')
    sql = text('select * from USER_INOUT UI join TYPE T on T.Tid = UI.Tid join CATEGORY C on C.Cid = T.Cid where :output = C.Cid and UI.Uid = :user_id and UIisin = 0 ORDER BY UIid DESC;')
    result = db.session.execute(sql,{'output':output,'user_id':user_id}).fetchall()
    list = []
    for row in result:
        sql = text('select T.Tname, C.Cname from TYPE T join CATEGORY C on C.Cid = T.Cid where T.Tid = :Tid')
        zhonglei = db.session.execute(sql,{'Tid':row[3]}).fetchone()
        type = zhonglei[0]
        category = zhonglei[1]

        if row[6] == 0:
            is_in = '支出'
        else:
            is_in = '收入'

        python_datetime = datetime.strptime(str(row[4]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

        list.append({
            "id": row[0],
            "time": python_datetime,
            "is_in": is_in,
            "category": category,
            "type": type,# type
            "money": row[2],
            "detail": row[5]
        })
    # print(list)

    response = {
        "code": 0,  # 成功状态码
        "msg": "",  # 消息字段
        "count": len(list),  # 数据总数
        "data": list  # 数据列表
    }

    return jsonify(response)

@bp.route('/add_data',methods=['POST','get'])
def index123B():
    return render_template("inp.html")


@bp.route('/receive',methods=['POST','get'])
def receive_add_data():
    data = request.get_json()
    is_shouru = data.get('is_in')
    if is_shouru == '收入':
        is_in = 1
    else:
        is_in = 0
    # category = data.get('category')
    type = data.get('type')
    money = data.get('money')
    detail = data.get('detail')
    dateTime = data.get('dateTime')
    user_id = session.get('user_id')

    # print(dateTime)
    # print('receive')
    sql = text('insert into USER_INOUT(Uid,UImoney,Tid,UIdetail,UIisin,UIdate) value(:user_id,:money,:type,:detail,:is_in,:dateTime)')
    db.session.execute(sql,{'user_id':user_id,'money':money,'type':type,'detail':detail,'is_in':is_in,'dateTime':dateTime})
    db.session.commit()
    # print('11')
    return jsonify({'status':'success'})

@bp.route('/delete/<output>',methods=['POST','get'])
def index123Baa111(output):
    # print('删除ID:',output)
    sql = text('delete from USER_INOUT where UIid = :output')
    db.session.execute(sql,{'output':output})
    db.session.commit()
    return '数据删除成功', 200
