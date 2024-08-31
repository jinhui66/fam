from flask import Blueprint
from flask import Flask,request,render_template,session,redirect,url_for,jsonify
from sqlalchemy import text
from exts import db
import hashlib
import json
import os
import time

w = [
  {
    "id": "001",
    "name": "张三家",
    "date": "2023-04-01"
  },
  {
    "id": "002",
    "name": "李四家",
    "date": "2023-05-15",
    "TotalMoney":20
  },
  {
    "id": "003",
    "name": "王五家",
    "date": "2023-06-20",
      "Detail": "dsadasdas"
  },
  {
    "id": "004",
    "name": "赵六家",
    "date": "2023-07-05"
  },
  {
    "id": "005",
    "name": "孙七家",
    "date": "2023-08-10"
  }
]

bp = Blueprint('family',__name__,url_prefix="/")


@bp.route('/get_invited_family',methods=['GET','POST'])
def get_invited_family():
    user_id = session.get('user_id')
    sql = text('select F.Fid, F.Fname, F.Fdate from FAMILY_REQUEST FR join FAMILY F on FR.Fid = F.Fid where Uid2 = :user_id;')
    result = db.session.execute(sql,{'user_id':user_id}).fetchall()
    print(result)
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
    print(list)
    return jsonify(list)

@bp.route('/family_data1',methods=['GET','POST'])#-------------------新加
def family_data1():
    # print(family_id)
    print('family_data1')
    return jsonify(w)

@bp.route('/family_data2',methods=['GET','POST'])#-------------------新加
def family_data2():
    # print(family_id)
    print('family_data')
    return jsonify(w)

@bp.route('/invite/<family_id>',methods=['POST','get'])
def invite(family_id):
    return render_template('invite.html',family_id=family_id)

@bp.route('/delete_family/<id>',methods=['POST','get'])
def delete_family(id):
    print(id)
    return  '数据删除成功', 200

@bp.route('/change',methods=['POST','get'])
def change(id):
    data = request.get_json()
    print(data)
    return 1

@bp.route('/get_in_family',methods=['GET','POST'])
def get_in_family():
    # print(family_id)
    return jsonify({'status':'success'})

@bp.route('/add_total',methods=['POST','get'])
def add_total():
    return render_template('add_total.html')

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

