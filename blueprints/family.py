from flask import Blueprint
from flask import Flask,request,render_template,session,redirect,url_for,jsonify
from sqlalchemy import text
from exts import db
import hashlib
import json
import os
import time

bp = Blueprint('family',__name__,url_prefix="/")


@bp.route('/delete_total/<output>',methods=['POST','get'])
def delete_total(output):
    print('删除ID:',output)
    sql = text('delete from FAMILY_INOUT where FIid = :output')
    db.session.execute(sql,{'output':output})
    db.session.commit()
    return '数据删除成功', 200


@bp.route('/change_total',methods=['POST','get'])
def change_total():
    data = request.get_json()
    money = data.get('money')
    detail = data.get('detail')
    id = data.get('id')

    sql = text('update FAMILY_INOUT set FImoney=:money, FIdetail=:detail where FIid = :id')
    db.session.execute(sql,{'money':money,'detail':detail,'id':id})
    db.session.commit()
    return jsonify({'status':'success'})


@bp.route('/change_invite_no',methods=['POST','get'])
def change_invite_no():
    data = request.get_json()
    sql = text('')
    return '数据删除成功', 200

@bp.route('/change_invite_ok',methods=['POST','get'])
def change_invite_yes():
    data = request.get_json()
    # print(data,"ok")
    return '数据删除成功', 200

@bp.route('/get_invited_family',methods=['GET','POST'])
def get_invited_family():
    user_id = session.get('user_id')
    sql = text('select F.Fid, F.Fname, F.Fdate, FR.FRid from FAMILY_REQUEST FR join FAMILY F on FR.Fid = F.Fid where Uid2 = :user_id;')
    result = db.session.execute(sql,{'user_id':user_id}).fetchall()
    # print(result)
    list = []
    if result == []:
        list.append()
    else:
        for row in result:
            list.append({
                "id": row[0],
                "name": row[1],
                "date": row[2],
                'FRid': row[3]
            })
        # print(result)
        # print(list)
    return jsonify(list)

@bp.route('/family_list',methods=['GET','POST'])
def family_list():
    user_id = session.get('user_id')
    sql = text('select * from FAMILY F join FAMILY_USER FU on F.Fid = FU.Fid where Uid = :user_id;')
    result = db.session.execute(sql,{'user_id':user_id}).fetchall()
    list = []
    if result == []:
        list.append()
    else:

        for row in result:
            list.append({
                "id": row[0],
                "name": row[1],
                "date": row[2]
            })
        # print(result)
    # print(list)
    return jsonify(list)

@bp.route('/family_data1/<family_id>',methods=['GET','POST'])#-------------------新加
def family_data1(family_id):

    sql = text('select * from FAMILY_USER_INOUT where FamilyID = :family_id')
    result = db.session.execute(sql,{'family_id':family_id})
    list = []
    for row in result:
        list.append({
            'name': row[2],
            'in': row[3],
            'out': row[4]
        })


    return jsonify(list)

@bp.route('/family_data2/<family_id>',methods=['GET','POST'])#-------------------新加
def family_data2(family_id):
    # print()
    sql = text('select * from FAMILY_INOUT where Fid = :family_id ORDER BY FIid DESC')
    result = db.session.execute(sql,{'family_id':family_id}).fetchall()
    print('result:',result)
    list = []
    for row in result:
        sql = text('select T.Tname, C.Cname from TYPE T join CATEGORY C on C.Cid = T.Cid where T.Tid = :Tid')
        zhonglei = db.session.execute(sql,{'Tid':row[4]}).fetchone()
        print(zhonglei)
        type = zhonglei[0]
        category = zhonglei[1]

        if row[7] == 0:
            is_in = '支出'
        else:
            is_in = '收入'

        list.append({
            "id": row[0],
            "time": row[5],
            "is_in": is_in,
            "category": category,
            "type": type,# type
            "money": row[3],
            "detail": row[6]
        })
        response = {
        "code": 0,  # 成功状态码
        "msg": "",  # 消息字段
        "count": len(list),  # 数据总数
        "data": list  # 数据列表
        }

    return jsonify(list)

@bp.route('/invite/<family_id>',methods=['POST','get'])
def invite(family_id):
    return render_template('invite.html',family_id=family_id)

@bp.route('/delete_family/<id>',methods=['POST','get'])
def delete_family(id):
    # print(id)
    return  '数据删除成功', 200

@bp.route('/change_family',methods=['POST','get'])
def change_family():
    data = request.get_json()
    # print(data)
    return 1

@bp.route('/get_in_family/<family_id>',methods=['GET','POST'])
def get_in_family(family_id):
    session['family_id'] = family_id
    # print(session['family_id'])
    return jsonify({'status':'success'})

@bp.route('/add_total',methods=['POST','get'])
def add_total():
    return render_template('add_total.html')


@bp.route('/receive_total',methods=['POST','get'])
def receive_total_add_data():
    data = request.get_json()
    family_id = session.get('family_id')
    is_shouru = data.get('is_in')
    if is_shouru == '收入':
        is_in = 1
    else:
        is_in = 0
    print(data)
    type = data.get('type')
    money = data.get('money')
    detail = data.get('detail')
    user_id = session.get('user_id')
    print('receive')
    sql = text('insert into FAMILY_INOUT(Fid,Uid,FImoney,Tid,FIdetail,FIisin) value(:family_id, :user_id,:money,:type,:detail,:is_in)')
    db.session.execute(sql,{'family_id':family_id,'user_id':user_id,'money':money,'type':type,'detail':detail,'is_in':is_in})
    db.session.commit()
    # print('11')
    return jsonify({'status':'success'})

@bp.route('/family_menu/<family_id>',methods=['GET','POST'])
def family_menu(family_id):
    return render_template('family_menu.html',family_id=family_id)

# 邀请进入家庭
@bp.route('/invite_family_action',methods=['GET','POST'])
def invite_family_action():
    data = request.get_json()
    account = data.get('account')
    family_id = data.get('family_id')
    user_id = session.get('user_id')

    with db.engine.connect() as connection:
        connection.execute(text('call FAMILY_INVITE(:FID, :UID, :account, @result);'),{"FID":family_id,"UID":user_id,'account':account})
        result = connection.execute(text('select @result')).fetchone()

        if result[0] == 0:
            message = '用户不存在'
            status = ''
        elif result[0] == 1:
            message = '成功发出邀请'
            status = 'success'
        else:
            message = '该用户已在家庭中'
            status = ''
        connection.commit()

    return jsonify({'status':status,'message':message})

# 创建家庭
@bp.route('/create_family_action',methods=['GET','POST'])
def create_family_action():
    data = request.get_json()

    user_id = session.get('user_id')
    family_name = data.get('name')

    with db.engine.connect() as connection:
        connection.execute(text('call FAMILY_SET(:ID, :name, @FID);'),{'ID':user_id, 'name':family_name})
        connection.commit()
    return jsonify({'status':'success','message':'创建成功'})



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

