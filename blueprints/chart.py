from flask import Blueprint
from flask import Flask,request,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from exts import db,mail
import string
import random
from flask_mail import Message
from sqlalchemy import text
from exts import db
import plotly.graph_objects as go


bp = Blueprint('chart',__name__,url_prefix="/")

@bp.route('/pie_chart',methods=['GET','POST'])
def pie_chart():
    # 模拟数据
    labels = ['Group A', 'Group B', 'Group C', 'Group D']
    values = [10, 20, 30, 40]

    # 创建饼状图
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # 将饼状图转换为HTML
    plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # 将饼状图传递给模板
    return render_template('pie.html', plot_div=plot_div)
