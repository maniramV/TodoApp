from flask import Flask, render_template, url_for, request, session, redirect
import mysql.connector
app = Flask(__name__)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mahesh",
  database="taskdb"
)

@app.route('/')
def hello_world():
	print(mydb)
	return render_template('login.html')

@app.route('/login', methods=['POST','get'])
def login():
	if request.method=="POST":
		uname=request.form['name']
		upass=request.form['pass']
		mycursor = mydb.cursor()
		val=""
		sql = "SELECT * FROM taskdb.users WHERE name = %s and pass = %s"
		adr = (uname,upass)
		mycursor.execute(sql,adr)
		myresult = mycursor.fetchall()
		if(myresult):
			session['username'] = uname
			session['userperm'] = myresult[0][2]
			print(myresult[0][2])
			mycursor = mydb.cursor()
			sql = "SELECT * FROM taskdb.task"
			mycursor.execute(sql)
			myresult = mycursor.fetchall()
			print(myresult)
			return render_template('dashboard.html',mydata=myresult)
		else:
			val="Invalid username or password"
			return render_template('login.html',val=val)
	else:
		return render_template('login.html')

@app.route('/register', methods=['POST','get'])
def register():
	val=""
	if request.method=="POST":
		uname=request.form['name']
		upass=request.form['pass']
		uperm=request.form['userperm']
		mycursor = mydb.cursor()
		sql = "INSERT INTO taskdb.users (name,pass,userperm) VALUES (%s, %s ,%s)"
		val = (uname,upass,uperm)
		mycursor.execute(sql, val)
		mydb.commit()
		return render_template('login.html',val="Registerd successfully....")
	else:
		return render_template('register.html')

@app.route('/insert1', methods=['POST','GET'])
def insert1():
	mycursor = mydb.cursor()
	sql = "SELECT * FROM taskdb.task"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	print(myresult)
	if(session['userperm']=="read"):
		return render_template("dashboard.html",mydata=myresult,val="You are not permitted to insert records..")
	return render_template('index.html')
@app.route('/insert', methods=['POST'])
def insert():
	if request.method=="POST":
		taskname=request.form['name']
		duedate=request.form['date']
		status=request.form['status']
		taskdesc=request.form['desc']
		id=request.form['id']
		mycursor = mydb.cursor()
		sql = "INSERT INTO task (taskname, duetime, status, taskdesc,id) VALUES (%s, %s, %s, %s,%s)"
		val = (taskname,duedate,status,taskdesc,id)
		mycursor.execute(sql, val)
		mydb.commit()
		mycursor = mydb.cursor()
		sql = "SELECT * FROM taskdb.task"
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		print(myresult)
		return render_template('dashboard.html',mydata=myresult)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
	if request.method=="POST":
		if session['userperm']=="write":
			mycursor = mydb.cursor()
			sql = "SELECT * FROM taskdb.task WHERE id = %s"
			adr=request.form['id1']
			print("----------",adr)
			mycursor.execute(sql,(adr,))
			myresult = mycursor.fetchall()
			print(myresult)
			return render_template('update.html',data=myresult)
		else:
			val="You have no permission to modify this task..."
			mycursor = mydb.cursor()
			sql = "SELECT * FROM taskdb.task"
			mycursor.execute(sql)
			myresult = mycursor.fetchall()
			print(myresult)
			return render_template('dashboard.html',val=val,mydata=myresult)
	return "nothing"
@app.route('/update', methods=['GET', 'POST'])
def update():
	if request.method=="POST":
		taskname=request.form['name']
		duedate=request.form['date']
		status=request.form['status']
		taskdesc=request.form['desc']
		id1=request.form['id']
		mycursor = mydb.cursor()
		sql = "UPDATE task SET taskname = %s, duetime = %s ,status = %s, taskdesc = %s WHERE id=%s"	
		val = (taskname,duedate,status,taskdesc,id1)
		mycursor.execute(sql, val)
		mydb.commit()
		mycursor = mydb.cursor()
		sql = "SELECT * FROM taskdb.task"
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		print(myresult)
		return render_template('dashboard.html',mydata=myresult)

@app.route('/logout')
def logout():
	session.clear()
	print("logged out")
	return render_template('login.html')

if __name__ == '__main__':
	app.secret_key = 'mysecret'
	app.run(debug=True)

