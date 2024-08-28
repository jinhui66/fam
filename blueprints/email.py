from flask import Blueprint
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from exts import db,mail
import string
import random
from flask_mail import Message
from sqlalchemy import text
from exts import db

bp = Blueprint('email',__name__,url_prefix="/")


@bp.route('/captcha/email',methods=['GET','POST'])
def get_email_captcha():
    email = request.args.get('email')
    source = string.digits*4
    captcha = random.sample(source,4)
    captcha = "".join(captcha)
    message = Message(subject='验证码',recipients=[email],body=f'您的验证码是:{captcha},请勿告知他人!')
    mail.send(message)
    sql = text('insert into EMAIL_CAPTCHA(ECaccount,ECcaptcha) value(:email, :captcha)')
    db.session.execute(sql,{'email':email, 'captcha': captcha})
    # db.session.add(email_captcha)
    db.session.commit()
    return jsonify({'code':200,'message':'','data':None})

