from functools import wraps
from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os

from utils import file_uploader

UPLOAD_FOLDER = os.getcwd() + '/static/images/uploads'

# config 
from configs.base import Development
# utils
from utils.file_uploader import image_upload
from utils.sms import sms


app = Flask(__name__)
app.config.from_object(Development)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# sqlalchemy
db = SQLAlchemy(app)

# models
from models.roles import Role
from models.user import User
from models.biashara import Biashara
from models.disposable import Disposable
from models.disposable_booking import DisposableBooking



# context processor
@app.context_processor
def utility_processor():
    def disposable_bookings(disposableId: int):
        records = DisposableBooking.fetch_by_disposable_id(id=disposableId)
        return records
    return dict(disposable_bookings=disposable_bookings)



"""
CREATE A LOGIN REQUIRED WRAPPER FOR USER
"""
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Sign in required", "danger")
            return redirect(url_for("login", next=request.url))
    return wrap


# HOMEPAGE
@app.route("/")
def home():
    return render_template("site/index.html")

# EXPLORE
@app.route("/explore")
def explore():
    items = Disposable.published()
    return render_template("/site/explore.html", items=items)



@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("successfully signed out", "success")
    return redirect(url_for("login"))

# login
@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # check email exists
        if User.check_email_exists(email=email):
            if User.validate_password(email=email, password=password):
                # get user object
                user = User.get_user_by_email(email)
                # set sessions
                session['user_id'] = user.id
                session['first_name'] = user.first_name
                session['email'] = user.email
                session['role'] = user.role.role
                session['logged_in'] = True
                flash("Successfully signed in", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid credentials", "danger")
                return redirect(url_for("login"))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for("login"))

    return render_template("auth/login.html")

# create account
# login
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("auth/register.html")

    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        hashed_pass = generate_password_hash(password=password, salt_length=8)

        # check email exists
        if User.check_email_exists(email=email):
            flash("email already in use", "danger")
            return redirect(url_for("register"))
        


        record = User(
            first_name=fname.title(),
            last_name=lname.title(),
            email=email.lower(),
            phone_number=phone,
            password = hashed_pass,
            role_id=2
        )

        # save the user
        record.save()

        flash("account has successfully been created", "success")
        return redirect(url_for("login"))

# dashboard
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if session:
        logged_in = session['logged_in']
        first_name = session['first_name']
        user_id = session['user_id'] 


        records = Biashara.user_biashara(user_id)
        

        return render_template("backend/dashboard.html", logged_in=logged_in, first_name=first_name, biz=len(records))
    else:
        flash("session expired", "danger")
        return redirect(url_for("login"))

# biashara
@app.route("/biashara", methods=["GET", "POST"])
@login_required
def biashara():
    if session:
        logged_in = session['logged_in']
        first_name = session['first_name']
        user_id = session['user_id'] 

        if request.method == "GET":
            records = Biashara.user_biashara(user_id)
            return render_template("backend/biashara.html", logged_in=logged_in, first_name=first_name, biz=records)

        if request.method == "POST":
            thumbnail = request.files['file']
            business_name = request.form['business_name']
            description = request.form['description']
            contact_email = request.form["contact_email"]
            contact_number = request.form["contact_number"]

            # check business name exists
            if Biashara.check_biashara_exists(business_name):
                flash("Biashara name already exist", "danger")
                return redirect(url_for("biashara"))
            else:

                thumbnail_url = image_upload(thumbnail)

                record = Biashara(
                    thumbnail=thumbnail_url,
                    name=business_name,
                    description=description,
                    contact_email=contact_email,
                    contact_number=contact_number,
                    user_id=user_id
                )
                record.save()

                flash("Biashara successfully created", "success")
                return redirect(url_for("biashara"))
    else:
        flash("session expired", "danger")
        return redirect(url_for("login"))

# UPDATE A BIASHARA
@app.route("/update/biashara/<int:id>", methods=["POST"])
def update_biashara(id):
    if request.method == "POST":
        business_name = request.form['business_name']
        description = request.form['description']
        contact_email = request.form["contact_email"]
        contact_number = request.form["contact_number"]

        try:
            # update
            Biashara.update(
                id=id,
                business_name=business_name,
                description=description,
                email=contact_email,
                phone=contact_number
            )

            flash("record updated successfully", "success")
            return redirect(url_for("biashara"))

        except Exception as e:
            flash(f"{e}", "danger")
            return redirect(url_for("biashara"))




