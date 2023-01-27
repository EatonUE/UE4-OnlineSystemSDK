from flask import Flask
from flask import jsonify
from flask import request
import pymysql
import send
from hashlib import md5
import random


def encrypt_md5(s):
    # 创建md5对象
    new_md5 = md5()
    # 这里必须用encode()函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
    new_md5.update(s.encode(encoding='utf-8'))
    # 加密
    return new_md5.hexdigest()


app = Flask(__name__)
# 打开数据库连接

mailcheck = {}
token = {}


@app.route('/get')
def mail():
    account = request.args.get('account')
    db = pymysql.connect(host='mysql.sqlpub.com',port=3306,user='csse_mail',password='17c64431c5adf6d3',database='csse_mail')
    cursor = db.cursor()
    sql = "SELECT * FROM mail where account='%s'" %(account)
    list_account=[]
    list_content=[]
    list_tit=[]
    list_id=[]
    list_state=[]
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for i in range(len(results)):
            tmp=results[i]
            mailid=tmp[0]
            list_id.append(mailid)
            account=tmp[1]
            list_account.append(account)
            title=tmp[2]
            list_tit.append(title)
            content=tmp[3]
            list_content.append(content)
            state=tmp[4]
            list_state.append(state)
        sql = "SELECT * FROM mail where account='0'"
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for i in range(len(results)):
            tmp=results[i]
            mailid=tmp[0]
            list_id.append(mailid)
            account=tmp[1]
            list_account.append(account)
            title=tmp[2]
            list_tit.append(title)
            content=tmp[3]
            list_content.append(content)
            state=tmp[4]
            list_state.append(state)
        db.close()
        return {"success":"Pass","id":list_id,"title":list_tit,"content":list_content,"state":list_state}
    except:
        db.close()
        return {"success":"服务器错误!"}


@app.route('/version')
def getversion():
    return {"version": "3.1.0"}


@app.route('/')
def test():
    return "thank you for your watch!"


@app.route('/registarclient')
def changecl():
    return '<p>SE账号注册注册成功后请记住Account的内容</p><form method="get" action="/reg"><label>用户名：<input type="text" name="n" value=""></label><br><label>密码：<input type="password" name="p" value=""><br><input type="submit" value="注册"></form>'


@app.route('/mailcheck', methods=['GET'])
def getmailcheck():
    email = request.args.get('email')
    res = send.send(email)
    mailcheck[email] = str(res)
    return {"success": "发送成功，请注意查收"}


@app.route("/login", methods=['GET'])  # "登录服务器 传入用户名和密码"
def login():
    account = request.args.get('u')
    password = request.args.get('p')
    db = pymysql.connect(host='mysql.sqlpub.com',port=3306,user='sestudio',password='96312c734e441b40',database='csse_all')
    cursor = db.cursor()
    # SQL 查询语句
    sql = "SELECT * FROM player WHERE account = '%s'" % (account)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            name = row[1]
            lname = row[2]
            userbp = row[3]
            fenghao = row[4]
            rp = row[6]
            # 打印结果 401=success;402=封号;403=password errow;404=not found
        db.close()
        if lname == password:
            if fenghao == '0':
                #token[account] = str(random.randint(1, 9999))
                return {"success": "Pass", "username": name, "id": account, "userbp": userbp, "rp": rp}  # 判断
            else:
                return {"success": "由于违规的游戏行为，您的账号已被封停！原因：" + fenghao}  # 判断
        else:
            return {"success": "密码错误！"}
    except:
        db.close()
        return {"success": "用户不存在！"}


