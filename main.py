
from flask import Flask, render_template, request, redirect
import os
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

app = Flask(__name__)
picFolder = os.path.join('static', 'pictures')
app.config['UPLOAD_FOLDER'] = picFolder
@app.route("/")

def index():
    return (render_template('index.html'))

@app.route("/start", methods=['GET', 'POST'])

def start():
    if request.method == "POST":
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
        category_df = pd.read_sql('SELECT category, SUM(amount) AS amount_spent FROM transactions GROUP BY category', connection)
        print(category_df['category'])
        fig, ax = plt.subplots()
        ax.pie(category_df['amount_spent'], labels=category_df['category'], autopct='%1.1f%%')
        fig.savefig('static\pictures\plot.png', transparent=True)

        graph = os.path.join(app.config['UPLOAD_FOLDER'], 'plot.png')



        return(render_template('start.html', value = final, plot_image = graph))
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





