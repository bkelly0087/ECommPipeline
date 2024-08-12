import csv
from datetime import datetime, timedelta
from faker import Faker
import random
import uuid

fake = Faker()

def generate_customers(num_customers):
    customers = []
    for _ in range(num_customers):
        customer = {
            'customer_id': str(uuid.uuid4()),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
            'address': fake.address().replace('\n', ', '),
            'created_at': fake.date_time_between(start_date='-5y', end_date='now').isoformat()
        }
        customers.append(customer)
    return customers

def generate_products(num_products):
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Kitchen', 'Sports & Outdoors']
    products = []
    for _ in range(num_products):
        category = random.choice(categories)
        if category == 'Electronics':
            name = f"{fake.company()} {fake.word()} {random.choice(['Smartphone', 'Laptop', 'Headphones', 'Tablet', 'Smartwatch'])}"
        elif category == 'Clothing':
            name = f"{fake.color_name()} {random.choice(['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Sweater'])}"
        elif category == 'Books':
            name = f"The {fake.word().title()} of {fake.word().title()}"
        elif category == 'Home & Kitchen':
            name = f"{fake.word().title()} {random.choice(['Blender', 'Toaster', 'Coffee Maker', 'Knife Set', 'Cookware'])}"
        else:  # Sports & Outdoors
            name = f"{fake.company()} {random.choice(['Running Shoes', 'Yoga Mat', 'Dumbbells', 'Tennis Racket', 'Bicycle'])}"
        
        product = {
            'product_id': str(uuid.uuid4()),
            'name': name,
            'category': category,
            'price': round(random.uniform(10, 1000), 2),
            'description': fake.text(max_nb_chars=200),
            'created_at': fake.date_time_between(start_date='-2y', end_date='now').isoformat()
        }
        products.append(product)
    return products

def generate_orders(customers, products, num_orders):
    orders = []
    order_items = []
    for _ in range(num_orders):
        customer = random.choice(customers)
        customer_created_at = datetime.fromisoformat(customer['created_at'])
        order_date = fake.date_time_between(start_date=customer_created_at, end_date='now')
        order = {
            'order_id': str(uuid.uuid4()),
            'customer_id': customer['customer_id'],
            'order_date': order_date.isoformat(),
            'status': random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled']),
            'total_amount': 0
        }
        
        # Generate order items
        num_items = random.randint(1, 5)
        order_total = 0
        for _ in range(num_items):
            product = random.choice(products)
            quantity = random.randint(1, 3)
            item_total = quantity * product['price']
            order_total += item_total
            
            order_item = {
                'order_item_id': str(uuid.uuid4()),
                'order_id': order['order_id'],
                'product_id': product['product_id'],
                'quantity': quantity,
                'price': product['price'],
                'total': item_total
            }
            order_items.append(order_item)
        
        order['total_amount'] = round(order_total, 2)
        orders.append(order)
    
    return orders, order_items

def write_to_csv(data, filename):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"data_generation/generated_data/{filename}_{timestamp}.csv"
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    return filepath

def main():
    num_customers = 1000
    num_products = 200
    num_orders = 5000
    

    print("Generating customers...")
    customers = generate_customers(num_customers)
    customer_file=write_to_csv(customers, 'customers')

    print("Generating products...")
    products = generate_products(num_products)
    product_file = write_to_csv(products, 'products')

    print("Generating orders...")
    orders, order_items = generate_orders(customers, products, num_orders)
    order_file = write_to_csv(orders, 'orders')
    order_item_file = write_to_csv(order_items, 'order_items')
    
    
    print(f"Generated files: {customer_file}, {product_file}, {order_file}, {order_item_file}")


if __name__ == "__main__":
    main()