from flask import Flask, request, render_template, jsonify, g
from flask_caching import Cache
from sqlalchemy import sql
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
    results = db.session.execute(
      'SELECT DISTINCT product_id, variation, COUNT(review_id) review_count FROM reviews GROUP BY 1, 2 ORDER BY 1 ASC, 3 DESC;'
      ).all()
    products = [[*p] for p in results]
    cache.set('all_products', products)
  else:
    products = cache.get('all_products')
  return products

def query_reviews(product_id, variation=None):
  if cache.get((product_id, variation)) is None:
    variation_statement = ""
    if variation is not None:
      variation_statement = f"AND variation='{variation}'"
    sql_statement = f"SELECT content FROM reviews WHERE product_id='{product_id}' {variation_statement};"
    print(sql_statement)
    results = db.session.execute(sql_statement).all()
    review_tokens = WordTree.generate_token((' ').join([p[0] for p in results]))
    cache.set((product_id,variation), review_tokens)
    print('caching')
  else:
    print('getting cache')
    review_tokens = cache.get((product_id, variation))
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
  head = request.args.get('head')
  (g.product_id, g.variation) = (product_id, variation)
  review_tokens = query_reviews(product_id, variation)
  wordtree = WordTree(review_tokens)
  wordtree_results = wordtree.train_and_print(head, levels=1)
  g.results = [[item[0],item[1], item[2]] for item in wordtree_results]
  print(g.results)
  return render_template('reviews.html')

if __name__ == "__main__":
    app.run(debug=True)