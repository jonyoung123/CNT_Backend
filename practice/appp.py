from flask import Flask

app = Flask(__name__)


@app.route('/')
def show_num():
    num = []
    for i in range(5):
        num.append(i)
    return num


@app.route('/greet', methods=['GET'])
def greet():
    return "Hi, How are you doing"


if __name__ == "__main__":
    app.run(debug=True)
