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
# Function to fetch all existing users
def fetch_existing_users():
    """Fetch existing users from the database."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT DISTINCT user_id 
            FROM User_Inventory_Table;
        """)
        existing_users = [row[0] for row in cursor.fetchall()]
        return existing_users
    except Exception as e:
        print("Error fetching existing users:", e)
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
# Function to fetch all user data
def fetch_user_data():
    """Fetch user data from the database."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT User_Id, Ingredient_Id_quantity 
            FROM User_Inventory_Table;
        """)
        all_inventory = cursor.fetchall()

        user_data = {}
        for user_id, ingredient_dict in all_inventory:
            ingredient_dict = ast.literal_eval(ingredient_dict)
            user_data[user_id] = {}
            for ingredient_id, quantity in ingredient_dict.items():
                cursor.execute("""
                    SELECT Ing_name
                    FROM Ingredient_Table
                    WHERE Ingredient_Id = %s;
                """, (ingredient_id,))
                ingredient_name = cursor.fetchone()[0]
                user_data[user_id][ingredient_name] = quantity

        return user_data
    except Exception as e:
        print("Error:", e)
        return {}
    finally:
        cursor.close()

def create_html_file():
    """Create an HTML file with user options."""
    existing_users = fetch_existing_users()
    all_ingredients = fetch_all_ingredients()
    user_data = fetch_user_data()
    
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
                overflow-x: hidden;
            }}
            h1 {{
                color: #2c3e50;
                text-align: center;
                position: relative;
            }}
            h1::after {{
                content: "🧊🍎🥬";
                position: absolute;
                top: -10px;
                right: -40px;
                animation: float 3s infinite ease-in-out;
            }}
            h2 {{
                color: #2c3e50;
                text-align: center;
            }}
            @keyframes float {{
                0%, 100% {{
                    transform: translateY(0);
                }}
                50% {{
                    transform: translateY(-10px);
                }}
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
                position: relative;
            }}
            .option-box:hover {{
                transform: translateY(-5px);
                background-color: #eaf2f8;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.15);
            }}
            .option-box::before {{
                content: "👆";
                font-size: 1.5em;
                position: absolute;
                top: -20px;
                left: 10px;
                animation: bounce 2s infinite;
            }}
            @keyframes bounce {{
                0%, 100% {{
                    transform: translateY(0);
                }}
                50% {{
                    transform: translateY(-5px);
                }}
            }}
            #existing-user-section, 
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
                animation: slideIn 0.5s ease-in;
            }}
            @keyframes slideIn {{
                from {{
                    opacity: 0;
                    transform: translateX(-100%);
                }}
                to {{
                    opacity: 1;
                    transform: translateX(0);
                }}
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
                background-color: #dceefb;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .selected-ingredient {{
                background-color: #aed6f1;
                border: 1px solid #5499c7;
            }}
            .quantity-metric-container {{
                display: flex;
                align-items: center;
                gap: 10px;
                margin-top: 10px;
            }}
            .quantity-metric-container select, 
            .quantity-metric-container input {{
                padding: 5px;
                font-size: 0.9em;
            }}
            #done-button {{
                margin-top: 20px;
                padding: 12px 24px;
                background-color: #34495e;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 1em;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
            #done-button:hover {{
                background-color: #2c3e50;
            }}
            #done-button::after {{
                content: "✅";
                margin-left: 10px;
            }}
            #selected-user-message, 
            #ingredient-added-message {{
                margin-top: 20px;
                font-size: 1.2em;
                font-weight: bold;
                color: #2c3e50;
            }}
            #ingredient-added-message {{
                animation: pop 0.5s ease-in-out;
            }}
            @keyframes pop {{
                0% {{
                    transform: scale(0.8);
                    opacity: 0;
                }}
                50% {{
                    transform: scale(1.1);
                    opacity: 1;
                }}
                100% {{
                    transform: scale(1);
                }}
            }}
            .user-ingredient-list {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 10px;
            }}
            .user-ingredient-item {{
                background-color: #f0f0f0;
                padding: 5px 10px;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
            .user-ingredient-item:hover {{
                background-color: #e0e0e0;
            }}
        </style>
    </head>
    <body>
        <h1>Fridge Inventory Management</h1>
        <div class="option-container">
            <div id="existing-user-option" class="option-box">
                <h2>📂 Select Existing User</h2>
                <p>Browse and manage contents of existing users</p>
            </div>
            <div id="create-fridge-option" class="option-box">
                <h2>🆕 Create New Fridge</h2>
                <p>Create a new fridge with available ingredients</p>
            </div>
        </div>

        <div id="existing-user-section">
            <h2>📂 Existing Users</h2>
            <div id="users-ingredients-list" class="ingredient-list">
                {' '.join(f'<div class="ingredient-item user-ingredient-item" data-userid="{user_id}">👥 User {user_id} Inventory: {", ".join(f"{ing} ({qty})" for ing, qty in ingredients.items())}</div>' for user_id, ingredients in user_data.items())}
            </div>
            <div id="user-contents" style="margin-top: 20px;"></div>
            <div id="selected-user-message"></div>
        </div>

        <div id="create-fridge-section">
            <h2>🆕 Create New Fridge</h2>
            <div class="ingredient-list" id="ingredient-list">
                {' '.join(f'<div class="ingredient-item" data-id="{ingredient_id}">🍴 {ingredient_name}</div>' for ingredient_id, ingredient_name in all_ingredients.items())}
            </div>
            <div id="selected-ingredients" style="margin-top: 20px;"></div>
            <button id="done-button" style="display:none;">Done</button>
            <div id="ingredient-added-message"></div>
        </div>

        <script>
            $(document).ready(function () {{
                const existingUsers = {json.dumps(user_data)};
                const allIngredients = {json.dumps(all_ingredients)};

                // Option selection
                $('#existing-user-option').on('click', function() {{
                    $('#existing-user-section').show();
                    $('#create-fridge-section').hide();
                    $('#selected-user-message').empty();
                }});

                $('#create-fridge-option').on('click', function() {{
                    $('#create-fridge-section').show();
                    $('#existing-user-section').hide();
                    $('#selected-user-message').empty();
                }});

                // Existing User Logic
                $('.user-ingredient-item').on('click', function () {{
                    const userId = $(this).data('userid');
                    $('#user-contents').empty();

                    if (userId && existingUsers[userId]) {{
                        const content = existingUsers[userId];
                        for (let name in content) {{
                            $('#user-contents').append(`<p>${{name}}: ${{content[name]}}</p>`);
                        }}
                        $('#selected-user-message').text('You selected user ' + userId);
                    }} else {{
                        $('#selected-user-message').empty();
                    }}
                }});

                // Create Fridge Logic
                $('.ingredient-item:not(.user-ingredient-item)').on('click', function() {{
                    const ingredientId = $(this).data('id');
                    const ingredientName = $(this).text();
                    $(this).toggleClass('selected-ingredient');
                    const selectedDiv = $('#selected-ingredients');
                    const existingItem = selectedDiv.find(`[data-id="${{ingredientId}}"]`);
                    if (existingItem.length) {{
                        existingItem.remove();
                    }} else {{
                        selectedDiv.append(`
                            <div data-id="${{ingredientId}}">
                                <span>${{ingredientName}}:</span>
                                <div class="quantity-metric-container">
                                    <input type="number" min="1" value="1" class="ingredient-quantity">
                                    <select class="ingredient-metric">
                                        <option value="ml">ml</option>
                                        <option value="g">g</option>
                                        <option value="unit">Unit</option>
                                    </select>
                                </div>
                            </div>
                        `);
                    }}
                    $('#done-button').toggle($('#selected-ingredients').children().length > 0);
                }});

                // Done Button Logic
                $('#done-button').on('click', function() {{
                    $('#ingredient-added-message').text('🎉 Ingredients added successfully!');
                    $('#done-button').hide();
                }});
            }});
        </script>
    </body>
    </html>
    """
    #Write to an HTML file (temporary one)
    with open('fridge_contents.html', 'w', encoding='utf-8') as f:
        f.write(html_content) 
    #Opening it in a web browser
    webbrowser.open('file://' + os.path.realpath('fridge_contents.html'))
if __name__ == '__main__':
    create_html_file()