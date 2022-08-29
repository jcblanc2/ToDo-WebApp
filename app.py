from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.secret_key = "Srtwcvxz6&^$y"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50))
    date = db.Column(db.String(50))


current_date = datetime.datetime.now()


@app.route('/')
def index():
    global list_todo
    global dict_of_date_id

    list_todo = Task.query.all()

    dict_of_date_id = {}
    for row in list_todo:
        dict_of_date_id[row.id] = row.date
    return render_template('index.html', list_todo=list_todo)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add', methods=['POST'])
def add():
    if len(list_todo) == 7:
        last_id = min(dict_of_date_id.values())
        task = Task.query.filter_by(date=last_id).first()
        db.session.delete(task)
        db.session.commit()

        task = request.form.get('task')
        new_todo = Task(task=task, date=current_date)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        task = request.form.get('task')
        new_todo = Task(task=task, date=current_date)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/update/<int:todo_id>')
def update(todo_id):
    global list_todo
    global id_to_update

    id_to_update = todo_id
    list_todo = Task.query.all()
    return render_template('update.html', list_todo=list_todo, id_to_update=id_to_update)


@app.route('/edit', methods=['POST'])
def edit():
    new_task = request.form.get('task')

    task_to_update = Task.query.filter_by(id=id_to_update).first()

    task_to_update.task = new_task
    task_to_update.date = datetime.datetime.now()

    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    task = Task.query.filter_by(id=todo_id).first()

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
