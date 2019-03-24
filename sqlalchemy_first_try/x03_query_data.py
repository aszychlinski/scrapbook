from Day09_hw.x01_setup_and_model import *
from Day09_hw.x02_insert_data import Session as PopulatedSession
# have all 3 files in the same folder and - ideally - run this file first, while the DB has not been created
# the DB will then be created as a side effect and queries will return results for a single insert of data


session = PopulatedSession()


def query_products():
    product_count = session.query(Product).count()
    print(f'There are {product_count} different kinds of products in the database.')

    products = session.query(Product).all()
    nonames = 0
    names = []
    for x in products:
        if x.Name:
            names.append(x.Name)
        else:
            nonames += 1

    print(f'Their names are: {", ".join(names)}.')
    print(f'{nonames} don\'t have a Name, although they have a Category.')


if __name__ == '__main__':
    query_products()
