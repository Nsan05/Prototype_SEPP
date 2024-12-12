import psycopg2
from typing import Dict,Any,List,Optional
import logging
import ast
import json

def parse_quantity(recipe_quantity: str, inventory_quantity: str) -> int:
    try:
        recipe_value = float(recipe_quantity.replace('g', '').replace('ml', ''))
        inventory_value = float(inventory_quantity.replace('g', '').replace('ml', '').replace('Unit',''))
        
        if recipe_value == 0:
            return 0
        
        percentage = min(int((inventory_value / recipe_value) * 100), 100)
        return max(percentage, 0)
    except Exception as e:
        print(e)
        return 0

class RecipeSuggestion:
    def __init__(self, db_params: Dict[str, str], user_id: int):
        self.user_id = user_id
        self.db_connection = None
        self.ingredient_names = {}
        self.alternatives = {}

        try:
            self.db_connection = psycopg2.connect(**db_params)
            self.db_connection.autocommit = True
            self.alternatives = self.get_alternatives()
            self.ingredient_names = self.get_ingredient_names()
        except (Exception, psycopg2.Error) as error:
            print(error)
            raise 

    def __del__(self):
        if self.db_connection:
            try:
                self.db_connection.close()
            except:
                pass

    def get_ingredient_names(self) -> Dict[int, str]:
        try:
            with self.db_connection.cursor() as cursor:
                query = "SELECT ingredient_id, ingredient_name FROM ingredient"
                cursor.execute(query)
                return dict(cursor.fetchall())
        except psycopg2.Error as e:
            print(e)
            return {}
        
    def get_recipes(self) -> Dict[int, Dict[str, Any]]:
        try:
            with self.db_connection.cursor() as cursor:
                query = """
                    SELECT recipe_id, recipe_name, ingredient_list, dietary_requirement, preparation_time, instructions
                    FROM recipe
                """
                cursor.execute(query)
                recipes_data = cursor.fetchall()

            recipes = {}

            for recipe_id, recipe_name, ingredient_list_str, dietary_requirement, preparation_time, instructions in recipes_data:
                
                try:
                    ingredient_list = ast.literal_eval(ingredient_list_str)
                except (ValueError, SyntaxError) as e:
                    print(e)
                    continue

                core = {}
                secondary = {}
                optional = {}

                for ingredient_id, ingredient_data in ingredient_list.items():
                    try:
                        ingredient_id = int(ingredient_id)
                        ingredient_quantity, importance_level = ingredient_data[:2]

                        if importance_level == "core":
                            core[ingredient_id] = ingredient_quantity
                        elif importance_level == "secondary":
                            secondary[ingredient_id] = ingredient_quantity
                        elif importance_level == "optional":
                            optional[ingredient_id] = ingredient_quantity
                        else:
                            print("Unknown importance level")
                    except Exception as e:
                        print(e)

                recipes[recipe_id] = {
                    'recipe_name': recipe_name,
                    'core': core,
                    'secondary': secondary,
                    'optional': optional,
                    'dietary_requirement': dietary_requirement,
                    'preparation_time': preparation_time,
                    'instructions': instructions
                }

            return recipes
        except psycopg2.Error as e:
            print(e)
            return {}    

    def get_inventory(self) -> Dict[int, str]:
            
            try:
                with self.db_connection.cursor() as cursor:
                    query = """
                        SELECT ingredients
                        FROM userinventory
                        WHERE user_id = %s 
                    """
                    cursor.execute(query, (self.user_id,))
                    result = cursor.fetchone()

                if result:
                    try:
                        raw_ingredients = ast.literal_eval(result[0])
                        inventory = {int(ingredient_id): str(quantity) for ingredient_id, quantity in raw_ingredients.items()}
                        return inventory
                    except (ValueError, SyntaxError) as e:
                        print(e)
                        return {}
                else:
                    print("No inventory found for user.")
                    return {}
            except psycopg2.Error as e:
                print(e)
                return {}
            
    def get_alternatives(self) -> Dict[int, List[str]]:
        
        try:
            with self.db_connection.cursor() as cursor:
                query = "SELECT ingredient_id, ingredient_name, alternatives_list FROM ingredient"
                cursor.execute(query)
                alternatives_data = cursor.fetchall()

            alternatives = {}
            for ingredient_id, ingredient_name, alternatives_list in alternatives_data:
                try:
                    parsed_alternatives = json.loads(alternatives_list) if alternatives_list else []
                    alternatives[ingredient_id] = parsed_alternatives
                except (json.JSONDecodeError, AttributeError) as e:
                    print(e)
            
            return alternatives
        except psycopg2.Error as e:
            print(e)
            return {}
        
    
         
    def calculate_score(self, percentages: Dict[int, int], core: Dict[int, str], 
                        secondary: Dict[int, str], optional: Dict[int, str]) -> float:
        
        core_score = sum(5 * (100 - min(percentages.get(ing, 0), 100)) for ing in core)
        secondary_score = sum(3 * (100 - min(percentages.get(ing, 0), 100)) for ing in secondary)
        optional_score = sum(1 * (100 - min(percentages.get(ing, 0), 100)) for ing in optional)
        
        return core_score + secondary_score + optional_score
    
    def suggest_recipes(self, dietary_requirement: Optional[str] = None) -> List[Dict[str, Any]]:
        recipes = self.get_recipes()
        fridge = self.get_inventory()

        results = []

        for recipe_id, recipe_data in recipes.items():

            recipe_diet = recipe_data['dietary_requirement'].lower()
            if dietary_requirement and recipe_diet != dietary_requirement:
                continue

            core = recipe_data["core"]
            secondary = recipe_data["secondary"]
            optional = recipe_data["optional"]

            percentages = {}
            all_ingredients = {**core, **secondary, **optional}


            for ingredient_id, required_qty in all_ingredients.items():
                available_qty = fridge.get(ingredient_id, '0')
                percentages[ingredient_id] = parse_quantity(required_qty, available_qty)
        
            for ingredient_id in core.keys():
                if percentages.get(ingredient_id, 0) < 85:  
                    for alt in self.alternatives.get(ingredient_id, []):
                        alt_id = next((id for id, name in self.ingredient_names.items() if name == alt), None)
                        if alt_id and alt_id in fridge:
                            alt_available_qty = fridge[alt_id]
                            percentages[ingredient_id] = max(percentages[ingredient_id], parse_quantity(required_qty, alt_available_qty))
            # checking secondary
            for ingredient_id in secondary.keys():
                if percentages[ingredient_id] < 65:  
                    for alt in self.alternatives.get(ingredient_id, []):
                        alt_id = next((id for id, name in self.ingredient_names.items() if name == alt), None)
                        if alt_id and alt_id in fridge:
                            alt_available_qty = fridge[alt_id]
                            alt_percentage = parse_quantity(secondary[ingredient_id], alt_available_qty)
                            percentages[ingredient_id] = max(percentages[ingredient_id], alt_percentage)
        
            core_complete = all(percentages.get(ing, 0) >= 95 for ing in core)
            secondary_complete = all(percentages.get(ing, 0) >= 95 for ing in secondary)
            optional_complete = all(percentages.get(ing, 0) >= 95 for ing in optional)
            
            if core_complete and secondary_complete and optional_complete:
                score1 = self.calculate_score(percentages, core, secondary, optional)
                results.append({
                    "recipe_name": recipe_data['recipe_name'], 
                    "case": "Complete", 
                    "score1": score1, 
                    "score2": 0, 
                    "total": score1,
                    "dietary_requirement": recipe_data['dietary_requirement'],
                    "preparation_time": recipe_data['preparation_time'],
                    "instructions": recipe_data['instructions']
                })
                continue  

            
            core_available = {ing for ing, perc in percentages.items() if 85 <= min(perc, 100) <= 100}
            secondary_available = {ing for ing, perc in percentages.items() if 65 <= min(perc, 100) <= 100}
            optional_available = {ing for ing, perc in percentages.items() if 45 <= min(perc, 100) <= 100}
            
            missing = set(core) - core_available
            missing.update(set(secondary) - secondary_available)
            missing.update(set(optional) - optional_available)

            total_ingredients = len(core) + len(secondary) + len(optional)
            missing_percentage = (len(missing) / total_ingredients) * 100 if total_ingredients > 0 else 100

            if missing_percentage > 30:
                results.append({
                    "recipe_name": recipe_data['recipe_name'],
                    "case": "Rejected",
                    "reason": "More than 30% missing ingredients",
                    "total": 0,
                    "dietary_requirement": recipe_data['dietary_requirement'],
                    "preparation_time": recipe_data['preparation_time'],
                    "instructions": recipe_data['instructions']
                })
                continue

            score1 = self.calculate_score(
                {ing : perc for ing, perc in percentages.items() if ing not in missing}, 
                {ing: qty for ing, qty in core.items() if ing not in missing}, 
                {ing: qty for ing, qty in secondary.items() if ing not in missing}, 
                {ing: qty for ing, qty in optional.items() if ing not in missing}
            )

            score2 = sum(
                (100 - percentages.get(ing, 0)) * (30 if ing in core else 20 if ing in secondary else 5)
                for ing in missing
            )

            results.append({
                "recipe_name": recipe_data['recipe_name'], 
                "case": "Partial", 
                "score1": score1, 
                "score2": score2, 
                "total": score1 + score2,
                "dietary_requirement": recipe_data['dietary_requirement'],
                "preparation_time": recipe_data['preparation_time'],
                "instructions": recipe_data['instructions']
            })

        results.sort(key=lambda x: x['total'], reverse=False)
        return results
