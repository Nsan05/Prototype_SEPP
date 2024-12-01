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

INSERT INTO Ingredient (ingredient_id, ingredient_name, alternatives_list)
VALUES
(101, 'Tomato', '["cherry tomato", "plum tomato"]'),
(102, 'Cucumber', '["english cucumber", "persian cucumber"]'),
(103, 'Red Onion', '["sweet onion", "white onion"]'),
(201, 'Chicken Breast', '["chicken thigh", "turkey breast"]'),
(202, 'Ginger', '["ginger paste", "minced ginger"]'),
(203, 'Coconut Milk', '["cream", "almond milk"]'),
(204, 'Curry Powder', '["garam masala", "turmeric"]'),
(205, 'Garlic', '["garlic paste", "dried garlic"]'),
(301, 'Mixed Vegetables', '["frozen vegetables", "seasonal vegetables"]'),
(302, 'Olive Oil', '["vegetable oil", "canola oil"]'),
(401, 'Bread', '["whole wheat bread", "sourdough"]'),
(402, 'Egg', '["egg whites", "vegan egg substitute"]'),
(501, 'Banana', '["frozen banana", "plantain"]'),
(502, 'Greek Yogurt', '["regular yogurt", "plant-based yogurt"]'),
(503, 'Honey', '["agave syrup", "maple syrup"]'),
(601, 'Salmon', '["trout", "tilapia"]'),
(602, 'Lemon', '["lime", "preserved lemon"]'),
(603, 'Dill', '["dried dill", "parsley"]'),
(701, 'Beef', '["ground beef", "steak", "sirloin"]'),
(702, 'Tofu', '["tempeh", "seitan", "plant-based protein"]'),
(703, 'Shrimp', '["prawns", "crab", "imitation crab"]'),
(704, 'Lamb', '["goat meat", "mutton"]'),
(801, 'Spinach', '["kale", "swiss chard", "collard greens"]'),
(802, 'Bell Pepper', '["capsicum", "paprika", "chili pepper"]'),
(803, 'Eggplant', '["aubergine", "brinjal"]'),
(804, 'Zucchini', '["courgette", "summer squash"]'),
(805, 'Carrot', '["baby carrot", "rainbow carrot"]'),
(901, 'Rice', '["basmati rice", "brown rice", "jasmine rice"]'),
(902, 'Pasta', '["spaghetti", "penne", "gluten-free pasta"]'),
(903, 'Potato', '["sweet potato", "yam", "fingerling potato"]'),
(1001, 'Cheese', '["cheddar", "mozzarella", "vegan cheese"]'),
(1002, 'Milk', '["almond milk", "soy milk", "oat milk"]'),
(1003, 'Cream', '["heavy cream", "light cream", "coconut cream"]'),
(1101, 'Basil', '["fresh basil", "dried basil", "thai basil"]'),
(1102, 'Cilantro', '["coriander leaves", "chinese parsley"]'),
(1103, 'Mint', '["peppermint", "spearmint"]'),
(1104, 'Paprika', '["smoked paprika", "hot paprika"]'),
(1105, 'Cumin', '["ground cumin", "whole cumin seeds"]'),
(1201, 'Apple', '["green apple", "red apple", "cooking apple"]'),
(1202, 'Orange', '["mandarin", "clementine", "blood orange"]'),
(1203, 'Avocado', '["hass avocado", "fuerte avocado"]'),
(1301, 'Soy Sauce', '["tamari", "light soy sauce", "dark soy sauce"]'),
(1302, 'Vinegar', '["apple cider vinegar", "rice vinegar", "balsamic vinegar"]'),
(1303, 'Mustard', '["dijon mustard", "whole grain mustard", "yellow mustard"]'),
(1401, 'Sugar', '["brown sugar", "raw sugar", "coconut sugar"]'),
(1402, 'Flour', '["wheat flour", "almond flour", "gluten-free flour"]'),
(1403, 'Vanilla Extract', '["vanilla bean", "vanilla paste"]'),
(1501, 'Almonds', '["sliced almonds", "almond flour", "roasted almonds"]'),
(1502, 'Chia Seeds', '["ground chia", "whole chia seeds"]'),
(1503, 'Peanut', '["roasted peanuts", "peanut butter"]'),
(1601, 'Quinoa', '["red quinoa", "white quinoa", "black quinoa"]'),
(1602, 'Lentils', '["red lentils", "green lentils", "brown lentils"]'),
(1603, 'Chickpeas', '["canned chickpeas", "dried chickpeas", "roasted chickpeas"]'),
(1604, 'Nutritional Yeast', '["fortified nutritional yeast", "non-fortified nutritional yeast"]'),
(1605, 'Tahini', '["light tahini", "dark tahini", "whole sesame tahini"]');