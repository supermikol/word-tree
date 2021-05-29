from flask import Flask, request, render_template
from word_tree_api.wordtree import get_paths, read_files, WordTree

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Review
from credentials import POSTGRESQL_USER, POSTGRESQL_PASSWORD

db_name = 'hooray_analysis_db'
db_host = 'localhost'
db_port = '5432'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

def create_review():
  new_review = Review('PYX010', 'thisisareview', {'rating': 5, 'quality': 'good'})
  with app.app_context():
    db.session.add(new_review)
    db.session.commit()

def decode_review(review):
  decoded_review = {
    'review_id': review.review_id,
    'content': review.content,
    'meta_data': review.meta_data,
    'product_id': review.product_id
  }
  return decoded_review

def decode_reviews(reviews):
  review_object = [decode_review(review) for review in reviews]
  return {"response": review_object}
        
@app.route("/")
def index():
  return render_template('index.html')

@app.route("/reviews/<product_id>", methods=['GET'])
def get_reviews(product_id):
  reviews = Review.query.filter_by(product_id=product_id).all()
  # print(type(reviews))
  return decode_reviews(reviews)

@app.route("/<name>", methods=['GET', 'POST'])
def greeting(name):
  username = request.args.get('username')
  return "Hello %s!! Your username is %s" % (name, username)



if __name__ == "__main__":
    app.run(debug=True)