def main():
    db_params = {
        "dbname": "sepp1",
        "user": "kavya",
        "password": "password",
        "host": "localhost",
        "port": "5434"
    }

    try:
        
        user_id = 1
        choice = input("Enter your dietary choice (veg, non-veg): ").strip().lower()
        if choice not in ['veg', 'non-veg']:
            print("Invalid choice. Please enter 'veg', 'non-veg'.")
            return
        
        recipe_suggester = RecipeSuggestion(db_params, user_id)
        results = recipe_suggester.suggest_recipes(choice)
        
        complete_recipes = [r for r in results if r['case'] == 'Complete' and r['dietary_requirement'] == choice]
        partial_recipes = [r for r in results if r['case'] == 'Partial' and r['dietary_requirement'] == choice]


        if complete_recipes: 
            print("\nCOMPLETE RECIPES:")
            print("-" * 50)
            for recipe in complete_recipes:
                print(f"Recipe: {recipe['recipe_name']}")
                print(f"Score: {recipe['total']:.2f}")
                print(f"Dietary Requirement: {recipe['dietary_requirement']}")
                print(f"Preparation Time: {recipe['preparation_time']} mins")
                print(f"Instructions: {recipe['instructions']}")
                print("-" * 50)
        else:
            print("\nNo complete recipes match your criteria.")

        if partial_recipes:
            print("\nPARTIAL RECIPES:")
            print("-" * 50)
            for recipe in partial_recipes:
                print(f"Recipe: {recipe['recipe_name']}")
                print(f"Total Score: {recipe['total']:.2f}")
                print(f"Score1: {recipe['score1']:.2f}")
                print(f"Score2: {recipe['score2']:.2f}")
                print(f"Dietary Requirement: {recipe['dietary_requirement']}")
                print(f"Preparation Time: {recipe['preparation_time']} mins")
                print(f"Instructions: {recipe['instructions']}")
                print("-" * 50)
        else:
            print("\nNo partial recipes match your criteria.")

        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()   