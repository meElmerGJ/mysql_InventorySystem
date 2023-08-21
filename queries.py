import mysql.connector
from Product import Product
from tabulate import tabulate

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='inventory'
)


cursor = conn.cursor()


# FUNCTION TO CREATE TABLES
def create_tables():
    # Creating tables <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    suppliers = """
            CREATE TABLE IF NOT EXISTS suppliers
                    (idSupplier int primary key auto_increment ,
                    supplierName varchar(100) unique,
                    contactName varchar(100),
                    contactNumber varchar(50),
                    address varchar(200))
            """
    cursor.execute(suppliers)

    categories = """
    CREATE TABLE IF NOT EXISTS categories
            (idCategory int primary key auto_increment,
            categoryName varchar(100))
    """
    cursor.execute(categories)

    products = """
    CREATE TABLE IF NOT EXISTS products
            (idProduct int primary key auto_increment,
            productName varchar(100) unique,
            idCategory int,
            idSupplier int,
            stockQuantity int,
            minStockQuantity int,
            price decimal(10, 2))
    """
    cursor.execute(products)

    transactions = """
    CREATE TABLE IF NOT EXISTS transactions
            (idTransaction int primary key auto_increment,
            idProduct int,
            transactionType enum('IN', 'OUT'),
            quantity int,
            transactionDate datetime)
    """
    cursor.execute(transactions)

    # Setting relationships <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    relation_1 = "ALTER TABLE products add foreign key (idCategory) references categories(idCategory)"
    relation_2 = "ALTER TABLE products add foreign key (idSupplier) references suppliers(idSupplier)"
    relation_3 = "ALTER TABLE transactions add foreign key (idProduct) references products(idProduct)"

    cursor.execute(relation_1)
    cursor.execute(relation_2)
    cursor.execute(relation_3)
#
#
#
#

# FUNCTION TO CREATE NEW PRODUCT


#
#
#
#
#

# FUNCTION TO GENERATE DATA
def generate_data():
    # Insert into suppliers
    suppliers_data = [
        ("AtomicSupply Co.", "John Atomic", "123-456-7890", "123 Atomic St."),
        ("QuickGoods Inc.", "Lucy Quick", "123-456-7891", "124 Quick Ave."),
        ("KidZone Enterprises", "Mike Kid", "123-456-7892", "125 Kid Rd."),
        ("BabyEssentials Ltd.", "Emily Essential", "123-456-7893", "126 Essential Blvd."),
        ("DigitalDynamics Co.", "Techie Tom", "123-456-7894", "127 Digital Dr."),
        ("BookBarn International", "Biblio Bob", "123-456-7895", "128 Bibliophile St."),
        ("TrendyThreads LLC", "Fashion Fiona", "123-456-7896", "129 Trendy Tr."),
        ("StationerySolutions Corp.", "Penny Pencil", "123-456-7897", "130 Stationery St."),
        ("FitLife Distributors", "Fit Frank", "123-456-7898", "131 Fitness Blvd."),
        ("GroceryGurus Pvt. Ltd.", "Grocer Greg", "123-456-7899", "132 Grocery Gd.")
    ]

    for record in suppliers_data:
        cursor.execute("""
            INSERT INTO suppliers (supplierName, contactName, contactNumber, address)
            VALUES (%s, %s, %s, %s)
        """, record)

    # Insert into categories
    categories_data = ["Shoes", "Personal Use", "Grocery", "Kids", "Baby", "Electronics", "Books", "Apparel", "Stationery", "Fitness"]
    for index, cat in enumerate(categories_data, 1):
        cursor.execute("""
            INSERT INTO categories (idCategory, categoryName)
            VALUES (%s, %s)
        """, (index, cat))

    # Insert into products
    products_data = [
        ("Running Shoes", 1, 1, 100, 10, 50.00),
        ("Shampoo", 2, 2, 100, 10, 5.99),
        ("Fresh Apples", 3, 10, 100, 10, 0.99),
        ("Toy Car Set", 4, 3, 50, 5, 20.00),
        ("Baby Mittens", 5, 4, 30, 5, 3.99),
        ("Wireless Headphones", 6, 5, 80, 5, 150.00),
        ("Redis Deep Dive Book", 7, 6, 60, 10, 30.00),
        ("Denim Jacket", 8, 7, 40, 5, 40.00),
        ("Colored Pencils", 9, 8, 100, 10, 4.99),
        ("Yoga Mat", 10, 9, 70, 5, 25.00)
    ]
    for index, record in enumerate(products_data, 1):
        cursor.execute("""
            INSERT INTO products (idProduct, productName, idCategory, idSupplier, stockQuantity, minStockQuantity, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (index, *record))

    # Insert into transactions
    for i in range(1, 11):
        cursor.execute("""
            INSERT INTO transactions (idTransaction, idProduct, transactionType, quantity, transactionDate)
            VALUES (%s, %s, %s, %s, %s)
        """, (i, i, "IN" if i % 2 == 0 else "OUT", 10, "2023-08-20 12:00:00"))
    # Commit the transactions
    conn.commit()


