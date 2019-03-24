from Day09_hw.x01_setup_and_model import *
from datetime import datetime
from time import time


session = Session()

# insert strategy:
# step1: Store, User, Category
# -step2: Product
# --step3: Offer
# ---step4: Transaction, Message
# some data generated from:
#  https://www.fakepersongenerator.com/
#  https://www.randomlists.com/things

# --- step1 begins ---
sas = Store(Name='Schucks Auto Supply', Address='2158 Elm Drive', Website='aryannesgarden.com', Contact='Ryan A. Buch')
tfh = Store(Name='The Flying Hippo', Address='2522 Shingleton Road', Contact='Elizabeth J. Rouse')
st = Store(Name='SoundTrack', Address='2885 Jerry Dove Drive', Website='voiceleague.com', Contact='Ricky D. Trueman')
fp = Store(Name='Future Plan', Address='571 Hog Camp Road', Website='lacameracoffee.com', Contact='Martin G. Smith')
tnc = Store(Name='The Network Chef', Address='2565 Trainer Avenue', Website='strabagcm.com', Contact='Rachel K. Jones')

p_f = Category(Category_name='Food, perishable', Category_description='Food with a relatively short shelf life')
c_f = Category(Category_name='Food, preserved', Category_description='Food with a relatively long shelf life')
ele = Category(Category_name='Electronics')
fur = Category(Category_name='Furniture')
clo = Category(Category_name='Clothing', Category_description='Things which can be worn')
o_s = Category(Category_name='Office Supplies')
b_s = Category(Category_name='Bathroom Supplies', Category_description='Things one\'d find in a bathroom')
ani = Category(Category_name='Animals', Category_description='TODO: check if this is legal')
car = Category(Category_name='Cars')
oth = Category(Category_name='Other', Category_description='Everything else')

ad1 = User(
    Username='Administrator',
    Login='admin',
    Password_hash='e00cf25ad42683b3df678c61f42c6bda',
    email='admin@compare.db',
    Active=True,
    Admin=True,
    GDPR_permission=True
)

us1 = User(
    Username='Maribel Lopez',
    Login='Standappsto',
    Password_hash='a6919f4657ee319b6c21f5726925d59e',
    email='uuwkpifl@sharklasers.com',
    Active=True,
    Admin=False,
    GDPR_permission=True
)

us2 = User(
    Username='Marie Imhoff',
    Login='concepcion',
    Password_hash='444f7561fc93a8618ce574814991906d',
    email='o4b0zsh3bmm@payspun.com',
    Active=True,
    Admin=False,
    GDPR_permission=True
)

us3 = User(
    Username='Tiffany Martin',
    Login='sofia_rules',
    Password_hash='06a1b294de2ca15d49a704e3f122ff03',
    email='dp4lr7yo8c8@iffymedia.com',
    Active=True,
    Admin=False,
    GDPR_permission=True
)


session.add_all([sas, tfh, st, fp, tnc])
session.add_all([p_f, c_f, ele, fur, clo, o_s, b_s, ani, car, oth])
session.add_all([ad1, us1, us2, us3])
session.commit()
# --- step1 ends ---
# --- step2 begins ---
eraser = Product(Category_ID=o_s.ID, Name='Eraser')
table = Product(Category_ID=fur.ID)
bottle_cap = Product(Category_ID=oth.ID, Name='Bottle cap')
usb = Product(Category_ID=ele.ID, Name='USB drive')
sketch_pad = Product(Category_ID=o_s.ID, Name='Sketch pad')
toothbrush = Product(Category_ID=b_s.ID, Name='Toothbrush')
washing_machine = Product(Category_ID=ele.ID, Name='Washing machine')
knife = Product(Category_ID=o_s.ID)
blouse = Product(Category_ID=clo.ID, Name='Blouse')
laptop = Product(Category_ID=ele.ID)


session.add_all([eraser, table, bottle_cap, usb, sketch_pad, toothbrush, washing_machine, knife, blouse, laptop])
session.commit()
# --- step2 ends ---
# --- step3 begins ---
lap_offer = Offer(
    Store_ID=tnc.ID,
    Product_ID=laptop.ID,
    User_ID=us3.ID,
    Name='Used laptop for sale',
    Price=4399.,
    Description='i5, 16GB RAM, 256GB SSD + 1TB HDD, no OS',
    State='Used',
    Delivery='Courier, Personal pickup',
    Active=True,
    # Added_date=datetime.fromtimestamp(time()),
    Added_date=datetime.fromisoformat('2019-03-24 16:38:21.905303'),
    # Expiration_date=datetime.fromtimestamp(time() + 1209600)
    Expiration_date=datetime.fromisoformat('2019-04-07 16:38:21.905303')
)

tab_offer = Offer(
    Store_ID=sas.ID,
    Product_ID=table.ID,
    User_ID=us1.ID,
    Name='Brand new table, pine',
    Price=800.,
    Description='Lenght: 1 m, width: 80 cm',
    State='New',
    Delivery='Courier',
    Active=True,
    Added_date=datetime.fromisoformat('2019-03-25 16:58:41.905303'),
    Expiration_date=datetime.fromisoformat('2019-04-08 16:58:41.905303')
)


session.add_all([lap_offer, tab_offer])
session.commit()
# --- step3 ends ---
# --- step4 begins ---
hi1 = Message(
    Sender=ad1.ID,
    Recipient=us1.ID,
    Date_sent=datetime.fromisoformat('2019-03-23 12:28:01.830540'),
    Is_read=True,
    Is_flagged_for_review=False,
    Is_deleted=True,
    Message_text='Hello and welcome!'
)

hi2 = Message(
    Sender=ad1.ID,
    Recipient=us2.ID,
    Date_sent=datetime.fromisoformat('2019-03-23 16:30:46.408321'),
    Is_read=False,
    Is_flagged_for_review=True,
    Is_deleted=True,
    Message_text='Hello and welcome!'
)

hi3 = Message(
    Sender=ad1.ID,
    Recipient=us3.ID,
    Date_sent=datetime.fromisoformat('2019-03-23 23:09:53.409832'),
    Is_read=True,
    Is_flagged_for_review=False,
    Is_deleted=False,
    Message_text='Hello and welcome!'
)

session.add_all([hi1, hi2, hi3])
session.commit()
# --- step4 ends ---
