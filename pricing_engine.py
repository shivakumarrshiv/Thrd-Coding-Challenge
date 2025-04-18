import csv

def load_csv(filepath: str) -> list:
    with open(filepath, newline='') as file:
        return list(csv.DictReader(file))

def save_updated_prices(data: list, filepath: str):
    with open(filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["sku", "old_price", "new_price"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

products = load_csv('data/products.csv')
sales = load_csv('data/sales.csv')
sales_map = {s['sku']: int(s['quantity_sold']) for s in sales}

results = []

for product in products:
    sku = product['sku']
    old_price = float(product['current_price'])
    cost_price = float(product['cost_price'])
    stock = int(product['stock'])
    quantity_sold = sales_map.get(sku, 0)

    new_price = old_price

    if stock < 20 and quantity_sold > 30:
        new_price = old_price * 1.15
    elif stock > 200 and quantity_sold == 0:
        new_price = old_price * 0.7
    elif stock > 100 and quantity_sold < 20:
        new_price = old_price * 0.9

    min_price = cost_price * 1.2
    if new_price < min_price:
        new_price = min_price

    results.append({
        "sku": sku,
        "old_price": f"{old_price:.2f} INR",
        "new_price": f"{round(new_price, 2):.2f} INR"
    })

save_updated_prices(results, "updated_prices.csv")
