import json

def parse_category_line(line):
    categories = line.strip().split('|')[1:]
    return [{cat.strip(']').split('[')[1]: cat.strip(']').split('[')[0]} for cat in categories]

def parse_review_line(line):
    data = line.strip().split()
    return {
        'date': data[0],
        'customer': data[2],
        'rating': int(data[4]),
        'votes': int(data[6]),
        'helpful': int(data[8])
    }

def parser_products(file_path, output_path):
    products = []
    product = {}

    with open(file_path, 'r') as file:
        for line in file:
            if 'discontinued' in line:
                product = {}
                continue

            if line.startswith("Id:"):
                if product:
                    # De-duplicate categories
                    if 'categories' in product:
                        unique_categories = {tuple(d.items()): d for d in product['categories']}
                        product['categories'] = list(unique_categories.values())
                    products.append(product)
                product = {'id': int(line.split()[1])}
            elif line.startswith("ASIN:"):
                product['asin'] = line.split()[1]
            elif line.startswith("  title:"):
                product['title'] = line[len("  title:"):].strip()
            elif line.startswith("  group:"):
                product['group'] = line[len("  group:"):].strip()
            elif line.startswith("  similar:"):
                product['similar'] = line.split()[2:]
            elif line.startswith("  categories:"):
                product['categories'] = []
            elif line.startswith("   |"):
                product['categories'].extend(parse_category_line(line))
            elif line.startswith("  reviews:"):
                product['reviews'] = []
            elif line.startswith("    "):
                product['reviews'].append(parse_review_line(line))

    # Process last product
    if product:
        if 'categories' in product:
            unique_categories = {tuple(d.items()): d for d in product['categories']}
            product['categories'] = list(unique_categories.values())
        products.append(product)

    with open(output_path, 'w') as json_file:
        json.dump(products, json_file, indent=2)

    return products
