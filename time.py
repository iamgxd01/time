import datetime, time
from flask import Flask, render_template, url_for, jsonify, request, redirect
from flask.ext.script import Manager,Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import func, desc
from flask.ext.migrate import Migrate, MigrateCommand
import os
import mytools
import json

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# 防止跨站请求伪造的攻击
# SECRET_KEY尽量设置一个复杂的值且要配置在环境变量中，不要直接写在程序中
app.config['SECRET_KEY'] = 'hard to guess string'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username


class List(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    listname = db.Column(db.String(64), unique=True)
    list_order = db.Column(db.Integer)
    tasks = db.relationship('Task', backref='lists')

    def __repr__(self):
        return '<List %r>' % self.listname


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time)
    taskname = db.Column(db.String(64), index=True)
    thought = db.Column(db.String(128))
    scheduled_time = db.Column(db.Integer)
    efficiency = db.Column(db.String(64))
    summary = db.Column(db.String(128))
    end_time = db.Column(db.Time)
    actual_time = db.Column(db.Integer)
    status = db.Column(db.Integer)
    date = db.Column(db.Date)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))

    # list = db.relationship('List', backref='list')

    def __repr__(self):
        return '<Task %r>' % self.taskname


@app.route('/', methods=['GET', 'POST'])
def index():
    date = str(datetime.date.today())
    print(date)
    calender_date_object = str_to_date(date)
    return render_template('time.html', taskjson=taskjson(calender_date_object),
                           list_id=List.query.filter_by(listname='今天')[0].id, date=date)


@app.route('/gettaskdata')
def gettaskdata():
    return taskjson()


@app.route('/getlistdata')
def getlistdata():
    return listjson()