@app.route("/reg", methods=['POST', 'GET'])
def reg():
    a = request.form.get('email')
    c = request.form.get('n')
    b = request.form.get('p')
    email = request.form.get('email')
    check = request.form.get('check')
    db = pymysql.connect(host='mysql.sqlpub.com',port=3306,user='sestudio',password='96312c734e441b40',database='csse_all')
    cursor = db.cursor()
    try:
        if check == mailcheck[email]:
            if c != '' and b != '':
                sql = "INSERT INTO `player` (`account`, `username`, `password`, `bp`, `fenghao`, `email`,`rp`) VALUES ('%s', '%s', '%s', 0, 0, '%s','1000')" % (
                    a, c, b, email)
                try:
                    cursor.execute(sql)
                    db.commit()
                    db.close()
                    return {"success": "Pass", "account": a}
                except:
                    # 如果发生错误则回滚
                    db.rollback()
                    db.commit()
                    db.close()
                    print("插入失败")
                    return {"success": "邮箱已被注册！"}
            else:
                db.close()
                return {"success": "账号密码不能为空"}
        else:
            db.close()
            return {"success": "验证码错误"}
    except:
        db.close()
        return {"success": "未申请验证码"}


@app.route('/changepassword')
def changepw():
    a = request.args.get('account')
    v = request.args.get('password')
    check = str(request.args.get('check'))
    email = a
    db = pymysql.connect(host='mysql.sqlpub.com',port=3306,user='sestudio',password='96312c734e441b40',database='csse_all')
    cursor = db.cursor()
    try:
        if check == mailcheck[email]:
            sql = "UPDATE `player` SET password='%s' WHERE account='%s'" % (v, a)
            try:
                cursor.execute(sql)
                db.commit()
                db.close()
                return {"success": "Pass"}
            except:
                db.rollback()
                db.commit()
                db.close()
                return {"success": "用户名不存在！"}
        else:
            db.close()
            return {"success": "验证码错误"}
    except:
        db.close()
        return {"success": "未申请验证码"}


@app.route('/change')
def change():
    a = request.args.get('account')
    k = request.args.get('key')
    v = request.args.get('value')
    sql = "UPDATE `player` SET %s='%s' WHERE account='%s'" % (k, v, a)
    db = pymysql.connect(host='mysql.sqlpub.com',port=3306,user='sestudio',password='96312c734e441b40',database='csse_all')
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return {"success": "Pass"}
    except:
        db.rollback()
        db.commit()
        db.close()
        return {"success": "Internal Server Errow"}


@app.route('/managerlogin')
def managerlogin():
    return '<p>SE后台管理</p><form method="post" action="/manager"><label>用户名：<input type="text" name="user" value=""></label><br><label>密码：<input type="password" name="password" value=""><br><input type="submit" value="登录"></form>'


@app.route('/manager', methods=['POST'])
def manager():
    u = request.form.get("user")
    p = request.form.get("password")
    if u == 'sebackpartmanager' and p == '1029831232':
        return '<p>SE后台管理</p><p>修改数据</p><form method="get" action="/change"><label>account：<input type="text" name="account" value=""></label><br><label>key：<input type="text" name="key" value=""></label><br><label>value：<input type="text" name="value" value=""><br><input type="submit" value="修改"></form><p>查询</p><form method="post" action="/find"><label>account：<input type="text" name="a" value=""></label><br><input type="submit" value="查询"></form>'
    else:
        return "<p>登陆失败，密码错误</p><a href='./managerlogin'  target='_self'>重新登陆</a>"


@app.route('/find', methods=['POST'])
def find():
    value = request.form.get('a')
    sql = "SELECT * FROM player WHERE account = '%s'" % (value)
    try:
        db = pymysql.connect(host='mysql.sqlpub.com',port=3306,user='sestudio',password='96312c734e441b40',database='csse_all')
        cursor = db.cursor()
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            account = row[0]
            name = row[1]
            userbp = row[3]
            fenghao = row[4]
            db.close()
            return '<p>账号:%s</p><p>用户名:%s</p><p>bp:%s</p><p>封号(0:正常/1:封号):%s</p>' % (
                account, name, userbp, fenghao)  # 判断
    except:
        db.close()
        return '<p>服务器错误</p>'
