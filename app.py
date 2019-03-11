import startThread
from flask import Flask,render_template,request,url_for
import  UDPSocket

app = Flask(__name__,template_folder='templates')


@app.route('/test', endpoint="xxx")
def test():
    v = url_for("xxx")
    print(v)
    
    
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)

