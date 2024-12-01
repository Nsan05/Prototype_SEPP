import psycopg2
import ast
import os
import json
import webbrowser
# Connect to the PostgreSQL database
connection = psycopg2.connect(
    dbname="prototype",
    user="postgres",
    password="idkpassword_2024",
    host="localhost",
    port="5432"
)
# Function to fetch all existing fridges from database
def fetch_existing_fridges():
    """Fetch existing fridges from the database."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT DISTINCT Fridge_Id 
            FROM User_Inventory_Table;
        """)
        existing_fridges = [row[0] for row in cursor.fetchall()]
        return existing_fridges
    except Exception as e:
        print("Error fetching existing fridges:", e)
        return []
    finally:
        cursor.close()
# Function to fetch all ingredients
def fetch_all_ingredients():
    """Fetch all available ingredients from the Ingredient_Table."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Ingredient_Id, Ing_name 
            FROM Ingredient_Table;
        """)
        ingredients = {str(row[0]): row[1] for row in cursor.fetchall()}
        return ingredients
    except Exception as e:
        print("Error fetching ingredients:", e)
        return {}
    finally:
        cursor.close()
# Function to fetch all fridge data
def fetch_fridge_data():
    """Fetch fridge data from the database."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Fridge_Id, Ingredient_Id_quantity 
            FROM User_Inventory_Table;
        """)
        all_inventory = cursor.fetchall()

        fridge_data = {}
        for fridge_id, ingredient_dict in all_inventory:
            ingredient_dict = ast.literal_eval(ingredient_dict)
            fridge_data[fridge_id] = {}
            for ingredient_id, quantity in ingredient_dict.items():
                cursor.execute("""
                    SELECT Ing_name
                    FROM Ingredient_Table
                    WHERE Ingredient_Id = %s;
                """, (ingredient_id,))
                ingredient_name = cursor.fetchone()[0]
                fridge_data[fridge_id][ingredient_name] = quantity

        return fridge_data
    except Exception as e:
        print("Error:", e)
        return {}
    finally:
        cursor.close()

# def display_all_fridge_contents():
#     try:
#         cursor = connection.cursor()

#         # Query the entire User_Inventory_Table to get all fridge contents
#         cursor.execute("""
#             SELECT Fridge_Id, Ingredient_Id_quantity 
#             FROM User_Inventory_Table;
#         """)
#         all_inventory = cursor.fetchall()

#         # Initialize a dictionary to group items by fridge
#         fridge_data = {}

#         for fridge_id, ingredient_dict in all_inventory:
#             # Parse the dictionary safely
#             ingredient_dict = ast.literal_eval(ingredient_dict)

#             # For each ingredient ID, query the Ingredient table for the name
#             fridge_data[fridge_id] = []  # Initialize fridge data for this Fridge_Id
#             for ingredient_id, quantity in ingredient_dict.items():
#                 cursor.execute("""
#                     SELECT Ing_name
#                     FROM Ingredient_Table
#                     WHERE Ingredient_Id = %s;
#                 """, (ingredient_id,))
#                 ingredient_name = cursor.fetchone()[0]  # Fetch the name

#                 # Append ingredient details to the fridge data
#                 fridge_data[fridge_id].append((ingredient_name, quantity))

#         # Display the fridge contents
#         for fridge_id, items in fridge_data.items():
#             print(f"\nFridge {fridge_id}")
#             print(f"{'Ingredient Name':<20}{'Quantity':<10}")
#             for ingredient_name, quantity in items:
#                 print(f"{ingredient_name:<20}{quantity:<10}")
#         # Prompt the user to choose a fridge
#         while True:
#             fridge_choice = input("\nWhich Fridge do you want to choose? : ")

#             # Check if the entered fridge ID exists
#             if fridge_choice.isdigit() and int(fridge_choice) in fridge_data:
#                 print(f"You selected Fridge {fridge_choice}")
#                 break  # Exit loop if valid choice
#             else:
#                 print("Invalid fridge choice. Please choose a valid fridge.")
#     except Exception as e:
#         print("Error:", e)
#     finally:
#         cursor.close()

# display_all_fridge_contents()
# connection.close()