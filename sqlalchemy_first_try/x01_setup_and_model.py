from sqlalchemy import create_engine, Column, Integer, String, Boolean, LargeBinary, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///compare.db', echo=False)  # True to display generated SQL in output
Base = declarative_base()


class Category(Base):
    __tablename__ = 'Category'
    ID = Column(Integer, primary_key=True, nullable=False)
    Category_name = Column(String(256), nullable=False)
    Category_description = Column(String(1024), nullable=True)

    categories_products = relationship('Product', back_populates='products_categories')


class Message(Base):
    __tablename__ = 'Messages'
    ID = Column(Integer, primary_key=True, nullable=False)
    Sender = Column(Integer, ForeignKey('User.ID'), nullable=False)
    Recipient = Column(Integer, ForeignKey('User.ID'), nullable=False)
    Date_sent = Column(DateTime, nullable=False)
    Is_read = Column(Boolean, nullable=False)
    Is_flagged_for_review = Column(Boolean, nullable=False)
    Is_deleted = Column(Boolean, nullable=False)
    Message_text = Column(String(1024), nullable=True)

    # https://www.reddit.com/r/flask/comments/2o4ejl/af_flask_sqlalchemy_two_foreign_keys_referencing/
    # ^ not working but is it necessary?
    #
    # messages_senders_users = relationship('User', back_populates='users_messages_senders', foreign_keys='User.ID')
    # messages_recipients_users = relationship('User', back_populates='users_messages_recipients', foreign_keys='User.ID')


class Offer(Base):
    __tablename__ = 'Offer'
    ID = Column(Integer, primary_key=True, nullable=False)
    Product_ID = Column(Integer, ForeignKey('Product.ID'), nullable=False)
    Store_ID = Column(Integer, ForeignKey('Store.ID'), nullable=False)
    User_ID = Column(Integer, ForeignKey('User.ID'), nullable=False)
    Name = Column(String(256), nullable=True)
    Price = Column(Numeric, nullable=True)
    Description = Column(String(1024), nullable=True)
    Photo = Column(LargeBinary, nullable=True)
    State = Column(String(256), nullable=True)
    Delivery = Column(String(256), nullable=True)
    Active = Column(Boolean, nullable=False)
    Added_date = Column(DateTime, nullable=True)
    Expiration_date = Column(DateTime, nullable=True)

    offers_products = relationship('Product', back_populates='products_offers')
    offers_stores = relationship('Store', back_populates='stores_offers')
    offers_users = relationship('User', back_populates='users_offers')


class Product(Base):
    __tablename__ = 'Product'
    ID = Column(Integer, primary_key=True, nullable=False)
    Category_ID = Column(Integer, ForeignKey('Category.ID'), nullable=False)
    Name = Column(String(256), nullable=True)

    products_categories = relationship('Category', back_populates='categories_products')
    products_offers = relationship('Offer', back_populates='offers_products')


class Store(Base):
    __tablename__ = 'Store'
    ID = Column(Integer, primary_key=True, nullable=False)
    Name = Column(String(512), nullable=True)
    Address = Column(String(512), nullable=True)
    Website = Column(String(512), nullable=True)
    Contact = Column(String(512), nullable=True)

    stores_offers = relationship('Offer', back_populates='offers_stores')


class Transaction(Base):
    __tablename__ = 'Transaction'
    ID = Column(Integer, ForeignKey('Offer.ID'), primary_key=True, nullable=False)
    Buyer = Column(Integer, ForeignKey('User.ID'), nullable=False)
    Seller = Column(Integer, ForeignKey('User.ID'), nullable=False)
    Transaction_time = Column(DateTime, nullable=False)

    # TODO: add relations?
    # TODO: add a TRIGGER that sets matching (Offer.ID == Transaction.ID) Offer.Active to False ON INSERT to Transaction


class User(Base):
    __tablename__ = 'User'
    ID = Column(Integer, primary_key=True, nullable=False)
    Username = Column(String(256), nullable=False)
    Login = Column(String(50), nullable=False)
    Password_hash = Column(String(1024), nullable=True)
    email = Column(String(256), nullable=False)
    Active = Column(Boolean, nullable=False)
    Admin = Column(Boolean, nullable=False)
    GDPR_permission = Column(Boolean, nullable=False)

    users_offers = relationship('Offer', back_populates='offers_users')
    # TODO: add relation with Message (is it necessary)
    # users_messages_senders = relationship('Message', back_populates='messages_senders_users', foreign_keys='Message.Sender')
    # users_messages_recipients = relationship('Message', back_populates='messages_senders_recipients', foreign_keys='Message.Recipient')


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
