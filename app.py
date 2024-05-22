from flask import Flask, render_template, request
import google.generativeai as palm
import replicate
import os
import csv


flag = 1
name = ""

makersuite_api = os.getenv("MAKERSUITE_API_TOKEN")
palm.configure(api_key=makersuite_api)

def get_user_name(username):
    csv_file_path = "Users.csv"
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:
            if row[0] == username:
                return row[1]
    return None


model = {"model" : "models/chat-bison-001"}
app = Flask(__name__)

@app.route("/",methods = ["GET","POST"])
def index():
    return(render_template("index.html"))




@app.route("/main",methods = ["GET","POST"])

def main():
    global flag, name, get_user_name
    if flag == 1:
        username1 = request.form.get("User")
        name = get_user_name(username1)   
        flag = 0
        if name==None:
            return(render_template("error.html"))
    return(render_template("main.html",r=name))


@app.route("/prediction",methods = ["GET","POST"])
def prediction():
    return(render_template("prediction.html"))

@app.route("/dbs_price",methods = ["GET","POST"])
def dbs_price():
    q = float(request.form.get("q"))
    return(render_template("dbs_price.html",r=(q*-50.6)+90.2))

@app.route("/generate_text",methods = ["GET","POST"])
def generate_text():
    return(render_template("generate_text.html"))

@app.route("/text_result_makersuite",methods = ["GET","POST"])
def text_result_makersuite():
    age = str(request.form.get("age"))
    risk = request.form.get("risk")
    inv = str(request.form.get("investmentyears"))
    r = palm.chat(**model, messages="Please provide financial advise to a {} year old person who has {} risk tolerance and a {} investment horizon".format(age,risk,inv))
    return(render_template("text_result_makersuite.html",r=r.last))

@app.route("/generate_image",methods = ["GET","POST"])
def generate_image():
    return(render_template("generate_image.html"))

@app.route("/image_result",methods = ["GET","POST"])
def image_result():
    q = request.form.get("q")
    r = replicate.run("stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
      input = {"prompt":q}
    )
    return(render_template("image_result.html",r=r[0]))

@app.route("/end",methods = ["GET","POST"]) 
def end():
    global flag
    flag = 1
    return(render_template("index.html"))


if __name__ == "__main__":
    app.run()