@app.route('/addtask', methods=['GET', 'POST'])
def addtask():
    status = ''
    task_add = ''
    if request.method == 'POST':
        value = request.form.get('value')
        name = request.form.get('name')
        task_id = request.form.get('task_id')
        list_id = request.form.get('list_id')
        task_date = request.form.get('task_date')
        task_date_object = str_to_date(task_date)
        # 如果是在今天中添加，则添加到收集箱清单中
        if List.query.filter_by(id=list_id)[0].listname == '今天':
            list_id = List.query.filter_by(listname='收集箱')[0].id
        task = Task.query.filter_by(id=task_id).first()
        if name == 'taskname':
            task_add = Task(taskname=value, list_id=list_id, date=task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.taskname = value
                db.session.add(task)

            db.session.commit()

        elif name == 'listname':
            list = List.query.filter_by(listname=value).first()
            if list is None:
                status = 'false'
            else:
                if task is None:
                    task_add = Task(list_id=list.id, date=task_date_object)
                    db.session.add(task_add)
                else:
                    task.list_id = list.id
                    db.session.add(task)

        elif name == 'start_time':
            hour = value[0:2]
            minute = value[3:5]
            value = datetime.time(int(hour), int(minute), 00)
            task_add = Task(start_time=value, list_id=list_id, date=task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.start_time = value
                db.session.add(task)
            db.session.commit()

        elif name == 'thought':
            task_add = Task(thought=value, list_id=list_id, date=task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.thought = value
                db.session.add(task)
            db.session.commit()

        elif name == 'scheduled_time':
            task_add = Task(scheduled_time=value, list_id=list_id, date=task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.scheduled_time = value
                db.session.add(task)
            db.session.commit()

        elif name == 'efficiency':
            task_add = Task(efficiency=value, list_id=list_id, date=task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.efficiency = value
                db.session.add(task)
            db.session.commit()

        elif name == 'summary':
            task_add = Task(summary=value, list_id=list_id, date=task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.summary = value
                db.session.add(task)
            db.session.commit()

        elif name == 'end_time':
            hour = value[0:2]
            minute = value[3:5]
            value = datetime.time(int(hour), int(minute), 00)
            task_add = Task(end_time=value, list_id=list_id, date=task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.end_time = value
                db.session.add(task)
            db.session.commit()

        elif name == 'actual_time':
            task_add = Task(actual_time=value, list_id=list_id, date=task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.actual_time = value
                db.session.add(task)
            db.session.commit()

        if task_id == ' ':
            task_id = task_add.id

        return jsonify(status=status, task_id=task_id)


@app.route('/deletetask', methods=['GET', 'POST'])
def deletetask():
    if request.method == 'POST':
        task_id = request.form.get('task_id')
        task = Task.query.filter_by(id=task_id).first()
        if task is not None:
            db.session.delete(task)
            db.session.commit()

    return jsonify()


@app.route('/addlist', methods=['GET', 'POST'])
def addlist():
    status = ''
    if request.method == 'POST':
        list_name = request.form.get('list_name')
        list = List.query.filter_by(listname=list_name).first()
        if list is None:
            db.session.add(List(listname=list_name))
            db.session.commit()
        else:
            status = 'false'
    return jsonify(status=status)


@app.route('/tasks/<listname>', methods=['GET', 'POST'])
def tasks(listname):
    calender_date = request.args.get('date')
    calender_date_object = str_to_date(calender_date)
    print(listname)
    print(calender_date)
    # 查询当前日期下所有task
    if listname == '今天':
        tasks = Task.query.filter_by(date=calender_date_object)
        list_id = List.query.filter_by(listname=listname)[0].id
    else:
        list = List.query.filter_by(listname=listname)
        tasks = Task.query.filter_by(list_id=list[0].id, date=calender_date_object)
        list_id = list[0].id
    # tasks = Task.query.filter_by(list_id=listid)
    try:

        task_host = []
        for task in tasks:
            task_host.append(task)
        taskjson = json.dumps(task_host, cls=new_alchemy_encoder(), check_circular=False)
        print('taskjson:::::::' + taskjson)
        return render_template('time.html', taskjson=taskjson, list_id=list_id, date=calender_date)

    except Exception as e:
        print(e)


@app.route('/get_notification', methods=['GET', 'POST'])
def get_notification():
    value = request.form.get('value')
    print(value)
    tasks_start_time = db.session.query(Task).filter(Task.date == mytools.get_now_date_object(),
                                                     Task.start_time == mytools.get_now_time_object())
    tasks_scheduled_time = db.session.query(Task).filter(Task.date == mytools.get_now_date_object(),
                                                         Task.start_time < mytools.get_now_time_object())

    notifications = []
    for task in tasks_start_time:
        data1 = {
            'title': task.taskname,
            'body': '任务开始',
            'type': 'start'
        }
        notifications.append(data1)
    for task in tasks_scheduled_time:
        if task.start_time is not None and task.scheduled_time is not None:
            add_time = mytools.time_add_time(task.start_time, mytools.int_to_time_object(int(task.scheduled_time)))
            if add_time == mytools.get_now_time_object():
                data2 = {
                    'title': task.taskname,
                    'body': '计时结束',
                    'type': 'scheduled'
                }
                notifications.append(data2)
    print(notifications)

    return jsonify(notifications=notifications)


@app.route('/datavisualization')
def datavisualization():
    return render_template('data-visualization.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/statistics/')
def statistics():
    calender_date = request.args.get('date')
    print(calender_date)
    calender_date_object = str_to_date(calender_date)
    return render_template('statistics.html', statisticjson=day_statistics(calender_date), date=calender_date_object)


@app.route('/manage')
def manage():
    return render_template('manage.html')


@app.route('/maps')
def maps():
    return render_template('maps.html')


@app.route('/preferences')
def preferences():
    return render_template('preferences.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# 把查询结果转换为json
def new_alchemy_encoder():
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                sts = obj
                str = dir(obj)
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    data = obj.__getattribute__(field)
                    try:
                        if isinstance(data, datetime.time):
                            data = data.strftime('%H:%M')
                            json.dumps(data)
                        elif isinstance(data, List):
                            data = list2dict(data)
                        else:
                            json.dumps(data)
                        fields[field] = data
                    except TypeError:
                        fields[field] = None
                return fields

                return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder


def list2dict(obj):
    fields = {}

    for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
        data = obj.__getattribute__(field)
        try:
            if isinstance(data, datetime.time):
                data = data.strftime('%H:%M')
            json.dumps(data)  # this will fail on non-encodable values, like other classes
            fields[field] = data
        except TypeError:
            fields[field] = None

    return fields


def object2dict(obj):
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                sts = obj
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    data = obj.__getattribute__(field)
                    try:
                        if isinstance(data, datetime.time):
                            data = data.strftime('%H:%M')
                            json.dumps(data)
                        elif isinstance(data, List):
                            data = list2dict(data)
                        else:
                            json.dumps(data)
                        fields[field] = data
                    except TypeError:
                        fields[field] = None
                return fields

    return AlchemyEncoder


def taskjson(date_object):
    tasks = Task.query.filter_by(date=date_object)
    try:

        task_host = []
        for task in tasks:
            task_host.append(task)
        taskjson = json.dumps(task_host, cls=new_alchemy_encoder(), check_circular=False)

        return taskjson
    except Exception as e:
        print(e)


def listjson():
    lists = db.session.query(List).order_by(List.list_order)

    try:

        Hosts = []
        for list in lists:
            # print json.dumps(vmc, cls=AlchemyEncoder)
            Hosts.append(list)
        listjson = json.dumps(Hosts, cls=new_alchemy_encoder(), check_circular=False)
        print("listjson" + listjson)
        return listjson
    except Exception as e:
        print(e)


def str_to_date(str):
    str_year = str[0:4]
    str_mouth = str[5:7]
    str_day = str[8:10]
    date_object = datetime.date(int(str_year), int(str_mouth), int(str_day))
    return date_object


def day_statistics(date_str):
    date_object = str_to_date(date_str)
    tasks = db.session.query(func.sum(Task.actual_time), List.listname, ). \
        join(List).filter(Task.date == date_object, Task.actual_time > 0). \
        group_by(Task.list_id).order_by(desc(func.sum(Task.actual_time)))
    task_list = []
    for task in tasks:
        data = {
            "listname": task[1],
            "time_sum": task[0]
        }
        task_list.append(data)
    json.dumps(task_list)
    print(json.dumps(task_list))
    return json.dumps(task_list)


# 给清单添加排序用的序号
def define_list_order(listname_str, order):
    List.query.filter(List.listname == listname_str).update({List.list_order: order})
    db.session.commit()
    print(List.query.filter(List.listname == listname_str)[0].list_order)


if __name__ == '__main__':
    manager.run()
    #
    # app.run(host="0.0.0.0",port=8080, debug=True)
    # app.run(debug=True)
