from src import connect, db

app = connect()


if __name__ == "__main__":
    app.run(debug=True, port=5000)

    db.create_all()
