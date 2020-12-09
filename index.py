from flask import Flask, render_template

app: Flask = Flask(__name__)

@app.route('/test')
def test() -> str:
    return "Testing server"

app.run(debug=True)