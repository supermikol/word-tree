from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, JSON, String, Text, text, Date

db = SQLAlchemy()

class Review(db.Model):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True, server_default=text("nextval('reviews_review_id_seq'::regclass)"))
    content = Column(Text, nullable=False)
    meta_data = Column(JSON)
    product_id = Column(String(80), nullable=False)
    variation = Column(String(80))
    review_date = Column(Date)
    rater_id = Column(String(80))
    product_rating = Column(Integer)

    def __init__(self, product_id, content, meta_data = None, variation=None, review_date = None, rater_id = None, product_rating= None):
        self.content = content
        self.meta_data = meta_data
        self.product_id = product_id
        self.variation = variation
        self.review_date = review_date
        self.rater_id = rater_id
        self.product_rating = product_rating

    def __repr__(self):
        return f"<Review: {self.product_id}, {self.meta_data}>"

