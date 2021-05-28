from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, JSON, String, Text, text

db = SQLAlchemy()

class Review(db.Model):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True, server_default=text("nextval('reviews_review_id_seq'::regclass)"))
    product_id = Column(String(80), nullable=False)
    content = Column(Text, nullable=False)
    meta_data = Column(JSON)

    def __init__(self, product_id, content, meta_data):
        # self.review_id = review_id
        self.product_id = product_id
        self.content = content
        self.meta_data = meta_data

    def __repr__(self):
        return f"<Review: {self.product_id}, {self.meta_data}>"

