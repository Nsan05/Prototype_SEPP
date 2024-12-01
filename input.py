import psycopg2
import pandas as pd
import ast
# Connect to the PostgreSQL database
connection = psycopg2.connect(
    dbname="prototype",
    user="postgres",
    password="idkpassword_2024",
    host="localhost",
    port="5432"
)
# Function to fetch and display all fridge contents
def display_all_fridge_contents():
    try:
        cursor = connection.cursor()

        # Query the entire User_Inventory_Table to get all fridge contents
        cursor.execute("""
            SELECT Fridge_Id, Ingredient_Id_quantity 
            FROM User_Inventory_Table;
        """)
        all_inventory = cursor.fetchall()

        # Initialize a dictionary to group items by fridge
        fridge_data = {}

        for fridge_id, ingredient_dict in all_inventory:
            # Parse the dictionary safely
            ingredient_dict = ast.literal_eval(ingredient_dict)

            # For each ingredient ID, query the Ingredient table for the name
            fridge_data[fridge_id] = []  # Initialize fridge data for this Fridge_Id
            for ingredient_id, quantity in ingredient_dict.items():
                cursor.execute("""
                    SELECT Ing_name
                    FROM Ingredient_Table
                    WHERE Ingredient_Id = %s;
                """, (ingredient_id,))
                ingredient_name = cursor.fetchone()[0]  # Fetch the name

                # Append ingredient details to the fridge data
                fridge_data[fridge_id].append((ingredient_name, quantity))

        # Display the fridge contents
        for fridge_id, items in fridge_data.items():
            print(f"\nFridge {fridge_id}")
            print(f"{'Ingredient Name':<20}{'Quantity':<10}")
            for ingredient_name, quantity in items:
                print(f"{ingredient_name:<20}{quantity:<10}")
        # Prompt the user to choose a fridge
        while True:
            fridge_choice = input("\nWhich Fridge do you want to choose? : ")

            # Check if the entered fridge ID exists
            if fridge_choice.isdigit() and int(fridge_choice) in fridge_data:
                print(f"You selected Fridge {fridge_choice}")
                break  # Exit loop if valid choice
            else:
                print("Invalid fridge choice. Please choose a valid fridge.")
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()

display_all_fridge_contents()
connection.close()