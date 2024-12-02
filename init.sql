CREATE DATABASE recipe_db; --remove for docker

\c recipe_db -- remove for docker

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
    PRIMARY KEY (user_id)
);

INSERT INTO Recipe (recipe_id, recipe_name, ingredient_list, preparation_time, serving_size, dietary_requirement, instructions)
VALUES 
(1, 'Mediterranean Tomato Cucumber Salad', 
    '{101: ["200g", "core"], 102: ["150g", "core"], 103: ["50g", "secondary"], 302: ["30ml", "secondary"]}', 
    15, 2, 'veg', 
    '1. Wash and chop tomatoes and cucumber into bite-sized pieces. 2. Thinly slice red onion. 3. Mix vegetables in a bowl. 4. Drizzle with olive oil. 5. Season with salt and pepper. 6. Serve chilled.'),

(2, 'Coconut Chicken Curry', 
    '{201: ["500g", "core"], 202: ["20g", "core"], 203: ["400ml", "core"], 
      204: ["30g", "secondary"], 205: ["10g", "secondary"], 
      302: ["30ml", "secondary"]}', 
    60, 4, 'non-veg', 
    '1. Chop chicken into cubes. 2. Sauté ginger and garlic in olive oil. 3. Add chicken and brown. 4. Stir in curry powder. 5. Pour coconut milk and simmer for 40 minutes. 6. Serve hot with rice.'),

(3, 'Vegetable Medley Roast', 
    '{301: ["400g", "core"], 302: ["50ml", "core"], 
      204: ["10g", "secondary"], 205: ["5g", "secondary"]}', 
    45, 3, 'veg', 
    '1. Chop mixed vegetables into uniform pieces. 2. Toss with olive oil and minced garlic. 3. Sprinkle curry powder. 4. Roast in oven at 200°C for 30 minutes. 5. Serve hot as a side dish.'),

(4, 'Classic Egg Toast', 
    '{401: ["2", "core"], 402: ["2", "core"], 302: ["10ml", "secondary"], 
      205: ["2", "optional"]}', 
    10, 1, 'non-veg', 
    '1. Heat olive oil in a pan. 2. Toast bread. 3. Fry eggs sunny-side up. 4. Place eggs on toast. 5. Sprinkle minced garlic if desired. 6. Season with salt and pepper.'),

(5, 'Banana Honey Smoothie', 
    '{501: ["200g", "core"], 
      502: ["150ml", "core"], 
      503: ["30ml", "secondary"], 
      302: ["10ml", "optional"]}', 
    10, 2, 'veg', 
    '1. Peel and chop banana. 2. Blend banana with Greek yogurt. 3. Add honey for sweetness. 4. Optional: Add a drop of olive oil for richness. 5. Blend until smooth. 6. Serve chilled.'),

(6, 'Lemon Dill Salmon', 
    '{601: ["600g", "core"], 
      602: ["30ml", "secondary"], 
      603: ["10g", "secondary"], 
      302: ["20ml", "core"]}', 
    40, 4, 'non-veg', 
    '1. Preheat oven to 180°C. 2. Place salmon on baking tray. 3. Drizzle with olive oil. 4. Squeeze lemon juice over salmon. 5. Sprinkle chopped fresh dill. 6. Bake for 20-25 minutes. 7. Serve hot with lemon wedges.'),

(7, 'Spinach and Tofu Stir Fry', 
    '{702: ["300g", "core"], 
      801: ["200g", "core"], 
      802: ["100g", "secondary"], 
      1101: ["10g", "secondary"], 
      1301: ["30ml", "secondary"]}', 
    25, 3, 'veg', 
    '1. Press and cube tofu. 2. Chop spinach and bell peppers. 3. Heat oil in a wok. 4. Stir-fry tofu until golden. 5. Add spinach and peppers. 6. Season with soy sauce and fresh basil. 7. Serve hot.'),

(8, 'Mediterranean Lamb with Roasted Vegetables', 
    '{704: ["500g", "core"], 
      803: ["250g", "core"], 
      804: ["200g", "core"], 
      805: ["150g", "secondary"], 
      1102: ["15g", "secondary"], 
      1104: ["5g", "secondary"]}', 
    70, 4, 'non-veg', 
    '1. Marinate lamb with paprika and herbs. 2. Chop eggplant, zucchini, and carrots. 3. Roast vegetables with olive oil. 4. Grill lamb to desired doneness. 5. Garnish with fresh cilantro. 6. Serve with roasted vegetables.'),

(9, 'Avocado and Shrimp Rice Bowl', 
    '{703: ["250g", "core"], 
      1203: ["200g", "core"], 
      901: ["150g", "core"], 
      802: ["100g", "secondary"], 
      1302: ["20ml", "secondary"], 
      1103: ["10g", "optional"]}', 
    30, 2, 'non-veg', 
    '1. Cook rice. 2. Sauté shrimp with vinegar. 3. Slice avocado and bell peppers. 4. Assemble rice bowl. 5. Top with fresh mint. 6. Drizzle with dressing.'),

