from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"ID: {self.id}\nTask: {self.title}\nDescription: {self.description}\nDone: {self.done}"

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_title = request.form['title']  # Change from 'content' to 'title'
        task_description = request.form['description']  # Ensure the form includes this field
        new_task = MyTask(title=task_title, description=task_description)  # Use title and description fields
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error adding task: {e}"
    else:
        tasks = MyTask.query.all()
        return render_template('index.html', tasks=tasks)



@app.route('/delete/<int:id>')
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Error deleting task: {e}"

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error editing task: {e}"
    else:
        return render_template('edit.html', task=task)
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080)
