from app import app

app.secret_key = 'agrigrenierkeysecret'
if __name__ == "__main__":
    app.run(debug=True)