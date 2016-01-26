import datetime,time

from flask import Flask, render_template, url_for, jsonify, request,redirect
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import create_engine
import os
import sqlite3
from flask_restful import fields, marshal
import json

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


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

    date = datetime.date.today()


    return render_template('manage-users.html', taskjson=taskjson(), list_id=1,date = date)


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

        task = Task.query.filter_by(id=task_id).first()
        if name == 'taskname':
            task_add = Task(taskname=value, list_id=list_id,date = task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.taskname = value
                db.session.add(task)

            db.session.commit()

        elif name == 'listname':
            list = List.query.filter_by(listname=value).first()
            if list is None:
                status  = 'false'
            else :
                if task is None:
                    task_add = Task(list_id=list.id,date = task_date_object )
                    db.session.add(task_add)
                else:
                    task.list_id = list.id
                    db.session.add(task)

        elif name == 'start_time':
            hour = value[0:2]
            minute = value[3:5]
            value = datetime.time(int(hour),int(minute),00)
            task_add =  Task(start_time=value, list_id=list_id,date = task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.start_time = value
                db.session.add(task)
            db.session.commit()

        elif name == 'thought':
            task_add =  Task(thought=value, list_id=list_id,date = task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.thought = value
                db.session.add(task)
            db.session.commit()

        elif name == 'scheduled_time':
            task_add = Task(scheduled_time=value, list_id=list_id,date = task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.scheduled_time = value
                db.session.add(task)
            db.session.commit()

        elif name == 'efficiency':
            task_add = Task(efficiency=value, list_id=list_id,date = task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.efficiency = value
                db.session.add(task)
            db.session.commit()

        elif name == 'summary':
            task_add = Task(summary=value, list_id=list_id,date = task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.summary = value
                db.session.add(task)
            db.session.commit()

        elif name == 'end_time':
            hour = value[0:2]
            minute = value[3:5]
            value = datetime.time(int(hour),int(minute),00)
            task_add = Task(end_time=value, list_id=list_id,date = task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.end_time = value
                db.session.add(task)
            db.session.commit()

        elif name == 'actual_time':
            task_add = Task(actual_time=value, list_id=list_id,date = task_date_object)
            if task is None:
                db.session.add(task_add)
            else:
                task.actual_time = value
                db.session.add(task)
            db.session.commit()

        if task_id== ' ' :
            task_id =  task_add.id


        return jsonify(status=status,task_id = task_id )


@app.route('/deletetask',methods=['GET','POST'])
def deletetask():

    if request.method=='POST':
        task_id  = request.form.get('task_id')
        task = Task.query.filter_by(id=task_id).first()
        if task is not None:
            db.session.delete(task)
            db.session.commit()

    return jsonify()

@app.route('/addlist',methods=['GET','POST'])
def addlist():
    status =''
    if request.method == 'POST':
        list_name = request.form.get('list_name')
        list = List.query.filter_by(listname=list_name).first()
        if list is None:
            db.session.add(List(listname=list_name))
            db.session.commit()
        else:
            status = 'false'
    return jsonify(status=status)


@app.route('/tasks/<listname>',methods=['GET','POST'] )
def tasks(listname):


    calender_date = request.args.get('date')
    calender_date_object = str_to_date(calender_date)
    # 查询当前日期下所有task
    if listname == '全部':
        tasks = Task.query.filter_by(date=calender_date_object)
        list_id = 0
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
        print('taskjson'+taskjson)
        return render_template('manage-users.html', taskjson=taskjson, list_id=list_id, date =calender_date )

    except Exception as e:
        print(e)








@app.route('/datavisualization')
def datavisualization():

    return render_template('data-visualization.html')

@app.route('/indexs')
def indexs():
    return render_template('indexs.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/manageusers')
def manageusers():
    return render_template('manage-users.html')

@app.route('/manage')
def manage():
    return render_template('manage.html')

@app.route('/maps')
def maps():
    return render_template('maps.html')

@app.route('/preferences')
def preferences():
    return render_template('preferences.html')

@app.route('/edit1')
def edit1():
    return render_template('edit.html')

@app.route('/edit2')
def edit2():
    return render_template('edit2.html')

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
                            data=data.strftime('%H:%M')
                            json.dumps(data)
                        elif isinstance(data, List):
                            data = list2dict(data)
                        else :json.dumps(data)
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
                data=data.strftime('%H:%M')
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
                            data=data.strftime('%H:%M')
                            json.dumps(data)
                        elif isinstance(data, List):
                            data = list2dict(data)
                        else :json.dumps(data)
                        fields[field] = data
                    except TypeError:
                        fields[field] = None
                return fields

  return AlchemyEncoder

                # return json.JSONEncoder.default(self, obj)



def taskjson():
    tasks = Task.query.all()
    try:

        task_host = []
        for task in tasks:
            task_host.append(task)
        taskjson = json.dumps(task_host, cls=new_alchemy_encoder(), check_circular=False)

        return taskjson
    except Exception as e:
        print(e)

def listjson():
    lists = List.query.all()
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
def str_to_date (str):
     str_year = str[0:4]
     str_mouth = str[5:7]
     str_day = str[8:10]
     date_object = datetime.date(int(str_year),int(str_mouth),int(str_day))
     return date_object

if __name__ == '__main__':

    app.run(debug=True)
