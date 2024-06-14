from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
mydb = mysql.connector.connect(
    host="project-database.chwdu6kczeib.us-east-1.rds.amazonaws.com",
    user="admin",
    password="Kupa1234",
    database="project"
)
cursor = mydb.cursor()

@app.route('/')
def home():
    # READ ALL RECORDS
    cursor.execute("SELECT * FROM książki ORDER BY title")
    all_books = cursor.fetchall()
    return render_template("index.html", books=all_books)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD
        new_book = (request.form["title"], request.form["author"], request.form["rating"])
        cursor.execute("INSERT INTO książki (title, author, rating) VALUES (?, ?, ?)", new_book)
        conn.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # UPDATE RECORD
        book_id = request.form["id"]
        rating = request.form["rating"]
        cursor.execute("UPDATE książki SET rating = ? WHERE id = ?", rating, book_id)
        conn.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    cursor.execute("SELECT * FROM książki WHERE id = ?", book_id)
    book_selected = cursor.fetchone()
    return render_template("edit_rating.html", book=book_selected)

@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    # DELETE A RECORD BY ID
    cursor.execute("DELETE FROM książki WHERE id = ?", book_id)
    conn.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()
