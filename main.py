from src import connect, db

if __name__ == "__main__":
    app = connect()
    app.run(debug=True, port=5000)

    db.create_all()
