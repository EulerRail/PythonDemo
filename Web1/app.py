from flask import Flask,request,render_template,jsonify
import json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/text',methods=['POST'] )
def login():
    text = request.get_json()['text']
    id = request.get_json()['id']
    print(text,id)
    ip_address = request.remote_addr
    return jsonify({"text":ip_address})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