(10, 'Vegetarian Potato and Cheese Bake', 
    '{903: ["400g", "core"], 
      1001: ["200g", "core"], 
      801: ["150g", "secondary"], 
      1105: ["5g", "secondary"], 
      1402: ["50g", "optional"]}', 
    55, 3, 'veg', 
    '1. Slice potatoes. 2. Layer with spinach and cheese. 3. Sprinkle cumin. 4. Optional: Add flour for thickening. 5. Bake until golden and crispy. 6. Let rest for 10 minutes before serving.'),

(11, 'Apple Cinnamon Oatmeal', 
    '{1201: ["200g", "core"], 
      1401: ["30g", "secondary"], 
      1403: ["10ml", "secondary"], 
      1502: ["15g", "optional"]}', 
    20, 2, 'veg', 
    '1. Dice apples. 2. Cook with sugar and vanilla. 3. Add chia seeds if desired. 4. Serve warm. 5. Can be topped with additional fruits or nuts.'),

(12, 'Beef and Vegetable Pasta', 
    '{701: ["400g", "core"], 
      902: ["250g", "core"], 
      802: ["150g", "secondary"], 
      804: ["100g", "secondary"], 
      1303: ["20g", "optional"]}', 
    45, 4, 'non-veg', 
    '1. Brown beef in pan. 2. Cook pasta. 3. Sauté bell peppers and zucchini. 4. Mix all ingredients. 5. Optional: Add mustard for extra flavor. 6. Garnish and serve hot.'),

(13, 'Zucchini Noodle Shrimp Alfredo', 
    '{703: ["300g", "core"], 
      804: ["400g", "core"], 
      1003: ["200ml", "core"], 
      1001: ["100g", "secondary"], 
      1101: ["15g", "secondary"]}', 
    35, 2, 'non-veg', 
    '1. Spiralize zucchini into noodles. 2. Sauté shrimp until pink. 3. Make cream sauce with cheese. 4. Combine shrimp, zucchini noodles, and sauce. 5. Garnish with fresh basil. 6. Serve immediately.'),

(14, 'Spicy Tofu and Bell Pepper Curry', 
    '{702: ["350g", "core"], 
      802: ["200g", "core"], 
      203: ["300ml", "core"], 
      1104: ["10g", "secondary"], 
      1105: ["5g", "secondary"], 
      1102: ["15g", "optional"]}', 
    40, 3, 'veg', 
    '1. Press and cube tofu. 2. Chop bell peppers. 3. Create curry base with coconut milk. 4. Add paprika and cumin. 5. Simmer tofu and peppers. 6. Garnish with fresh cilantro. 7. Serve with rice.'),

(15, 'Mediterranean Lamb Salad', 
    '{704: ["400g", "core"], 
      801: ["150g", "core"], 
      102: ["100g", "core"], 
      103: ["50g", "secondary"], 
      1302: ["30ml", "secondary"], 
      1101: ["10g", "optional"]}', 
    45, 4, 'non-veg', 
    '1. Grill lamb to medium rare. 2. Slice thinly. 3. Prepare bed of spinach and cucumber. 4. Add red onions. 5. Dress with vinegar. 6. Top with fresh basil. 7. Serve chilled or at room temperature.'),

(16, 'Loaded Vegetable Potato Skins', 
    '{903: ["500g", "core"], 
      1001: ["150g", "core"], 
      802: ["100g", "secondary"], 
      801: ["100g", "secondary"], 
      1503: ["50g", "optional"]}', 
    60, 4, 'veg', 
    '1. Bake potatoes until soft. 2. Scoop out potato centers. 3. Fill with cheese, bell peppers, and spinach. 4. Top with chopped peanuts if desired. 5. Bake until cheese melts. 6. Serve hot.'),

(17, 'Tropical Shrimp Coconut Rice', 
    '{703: ["300g", "core"], 
      901: ["200g", "core"], 
      203: ["250ml", "core"], 
      1202: ["150g", "secondary"], 
      1103: ["10g", "optional"]}', 
    35, 3, 'non-veg', 
    '1. Cook rice in coconut milk. 2. Sauté shrimp. 3. Segment oranges. 4. Mix shrimp with rice. 5. Garnish with fresh mint. 6. Serve with orange segments.'),

