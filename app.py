from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Pigboy11!@localhost/writePage'
db = SQLAlchemy(app)
app.secret_key = '8063'


class User(db.Model):
    __tablename__ = 'userPID_post'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False) #이거 사용자 아이디입니다
    password = db.Column(db.String(255), nullable=False)
    passwordcheck = db.Column(db.String(255), nullable=False)
    Pname = db.Column(db.String(255), nullable=False)
    


class AllPost(db.Model):
    __tablename__ = 'all_post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    
class ChatPost(db.Model):
    __tablename__ = 'chat_post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)

class RequestPost(db.Model):
    __tablename__ = 'request_post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)

class RoommatePost(db.Model):
    __tablename__ = 'roommate_post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    
class TogetherPost(db.Model):
    __tablename__ = 'together_post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    
    

@app.route('/')
def splash():
    return render_template('Splash.html')


@app.route('/Login_main')
def Lmain():
    return render_template('Login_main.html')

@app.route('/Login_main/submit', methods=['GET', 'POST'])
def Lmain_submit():
    if request.method == 'POST':
        input_name = request.form['write_id']
        input_password = request.form['write_pw']


        user = User.query.filter_by(name=input_name).first()

        if user and user.password == input_password:
            # 비밀번호가 일치하면 로그인 성공
            session['name'] = input_name
            return redirect(url_for('onboarding1'))
        else:
            # 비밀번호가 일치하지 않으면 로그인 실패
            return redirect(url_for('Lmain'))
        
@app.route('/Home')
def Lmain_home():
    input_name = session.get('name')
    user = User.query.filter_by(name=input_name)
    return render_template('Home.html', user=user)

@app.route('/Login1')
def L1():
    return render_template('Login1.html')

@app.route('/Login1-1')
def L1_1():
    return render_template('Login1-1.html')

@app.route('/Login2')
def L2():
    return render_template('Login2.html')

@app.route('/Login2/submit', methods= ['GET', 'POST'])
def L2_submit():
    if request.method == 'POST':
        name = request.form['write_id']
        password = request.form['write_pw']
        passwordcheck = request.form['write_pw_check']
        # Pname = request.form['Pname']

        if password == passwordcheck:
            new_post = User(name=name, password=password, passwordcheck=passwordcheck)
            session['name'] = name
        elif password!=passwordcheck :
            return redirect(url_for('L2'))

        db.session.add(new_post)
        db.session.commit()

    return redirect(url_for('L3'))

@app.route('/Login3')
def L3():
    return render_template('Login3.html')

@app.route('/Login3/submit', methods= ['GET', 'POST'])
def L3_submit():
    if request.method == 'POST':
        input_name = session.get('name')
        Pname = request.form['Pname']

        user = User.query.filter_by(name=input_name).first()

        if user :
            user.Pname = Pname
            db.session.commit()

    return redirect(url_for('L4'))

@app.route('/Login4')
def L4():
    return render_template('Login4.html')

@app.route('/Login5')
def L5():
    return render_template('Login5.html')

@app.route('/Home')
def home():
    input_name = session.get('name')
    user = User.query.filter_by(name=input_name)
    return render_template('Home.html', user=user)

@app.route('/Onboarding1')
def onboarding1():
    return render_template('Onboarding1.html')

@app.route('/Onboarding2')
def onboarding2():
    return render_template('Onboarding2.html')

@app.route('/Onboarding3')
def onboarding3():
    return render_template('Onboarding3.html')

@app.route('/Home')
def buttonHome():
    input_name = session.get('name')
    user = User.query.filter_by(name=input_name)
    return render_template('Home.html', user=user)

@app.route('/Mate')
def buttonMate():
    return render_template('Mate.html')

@app.route('/Mate_make_chat')
def mateMakeChat():
    return render_template('Mate_make_chat.html')
@app.route('/Profile')
def Profile():
    return render_template('Profile.html')

@app.route('/Community')
def buttonCommunity():
    all_posts = AllPost.query.all()
    chat_posts = ChatPost.query.all()
    request_posts = RequestPost.query.all()
    roommate_posts = RoommatePost.query.all()
    together_posts = TogetherPost.query.all()
    return render_template('Community.html', all_posts=all_posts, chat_posts=chat_posts, request_posts=request_posts, roommate_posts=roommate_posts, together_posts=together_posts)

@app.route('/Community/Writepage', methods= ['GET', 'POST'])
def buttonWrite():
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']

        new_post = None
        
        # 카테고리에 따라 적절한 테이블에 저장
        if category == 'all':
            new_post = AllPost(title=title, content=content)
        elif category == 'chat':
            new_post = ChatPost(title=title, content=content)
        elif category == 'request':
            new_post = RequestPost(title=title, content=content)
        elif category == 'roommate':
            new_post = RoommatePost(title=title, content=content)
        elif category == 'together':
            new_post = TogetherPost(title=title, content=content)

        if new_post is not None:
            db.session.add(new_post)
            db.session.commit()
        
        return redirect(url_for('buttonCommunity'))
    return render_template('Writepage.html')



@app.route('/Profile')
def buttonProfile():
    return render_template('Profile.html')




if __name__ == '__main__':
    
    with app.app_context():
        db.create_all()
    
    app.debug = True
    app.run()