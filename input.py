# #LIGHT THEME
import psycopg2
import ast
import os
import json
import webbrowser
import flask
from flask import Flask, request, jsonify
from flask_cors import CORS

# Connect to the PostgreSQL database
# connection = psycopg2.connect(
#     dbname="prototype",
#     user="postgres",
#     password="idkpassword_2024",
#     host="localhost",
#     port="5432"
# )
connection = psycopg2.connect(
    dbname="sepp1",
    user="postgres",
    password="raisa",
    host="localhost",
    port="5432"
)
#raisa-func added to access user id 
def get_next_user_id():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COALESCE(MAX(user_id), 0) + 1 FROM UserInventory")
        next_user_id = cursor.fetchone()[0]
        return next_user_id
    except Exception as e:
        print(f"Error getting next user ID: {e}")
        return None
    finally:
        cursor.close()
    
# Function to save user inventory -- changed made(raisa)
def save_user_inventory(user_id, inventory_dict):
    """
    Save user inventory to the database and print details to the terminal.
    
    Args:
    user_id (int): The unique identifier for the user
    inventory_dict (dict): Dictionary of ingredients with their quantities
    """
    try:
        user_id = get_next_user_id()
        fridge_id = user_id  # Use same ID for fridge
        cursor = connection.cursor()
        
        # Convert inventory dict to string representation for database storage
        inventory_str = str(inventory_dict)
        
        # Insert or update user inventory - raisa(changed command)
        cursor.execute("""
            INSERT INTO UserInventory (User_Id, Fridge_Id, Ingredients)
            VALUES (%s, %s, %s);
        """, (user_id, fridge_id, inventory_str))
        
        connection.commit()
        
        # Print user inventory details to terminal
        print(f"\n--- New User Inventory (User ID: {user_id}) ---")
        all_ingredients = fetch_all_ingredients()
        for ingredient_id, quantity in ast.literal_eval(inventory_str).items():
            ingredient_name = all_ingredients.get(str(ingredient_id), "Unknown Ingredient")
            print(f"- {ingredient_name} (ID: {ingredient_id}): {quantity}")
        print("-------------------------\n")
        
        return True
    except Exception as e:
        print(f"Error saving user inventory: {e}")
        connection.rollback()
        return Nonde
    finally:
        cursor.close()

