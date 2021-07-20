from flask import Flask, request, render_template, jsonify, g
from flask_caching import Cache
from sqlalchemy import sql, func, desc
from word_tree_api.wordtree import get_paths, read_files, WordTree

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Review
from credentials import POSTGRESQL_USER, POSTGRESQL_PASSWORD, POSTGRESQL_DB, POSTGRESQL_HOST
db_name = POSTGRESQL_DB
db_host = POSTGRESQL_HOST
db_port = '5432'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['CACHE_TYPE'] = "SimpleCache"
app.config['CACHE_DEFAULT_TIMEOUT'] = 2000

cache = Cache(app)

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
  if cache.get('all_products') is None:
    results = (db.session.query(
                                Review.product_id, 
                                Review.variation, 
                                func.count(Review.review_id).label('review_count')
                                )
                          .group_by(Review.product_id, Review.variation)
                          .order_by(Review.product_id, desc('review_count'))
                          .all())
    products = [[*p] for p in results]
    cache.set('all_products', products)
  else:
    products = cache.get('all_products')
  return products

def query_reviews(product_id, variation=None, rating=[1,2,3,4,5]):
  string_rating = (',').join(map(str, rating))
  if cache.get((product_id, variation, string_rating)) is None:
    if variation is not None:
      results = (db.session.query(
                              Review.content
                              )
                            .filter(Review.product_id == product_id,
                              Review.variation == variation,
                              Review.product_rating.in_(rating))
                            .all())
    else:
      results = (db.session.query(
                              Review.content
                              )
                            .filter(Review.product_id == product_id,
                              Review.product_rating.in_(rating))
                            .all())
    review_tokens = WordTree.generate_token((' ').join([p[0] for p in results]))
    cache.set((product_id,variation,string_rating), review_tokens)
  else:
    review_tokens = cache.get((product_id, variation, string_rating))
  return review_tokens
        
@app.route("/")
def index():
  g.products = query_products()
  return render_template('products.html')

@app.route("/wordtree/products", methods=['GET'])
def get_products():
  g.products = query_products()
  return render_template('products.html')

@app.route("/wordtree/products/<product_id>", methods=['GET'])
def get_reviews(product_id):
  variation = request.args.get('variation')
  trailing = request.args.get('trailing')
  direction = request.args.get('direction')
  nested_trailing = request.args.get('nested_trailing')
  if trailing is None:
    trailing = 3
  if nested_trailing is None:
    nested_trailing = 3
  if direction is None:
    direction='forward'
  if type(request.args.get('rating')) == str:
    rating = request.args.get('rating').split(',')
  else:
    rating = ['1,2,3,4,5']
  head = request.args.get('head')
  (g.product_id, g.variation, g.rating) = (product_id, variation, (',').join(rating))
  review_tokens = query_reviews(product_id, variation, rating)
  wordtree = WordTree(review_tokens)
  wordtree_results = wordtree.train_and_print(head, direction=direction, trailing_grams=int(trailing), nested_trailing_grams=int(nested_trailing), levels=1)
  g.results = [[item[0],item[1], item[2]] for item in wordtree_results]
  return render_template('reviews.html')

if __name__ == "__main__":
    app.run(debug=True)