from flask import render_template , redirect , url_for , flash , request , abort
from TodoList import app , db
from TodoList.forms import SignForm , LoginForm , ToDoForm
from TodoList.models import User , Todo
from TodoList import bcrypt 
from flask_login import login_user , current_user , logout_user , login_required

@app.route('/' , methods = ['GET' , 'POST'])
def HomePage():
    title = "ToDoList"
    form = ToDoForm()
    if current_user.is_authenticated:
        user = current_user
        Todos = Todo.query.filter_by(user_id = current_user.id).all() 
        return render_template("homepage.html" , title = title , user = user , form = form , Todos = Todos)
    
    user = current_user

    return render_template("homepage.html" , title = title , form = form , user = user)


@app.route('/Sign' , methods = ['GET' , 'POST'])
def Sign():
    title = "Sign"
    form = SignForm()
    if current_user.is_authenticated:
        return redirect(url_for("HomePage"))
    
    if form.validate_on_submit():
        hashed_password =  bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data , email = form.email.data , password =  hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!" , "success")
        return redirect(url_for("HomePage"))
    return render_template("Sign.html" , title = title , form = form , user = current_user)

@app.route('/Login' , methods = ["GET" , "POST"])
def Login():
    title = "Login"
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("HomePage"))
    
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user , remember=True)
            flash(f"You have been logged in!" , "success")
            return redirect(url_for("HomePage"))
        else:
            flash(f"Login Unsuccessful. Please check email and password" , "danger")
            return redirect(url_for("Login"))

    return render_template("Login.html" , title = title , form = form , user = current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("HomePage"))

@app.route('/Todo/Add' , methods = ['GET' , 'POST'])
@login_required
def Add_Todo():
    form = ToDoForm()

    if request.method == 'POST':
        todo = Todo(title = form.title.data , user_id = current_user.id)
        db.session.add(todo)
        db.session.commit()
        flash(f"New Todo Added!" , "success")
        print(todo)
        return redirect(url_for("HomePage"))
    else:
        flash(f"Some Thing Went Wrong , Try Again" , "danger")
        

    return redirect(url_for('HomePage'))

@app.route('/Todo/<int:todo_id>/Description' , methods = ['GET' , 'POST'])
@login_required
def Add_Description(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if todo.author != current_user:
        abort(403)

    print(request.form['description'])

    if request.method == "POST" and request.form['description'] != '':
        todo.description = request.form['description']
        db.session.commit()
        flash(f"Description Added!" , "success")
    


    return redirect(url_for('HomePage'))

@app.route('/Todo/<int:todo_id>/Achieve' , methods = ['GET' , 'POST'])
@login_required
def Achieve_Todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if todo.author != current_user:
        abort(403)

    if request.method == "POST" and todo.achived == False:
        todo.achived = True
        db.session.commit()
        flash(f"Congratulation you Achived Todo !" , "success")
    


    return redirect(url_for('HomePage'))

@app.route('/Todo/<int:todo_id>/UnAchieve' , methods = ['GET' , 'POST'])
@login_required
def Un_Achieve_Todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if todo.author != current_user:
        abort(403)

    if request.method == "POST" and todo.achived == True:
        todo.achived = False
        db.session.commit()
        flash(f"You Un Achived the Todo !" , "success")
    


    return redirect(url_for('HomePage'))

@app.route('/Todo/<int:todo_id>/Delete' , methods = ['POST'])
@login_required
def Delete_Todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if todo.author != current_user:
        abort(403)

    if request.method == "POST" and todo:
        db.session.delete(todo)
        db.session.commit()
        flash(f"Todo has been Deleted" , "success")

    return redirect(url_for('HomePage'))