from app import create_app

app = create_app()
app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)
