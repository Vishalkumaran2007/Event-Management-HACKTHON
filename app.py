from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import gridfs

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- MONGO CONNECTION ----------------
app.config["MONGO_URI"] = "mongodb+srv://TheLoneWolf:vvk123@cluster0.swwo4kk.mongodb.net/Comp"
mongo = PyMongo(app)

# Access the actual Database object
db = mongo.cx.get_database("Comp")

# GridFS setup with correct Database object
fs = gridfs.GridFS(db)

# SocketIO for future notifications
socketio = SocketIO(app)

# ---------------- LOGIN MANAGER ----------------
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, user):
        self.id = str(user["_id"])
        self.email = user["email"]
        self.role = user["role"]

@login_manager.user_loader
def load_user(user_id):
    u = db.users.find_one({"_id": ObjectId(user_id)})
    if u:
        return User(u)
    return None

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        role = request.form["role"]
        if db.users.find_one({"email": email}):
            return "User already exists"
        db.users.insert_one({"email": email, "password": password, "role": role})
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = db.users.find_one({"email": email})
        if user and check_password_hash(user["password"], password):
            login_user(User(user))
            return redirect(url_for("dashboard_admin" if user["role"] == "admin" else "dashboard_volunteer"))
        return "Invalid credentials"
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/dashboard_admin")
@login_required
def dashboard_admin():
    if current_user.role != "admin":
        return "Access denied"
    shifts = list(db.shifts.find())
    return render_template("dashboard_admin.html", shifts=shifts)

@app.route("/dashboard_volunteer")
@login_required
def dashboard_volunteer():
    if current_user.role != "volunteer":
        return "Access denied"
    shifts = list(db.shifts.find({"volunteers": current_user.email}))
    return render_template("dashboard_volunteer.html", shifts=shifts)

@app.route("/create_shift", methods=["POST"])
@login_required
def create_shift():
    if current_user.role != "admin":
        return "Access denied"
    shift_name = request.form["shift_name"]
    date = request.form["date"]
    db.shifts.insert_one({"shift_name": shift_name, "date": date, "volunteers": []})
    return redirect(url_for("dashboard_admin"))

@app.route("/calendar", methods=["GET", "POST"])
@login_required
def calendar():
    if request.method == "POST":
        date = request.form["date"]
        available = request.form["available"]
        existing = db.availability.find_one({"email": current_user.email, "date": date})
        if existing:
            db.availability.update_one({"_id": existing["_id"]}, {"$set": {"available": available}})
        else:
            db.availability.insert_one({"email": current_user.email, "date": date, "available": available})
    availability = list(db.availability.find({"email": current_user.email}))
    return render_template("calendar.html", availability=availability)

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files["document"]
        if file:
            fs.put(file, filename=file.filename, email=current_user.email)
            return "Uploaded successfully"
    return render_template("upload.html")

@app.route("/search", methods=["GET"])
@login_required
def search():
    query = request.args.get("q", "")
    volunteers = db.users.find({"role": "volunteer", "email": {"$regex": query, "$options": "i"}})
    return render_template("search.html", volunteers=volunteers)

@app.route("/report")
@login_required
def report():
    if current_user.role != "admin":
        return "Access denied"
    report_data = db.users.aggregate([
        {"$match": {"role": "volunteer"}},
        {"$group": {"_id": "$role", "count": {"$sum": 1}}}
    ])
    return render_template("report.html", data=list(report_data))

# ---------------- RUN ----------------
if __name__ == "__main__":
    socketio.run(app, debug=True)
