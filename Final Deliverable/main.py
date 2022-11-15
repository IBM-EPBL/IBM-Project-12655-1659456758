from flask import Flask, render_template, request
from Model import predict
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/prediction',methods=['POST','GET'])
def prediction():
    args = [i for i in request.form.values()]
    args = tuple(args[:3])
    out = int(predict(*args)[0])
    if out == 0:
        return render_template("index.html",output_text="Flight will arrive at the scheduled time ...")
    elif out==1:
        return render_template("index.html",output_text="Flight may be delayed by 15 minutes or more ...")
    else:
        return render_template("index.html",output_text="Invalid source or destination !!!")
        

if __name__ == '__main__':
    app.run()