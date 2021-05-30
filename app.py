from flask import Flask, request, render_template, jsonify, g
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

def serializer(reviews):
  review_object = [review.serialize for review in reviews]
  return {"response": review_object}

def query_products():
  # products = Review.query.with_entities(Review.product_id, Review.variation).distinct(Review.variation).group_by(Review.product_id).all()
  products = db.session.execute('SELECT DISTINCT product_id, variation FROM reviews GROUP BY 1, 2;').all()
  return products
  # return [pdt[0] for pdt in products]
        
@app.route("/")
def index():
  return render_template('index.html')

@app.route("/wordtree/products", methods=['GET'])
def get_products():
  current_products = query_products()
  print(current_products)
  return render_template('products.html')

@app.route("/wordtree/products/<product_id>", methods=['GET'])
def get_reviews(product_id):
  reviews = Review.query.filter_by(product_id=product_id).limit(10)
  # reviews = Review.query.filter_by(product_id=product_id).with_entities(Review.product_id).limit(10)
  # return jsonify(reviews)
  # print(type(reviews))
  return serializer(reviews)

@app.route("/<name>", methods=['GET', 'POST'])
def greeting(name):
  username = request.args.get('username')
  return "Hello %s!! Your username is %s" % (name, username)



if __name__ == "__main__":
    app.run(debug=True)