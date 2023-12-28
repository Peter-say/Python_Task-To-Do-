from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import sys
from pprint import pprint

app = Flask(__name__)

# Set the secret key
app.secret_key = "]{\\\xa0\x9e\xb4~\xdf\xd5\xcf\xca\xd6z\xfa2mI\xf3\x96\xd0\xb2\x04\x92\x00"

app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/task_manager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.use_x_sendfile = False


db = SQLAlchemy(app)
class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_description = request.form.get('taskDescription')
    task_image = None  # Initialize task_image outside of the if block

    # Handle file upload
    if 'image' in request.files:
        task_image = request.files['image']

        if task_image.filename != '' and allowed_file(task_image.filename):
            # Process the file (save, resize, etc.)
            filename = secure_filename(task_image.filename)
            task_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Invalid file type', 'error')

    new_task = Task(description=task_description, image=task_image.filename if task_image else None)
    db.session.add(new_task)
    db.session.commit()
    flash("Task created successfully", 'success')
    return redirect('/')
@app.route('/remove_task/<int:task_id>')
def remove_task(task_id):
    try:
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            flash(f"Task '{task_id}' removed successfully", 'success')
        else:
            flash('Invalid task ID: {}'.format(task_id), 'error')
    except Exception as e:
        flash('Error: {}'.format(e), 'error')

    return redirect(url_for('index'))





@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    pprint(task)
    
    if task is None:
        flash(f'Task with ID {task_id} not found', 'error')
        return redirect(url_for('index'))

    # Initialize variables with existing values or request.form values
    task_description = task.description or request.form.get('newDescription')
    task_image = task.image or None

    # Handle file upload
    if 'image' in request.files:
        new_task_image = request.files['image']

        if new_task_image.filename != '' and allowed_file(new_task_image.filename):
            # Process the file (save, resize, etc.)
            filename = secure_filename(new_task_image.filename)
            new_task_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            task_image = filename  # Use the filename instead of the file object
        else:
            flash('Invalid file type', 'error')

    # Update the task with the new values
    task.description = task_description
    task.image = task_image if task_image else None
    db.session.commit()

    flash(f'Task {task_id} updated successfully', 'success')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
    with app.app_context():
        # Create the database table
        db.create_all()



 