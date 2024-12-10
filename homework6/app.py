from flask import Flask, render_template, request, redirect, url_for

import models
from connection import get_db

app = Flask(__name__)
models.init_db()



# Главная страница
@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    users = cursor.execute('SELECT * FROM users').fetchall()
    test_stands = cursor.execute('SELECT * FROM stands').fetchall()
    bookings = cursor.execute('SELECT * FROM bookings').fetchall()
    print(users)
    print(test_stands)
    print(bookings)
    cursor.close()
    return render_template('index.html', users=users, test_stands=test_stands, bookings=bookings)

# Страница для добавления нового пользователя
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        last_name = request.form['last_name']
        first_name = request.form['first_name']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (last_name, first_name) VALUES (?, ?)", (last_name, first_name))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_user.html')

# Страница для добавления нового стенда
@app.route('/add_stand', methods=['GET', 'POST'])
def add_stand():
    if request.method == 'POST':
        stand_type = request.form['stand_type']
        operating_system = request.form['operating_system']
        os_version = request.form['os_version']
        ip_address = request.form['ip_address']
        cpu_count = int(request.form['cpu_count'])
        memory_size = int(request.form['memory_size'])
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO stands (stand_type, operating_system, os_version, ip_address, cpu_count, memory_size) VALUES (?, ?, ?, ?, ?, ?)",
                     (stand_type, operating_system, os_version, ip_address, cpu_count, memory_size))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_stand.html')


# Страница для бронирования оборудования
@app.route('/make_booking', methods=['GET', 'POST'])
def make_booking():
    conn = get_db()
    cursor = conn.cursor()
    users = cursor.execute('SELECT * FROM users').fetchall()
    print(users)
    stands = cursor.execute('SELECT * FROM stands').fetchall()
    print(stands)
    cursor.close()

    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        stand_id = int(request.form['stand_id'])
        start_time = request.form['start_time']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bookings (user_id, stand_id, start_time) VALUES (?, ?, ?)",
                     (user_id, stand_id, start_time))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('make_booking.html', users=users, stands=stands)


# Страница для изменения статуса бронирования
@app.route('/update_status/<int:booking_id>', methods=['GET', 'POST'])
def update_status(booking_id):
    conn = get_db()
    cursor = conn.cursor()
    booking = cursor.execute('SELECT * FROM bookings WHERE id = ?', (booking_id,)).fetchone()
    cursor.close()

    if request.method == 'POST':
        completed = request.form['completed']
        end_time = request.form['end_time'] if completed else None

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE bookings SET completed = ?, end_time = ? WHERE id = ?",
                     (completed, end_time, booking_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('update_status.html', booking=booking)


if __name__ == '__main__':
    app.run(debug=True)
