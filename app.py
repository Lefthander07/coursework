import json
from flask import Flask, render_template, session, request, redirect
from blueprint_query.route import blueprint_query
from blueprint_auth.route import blueprint_auth
from blueprint_basket.route import blueprint_basket
from blueprint_report.route import blueprint_report


from access import login_required, group_required


app = Flask(__name__)
app.secret_key = 'adffwedwefweeccccccccw'


app.register_blueprint(blueprint_query, url_prefix='/queries')
app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_basket, url_prefix='/basket')
app.register_blueprint(blueprint_report, url_prefix='/report')

app.config['DB_CONFIG'] = json.load(open('configs/db.json'))
app.config['access_config'] = json.load(open('configs/access.json'))
app.config['cache_config'] = json.load(open('configs/cache.json'))

with open('reports.json', 'r', encoding='UTF-8') as f:
    reports = json.load(f)
    reports_list = []
    reports_url = {}


    for i in reports:
        reports_list.append({'rep_name': i['rep_name'], 'rep_id': i['rep_id']})
        reports_url[i['rep_id']] = {'create_rep': i['url']['create_rep'], 'view_rep': i['url']['view_rep']}

    app.config['reports_list'] = reports_list
    app.config['reports_url'] = reports_url











@app.route('/')
def index():
    if 'login_user' not in session:
        return redirect('/auth')
    else:
        print(session)
        print(session['login_user'])
        return render_template('index_main.html', session = session)


def auth_access(main_app: Flask, blueprint_list, decorator):
    for name, v_func in app.view_functions.items():
        name_parts = name.split('.')
        if len(name_parts) > 1:
            name_blueprint = name_parts[0]
            name_handler = name_parts[1]
            print(name_parts)

            if name_blueprint in blueprint_list:
                v_func = decorator(v_func)
                main_app.view_functions[name] = v_func
    return main_app




if __name__ == '__main__':
    app = auth_access(app,['bp_query', 'bp_basket', 'bp_report'], login_required)
    app = auth_access(app,['bp_query', 'bp_basket', 'bp_report'],  group_required)
    app.run(host='127.0.0.1', port=5003)