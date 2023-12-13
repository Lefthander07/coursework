from flask import Blueprint, render_template, current_app, request, session

from database.operations import select
from database.sql_provider import SQLProvider
blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')
sql_provider = SQLProvider('blueprint_query/sql')

col_name = {'name': "имя", "gname":"продукт", "idbuyers":"идентификатор клиента",
            "sum(order_line.quantity)":"стоимость купленного товара",
            'idgoods':"артикль", 'unit':'единица_товара',"price":"цена", "quantity":"количество на складе", "quantity_update":"дата обновления количества",
            "ordered":"заказано", "ordered_update":"дата обновления заказанного",
            "address":"адрес", "contact_number":"номер телефона", "BIC":"bic",
            "account_number":"счёт", "bank":"банк", "conclusion_date":"дата заключения контракта", "total_spent":"всего потрачено"
            ,"countt":"покупок"}
def find_query1(request):
    if request.form['date']:
        print("date")
        year = request.form['date'].split('-')[0]
        month= request.form['date'].split('-')[-1]
        sql_statement = sql_provider.get('1.sql', year = year,
                                         month = month,col_name=col_name)

        result = select(current_app.config['DB_CONFIG'], sql_statement)

        if result:
            print("yes")
            return result
        else:
            print("no")
            return None


def find_query2(request):
    if request.form['date'] and request.form['name']:
        year = request.form['date'].split('-')[0]
        month = request.form['date'].split('-')[-1]
        print(request.form['name'])
        sql_statement = sql_provider.get('2.sql', bname=request.form['name'], year=year, month=month)

    result = select(current_app.config['DB_CONFIG'], sql_statement)
    print(result)
    if result:
        print("yes")
        return result
    else:
        return None


def find_query3(request):
    sql_statement = sql_provider.get('3.sql', minmax=request.form['flexRadioDefault'])
    print(sql_statement)
    result = select(current_app.config['DB_CONFIG'], sql_statement)
    if result:
        return result
    else:
        return None


def find_query5(request):
    if request.form['date']:
        year = request.form['date'].split('-')[0]
        month = request.form['date'].split('-')[-1]
        print(request.form)
        sql_statement = sql_provider.get('5.sql', year = year,
                                         month = month)

    result = select(current_app.config['DB_CONFIG'], sql_statement)
    print(result)
    if result:
        print("yes")
        return result
    else:
        return None


def find_query6(request):
    if request.form['year']:
        print(request.form)
        sql_statement = sql_provider.get('6.sql', date = request.form['year'])

    result = select(current_app.config['DB_CONFIG'], sql_statement)
    print(result)
    if result:
        print("yes")
        return result
    else:
        return None


def find_query4(request):
    sql_statement = sql_provider.get('4.sql', status = request.form['flexRadioDefault'])
    result = select(current_app.config['DB_CONFIG'], sql_statement)
    print(result)
    if result:
        print("yes")
        return result
    else:
        return None


@blueprint_query.route('/')
def query_index():
    return render_template("queries_index.html")


@blueprint_query.route('/1', methods=['GET', 'POST'])
def query1():
    if request.method == "GET":
        return render_template("1.html", session = session)
    else:
        print(col_name['idgoods'])
        return render_template('table.html', employees = find_query1(request), query = 1, request=request,col_name=col_name)


@blueprint_query.route('/2', methods=['GET', 'POST'])
def query2():
    if request.method == "GET":
        return render_template("2.html")
    else:
        return render_template('table.html', employees = find_query2(request), query=2,request=request, col_name=col_name)


@blueprint_query.route('/3', methods=['GET','POST'])
def query3():
    if request.method == "GET":
        return render_template("3.html")
    else:
        print(request)
        return render_template('table.html', employees = find_query3(request), query=3,request=request.form['flexRadioDefault'], col_name=col_name)


@blueprint_query.route('/4', methods=['GET','POST'])
def query4():
    if request.method == "GET":
        return render_template('4.html')
    return render_template('table.html', employees=find_query4(request),query=4, request=request.form['flexRadioDefault'], col_name=col_name)


@blueprint_query.route('/5', methods=['GET', 'POST'])
def query5():
    if request.method == "GET":
        return render_template("5.html")
    else:
        return render_template('table.html', employees = find_query5(request),query=5, request=request, col_name=col_name)


@blueprint_query.route('/6', methods=['GET', 'POST'])
def query6():
    if request.method == "GET":
        return render_template("6.html")
    else:
        return render_template('table.html', employees = find_query6(request),query=6, request=request, col_name=col_name)