# Function to fetch all existing users
def fetch_existing_users():
    """Fetch existing users from the database."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT DISTINCT user_id 
            FROM UserInventory;
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
    """Fetch all available ingredients from the Ingredient."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Ingredient_Id, Ingredient_name
            FROM Ingredient;
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
            SELECT User_Id, Ingredients 
            FROM UserInventory;
        """)
        all_inventory = cursor.fetchall()

        user_data = {}
        for user_id, ingredient_dict in all_inventory:
            ingredient_dict = ast.literal_eval(ingredient_dict)
            user_data[user_id] = {}
            for ingredient_id, quantity in ingredient_dict.items():
                cursor.execute("""
                    SELECT Ingredient_name
                    FROM Ingredient
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
def log_selected_ingredients(user_id, ingredients):
    """
    Log selected ingredients to the terminal.
    
    Args:
    user_id (int or None): The user ID if an existing user is selected
    ingredients (dict): Dictionary of selected ingredients
    """
    if user_id is not None:
        print(f"\n--- Existing User {user_id} Ingredients ---")
        for ingredient_name, quantity in ingredients.items():
            print(f"- {ingredient_name}: {quantity}")
    else:
        print("\n--- New Fridge Ingredients ---")
        all_ingredients = fetch_all_ingredients()
        for ingredient_id, quantity in ingredients.items():
            ingredient_name = all_ingredients.get(ingredient_id, "Unknown Ingredient")
            print(f"- {ingredient_name}: {quantity}")
    print("----------------------------\n")

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
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <style>
            :root {{
                --primary-blue: #3498db;
                --dark-blue: #2980b9;
                --light-blue: #5dade2;
                --background-blue: #ebf5fb;
                --text-color: #2c3e50;
            }}

            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: 'Poppins', sans-serif;
                background-color: var(--background-blue);
                color: var(--text-color);
                max-width: 900px;
                margin: 30px auto;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
                background-image: linear-gradient(to bottom right, 
                    rgba(255, 255, 255, 0.3), 
                    rgba(255, 255, 255, 0.1)
                );
            }}

            h1 {{
                color: var(--dark-blue);
                text-align: center;
                font-weight: 600;
                margin-bottom: 30px;
                position: relative;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
            }}

            h1::after {{
                content: "🧊🍎🥬";
                position: absolute;
                top: -10px;
                right: -40px;
                animation: float 3s infinite ease-in-out;
            }}

            h2 {{
                color: var(--dark-blue);
                text-align: center;
                margin-bottom: 15px;
                font-weight: 500;
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
                gap: 20px;
            }}

            .option-box {{
                flex: 1;
                border: 2px solid var(--light-blue);
                background-color: white;
                padding: 25px;
                text-align: center;
                cursor: pointer;
                border-radius: 15px;
                transition: all 0.3s ease;
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
                position: relative;
                overflow: hidden;
            }}

            .option-box::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(45deg, 
                    rgba(var(--light-blue), 0.1), 
                    rgba(var(--dark-blue), 0.1)
                );
                opacity: 0;
                transition: opacity 0.3s ease;
                z-index: 1;
            }}

            .option-box:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
            }}

            .option-box:hover::before {{
                opacity: 1;
            }}

            .option-box p {{
                color: var(--text-color);
                opacity: 0.7;
            }}

            #existing-user-section, 
            #create-fridge-section {{
                display: none;
                margin-top: 20px;
                padding: 25px;
                background-color: white;
                border: 2px solid var(--light-blue);
                border-radius: 15px;
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
            }}

            .ingredient-list {{
                max-height: 300px;
                overflow-y: auto;
                border: 1px solid var(--light-blue);
                padding: 15px;
                margin-top: 15px;
                background-color: var(--background-blue);
                border-radius: 10px;
                scrollbar-width: thin;
                scrollbar-color: var(--light-blue) transparent;
            }}

            .ingredient-list::-webkit-scrollbar {{
                width: 8px;
            }}

            .ingredient-list::-webkit-scrollbar-thumb {{
                background-color: var(--light-blue);
                border-radius: 4px;
            }}

            .ingredient-item {{
                padding: 10px;
                margin-bottom: 8px;
                background-color: white;
                border: 1px solid var(--light-blue);
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}

            .ingredient-item:hover {{
                background-color: var(--background-blue);
                transform: scale(1.02);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}

            .selected-ingredient {{
                background-color: var(--light-blue);
                color: white;
            }}

            .quantity-metric-container {{
                display: flex;
                align-items: center;
                gap: 10px;
                margin-top: 10px;
            }}

            .quantity-metric-container select, 
            .quantity-metric-container input {{
                padding: 8px;
                border: 1px solid var(--light-blue);
                border-radius: 5px;
                font-size: 0.9em;
            }}

            #done-button {{
                display: none;
                margin-top: 20px;
                padding: 12px 24px;
                background-color: var(--dark-blue);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 1em;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }}

            #done-button:hover {{
                background-color: var(--primary-blue);
                transform: translateY(-3px);
            }}

            #selected-user-message, 
            #ingredient-added-message {{
                margin-top: 20px;
                font-size: 1.2em;
                font-weight: 600;
                color: var(--dark-blue);
                text-align: center;
            }}

            .user-ingredient-list {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 10px;
            }}
            .user-ingredient-item {{
                background-color: var(--background-blue);
                padding: 8px 12px;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s ease;
                border: 1px solid var(--light-blue);
            }}

            .user-ingredient-item:hover {{
                background-color: var(--light-blue);
                color: white;
            }}
             /* raisa- added styles for recipe display */
            #recipe-suggestions-section {{
                margin-top: 30px;
                padding:20px;
                background-color: white;
                border-radius:15px;
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
            }}

            .recipe-list {{
                display: flex;
                flex-wrap:wrap;
                gap: 15px;
                justify-content: center;
            }}

            .recipe-card {{
                background-color:var(--background-blue);
                border: 1px solid var(--light-blue);
                border-radius: 10px;
                padding:15px;
                width:250px;
                text-align:center;
                transition:all 0.3s ease;
            }}

            .recipe-card:hover {{
                transform:scale(1.05);
                box-shadow:0 5px 15px rgba(0, 0, 0, 0.2);
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
            <button id="done-button">Done</button>
            <div id="ingredient-added-message"></div>

        <!-- raisa-added section for recipe suggestion  -->
        <div id="recipe-suggestions-section" style="display:none;">
            <h2>🍽️ Recipe Suggestions</h2>
            <div id="complete-recipes-section">
                <h3>Complete Recipes</h3>
                <div id="complete-recipes-list" class="recipe-list"></div>
            </div>
            <div id="partial-recipes-section">
                <h3>Partial Recipes</h3>
                <div id="partial-recipes-list" class="recipe-list"></div>
            </div>
        </div>

        <script>
        //raisa-recip suggestion func
           function suggestRecipes(ingredients) {{
                $.ajax({{
                    url: 'http://localhost:5000/suggest_recipes',
                    method:'POST',
                    contentType:'application/json',
                    data: JSON.stringify({{
                        'inventory':ingredients
                    }}),
                    success: function(response) {{
                        $('#recipe-suggestions-section').show();
                        //display complete
                        const completeRecipesList =$('#complete-recipes-list');
                        completeRecipesList.empty();
                        response.complete_recipes.forEach(recipe => {{
                            completeRecipesList.append(`
                                <div class="recipe-card">
                                    <h4>${{recipe.recipe}}</h4>
                                    <p>Total Score:${{recipe.total.toFixed(2)}}</p>
                                </div>
                            `);
                        }});

                        //display full
                        const partialRecipesList= $('#partial-recipes-list');
                        partialRecipesList.empty();
                        response.partial_recipes.forEach(recipe => {{
                            partialRecipesList.append(`
                                <div class="recipe-card">
                                    <h4>${{recipe.recipe}}</h4>
                                    <p>Total Score:${{recipe.total.toFixed(2)}}</p>
                                    <p>Score 1: ${{recipe.score1.toFixed(2)}}</p>
                                    <p>Score 2:${{recipe.score2.toFixed(2)}}</p>
                                </div>
                            `);
                        }});
                    }},
                    error: function(error) {{
                        console.error('Error getting recipe suggestions:', error);
                    }}
                }});
            }}
            // Global variables to store selected user or new fridge data
            let selectedUserId = null;
            let selectedUserIngredients = null;
            let newFridgeIngredients = {{}};

            $(document).ready(function () {{
                const existingUsers = {json.dumps(user_data)};
                const allIngredients = {json.dumps(all_ingredients)};

                // Option selection
                $('#existing-user-option').on('click', function() {{
                    $('#existing-user-section').show();
                    $('#create-fridge-section').hide();
                    $('#selected-user-message').empty();
                    // Reset new fridge data
                    newFridgeIngredients = {{}};
                }});

                $('#create-fridge-option').on('click', function() {{
                    $('#create-fridge-section').show();
                    $('#existing-user-section').hide();
                    $('#selected-user-message').empty();
                    // Reset selected user data
                    selectedUserId = null;
                    selectedUserIngredients = null;
                }});

                // Existing User Logic
                $('.user-ingredient-item').on('click', function () {{
                    const userId = $(this).data('userid');
                    $('#user-contents').empty();

                    if (userId && existingUsers[userId]) {{
                        // Save selected user data to global variables
                        selectedUserId = userId;
                        selectedUserIngredients = existingUsers[userId];

                        const content = existingUsers[userId];
                        for (let name in content) {{
                            $('#user-contents').append(`<p>${{name}}: ${{content[name]}}</p>`);
                        }}
                        $('#selected-user-message').text('You selected user ' + userId);

                        //raisa- suggesting recipes for this user inventory
                        const userIngredients = Object.fromEntries(
                            Object.entries(existingUsers[userId]).map(([name, qty]) => 
                                [Object.keys(allIngredients).find(k => allIngredients[k] === name), qty]
                            )
                        );
                        suggestRecipes(userIngredients, userId);
                        // Log to the terminal
                        console.log('Selected User ID:', userId);
                        console.log('Selected User Ingredients:', selectedUserIngredients);
                    }} else {{
                        $('#selected-user-message').empty();
                        selectedUserId = null;
                        selectedUserIngredients = null;
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
                        delete newFridgeIngredients[ingredientId];
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

            //raisa- combined the the done button handlers 
            $('#done-button').on('click', function() {{
            
            newFridgeIngredients = {{}};
            $('#selected-ingredients>div').each(function() {{
                const ingredientId = $(this).data('id');
                const quantity = $(this).find('.ingredient-quantity').val();
                const metric = $(this).find('.ingredient-metric').val();
                newFridgeIngredients[ingredientId] = quantity+metric;
            }});

            $('#ingredient-added-message').text('🎉 Ingredients added successfully!');
            $('#done-button').hide();
        
            suggestRecipes(newFridgeIngredients);
            console.log('New Fridge Ingredients:', newFridgeIngredients);
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
app = Flask(__name__)
CORS(app)

@app.route('/log_ingredients', methods=['POST'])
def log_ingredients():
    data = request.json
    user_id = save_user_inventory(ingredients)
    ingredients = data.get('ingredients')
    if user_id:
        return jsonify({"status": "success", "user_id": user_id})
    else:
        return jsonify({"status": "error"}), 500
   
if __name__ == '__main__':
    create_html_file()