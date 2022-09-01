
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route("/")

def index():
    return (render_template('index.html'))

@app.route("/start", methods=['GET', 'POST'])

def start():
    import pandas as pd
    if request.method == "POST":
        import sqlite3
        connection = sqlite3.connect('transactions.db')
        cursor = connection.cursor()
        amount = request.form.get('amount')
        description = request.form.get('description')
        category = request.form.get('category')

        cursor.execute(f"""INSERT INTO transactions (amount, description, category)
                            VALUES (?,?,?)""", (amount, description, category))
        
        data = pd.read_sql("SELECT * FROM transactions", connection)
        data = data.reset_index(drop=True)
        final = data.to_string()
        cursor.close()
        connection.commit()

        
        return(render_template('start.html', value = final))
    else:
        return(render_template('start.html'))

@app.route('/clear')
def clear():
    import sqlite3
    connection = sqlite3.connect('transactions.db')
    cursor = connection.cursor()

    cursor.execute("DELETE FROM transactions")
    cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='transactions'")
    cursor.close()
    connection.commit()
    print('DATABASE CLEARED...')
    return redirect('/start')



