CREATE TABLE Recipe (
    recipe_id INT PRIMARY KEY,
    recipe_name TEXT NOT NULL,
    ingredient_list TEXT,  -- Dictionary of ingredients with their quantities and importance as values
    preparation_time INT,  -- Time in minutes
    serving_size INT,  -- Number of servings
    dietary_requirement TEXT CHECK (dietary_requirement IN ('veg', 'non-veg')),
    instructions TEXT 
);

CREATE TABLE Ingredient (
    ingredient_id INT PRIMARY KEY,
    ingredient_name TEXT NOT NULL,
    alternatives_list TEXT 
);

CREATE TABLE UserInventory (
    user_id INT NOT NULL,
    fridge_id INT NOT NULL,
    ingredients TEXT NOT NULL, 
    PRIMARY KEY (user_id, fridge_id)
);