(18, 'Vegan Lentil and Vegetable Stew', 
    '{702: ["250g", "core"], 
      801: ["200g", "core"], 
      804: ["150g", "core"], 
      1105: ["5g", "secondary"], 
      1104: ["5g", "secondary"], 
      1102: ["15g", "optional"]}', 
    50, 4, 'veg', 
    '1. Crumble tofu. 2. Chop spinach and zucchini. 3. Create stew base with cumin and paprika. 4. Slow cook all ingredients. 5. Garnish with fresh cilantro. 6. Serve with crusty bread.'),

(19, 'Apple Almond Breakfast Parfait', 
    '{1201: ["200g", "core"], 
      1501: ["100g", "core"], 
      1002: ["250ml", "core"], 
      1401: ["30g", "secondary"], 
      1502: ["15g", "optional"]}', 
    20, 2, 'veg', 
    '1. Dice apples. 2. Layer with almonds and milk. 3. Sprinkle sugar. 4. Add chia seeds if desired. 5. Chill for 10 minutes. 6. Serve cold.'),

(20, 'Mediterranean Beef and Quinoa Pasta', 
    '{701: ["400g", "core"], 
      902: ["250g", "core"], 
      803: ["150g", "secondary"], 
      1601: ["100g", "secondary"], 
      1103: ["10g", "optional"], 
      1303: ["20g", "secondary"]}', 
    45, 4, 'non-veg', 
    '1. Brown beef in pan. 2. Cook pasta and quinoa separately. 3. Sauté eggplant. 4. Mix beef, pasta, quinoa, and eggplant. 5. Add mustard. 6. Garnish with mint. 7. Serve hot.'),

(21, 'Protein-Packed Chickpea Power Bowl', 
    '{1603: ["250g", "core"], 
      903: ["200g", "core"], 
      801: ["150g", "core"], 
      1605: ["30ml", "secondary"], 
      1103: ["10g", "optional"], 
      302: ["20ml", "core"]}', 
    40, 3, 'veg', 
    '1. Roast sweet potatoes. 2. Prepare chickpeas. 3. Sauté kale in olive oil. 4. Create tahini dressing. 5. Layer ingredients in a bowl. 6. Garnish with mint. 7. Serve at room temperature.'),

(22, 'Spicy Mediterranean Roasted Vegetable and Lentil Medley', 
    '{802: ["250g", "core"], 
      1602: ["200g", "core"], 
      1202: ["150g", "secondary"], 
      302: ["40ml", "core"], 
      1604: ["10g", "secondary"], 
      1104: ["10g", "secondary"], 
      1105: ["10g", "secondary"]}', 
    55, 4, 'veg', 
    '1. Roast cauliflower and bell peppers. 2. Cook lentils. 3. Segment oranges. 4. Toss vegetables with olive oil. 5. Sprinkle with paprika and cumin. 6. Top with nutritional yeast. 7. Garnish with orange segments. 8. Serve hot.'),

(23, 'Coconut Seitan Vegetable Curry', 
    '{702: ["350g", "core"], 
      203: ["300ml", "core"], 
      804: ["200g", "core"], 
      1503: ["30g", "secondary"], 
      1103: ["10g", "optional"], 
      302: ["25ml", "secondary"]}', 
    50, 3, 'veg', 
    '1. Prepare seitan. 2. Roast butternut squash. 3. Create curry base with coconut milk. 4. Add seitan and vegetables. 5. Simmer until flavors meld. 6. Garnish with peanuts and mint. 7. Serve with rice.'),

(24, 'Mediterranean Halloumi and Roasted Vegetable Salad', 
    '{1001: ["250g", "core"], 
      1202: ["150g", "secondary"], 
      102: ["100g", "core"], 
      103: ["50g", "secondary"], 
      302: ["30ml", "core"], 
      1302: ["20ml", "secondary"]}', 
    35, 2, 'veg', 
    '1. Grill halloumi. 2. Roast pumpkin. 3. Prepare cucumber and red onion. 4. Add pomegranate seeds. 5. Create orange-infused dressing. 6. Layer ingredients. 7. Serve chilled.'),

(25, 'Spicy Tempeh and Bok Choy Stir Fry', 
    '{702: ["250g", "core"], 
      1201: ["200g", "core"], 
      804: ["150g", "core"], 
      1301: ["30ml", "secondary"], 
      602: ["20ml", "secondary"], 
      1101: ["10g", "optional"]}', 
    30, 3, 'veg', 
    '1. Press and marinate tempeh. 2. Prepare water chestnuts. 3. Chop bok choy. 4. Heat soy sauce and lime juice in wok. 5. Stir-fry tempeh until golden. 6. Add vegetables. 7. Garnish with Thai basil. 8. Serve immediately.'),

