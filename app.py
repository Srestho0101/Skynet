from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# DB location
db_file = "/data/data/com.termux/files/home/storage/shared/Skynet/skynet.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Uploads folder (inside static/Photos)
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'Photos')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)

# Models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80), nullable=False)
    image_filename = db.Column(db.String(200), nullable=True)
    quote = db.Column(db.Text, nullable=False)

class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    threat_level = db.Column(db.String(20), nullable=False)

# Check extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('index.html', posts=posts)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if not username:
            flash("Please enter username", "warning")
            return redirect(url_for('login'))
        return redirect(url_for('user', username=username))
    return render_template('login.html')

@app.route("/<username>")
def user(username):
    user_posts = Post.query.filter_by(author=username).order_by(Post.id.desc()).all()
    return render_template('user.html', username=username, posts=user_posts)

@app.route("/create", methods=["GET", "POST"])
@app.route("/create", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        author = request.form.get("author", "").strip()
        quote = request.form.get("quote", "").strip()
        image_filename = request.form.get("image_filename", "").strip()

        if not author or not quote:
            flash("Author and quote are required!", "danger")
            return redirect(url_for('create_post'))

        # just store filename, no Pillow needed
        new_post = Post(author=author, image_filename=image_filename or None, quote=quote)
        db.session.add(new_post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for('home'))

    return render_template('create.html')

def seed_data():
    with app.app_context():
        db.create_all()
        if Post.query.count() == 0:
            examples = [
                Post(author="Muntah Mahfuz Srestho", image_filename="Srestho.png",
                     quote="Building the momentum is the hardest part. But if you can gain the momentum once, you become unstoppable!"),
                Post(author="Tony Stark", image_filename="Tony_Stark.jpeg",
                     quote="If you're nothing without this suit, then you shouldn't have it."),
                Post(author="Banglar Gamer", image_filename="Banglar_Gamer.png",
                     quote="Pain now, suffer later..."),
                Post(author="Kaka Babu", image_filename="Kaka_Babu.jpg",
                     quote="In a world of joy, I chose suffering!")
            ]
            db.session.bulk_save_objects(examples)
            db.session.commit()
            print("Seeded example posts.")

if __name__ == '__main__':
    seed_data()
    app.run(host='0.0.0.0', port=5000, debug=True)