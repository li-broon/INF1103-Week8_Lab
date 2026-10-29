import json
import os

class Product:
    def __init__(self, productId, name, price, stock):
        self._productid = productId
        self.name = name
        self._price = price
        self._stock = stock
    
    def update_stock(self, quantity:int):
        self._stock = quantity if quantity >= 0 else 0

    def display_information(self):
        print("---------------------------\n")
        print(f"Product Name: {self.name}\n")
        print(f"Product ID: {self._productid}\n")
        print(f"Product ID: {self._price}\n")
        print(f"Product ID: {self._stock}\n")
        print("---------------------------\n")

    def to_dict(self):
        return {
            "product_id": self._productid,
            "name": self.name,
            "price": self._price,
            "stock": self._stock
        }
    



class Inventory:
    def __init__(self,products):
        self.productslist = products

    def add_product(self, product):
        self.productslist.append(product)

    def search_product(self, target_name):
        for product in self.productslist:
            if product.name.lower() == target_name.lower():
                return product
        return None

    def display_all(self):
        for product in self.productslist:
            product.display_information()

def save_inventory_to_json(inventoryList):
    dict_inventory = []

    for product in inventoryList:
        dict_inventory.append(product.to_dict())

    with open("inventory.json","w") as file:
         json.dump(dict_inventory, file, indent=4)

def load_inventory_from_json():
    if not os.path.exists("inventory.json"):
        return [] 
    
    with open("inventory.json", "r") as file:
        try:
            data = json.load(file)
            inventorylist = []

            for item_object in data:
                existing_product = Product(item_object["product_id"], item_object["name"], item_object["price"], item_object["stock"])
                inventorylist.append(existing_product)

            return inventorylist
        except json.JSONDecodeError:
            return []

def main():
    # 1. Load initial data and create Inventory object
    loaded_products = load_inventory_from_json()
    inventory = Inventory(loaded_products)

    while True:
        print("\n=== Inventory Management System ===")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            inventory.display_all()

        elif choice == '2':
            # Main program handles input, Inventory handles storage
            p_id = input("Enter Product ID: ")
            name = input("Enter Product Name: ")
            price = float(input("Enter Price: "))
            stock = int(input("Enter Stock Quantity: "))
            
            new_product = Product(p_id, name, price, stock)
            inventory.add_product(new_product)
            print(f"Product '{name}' added successfully.")

        elif choice == '3':
            target = input("Enter the name of the product to update: ")
            # Menu interacts with Inventory to find the object
            product = inventory.search_product(target)
            
            if product:
                new_qty = int(input(f"Enter new stock quantity for {product.name}: "))
                # Product object manages its own state
                product.update_stock(new_qty)
                print("Stock updated successfully.")
            else:
                print("Product not found.")

        elif choice == '4':
            target = input("Enter the name of the product to search: ")
            product = inventory.search_product(target)
            
            if product:
                product.display_information()
            else:
                print("Product not found.")

        elif choice == '5':
            # Pass the list of Product objects to your save function
            save_inventory_to_json(inventory.productslist)
            print("Inventory saved successfully to inventory.json.")

        elif choice == '6':
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()
