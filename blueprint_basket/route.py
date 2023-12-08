from flask import Blueprint, request, render_template, session, current_app, redirect, url_for
from database.operations import select,update
from database.sql_provider import SQLProvider
from database.connection import DBContextManager
from datetime import datetime, timedelta
from cache.wrapper import fetch_from_cache, fetch_from_cache_force

blueprint_basket = Blueprint('bp_basket', __name__, template_folder='templates', static_folder='static')
sql_provider = SQLProvider('blueprint_basket/sql')

def clear():
    if 'basket' in session:
         session.pop('basket')

@blueprint_basket.route('/', methods=['GET', 'POST'])
def basket_index():
    cached_select = fetch_from_cache('all_items', current_app.config['cache_config'])(select)
    if request.method == 'GET':
        sql_statement = sql_provider.get('all.sql')
        items = cached_select(current_app.config['DB_CONFIG'], sql_statement)
        basket_items = session.get('basket', {})
        return render_template('basket_index.html', items=items, basket=basket_items)
    else:
        id = request.form['item_id']
        sql_statement = sql_provider.get('goods.sql', idgood=id)
        items = select(current_app.config['DB_CONFIG'], sql_statement)
        add(id, items[0])
        return redirect('/basket')


@blueprint_basket.route('/amount', methods=['GET', 'POST'])
def edit_amount_basket():
    curr_basket = session.get('basket', {})
    if 'value' in request.args:
        id_detail = request.args['id_detail']
        amount = curr_basket[id_detail]['count'] + int(request.args['value'])
    else:
        id_detail = request.form['detail']
        amount = int(request.form['amount'])
    max_amount = int(curr_basket[id_detail]['available'])

    amount = 1 if amount < 1 else amount
    amount = max_amount if amount > max_amount else amount

    curr_basket[id_detail]['count'] = amount

    session['basket'] = curr_basket
    session.permanent = True

    return redirect(url_for('bp_basket.basket_index'))


@blueprint_basket.route('/clear')
def clear_basket():
    clear()
    return redirect('/basket')
@blueprint_basket.route('/delete', methods=['GET', 'POST'])
def delete_from_basket():
    curr_basket = session.get('basket', {})
    curr_basket.pop(request.args['id'])
    session['basket'] = curr_basket
    session.permanent = True
    return redirect(url_for('bp_basket.basket_index'))

def view_order_list():
    sql_statement = sql_provider.get('orders_by_user_id.sql', user_id=1)
    result = select(current_app.config['DB_CONFIG'], sql_statement)
    return result

def view_order_info(idorder):
    sql_statement1 = sql_provider.get('orders_line_by_order_id.sql', idorder = idorder)
    result1 = select(current_app.config['DB_CONFIG'], sql_statement1)

    sql_statement2 = sql_provider.get('total.sql', idorder = idorder)
    result2 = select(current_app.config['DB_CONFIG'], sql_statement2)

    return result1, result2


def make_order(status):
    basket = session.get('basket', {})
    print(basket)
    if basket:
        with DBContextManager(current_app.config['DB_CONFIG']) as cursor:
            goods_ids = [goods_id for goods_id in basket]
            goods_ids = ','.join(goods_ids)
            sql_statement = sql_provider.get('goods_by_id.sql', goods_ids=goods_ids)
            cursor.execute(sql_statement)
            schema = [col[0] for col in cursor.description]
            item_descriptions = [dict(zip(schema, row)) for row in cursor.fetchall()]
            order_date = datetime.today().strftime('%Y-%m-%d')
            deadline_date = (datetime.today() + timedelta(days=3)).strftime('%Y-%m-%d')

            total = 0
            for i in basket:
                total += basket[i]['count'] * basket[i]['price']
            payment_date = 'NULL'
            if status:
                payment_date = '\''+str(datetime.today().strftime('%Y-%m-%d')) + '\''
            sql_statement = sql_provider.get('create_order.sql', user_id=session['id_user'],\
                                             order_date=order_date, deadline_date=deadline_date,total=total, status=status,
                                             payment_date = payment_date)
            for item_description in item_descriptions:
                n_inserts = basket[str(item_description['idgoods'])]['count']
                n_left = int(item_description['available']) - n_inserts
                if (n_left < 0):
                    print("В корзине больше чем доступно")
                    return redirect('/basket')
                elif (n_left == 0):
                    pass

            cursor.execute(sql_statement)
            order_id = cursor.lastrowid
            for item_description in item_descriptions:
                n_inserts = basket[str(item_description['idgoods'])]['count']
                idgoods = basket[str(item_description['idgoods'])]['id']
                sql_statement = sql_provider.get('create_order_line.sql', idgoods=idgoods,idorder=order_id, quantity=n_inserts)
                cursor.execute(sql_statement)
            clear()
            message = 'Заказ зарезервирован'
            if status:
                message = 'Заказ оплачен'
            return render_template('status_page.html', message = message)
    return render_template("status_page.html", message="Произошла ошибка оформления заказа")