@app.route("/biashara/<int:id>", methods=["GET", "POST"])
@login_required
def biashara_id(id):
    if session:
        logged_in = session['logged_in']
        first_name = session['first_name']
        user_id = session['user_id'] 

        if request.method == "POST":
            title = request.form["title"]
            brief_description = request.form["brief_description"]
            details = request.form["details"]
            
            record = Disposable(
                title=title.title(),
                brief_description=brief_description,
                details=details,
                biashara_id=id,
                user_id=user_id
            )

            r = record.save()

            flash("successfully added", "success")
            return redirect(url_for("biashara_id", id=id))

        biashara = Biashara.get_biashara_by_id(id)
        disposables = Disposable.fetch_by_biashara_id(id=id)
        return render_template("backend/manage_biashara.html", id=id, bizname=biashara.name,
                                disposables=disposables, biz_id=id, logged_in=logged_in, first_name=first_name)

    else:
        flash("session expired", "danger")
        return redirect(url_for("login"))


@app.route("/biashara/<int:biashara_id>/update/<int:id>/disposable", methods=["POST"])
def update_disposable(biashara_id,id):
    if request.method == "POST":
        title = request.form["title"]
        brief_description = request.form["brief_description"]
        details = request.form["details"]

        try:
            Disposable.update(
                id=id,
                title=title.title(),
                brief_description=brief_description,
                details=details
            )

            flash("update successfull", "success")
            return redirect(url_for("biashara_id", id=biashara_id))
        except Exception as e:
            print(f"{e}", "danger")
            return redirect(url_for("biashara_id", id=biashara_id))


@app.route("/unpublish/biashara/<int:biashara_id>/item/<int:id>", methods=["POST"])
def unpublish(biashara_id,id):
    if request.method == "POST":
        try:
            Disposable.change_publish_status(id=id)
            flash("Publish status changed successfully", "success")
            return redirect(url_for("biashara_id", id=biashara_id))

        except Exception as e:
            flash(e, "danger")
            return redirect(url_for("biashara_id", id=biashara_id))


@app.route("/disposable/<int:id>/book", methods=["POST"])
def book(id):
    
    if request.method == "POST":
        email = request.form['email']
        phone = request.form['phone']
        fullname = request.form['fullname']
        biashara = request.form["biashara"]
        item = request.form["item"]
        contact = request.form["contact_number"]

        # check if the email has made the booking before
        if DisposableBooking.check_email_exists(email):
            flash("email already has a booking")
            return redirect(url_for("explore"))

        else:
            record = DisposableBooking(
                email=email.lower(),
                phone_number=phone,
                full_name = fullname.title(),
                disposable_id=id
            )

            r = record.save()

            msg = f"""Dear {fullname.title()}, your booking for {item.title()} by {biashara.title()} has successfully been made.You will be contacted for further information on the phone number and email you have submitted.Contact {biashara.title()} on +{contact}"""

            sms.send([f"+{phone}"], message=msg)

            flash("booking received. You will be notified soon")

            return redirect(url_for("explore"))
    

def unpublished(each):
    print(each.is_published)
    return each     


@app.route("/bookings", methods=["GET", "POST"])
def bookings():
    if session:
        logged_in = session['logged_in']
        first_name = session['first_name']
        user_id = session['user_id'] 

        if request.method == "GET":
            
            unpublished = Disposable.user_not_published(user_id=user_id)
            published = Disposable.user_published(user_id=user_id)

            return render_template("backend/bookings.html", unpublished=unpublished, published=published,
                                    logged_in=logged_in, first_name=first_name)
    else:
        flash("session expired", "danger")
        return redirect(url_for("login"))


# reports
@app.route("/reports")
def reports():
    if session:
        logged_in = session['logged_in']
        first_name = session['first_name']
        user_id = session['user_id']

        records = Biashara.user_biashara(user_id=user_id)
        all_disposable = Disposable.all_user_disposables(user_id=user_id)
        return render_template("backend/reports.html", biz=records, items=all_disposable, logged_in=logged_in, first_name=first_name)
    else:
        flash("session expired", "danger")
        return redirect(url_for("login"))

# role
@app.route("/roles", methods=["GET", "POST"])
def role():
    

    # logged_in = session['logged_in']
    # first_name = session['first_name']

    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']

        # check role exists
        if Role.check_role_exists(name=name):
            flash("Role already exists", "danger")
            return redirect(url_for("role"))
        else:
            record = Role(role=name.title(), description=description)
            record.save()
            flash("New role has successfully been created", "success")
            return redirect(url_for("role"))

    if request.method == "GET":
        roles = Role.all()
        return render_template("backend/role.html", roles=roles) #logged_in=logged_in, first_name=first_name

        # flash("session expired", "danger")
        # return redirect(url_for("login"))





if __name__ == "__main__":
    app.run(port=5000, debug=True)