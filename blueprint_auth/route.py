from flask import Blueprint, render_template, current_app, request, session, redirect
from database.operations import select, insert
from database.sql_provider import SQLProvider #вызов объекта реализации запроса
from database.connection import DBContextManager
blueprint_auth = Blueprint('bp_auth', __name__, template_folder='templates')
sql_provider = SQLProvider('blueprint_auth/sql')

def ident(login, password):
    sql_statement1 = sql_provider.get('find_ext.sql', login=login, password=password)
    sql_statement2 = sql_provider.get('find_int.sql', login=login, password=password)


    info1 = select(current_app.config['DB_CONFIG'], sql_statement1)
    info2 = select(current_app.config['DB_CONFIG'], sql_statement2)


    if info1:
        return info1[0]
    elif info2:
        return info2[0]
    else:
        return "пользователь не найден"

def check_login(login):
    sql_statement = sql_provider.get('find_login.sql', login=login)
    info = select(current_app.config['DB_CONFIG'], sql_statement)
    if info:
        return True
    else:
        return False


def auth(request):
    login = request.form.get('login')
    password = request.form.get('password')
    user = ident(login, password)

    if isinstance(user, dict):
        session['id_user'] = user['id']
        session['group_user'] = user['cgroup']
        session['login_user'] = user['login']
        session.permanent = True
        return redirect('/')
    else:
        return render_template('error.html')


@blueprint_auth.route('/', methods=["POST", "GET"])
def bp_auth_index_handler():
    if request.method == "GET":
        return render_template("login.html")
    else:
        return auth(request)




@blueprint_auth.route('/reg', methods = ["GET", "POST"])
def reg_handler():
    if request.method == "GET":
        return render_template('reg.html')
    else:
        login = request.form.get('username')
        password = request.form.get('password')
        repeat_password = request.form.get("r_password")
        name = request.form.get("name")
        city = request.form.get("city")


        if (check_login(login)):
            msg1 = 'Логин занят. Придумайте другой'
            return render_template('reg.html', msg = msg1)
        if (password != repeat_password):
            msg1 = 'Пароли не совпадают. Повторите ввод'
            return render_template('reg.html', msg = msg1)

        

        sql_statement = sql_provider.get('create_client.sql', nameClient=name)
        result = insert(current_app.config['DB_CONFIG'], sql_statement)
        if (result):
            return "Пользователь создан"
        else:
            return render_template('reg.html', msg='Что-то пошло не так. Попробуйте заново')



@blueprint_auth.route('/logout')
def logout_handler():
    session.clear()
    return redirect('/')



