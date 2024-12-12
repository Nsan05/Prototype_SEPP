import pytest
from main import RecipeSuggestion

# # Credentials for dockerised setup
db_params = {
    "dbname": "recipe_db",
    "user": "SEPP",
    "password": "prototype",
    "host": "localhost",
    "port": "5432"
}

test_cases = [
    {
        'user_id': 1,
        'expected_recipes': [
            {"recipe": "Mediterranean Tomato Cucumber Salad", "case": "Complete"},
            {"recipe": "Classic Egg Toast", "case": "Complete"},
            {"recipe": "Mediterranean Lamb with Roasted Vegetables", "case": "Complete"},
            {"recipe": "Avocado and Shrimp Rice Bowl", "case": "Complete"},
            {"recipe": "Mediterranean Trout with Preserved Lemon", "case": "Partial"},
            {"recipe": "Loaded Vegetable Potato Skins", "case": "Partial"},
            {"recipe": "Whole Wheat Egg White Toast", "case": "Partial"},
            {"recipe": "Trout with Capsicum and Parsley", "case": "Partial"},
            {"recipe": "Plantain Green Smoothie", "case": "Partial"},
            {"recipe": "Vegetarian Potato and Cheese Bake", "case": "Partial"},
            {"recipe": "Banana Honey Smoothie", "case": "Partial"}, 
            {"recipe": "Lemon Dill Salmon", "case": "Partial"},
            {"recipe": "Mediterranean Lamb Salad", "case": "Partial"},
            {"recipe": "Mediterranean Feta and Vegetable Feast", "case": "Partial"},
            {"recipe": "Vegan Lentil and Vegetable Stew", "case": "Partial"},
            {"recipe": "Roasted Vegetable and Tempeh Medley", "case": "Partial"},
            {"recipe": "Apple Cinnamon Oatmeal", "case": "Partial"}
        ]
    },
    {
        'user_id': 2,
        'expected_recipes': [
            {"recipe": "Beef and Vegetable Pasta", "case": "Complete"},
            {"recipe": "Zucchini Noodle Shrimp Alfredo", "case": "Complete"},
            {"recipe": "Mediterranean Lamb Salad", "case": "Complete"},
            {"recipe": "Tropical Shrimp Coconut Rice", "case": "Partial"},
            {"recipe": "Apple Almond Breakfast Parfait", "case": "Partial"},
            {"recipe": "Avocado and Shrimp Rice Bowl", "case": "Partial"},
            {"recipe": "Coconut Seitan Vegetable Curry", "case": "Partial"}
        ]
    },
    {
        'user_id': 3,
        'expected_recipes': [
            {"recipe": "Coconut Seitan Vegetable Curry", "case": "Complete"},
            {"recipe": "Mediterranean Halloumi and Roasted Vegetable Salad", "case": "Complete"},
            {"recipe": "Spicy Tempeh and Bok Choy Stir Fry", "case": "Complete"},
            {"recipe": "Spicy Tempeh and Butternut Squash Curry", "case": "Partial"},
            {"recipe": "Protein-Rich Seitan and Vegetable Stir Fry", "case": "Complete"},
            {"recipe": "Plantain Green Smoothie", "case": "Partial"},
            {"recipe": "Mediterranean Trout with Preserved Lemon", "case": "Partial"},
            {"recipe": "Zucchini and Tofu Mediterranean Stir Fry", "case": "Partial"},
            {"recipe": "Banana Honey Smoothie", "case": "Partial"},
            {"recipe": "Lemon Dill Salmon", "case": "Partial"},
            {"recipe": "Spicy Tempeh Stir Fry with Thai Basil", "case": "Partial"},
            {"recipe": "Apple Cinnamon Oatmeal", "case": "Partial"}
        ]
    },
    {
        'user_id': 4,
        'expected_recipes': [
            {"recipe": "Protein-Packed Black Bean and Avocado Bowl", "case": "Complete"},
            {"recipe": "Rustic Chicken Thigh Curry", "case": "Complete"},
            {"recipe": "Trout with Capsicum and Parsley", "case": "Partial"},
            {"recipe": "Loaded Vegetable Potato Skins", "case": "Partial"},
            {"recipe": "Apple Almond Breakfast Parfait", "case": "Partial"},
            {"recipe": "Coconut Seitan Vegetable Curry", "case": "Partial"},
            {"recipe": "Spicy Tempeh and Butternut Squash Curry", "case": "Partial"},
            {"recipe": "Coconut Chicken Curry", "case": "Partial"},
            {"recipe": "Mediterranean Trout with Preserved Lemon", "case": "Partial"},
            {"recipe": "Apple Cinnamon Oatmeal", "case": "Partial"},
            {"recipe": "Vegetable Medley Roast", "case": "Partial"},
            {"recipe": "Lemon Dill Salmon", "case": "Partial"}
        ]
    },
    {
        'user_id': 5,
        'expected_recipes': [
            {"recipe": "Protein-Packed Black Bean and Avocado Bowl", "case": "Complete"},
            {"recipe": "Zucchini and Tofu Mediterranean Stir Fry", "case": "Partial"},
            {"recipe": "Plantain and Almond Milk Smoothie Bowl", "case": "Complete"},
            {"recipe": "Loaded Vegetable Potato Skins", "case": "Partial"},
            {"recipe": "Apple Almond Breakfast Parfait", "case": "Partial"},
            {"recipe": "Coconut Seitan Vegetable Curry", "case": "Partial"},
            {"recipe": "Whole Wheat Egg White Toast", "case": "Partial"},
            {"recipe": "Spicy Tempeh and Bok Choy Stir Fry", "case": "Partial"},
            {"recipe": "Spicy Tempeh Stir Fry with Thai Basil", "case": "Partial"},
            {"recipe": "Spicy Tempeh and Butternut Squash Curry", "case": "Partial"},
            {"recipe": "Apple Cinnamon Oatmeal", "case": "Partial"},
            {"recipe": "Classic Egg Toast", "case": "Partial"}
        ]
    }
]

@pytest.mark.parametrize("test_case", test_cases)
def test_recipe_cases_by_user(test_case):
    user_id = test_case['user_id']
    recipe_suggester = RecipeSuggestion(db_params, user_id)
    results = recipe_suggester.suggest_recipes()

    # Extract only recipe and case
    simplified_results = [
        {"recipe": result["recipe_name"], "case": result["case"]} 
        for result in results
    ]

    # Check if all expected recipes are in the results
    for expected_recipe in test_case['expected_recipes']:
        assert expected_recipe in simplified_results, \
            f"Expected recipe {expected_recipe} not found for user {user_id}"
        
# if __name__ == "__main__":
#     pytest.main(["-v", __file__])

