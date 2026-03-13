from flask import Flask, render_template,request,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin,logout_user
from datetime import datetime

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
app.config['SECRET_KEY']='thisissecret'
# initialize the app with the extension
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(200),unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250),unique=True ,nullable=False)
    fname = db.Column(db.String(250), nullable=False)
    lname = db.Column(db.String(250), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username
    

class Blog(db.Model):
    blog_id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    content=db.Column(db.Text(), nullable=False)
    pub_date = db.Column(db.DateTime(),default=datetime.utcnow)

    def __repr__(self):
        return '<Blog %r>' % self.title


with app.app_context():
    db.create_all()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/') # Blank URL
def home():
    data = Blog.query.all()
    return render_template('home.html',data=data)

@app.route('/main') # main URL
def main():
    return render_template("main.html")

@app.route('/register',methods=['GET','POST']) # register URL
def register():
    if request.method == 'POST':
        email = request.form.get('email')  # email fetch field on register
        password = request.form.get('password') 
        username = request.form.get('uname') 
        first_name = request.form.get('fname')
        last_name = request.form.get('lname') 
       # print(email,password,username,fname,lname) # we want to check user pass the info here it is fetch or not
        user = User(username=username,email=email,password=password,fname=first_name,lname = last_name)
        db.session.add(user)
        db.session.commit()
        flash('User has been Registered Succesfully','Success') # 'message','error or suuccess type'
        return redirect('/login')

    return render_template("register.html")

@app.route('/login' ,methods=['GET','POST']) # login URL
def login():
    if request.method =='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user  and password == user.password:
            login_user(user)
            return redirect('/')
        
        elif not username or not password:
            flash('Please fill in both Username and Password' , 'warning')
            return redirect('/login')
       
        else:
            flash('Invalid Username or Password' , 'danger')
            return redirect('/login')
    return render_template("login.html")


@app.route('/logout') 
def logout():
    logout_user()
    return redirect('/')


@app.route('/blogpost' , methods=['GET','POST']) 
def blogpost():
     
    if request.method == 'POST':
        title = request.form.get('title')  # email fetch field on register
        author = request.form.get('Author') 
        content = request.form.get('content') 
       # print(email,password,username,fname,lname) # we want to check user pass the info here it is fetch or not
        blog_user = Blog(title=title,author=author,content=content)
        db.session.add(blog_user)
        db.session.commit()
        flash('Blog post has been created successfully!', 'success') # 'message','error or suuccess type'
        return redirect('/')
    return render_template('blog.html')


@app.route('/blog_details/<int:id>',methods=['GET','POST'])
def blog_detail(id):
    blog = Blog.query.get(id)
    return render_template('blog_detail.html',blog=blog)

@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete_post(id):
    blog = Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    flash("Post has been deleted",'success')
    return redirect('/')

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit_post(id):
    blog = Blog.query.get(id)
    if request.method == 'POST':
        blog.title = request.form.get('title')  # email fetch field on register
        blog.author = request.form.get('Author') 
        blog.content = request.form.get('content') 
        db.session.commit()
        flash('Post has been Updated', 'success') # 'message','error or suuccess type'
        return redirect('/')
    return render_template('edit.html',blog=blog)

if __name__ == "__main__":
    app.run(debug=True)