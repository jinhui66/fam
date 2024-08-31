from flask import Blueprint
from flask import Flask,request,render_template,session,redirect,url_for,jsonify
from sqlalchemy import text
from exts import db
import hashlib
import json
import os
import time
import plotly.graph_objects as go
import numpy as np


bp = Blueprint('index',__name__,url_prefix="/")

@bp.route('/welcome',methods=['GET','POST'])
def welcome():
    return render_template('welcome.html')

@bp.route('/test',methods=['GET','POST'])
def test():
    user_id = session.get('user_id')
    sql = text('select Uaccount from USER where Uid = :user_id')
    account = db.session.execute(sql,{'user_id':user_id}).fetchone()
    account = account[0]
    return render_template('test.html', account = account)

@bp.route('/user_in',methods=['GET','POST'])
def user_in():
        # 模拟数据
    user_id = session.get('user_id')
    sql = text('select C.Cname, sum(TotalMoney) from USER_INOUT_SUM U left join TYPE T on T.Tid = U.Tid left join CATEGORY C on C.Cid = T.Cid where UIisin = 1 and Uid=:user_id group by C.Cid;')
    label_value = db.session.execute(sql,{'user_id':user_id}).fetchall()

    labels = []
    values = []

    print(label_value)

    for row in label_value:
        labels.append(row[0])
        values.append(row[1])
    # 创建饼状图
    fig1 = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # 将饼状图转换为HTML
    plot_div1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')

    sql = text('select Month, sum(TotalMoney) from USER_INOUT_SUM where Uid = :user_id and UIisin = 1 group by Month order by Month;')
    label_value = db.session.execute(sql,{'user_id':user_id}).fetchall()
    print(label_value)
    labels = []
    values = []
    for row in label_value:
        labels.append(str(row[0])+'月')
        values.append(row[1])
    # 创建条形图
    fig2 = go.Figure(data=[go.Bar(x=labels, y=values)])

    fig2.update_layout(title_text='每月收入', xaxis_title="时间", yaxis_title="金额")
    plot_div2 = fig2.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template('user_in.html',plot_div1=plot_div1,plot_div2=plot_div2)

@bp.route('/user_out',methods=['GET','POST'])
def user_out():
        # 模拟数据
    user_id = session.get('user_id')
    sql = text('select C.Cname, sum(TotalMoney) from USER_INOUT_SUM U left join TYPE T on T.Tid = U.Tid left join CATEGORY C on C.Cid = T.Cid where UIisin = 0 and Uid=:user_id group by C.Cid;')
    label_value = db.session.execute(sql,{'user_id':user_id}).fetchall()

    labels = []
    values = []

    print(label_value)

    for row in label_value:
        labels.append(row[0])
        values.append(row[1])
    # 创建饼状图
    fig1 = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # 将饼状图转换为HTML
    plot_div1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')

    sql = text('select Month, sum(TotalMoney) from USER_INOUT_SUM where Uid = :user_id and UIisin = 0 group by Month order by Month;')
    label_value = db.session.execute(sql,{'user_id':user_id}).fetchall()
    print(label_value)
    labels = []
    values = []
    for row in label_value:
        labels.append(str(row[0])+'月')
        values.append(row[1])
    # 创建条形图
    fig2 = go.Figure(data=[go.Bar(x=labels, y=values)])

    fig2.update_layout(title_text='每月支出', xaxis_title="时间", yaxis_title="金额")
    plot_div2 = fig2.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template('user_out.html',plot_div1=plot_div1,plot_div2=plot_div2)

@bp.route('/get_family',methods=['GET','POST'])
def get_family():
    return render_template('get_family.html')

@bp.route('/invited_family',methods=['GET','POST'])
def invited_family():
    return render_template('invited_family.html')

@bp.route('/families',methods=['GET','POST'])
def families():
    return render_template('families.html')
