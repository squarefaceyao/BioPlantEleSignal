from flask import Flask,render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/index')
def home1():
    # return render_template("index.html")
    return home()


@app.route('/index.html')
def index():
    return home()


@app.route('/movie')
def movie():
    datalist = []
    con=sqlite3.connect("movie.db")
    cur=con.cursor()
    sql = "select * from movie"
    data = cur.execute(sql)
    for item in data:  #若执行后直接关掉数据库相应的数据也会消失
        datalist.append(item)
    cur.close()
    con.close()
    return render_template("movie.html",movies=datalist)


@app.route('/score')
def score():
    datalist = []
    score = []  #评分
    num = []    #评分人数
    con=sqlite3.connect("movie.db")
    cur=con.cursor()
    sql = "select score,count(score) from movie group by score"
    data = cur.execute(sql)

    for item in data:  #若执行后直接关掉数据库相应的数据也会消失
        score.append(item[0])  #str(item[0])
        num.append(item[1])

    cur.close()
    con.close()

    return render_template("score.html",score=score,num=num)


@app.route('/clouds')
def clouds():
    return render_template("clouds.html")


@app.route('/team')
def team():
    return render_template("team.html")


@app.route('/test')
def test():
    return render_template("test.html")



if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