(26, 'Protein-Packed Black Bean and Avocado Bowl', 
    '{1603: ["300g", "core"], 
      1203: ["200g", "core"], 
      902: ["150g", "core"], 
      302: ["40ml", "core"], 
      1102: ["5g", "optional"]}', 
    40, 3, 'veg', 
    '1. Prepare black beans. 2. Roast corn. 3. Slice avocado. 4. Mix ingredients in a bowl. 5. Dress with lime juice and olive oil. 6. Garnish with cilantro and pumpkin seeds. 7. Serve at room temperature.'),

(27, 'Mediterranean Feta and Vegetable Feast', 
    '{1001: ["250g", "core"], 
      102: ["200g", "core"], 
      801: ["150g", "secondary"], 
      302: ["30ml", "core"], 
      1302: ["20ml", "secondary"], 
      1102: ["10g", "optional"]}', 
    35, 2, 'veg', 
    '1. Crumble feta cheese. 2. Roast artichoke hearts. 3. Add sun-dried tomatoes. 4. Chop cucumber and spinach. 5. Dress with balsamic vinegar. 6. Sprinkle dried oregano. 7. Serve chilled or at room temperature.'),

(28, 'Spicy Tempeh and Butternut Squash Curry', 
    '{702: ["350g", "core"], 
      203: ["300ml", "core"], 
      804: ["250g", "core"], 
      1503: ["40g", "secondary"], 
      1102: ["5g", "optional"], 
      302: ["25ml", "secondary"]}', 
    55, 4, 'veg', 
    '1. Prepare tempeh. 2. Roast butternut squash. 3. Create curry base with coconut milk. 4. Add tempeh and squash. 5. Top with roasted cashews. 6. Garnish with pomegranate seeds. 7. Serve with steamed rice.'),

(29, 'Roasted Vegetable and Tempeh Medley', 
    '{702: ["300g", "core"], 
      805: ["200g", "core"], 
      804: ["150g", "core"], 
      302: ["35ml", "core"], 
      1104: ["5g", "secondary"], 
      1105: ["5g", "secondary"], 
      1102: ["10g", "optional"]}', 
    50, 3, 'veg', 
    '1. Press and marinate tempeh. 2. Roast beetroot and fennel. 3. Chop zucchini and carrots. 4. Toss with olive oil and fresh rosemary. 5. Sprinkle paprika and cumin. 6. Drizzle with maple syrup. 7. Serve hot as a main course.'),

(30, 'Protein-Rich Seitan and Vegetable Stir Fry', 
    '{702: ["250g", "core"], 
      1201: ["200g", "core"], 
      804: ["150g", "core"], 
      1301: ["30ml", "secondary"], 
      202: ["20g", "secondary"], 
      1101: ["10g", "optional"]}', 
    35, 2, 'veg', 
    '1. Prepare seitan. 2. Add water chestnuts. 3. Slice purple cabbage and zucchini. 4. Heat soy sauce in wok. 5. Stir-fry with fresh ginger. 6. Garnish with toasted sesame seeds. 7. Serve immediately.'),

(31, 'Rustic Chicken Thigh Curry', 
    '{1611: ["500g", "core"], 1613: ["20g", "core"], 203: ["400ml", "core"], 
      1617: ["30g", "secondary"], 1619: ["10g", "secondary"], 
      1623: ["30ml", "secondary"]}', 
    55, 4, 'non-veg', 
    '1. Marinate chicken thighs in ginger paste. 2. Sauté ginger paste in vegetable oil. 3. Add chicken and brown. 4. Stir in garam masala. 5. Pour coconut milk and simmer. 6. Serve with rice.'),

(32, 'Whole Wheat Egg White Toast', 
    '{1625: ["2", "core"], 1627: ["2", "core"], 1623: ["10ml", "secondary"], 
      1619: ["2", "optional"]}', 
    10, 1, 'non-veg', 
    '1. Heat vegetable oil in a pan. 2. Toast whole wheat bread. 3. Fry egg whites. 4. Place egg whites on toast. 5. Sprinkle dried garlic if desired. 6. Season to taste.'),

(33, 'Plantain Green Smoothie', 
    '{1630: ["200g", "core"], 
      1631: ["150ml", "core"], 
      1633: ["30ml", "secondary"], 
      1623: ["10ml", "optional"]}', 
    10, 2, 'veg', 
    '1. Peel and chop plantain. 2. Blend plantain with regular yogurt. 3. Add agave syrup for sweetness. 4. Optional: Add vegetable oil for richness. 5. Blend until smooth. 6. Serve chilled.'),

(34, 'Mediterranean Trout with Preserved Lemon', 
    '{1635: ["600g", "core"], 
      1638: ["20ml", "secondary"], 
      1639: ["10g", "secondary"], 
      1623: ["20ml", "core"]}', 
    40, 4, 'non-veg', 
    '1. Preheat oven to 180°C. 2. Place trout on baking tray. 3. Drizzle with vegetable oil. 4. Add preserved lemon. 5. Sprinkle dried dill. 6. Bake for 20-25 minutes. 7. Serve hot with lemon wedges.'),