# FUNCTION TO GET ALL PRODUCTS
def get_products():
    cursor.execute("SELECT * FROM products")
    table = cursor.fetchall()
    print(tabulate(table, headers=["Product ID", "Articulo", "ID Categoria", "ID Proveedor", "Cantidad", "Cantidad minima", "Precio"], tablefmt="psql"))


# FUNCTION TO GET ALL CATEGORIES
def get_categories():
    cursor.execute("SELECT * FROM categories")
    table = cursor.fetchall()
    print(tabulate(table, headers=["Categoria ID", "Categoria"], tablefmt="psql"))


# FUNCTION TO GET ALL SUPPLIERS
def get_suppliers():
    cursor.execute("SELECT * FROM suppliers")
    table = cursor.fetchall()
    print(tabulate(table, headers=["Proveedor ID", "Proveedor", "Nombre de contacto", "Numero de contacto", "Direccion"], tablefmt="psql"))


# FUNCTION TO GET ALL TRANSACTIONS
def get_transactions():
    cursor.execute("SELECT * FROM transactions")
    table = cursor.fetchall()
    print(tabulate(table, headers=["Transaccion ID", "Producto ID", "Tipo de Transaccion", "Cantidad", "Fecha"], tablefmt="psql"))


# FUNCTION TO CRETE NEW PRODUCT
def new_product():
    product_name = input("Ingrese el Nombre: ")
    get_categories()
    category_id = input("Ingrese la Categoria: ")
    get_suppliers_list()
    supplier_id = input("Ingrese el Proveedor: ")
    quantity = input("Ingrese la Cantidad: ")
    min_quantity = input("Ingrese la Cantidad minima: ")
    price = input("Ingrese el Precio: ")

    p = Product(product_name, category_id, supplier_id, quantity, min_quantity, price)
    cursor.execute("""INSERT INTO products(productName, idCategory, idSupplier, stockQuantity, minStockQuantity, price)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   """, (p.productName, p.idCategory, p.idSupplier, p.stockQuantity, p.minStockQuantity, p.price))
    conn.commit()


# FUNCTION TO PRINT SUPPLIERS NAME
def get_suppliers_list():
    cursor.execute("SELECT idSupplier, supplierName FROM suppliers")
    table = cursor.fetchall()
    print(tabulate(table, headers=["ID", "Proveedor"], tablefmt="psql"))


# FUNCTION TO DELETE A PRODUCT
def del_product(value):
    query = "DELETE FROM products WHERE productName=%s"
    cursor.execute(query, [value])
    conn.commit()


# FUNCTION TO GET A PRODUCT ENTERED
def get_product(value):
    query = "SELECT * FROM products WHERE productName = %s"
    cursor.execute(query, [value])
    table = cursor.fetchall()
    print(tabulate(table, headers=["Product ID", "Articulo", "ID Categoria", "ID Proveedor", "Cantidad", "Cantidad minima", "Precio"], tablefmt="psql"))


def edit_product(value, col, new_value):
    global _query
    match int(col):
        case 1:
            _query = "UPDATE products SET productName = %s WHERE idProduct = %s"
        case 2:
            _query = "UPDATE products SET idCategory = %s WHERE idProduct = %s"
        case 3:
            _query = "UPDATE products SET idSupplier = %s WHERE idProduct = %s"
        case 4:
            _query = "UPDATE products SET stockQuantity = %s WHERE idProduct = %s"
        case 5:
            _query = "UPDATE products SET minStockQuantity = %s WHERE idProduct = %s"
        case 6:
            _query = "UPDATE products SET price = %s WHERE idProduct = %s"
    cursor.execute(_query, [new_value, value])
    conn.commit()

#
#
#
#
#
#
#
#
#
#


# testing Functions
