from flask import Blueprint, render_template, current_app, request, session, url_for, redirect
from datetime import datetime
from database.operations import select, call_proc

from database.sql_provider import SQLProvider
blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
sql_provider = SQLProvider('blueprint_report/sql')

col_name = {'gname': "продукт", "idgoods":"артикль", "idbuyers":"идентификатор клиента", "quantity":"количество",
            'total':"на сумму", "name": 'ФИО', 'bank':'банк', 'spent':'потрачено','concl_date':'дата заключения контракта'
            }
#
@blueprint_report.route('/', methods=['GET', 'POST'])
def start_report():
    report_url = current_app.config['reports_url']
    if request.method == 'GET':
        return render_template('index.html', report_list=current_app.config['reports_list'], session=session)
    else:
        rep_id = request.form.get('rep_id')

        if request.form.get('create_rep'):
            url_rep = report_url[rep_id]['create_rep']
            print(url_rep)
        else:
            url_rep = report_url[rep_id]['view_rep']

        return redirect(url_rep.split('.')[-1])

def create_rep(number):
    report_list = current_app.config['reports_list']
    form_page = 'report.html'
    if request.method == 'GET':
        return render_template(form_page, mode="create", name=report_list[number-1]['rep_name'])
    else:
        rep_start = request.form.get('input_start')
        rep_end = request.form.get('input_end')

        rep_start1 = (rep_start.split('-'))
        rep_end1 = (rep_end.split('-'))
        if int(rep_start1[0]) < 2100 and int(rep_end1[0]) < 2100 and (int(rep_start1[0]) <= int(rep_end1[0])) and \
                (int(rep_start1[1]) <= int(rep_end1[1])) and (int(rep_start1[-1]) <= int(rep_end1[-1])):



            sql_statement = sql_provider.get(str(number)+'.sql', date_from=rep_start, date_to=rep_end)
            result = select(current_app.config['DB_CONFIG'], sql_statement)

            if not result:
                result = call_proc(current_app.config['DB_CONFIG'], 'report'+str(number),rep_start, rep_end)
                print("cal", result)
                return render_template('success_report.html')

            else:
                return render_template(form_page, mode="create", message="Отчёт за заданный период существует")
        else:
            return render_template(form_page, mode="create", message="Некорректный ввод!")


@blueprint_report.route('/create_rep_1', methods=['GET', 'POST'])
@blueprint_report.route('/create_rep_2', methods=['GET', 'POST'])
def create():
    report_n = request.path.split('_')[-1]
    return create_rep(int(report_n))


def get_exist_report(number):
    sql_statement = sql_provider.get("report" + str(number)+".sql")
    result = select(current_app.config['DB_CONFIG'], sql_statement)
    return result


@blueprint_report.route('/view_rep_1', methods=['GET', 'POST'])
@blueprint_report.route('/view_rep_2', methods=['GET', 'POST'])
def view():
    number = int((request.path.split('_')[-1]))
    report_list = current_app.config['reports_list']
    if request.method == 'GET':
        exists = get_exist_report(number)
        print(exists)
        print("number:", number, "exist", exists)
        return render_template("report_list.html", exists=exists, name=report_list[number-1]['rep_name'])
    else:
        period = (request.form.get('period').split('/'))
        rep_start = period[0]
        rep_end = period[1]

        sql_statement = sql_provider.get(str(number)+".sql", date_from=rep_start, date_to=rep_end)
        product_result = select(current_app.config['DB_CONFIG'], sql_statement)
        if not product_result:
            product_result = None
        return render_template('result_rep.html', employees=product_result, col_name=col_name,
                                   name=report_list[number-1]['rep_name'])