@blueprint_basket.route('/list', methods=['GET','POST'])
def order_list():
    if request.method == "GET":
        return render_template('new_order_list.html', order_list = view_order_list())


@blueprint_basket.route('/list/order', methods=['GET', 'POST'])
def view_order():
    if request.method == "POST":
        items, order_info = view_order_info(request.form['order'])
        return render_template('order.html',items = items, order_info=order_info[0])

@blueprint_basket.route('/list/order/update', methods=['POST'])
def update_status():
    if request.method == "POST":
        payment_date = datetime.today().strftime('%Y-%m-%d')
        sql_statement = sql_provider.get('update_status.sql', idorder = request.form['idorder'], payment_date=payment_date)
        a = update(current_app.config['DB_CONFIG'], sql_statement)
        return render_template('status_page.html', message='Заказ оплачен')




@blueprint_basket.route('/order')
def order():
    return make_order(0)

@blueprint_basket.route('/buy')
def buy():
    return make_order(1)
    # basket = session.get('basket', {})
    # print(basket)
    # if basket:
    #     with DBContextManager(current_app.config['DB_CONFIG']) as cursor:
    #         goods_ids = [goods_id for goods_id in basket]
    #         goods_ids = ','.join(goods_ids)
    #         sql_statement = sql_provider.get('goods_by_id.sql', goods_ids=goods_ids)
    #         cursor.execute(sql_statement)
    #         schema = [col[0] for col in cursor.description]
    #         item_descriptions = [dict(zip(schema, row)) for row in cursor.fetchall()]
    #         order_date = datetime.today().strftime('%Y-%m-%d')
    #         deadline_date = (datetime.today() + timedelta(days=3)).strftime('%Y-%m-%d')
    #
    #         total = 0
    #         for i in basket:
    #             total += basket[i]['count'] * basket[i]['price']
    #
    #         sql_statement = sql_provider.get('create_order.sql', user_id=session['id_user'],\
    #                                          order_date=order_date, deadline_date=deadline_date,total=total, status=0)
    #
    #
    #         cursor.execute(sql_statement)
    #         order_id = cursor.lastrowid
    #         for item_description in item_descriptions:
    #             n_inserts = basket[str(item_description['idgoods'])]['count']
    #             idgoods = basket[str(item_description['idgoods'])]['id']
    #             sql_statement = sql_provider.get('create_order_line.sql', idgoods=idgoods,idorder=order_id, quantity=n_inserts)
    #             cursor.execute(sql_statement)
    #
    #             sql_statement = sql_provider.get('update.sql', idgoods = idgoods, ordered=n_inserts)
    #             cursor.execute(sql_statement)
    #         clear()
    #         return render_template('success_order.html')
    # return render_template("error.html")

def add(id, goods):
    basket = session.get('basket', {})
    if id in basket:
        if basket[id]['count'] < basket[id]['available']:
            basket[id]['count'] += 1
    else:
        basket[id] = {
            'id': id,
            'gname': goods['gname'],
            'unit': goods['unit'],
            'price': goods['price'],
            'count': 1,
            'available': goods['available']
        }

        session['basket'] = basket
        session.permanent = True