(35, 'Spicy Tempeh Stir Fry with Thai Basil', 
    '{1644: ["250g", "core"], 
      1684: ["10g", "optional"], 
      804: ["200g", "core"], 
      1701: ["30ml", "secondary"], 
      1637: ["20ml", "secondary"]}', 
    30, 3, 'veg', 
    '1. Press and marinate tempeh. 2. Chop zucchini. 3. Heat tamari and lime juice in wok. 4. Stir-fry tempeh until golden. 5. Add vegetables. 6. Garnish with Thai basil. 7. Serve immediately.'),

(36, 'Prawns with Tilapia Seafood Medley',
    '{1647: ["300g", "core"], 
      1636: ["300g", "core"], 
      1637: ["20ml", "secondary"], 
      1640: ["10g", "optional"], 
      1623: ["30ml", "core"], 
      1705: ["15ml", "secondary"]}',
    35, 4, 'non-veg',
    '1. Clean and devein prawns. 2. Cut tilapia into bite-sized pieces. 3. Heat vegetable oil in a large skillet. 4. Add prawns and tilapia, sear until golden. 5. Deglaze pan with rice vinegar and lime juice. 6. Sprinkle parsley as garnish. 7. Serve hot with side of choice.'),

(37, 'Zucchini and Tofu Mediterranean Stir Fry',
    '{1660: ["300g", "core"],
     1644: ["250g", "core"], 
     1637: ["20ml", "secondary"], 
     1701: ["30ml", "secondary"], 
     1685: ["10g", "optional"]}',
    35, 3, 'veg',
    '1. Press and cube tempeh. 2. Slice summer squash into ribbons. 3. Heat tamari and lime in a wok. 4. Stir-fry tempeh until golden. 5. Add summer squash. 6. Garnish with coriander leaves. 7. Serve hot.'),

(38, 'Sweet Potato and Goat Meat Roast',
    '{1670: ["400g", "core"], 
    1650: ["500g", "core"], 
    1689: ["15g", "secondary"], 
    1623: ["30ml", "secondary"], 
    1682: ["10g", "optional"]}',
    75, 4, 'non-veg',
    '1. Preheat oven to 200°C. 2. Cut sweet potatoes into wedges. 3. Marinate goat meat in vegetable oil. 4. Sprinkle smoked paprika over both. 5. Roast in oven for 60 minutes. 6. Garnish with fresh basil. 7. Serve hot.'),

(39, 'Plantain and Almond Milk Smoothie Bowl',
    '{1630: ["200g", "core"], 
    1676: ["250ml", "core"], 
    1718: ["50g", "topping"], 
    1633: ["20ml", "secondary"]}',
    15, 2, 'veg',
    '1. Blend plantain with almond milk. 2. Add agave syrup for sweetness. 3. Pour into bowl. 4. Top with sliced almonds. 5. Serve chilled.'),

