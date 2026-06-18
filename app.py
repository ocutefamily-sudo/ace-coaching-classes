from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "ace_coaching_secret"
ADMIN_PASSWORD = "aceadmin123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =====================
# DATABASE MODEL
# =====================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    father_name = db.Column(db.String(100))
    school_name = db.Column(db.String(150))

    email = db.Column(db.String(100))
    mobile = db.Column(db.String(20))

    student_class = db.Column(db.String(50))
    subject = db.Column(db.String(100))

    address = db.Column(db.String(300))
    dob = db.Column(db.String(30))

    password = db.Column(db.String(200))





# =====================
# HOME PAGE
# =====================

@app.route("/")
def home():
    return render_template("index.html")


# ====================
# LOGIN PAGE
# =====================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session["user"] = user.name

            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")


# =====================
# SIGNUP PAGE
# =================


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        father_name = request.form["father_name"]
        school_name = request.form["school_name"]

        email = request.form["email"]
        mobile = request.form["mobile"]

        student_class = request.form["student_class"]
        subject = request.form["subject"]

        address = request.form["address"]
        dob = request.form["dob"]

        password = request.form["password"]

        user = User(
            name=name,
            father_name=father_name,
            school_name=school_name,
            email=email,
            mobile=mobile,
            student_class=student_class,
            subject=subject,
            address=address,
            dob=dob,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/dashboard")

    return render_template("signup.html")






# =====================
# DASHBOARD
# =====================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["user"]
    )
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")
@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "profile.html",
        username=session["user"]
    )
# =====================
# ADMIN PANEL
# =====================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        password = request.form["password"]

        if password == ADMIN_PASSWORD:

            session["admin"] = True

            return redirect("/admin-panel")

        return "Wrong Admin Password"

    return render_template("admin_login.html")

@app.route("/certificate")
def certificate():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "certificate.html",
        username=session["user"]
    )
@app.route("/admin-panel")
def admin_panel():

    if "admin" not in session:
        return redirect("/admin")

    users = User.query.all()

    return render_template(
        "admin.html",
        users=users
    )


# =====================
# COURSES PAGE
# =====================

@app.route("/courses")
def courses():
    return render_template("courses.html")


# =====================
# NOTES PAGE
# =====================

@app.route("/notes")
def notes():
    return render_template("notes.html")
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

# =====================
# RUN APP
# =====================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)
