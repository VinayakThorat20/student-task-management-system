from flask import Flask, render_template, request, redirect, session
import mysql.connector
from datetime import date

app = Flask(__name__)
app.secret_key = "secretkey123"

# MySQL Connection
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="@Vinayakst1104",
    database="student_task_db"
)
cursor = db.cursor(dictionary=True)

# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']

            if user['role'] == 'admin':
                return redirect('/admin')
            else:
                return redirect('/student')

    return render_template('login.html')


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        cursor.execute(
            "INSERT INTO users(name,email,password,role) VALUES(%s,%s,%s,%s)",
            (
                request.form['name'],
                request.form['email'],
                request.form['password'],
                request.form['role']
            )
        )
        db.commit()
        return redirect('/')
    return render_template('register.html')


# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('role') != 'admin':
        return redirect('/')

    # Add Task
    if request.method == 'POST':
        cursor.execute(
            "INSERT INTO tasks(title,description,due_date,student_id) VALUES(%s,%s,%s,%s)",
            (
                request.form['title'],
                request.form['description'],
                request.form['due'],
                request.form['student']
            )
        )
        db.commit()

    cursor.execute("SELECT * FROM users WHERE role='student'")
    students = cursor.fetchall()

    cursor.execute("""
        SELECT tasks.*, users.name 
        FROM tasks JOIN users ON tasks.student_id = users.id
    """)
    tasks = cursor.fetchall()

    return render_template(
        'admin.html',
        students=students,
        tasks=tasks,
        today=date.today()
    )


# ---------------- DELETE TASK (ADMIN) ----------------
@app.route('/delete/<int:id>')
def delete_task(id):
    if session.get('role') == 'admin':
        cursor.execute("DELETE FROM tasks WHERE id=%s", (id,))
        db.commit()
    return redirect('/admin')


# ---------------- STUDENT DASHBOARD ----------------
@app.route('/student', methods=['GET', 'POST'])
def student():
    if session.get('role') != 'student':
        return redirect('/')

    if request.method == 'POST':
        cursor.execute(
            "UPDATE tasks SET status='Completed' WHERE id=%s",
            (request.form['task_id'],)
        )
        db.commit()

    cursor.execute(
        "SELECT * FROM tasks WHERE student_id=%s",
        (session['user_id'],)
    )
    tasks = cursor.fetchall()

    return render_template(
        'student.html',
        tasks=tasks,
        today=date.today()
    )


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