(40, 'Trout with Capsicum and Parsley',
    '{1635: ["600g", "core"],
    1655: ["300g", "core"],
    1640: ["15g", "optional"],
    1623: ["30ml", "secondary"],
    1637: ["10ml", "secondary"]}',
    40, 4, 'non-veg',
    '1. Preheat oven to 180°C. 2. Slice capsicum. 3. Place trout on baking tray. 4. Drizzle with vegetable oil and lime juice. 5. Add capsicum slices. 6. Bake for 25 minutes. 7. Garnish with parsley. 8. Serve hot.');

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
(1605, 'Tahini', '["light tahini", "dark tahini", "whole sesame tahini"]'),
-- Tomato Alternatives
(1605, 'cherry tomato', '["Tomato", "plum tomato"]'),
(1606, 'plum tomato', '["Tomato", "cherry tomato"]'),
-- Cucumber Alternatives
(1607, 'english cucumber', '["Cucumber", "persian cucumber"]'),
(1608, 'persian cucumber', '["Cucumber", "english cucumber"]'),
-- Red Onion Alternatives
(1609, 'sweet onion', '["Red Onion", "white onion"]'),
(1610, 'white onion', '["Red Onion", "sweet onion"]'),
-- Chicken Breast Alternatives
(1611, 'chicken thigh', '["Chicken Breast", "turkey breast"]'),
(1612, 'turkey breast', '["Chicken Breast", "chicken thigh"]'),
-- Ginger Alternatives
(1613, 'ginger paste', '["Ginger", "minced ginger"]'),
(1614, 'minced ginger', '["Ginger", "ginger paste"]'),
-- Coconut Milk Alternatives
(1615, 'cream', '["Coconut Milk", "almond milk"]'),
(1616, 'almond milk', '["Coconut Milk", "cream"]'),
-- Curry Powder Alternatives
(1617, 'garam masala', '["Curry Powder", "turmeric"]'),
(1618, 'turmeric', '["Curry Powder", "garam masala"]'),
-- Garlic Alternatives
(1619, 'garlic paste', '["Garlic", "dried garlic"]'),
(1620, 'dried garlic', '["Garlic", "garlic paste"]'),
-- Mixed Vegetables Alternatives
(1621, 'frozen vegetables', '["Mixed Vegetables", "seasonal vegetables"]'),
(1622, 'seasonal vegetables', '["Mixed Vegetables", "frozen vegetables"]'),
-- Olive Oil Alternatives
(1623, 'vegetable oil', '["Olive Oil", "canola oil"]'),
(1624, 'canola oil', '["Olive Oil", "vegetable oil"]'),
-- Bread Alternatives
(1625, 'whole wheat bread', '["Bread", "sourdough"]'),
(1626, 'sourdough', '["Bread", "whole wheat bread"]'),
-- Egg Alternatives
(1627, 'egg whites', '["Egg", "vegan egg substitute"]'),
(1628, 'vegan egg substitute', '["Egg", "egg whites"]'),
-- Banana Alternatives
(1629, 'frozen banana', '["Banana", "plantain"]'),
(1630, 'plantain', '["Banana", "frozen banana"]'),
-- Greek Yogurt Alternatives
(1631, 'regular yogurt', '["Greek Yogurt", "plant-based yogurt"]'),
(1632, 'plant-based yogurt', '["Greek Yogurt", "regular yogurt"]'),
-- Honey Alternatives
(1633, 'agave syrup', '["Honey", "maple syrup"]'),
(1634, 'maple syrup', '["Honey", "agave syrup"]'),
-- Salmon Alternatives
(1635, 'trout', '["Salmon", "tilapia"]'),
(1636, 'tilapia', '["Salmon", "trout"]'),
-- Lemon Alternatives
(1637, 'lime', '["Lemon", "preserved lemon"]'),
(1638, 'preserved lemon', '["Lemon", "lime"]'),
-- Dill Alternatives
(1639, 'dried dill', '["Dill", "parsley"]'),
(1640, 'parsley', '["Dill", "dried dill"]'),
-- Beef Alternatives
(1641, 'ground beef', '["Beef", "steak", "sirloin"]'),
(1642, 'steak', '["Beef", "ground beef", "sirloin"]'),
(1643, 'sirloin', '["Beef", "ground beef", "steak"]'),
-- Tofu Alternatives
(1644, 'tempeh', '["Tofu", "seitan", "plant-based protein"]'),
(1645, 'seitan', '["Tofu", "tempeh", "plant-based protein"]'),
(1646, 'plant-based protein', '["Tofu", "tempeh", "seitan"]'),
-- Shrimp Alternatives
(1647, 'prawns', '["Shrimp", "crab", "imitation crab"]'),
(1648, 'crab', '["Shrimp", "prawns", "imitation crab"]'),
(1649, 'imitation crab', '["Shrimp", "prawns", "crab"]'),
-- Lamb Alternatives
(1650, 'goat meat', '["Lamb", "mutton"]'),
(1651, 'mutton', '["Lamb", "goat meat"]'),
-- Spinach Alternatives
(1652, 'kale', '["Spinach", "swiss chard", "collard greens"]'),
(1653, 'swiss chard', '["Spinach", "kale", "collard greens"]'),
(1654, 'collard greens', '["Spinach", "kale", "swiss chard"]'),
-- Bell Pepper Alternatives
(1655, 'capsicum', '["Bell Pepper", "paprika", "chili pepper"]'),
(1656, 'paprika', '["Bell Pepper", "capsicum", "chili pepper"]'),
(1657, 'chili pepper', '["Bell Pepper", "capsicum", "paprika"]'),
-- Eggplant Alternatives
(1658, 'aubergine', '["Eggplant", "brinjal"]'),
(1659, 'brinjal', '["Eggplant", "aubergine"]'),
-- Zucchini Alternatives
(1660, 'courgette', '["Zucchini", "summer squash"]'),
(1661, 'summer squash', '["Zucchini", "courgette"]'),
-- Carrot Alternatives
(1662, 'baby carrot', '["Carrot", "rainbow carrot"]'),
(1663, 'rainbow carrot', '["Carrot", "baby carrot"]'),
-- Rice Alternatives
(1664, 'basmati rice', '["Rice", "brown rice", "jasmine rice"]'),
(1665, 'brown rice', '["Rice", "basmati rice", "jasmine rice"]'),
(1666, 'jasmine rice', '["Rice", "basmati rice", "brown rice"]'),
-- Pasta Alternatives
(1667, 'spaghetti', '["Pasta", "penne", "gluten-free pasta"]'),
(1668, 'penne', '["Pasta", "spaghetti", "gluten-free pasta"]'),
(1669, 'gluten-free pasta', '["Pasta", "spaghetti", "penne"]'),
-- Potato Alternatives
(1670, 'sweet potato', '["Potato", "yam", "fingerling potato"]'),
(1671, 'yam', '["Potato", "sweet potato", "fingerling potato"]'),
(1672, 'fingerling potato', '["Potato", "sweet potato", "yam"]'),
-- Cheese Alternatives
(1673, 'cheddar', '["Cheese", "mozzarella", "vegan cheese"]'),
(1674, 'mozzarella', '["Cheese", "cheddar", "vegan cheese"]'),
(1675, 'vegan cheese', '["Cheese", "cheddar", "mozzarella"]'),
-- Milk Alternatives
(1676, 'almond milk', '["Milk", "soy milk", "oat milk"]'),
(1677, 'soy milk', '["Milk", "almond milk", "oat milk"]'),
(1678, 'oat milk', '["Milk", "almond milk", "soy milk"]'),
-- Cream Alternatives
(1679, 'heavy cream', '["Cream", "light cream", "coconut cream"]'),
(1680, 'light cream', '["Cream", "heavy cream", "coconut cream"]'),
(1681, 'coconut cream', '["Cream", "heavy cream", "light cream"]'),
-- Basil Alternatives
(1682, 'fresh basil', '["Basil", "dried basil", "thai basil"]'),
(1683, 'dried basil', '["Basil", "fresh basil", "thai basil"]'),
(1684, 'thai basil', '["Basil", "fresh basil", "dried basil"]'),
-- Cilantro Alternatives
(1685, 'coriander leaves', '["Cilantro", "chinese parsley"]'),
(1686, 'chinese parsley', '["Cilantro", "coriander leaves"]'),
-- Mint Alternatives
(1687, 'peppermint', '["Mint", "spearmint"]'),
(1688, 'spearmint', '["Mint", "peppermint"]'),
-- Paprika Alternatives
(1689, 'smoked paprika', '["Paprika", "hot paprika"]'),
(1690, 'hot paprika', '["Paprika", "smoked paprika"]'),
-- Cumin Alternatives
(1691, 'ground cumin', '["Cumin", "whole cumin seeds"]'),
(1692, 'whole cumin seeds', '["Cumin", "ground cumin"]'),
-- Apple Alternatives
(1693, 'green apple', '["Apple", "red apple", "cooking apple"]'),
(1694, 'red apple', '["Apple", "green apple", "cooking apple"]'),
(1695, 'cooking apple', '["Apple", "green apple", "red apple"]'),
-- Orange Alternatives
(1696, 'mandarin', '["Orange", "clementine", "blood orange"]'),
(1697, 'clementine', '["Orange", "mandarin", "blood orange"]'),
(1698, 'blood orange', '["Orange", "mandarin", "clementine"]'),
-- Avocado Alternatives
(1699, 'hass avocado', '["Avocado", "fuerte avocado"]'),
(1700, 'fuerte avocado', '["Avocado", "hass avocado"]'),
-- Soy Sauce Alternatives
(1701, 'tamari', '["Soy Sauce", "light soy sauce", "dark soy sauce"]'),
(1702, 'light soy sauce', '["Soy Sauce", "tamari", "dark soy sauce"]'),
(1703, 'dark soy sauce', '["Soy Sauce", "tamari", "light soy sauce"]'),
-- Vinegar Alternatives
(1704, 'apple cider vinegar', '["Vinegar", "rice vinegar", "balsamic vinegar"]'),
(1705, 'rice vinegar', '["Vinegar", "apple cider vinegar", "balsamic vinegar"]'),
(1706, 'balsamic vinegar', '["Vinegar", "apple cider vinegar", "rice vinegar"]'),
-- Mustard Alternatives
(1707, 'dijon mustard', '["Mustard", "whole grain mustard", "yellow mustard"]'),
(1708, 'whole grain mustard', '["Mustard", "dijon mustard", "yellow mustard"]'),
(1709, 'yellow mustard', '["Mustard", "dijon mustard", "whole grain mustard"]'),
-- Sugar Alternatives
(1710, 'brown sugar', '["Sugar", "raw sugar", "coconut sugar"]'),
(1711, 'raw sugar', '["Sugar", "brown sugar", "coconut sugar"]'),
(1712, 'coconut sugar', '["Sugar", "brown sugar", "raw sugar"]'),
-- Flour Alternatives
(1713, 'wheat flour', '["Flour", "almond flour", "gluten-free flour"]'),
(1714, 'almond flour', '["Flour", "wheat flour", "gluten-free flour"]'),
(1715, 'gluten-free flour', '["Flour", "wheat flour", "almond flour"]'),
-- Vanilla Extract Alternatives
(1716, 'vanilla bean', '["Vanilla Extract", "vanilla paste"]'),
(1717, 'vanilla paste', '["Vanilla Extract", "vanilla bean"]'),
-- Almonds Alternatives
(1718, 'sliced almonds', '["Almonds", "almond flour", "roasted almonds"]'),
(1719, 'almond flour', '["Almonds", "sliced almonds", "roasted almonds"]'),
(1720, 'roasted almonds', '["Almonds", "sliced almonds", "almond flour"]'),
-- Chia Seeds Alternatives
(1721, 'ground chia', '["Chia Seeds", "whole chia seeds"]'),
(1722, 'whole chia seeds', '["Chia Seeds", "ground chia"]'),
-- Peanut Alternatives
(1723, 'roasted peanuts', '["Peanut", "peanut butter"]'),
(1724, 'peanut butter', '["Peanut", "roasted peanuts"]'),
-- Quinoa Alternatives
(1725, 'red quinoa', '["Quinoa", "white quinoa", "black quinoa"]'),
(1726, 'white quinoa', '["Quinoa", "red quinoa", "black quinoa"]'),
(1727, 'black quinoa', '["Quinoa", "red quinoa", "white quinoa"]'),
-- Lentils Alternatives
(1728, 'red lentils', '["Lentils", "green lentils", "brown lentils"]'),
(1729, 'green lentils', '["Lentils", "red lentils", "brown lentils"]'),
(1730, 'brown lentils', '["Lentils", "red lentils", "green lentils"]'),
-- Chickpeas Alternatives
(1731, 'canned chickpeas', '["Chickpeas", "dried chickpeas", "roasted chickpeas"]'),
(1732, 'dried chickpeas', '["Chickpeas", "canned chickpeas", "roasted chickpeas"]'),
(1733, 'roasted chickpeas', '["Chickpeas", "canned chickpeas", "dried chickpeas"]'),
-- Nutritional Yeast Alternatives
(1734, 'fortified nutritional yeast', '["Nutritional Yeast", "non-fortified nutritional yeast"]'),
(1735, 'non-fortified nutritional yeast', '["Nutritional Yeast", "fortified nutritional yeast"]'),
-- Tahini Alternatives
(1736, 'light tahini', '["Tahini", "dark tahini", "whole sesame tahini"]'),
(1737, 'dark tahini', '["Tahini", "light tahini", "whole sesame tahini"]'),
(1738, 'whole sesame tahini', '["Tahini", "dark tahini", "light tahini"]');

