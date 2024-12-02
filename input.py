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

def create_html_file():
    """Create an HTML file with fridge options."""
    existing_fridges = fetch_existing_fridges()
    all_ingredients = fetch_all_ingredients()
    fridge_data = fetch_fridge_data()
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fridge Inventory Management</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f8f9fa;
                color: #333;
                max-width: 900px;
                margin: 30px auto;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }}
            h1, h2 {{
                color: #4CAF50;
                text-align: center;
            }}
            .option-container {{
                display: flex;
                justify-content: space-around;
                margin-bottom: 30px;
            }}
            .option-box {{
                border: 1px solid #ddd;
                background-color: #ffffff;
                padding: 20px;
                width: 40%;
                text-align: center;
                cursor: pointer;
                border-radius: 10px;
                transition: transform 0.2s, background-color 0.3s, box-shadow 0.3s;
            }}
            .option-box:hover {{
                transform: translateY(-5px);
                background-color: #f0f8ff;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.15);
            }}
            #existing-fridge-section, 
            #create-fridge-section {{
                display: none;
                margin-top: 20px;
                padding: 20px;
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 10px;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .ingredient-list {{
                max-height: 300px;
                overflow-y: auto;
                border: 1px solid #ddd;
                padding: 10px;
                margin-top: 10px;
                background-color: #fefefe;
                border-radius: 5px;
            }}
            .ingredient-item {{
                padding: 8px;
                margin-bottom: 5px;
                background-color: #f9f9f9;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s, box-shadow 0.3s;
            }}
            .ingredient-item:hover {{
                background-color: #e9f5e9;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .selected-ingredient {{
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
            }}
            .quantity-metric-container {{
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .quantity-metric-container select, 
            .quantity-metric-container input {{
                padding: 5px;
                font-size: 0.9em;
            }}
            #done-button {{
                margin-top: 20px;
                padding: 12px 24px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 1em;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
            #done-button:hover {{
                background-color: #218838;
            }}
            #fridge-select {{
                padding: 10px;
                font-size: 1em;
                width: 100%;
                border-radius: 5px;
                border: 1px solid #ddd;
            }}
            p {{
                margin: 10px 0;
            }}
            #selected-fridge-message, 
            #ingredient-added-message {{
                margin-top: 20px;
                font-size: 1.2em;
                font-weight: bold;
                color: #155724;
            }}
        </style>
    </head>
    <body>
        <h1>Fridge Inventory Management</h1>
        <div class="option-container">
            <div id="existing-fridge-option" class="option-box">
                <h2>Select Existing Fridge</h2>
                <p>Browse and manage contents of existing fridges</p>
            </div>
            <div id="create-fridge-option" class="option-box">
                <h2>Create New Fridge</h2>
                <p>Create a new fridge with available ingredients</p>
            </div>
        </div>

        <div id="existing-fridge-section">
            <h2>Existing Fridges</h2>
            <select id="fridge-select">
                <option value="">-- Select a Fridge --</option>
                {' '.join(f'<option value="{fridge_id}">{fridge_id}</option>' for fridge_id in existing_fridges)}
            </select>
            <div id="fridge-contents" style="margin-top: 20px;"></div>
            <div id="selected-fridge-message"></div>
        </div>

        <div id="create-fridge-section">
            <h2>Create New Fridge</h2>
            <div class="ingredient-list" id="ingredient-list">
                {' '.join(f'<div class="ingredient-item" data-id="{ingredient_id}">{ingredient_name}</div>' for ingredient_id, ingredient_name in all_ingredients.items())}
            </div>
            <div id="selected-ingredients" style="margin-top: 20px;"></div>
            <button id="done-button" style="display:none;">Done</button>
            <div id="ingredient-added-message"></div>
        </div>

        <script>
            $(document).ready(function () {{
                const existingFridges = {json.dumps(fridge_data)}; 
                const allIngredients = {json.dumps(all_ingredients)}; 

                // Option selection
                $('#existing-fridge-option').on('click', function() {{
                    $('#existing-fridge-section').show();
                    $('#create-fridge-section').hide();
                    $('#selected-fridge-message').empty();
                }});

                $('#create-fridge-option').on('click', function() {{
                    $('#create-fridge-section').show();
                    $('#existing-fridge-section').hide();
                    $('#selected-fridge-message').empty();
                }});

                // Existing Fridge Logic
                $('#fridge-select').on('change', function () {{
                    const fridgeId = $(this).val();
                    $('#fridge-contents').empty();

                    if (fridgeId && existingFridges[fridgeId]) {{
                        const content = existingFridges[fridgeId];
                        for (let name in content) {{
                            $('#fridge-contents').append(`<p>${{name}}: ${{content[name]}}</p>`);
                        }}
                        $('#selected-fridge-message').text('You selected fridge ' + fridgeId);
                    }} else {{
                        $('#selected-fridge-message').empty();
                    }}
                }});

                // Create Fridge Logic
                $('.ingredient-item').on('click', function() {{
                    const ingredientId = $(this).data('id');
                    const ingredientName = $(this).text();
                    $(this).toggleClass('selected-ingredient');
                    const selectedDiv = $('#selected-ingredients');
                    const existingItem = selectedDiv.find(`[data-id="${{ingredientId}}"]`);
                    if (existingItem.length) {{
                        existingItem.remove();
                    }} else {{
                        selectedDiv.append(`<p data-id="${{ingredientId}}">${{ingredientName}}</p>`);
                    }}
                    $('#done-button').toggle($('#selected-ingredients').children().length > 0);
                }});

                // Done Button Logic
                $('#done-button').on('click', function() {{
                    $('#ingredient-added-message').text('Ingredients added successfully!');
                    $('#done-button').hide();
                }});
            }});
        </script>
    </body>
    </html>
    """
    #Write to an HTML file (temporary one)
    with open('fridge_contents.html', 'w') as f:
        f.write(html_content)
    
    #Opening it in a web browser
    webbrowser.open('file://' + os.path.realpath('fridge_contents.html'))
if __name__ == '__main__':
    create_html_file()