INSERT INTO UserInventory (user_id, fridge_id, ingredients)
VALUES 
(1, 1, '{101: "300g", 102: "250g", 103: "100g", 302: "40ml", 401: "2", 402: "2", 205: "2", 704: "600g", 803: "250g", 804: "250g", 805: "150g", 1102: "20g", 1104: "7g", 501: "180g", 502: "130ml", 503: "22ml", 601: "520g", 602: "21ml", 603: "7g"}'),
-- Complete: 1, 4, 8
-- Partial: 5, 6

-- From here u need to change
-- Complete, Complete with alternative, partial, partial with missing (Only rejected if the no. of ingredients present do not make up atleast 70%)
-- if it goes below partial check for alternative -> if it meets criteria then it might have with alternative tag 
(2, 1, '{}'), 
-- Complete: 12, 13
-- Partial: 17, 22

(3, 2, '{702: "350g", 801: "200g", 802: "200g", 203: "300ml", 1104: "10g", 1105: "5g", 302: "25ml"}'), 
-- Complete: 23, 24, 25
-- Partial: 11, 9

(4, 2, '{401: "2", 402: "2", 302: "10ml", 205: "2", 1001: "100g", 903: "200g"}'), 
-- Complete: 26
-- Partial: 16, 19

(5, 3, '{501: "200g", 502: "150ml", 503: "30ml", 302: "10ml", 1201: "200g", 1401: "30g", 1403: "10ml"}'), 
-- Complete: 29, 30
-- Partial: 16, 18

(6, 3, '{601: "600g", 602: "30ml", 603: "10g", 302: "20ml", 1102: "10g", 703: "250g", 901: "200g"}'), 
-- Complete: 13
-- Partial: 21, 25

(7, 4, '{702: "300g", 801: "200g", 802: "150g", 1101: "10g", 1301: "30ml", 1203: "200g", 902: "150g"}'), 
-- Complete: 17, 20
-- Partial: 25

(8, 4, '{704: "500g", 803: "250g", 804: "200g", 805: "150g", 1102: "15g", 1104: "5g", 1001: "150g", 302: "30ml"}');
-- Complete: 6, 7, 18
-- Partial: 26, 30
