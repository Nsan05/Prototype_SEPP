import psycopg2
from typing import Dict,Any,List,Optional
import logging
import ast

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

def parse_quantity(recipe_quantity: str, inventory_quantity: str) -> int:
    try:
        recipe_value = float(recipe_quantity.replace('g', '').replace('ml', ''))
        inventory_value = float(inventory_quantity.replace('g', '').replace('ml', ''))
        
        if recipe_value == 0:
            return 0
        
        percentage = min(int((inventory_value / recipe_value) * 100), 100)
        return max(percentage, 0)
    
    except Exception as e:
        logger.error(f"Error parsing quantities: {e}")
        return 0

class RecipeSuggestion:
    def __init__(self, db_params: Dict[str, str], user_id: int):
        
        try:
            self.db_connection = psycopg2.connect(**db_params)
            self.db_connection.autocommit = True
            self.user_id = user_id
            self.alternatives = self.get_alternatives()
            self.ingredient_names = self.get_ingredient_names()
        except (Exception, psycopg2.Error) as error:
            logging.error(f"Error connecting to database: {error}")
            raise 

    def _del_(self):
        if hasattr(self, 'db_connection'):
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
            logging.error(f"Database error in get_ingredient_names: {e}")
            return {}
        
    def get_recipes(self) -> Dict[int, Dict[str, Any]]:
        try:
            with self.db_connection.cursor() as cursor:
                query = """
                    SELECT recipe_id, recipe_name, ingredient_list
                    FROM recipe
                """
                cursor.execute(query)
                recipes_data = cursor.fetchall()

            recipes = {}

            for recipe_id, recipe_name, ingredient_list_str in recipes_data:
                logger.info(f"Processing recipe {recipe_id}: {recipe_name}")

                try:
                    ingredient_list = ast.literal_eval(ingredient_list_str)
                except (ValueError, SyntaxError) as e:
                    logger.error(f"Error parsing ingredient list for recipe {recipe_id}: {e}")
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
                            logger.warning(f"Unknown importance level {importance_level} for ingredient {ingredient_id}")

                    except Exception as e:
                        logger.error(f"Unexpected error processing ingredient {ingredient_id} in recipe {recipe_id}: {e}")

                recipes[recipe_id] = {
                    'recipe_name': recipe_name,
                    'core': core,
                    'secondary': secondary,
                    'optional': optional
                }

                logger.info(f"Recipe {recipe_id} processed successfully")

            return recipes
        except psycopg2.Error as e:
            logger.error(f"Database error in get_recipes: {e}")
            return {}    

    def get_inventory(self) -> Dict[int, str]:
            
            try:
                with self.db_connection.cursor() as cursor:
                    query = """
                        SELECT ingredients
                        FROM userinventory
                        WHERE user_id = %s AND fridge_id = 2
                    """
                    cursor.execute(query, (self.user_id,))
                    result = cursor.fetchone()

                if result:
                    try:
                        raw_ingredients = ast.literal_eval(result[0])
                        inventory = {int(ingredient_id): str(quantity) for ingredient_id, quantity in raw_ingredients.items()}
                        return inventory
                    except (ValueError, SyntaxError):
                        logger.error("Error parsing inventory ingredients")
                        return {}
                else:
                    logger.warning("No inventory found for user.")
                    return {}
            except psycopg2.Error as e:
                logger.error(f"Database error in get_inventory: {e}")
                return {}
            
    def get_alternatives(self) -> Dict[int, List[str]]:
        
        try:
            with self.db_connection.cursor() as cursor:
                query = "SELECT ingredient_id, alternatives_list FROM ingredient"
                cursor.execute(query)
                alternatives_data = cursor.fetchall()

            alternatives = {}
            for ingredient_id, alternatives_list in alternatives_data:
                try:
                    alternatives[ingredient_id] = [alt.strip() for alt in alternatives_list.split(",") if alt.strip()]
                except AttributeError:
                    logger.error(f"Error processing alternatives for ingredient {ingredient_id}")

            return alternatives
        except psycopg2.Error as e:
            logger.error(f"Database error in get_alternatives: {e}")
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

        logger.debug(f"Recipes: {recipes}")
        logger.debug(f"Fridge Inventory: {fridge}")

        results = []

        for recipe_id, recipe_data in recipes.items():
            core = recipe_data["core"]
            secondary = recipe_data["secondary"]
            optional = recipe_data["optional"]

            percentages = {}
            all_ingredients = {**core, **secondary, **optional}


            for ingredient_id, required_qty in all_ingredients.items():
                available_qty = fridge.get(ingredient_id, '0')
                percentages[ingredient_id] = parse_quantity(required_qty, available_qty)
                logger.debug(f"Ingredient ID: {ingredient_id}, Required: {required_qty}, Available: {available_qty}, Percentage: {percentages[ingredient_id]}")
        
            for ingredient_id in core.keys():
                if percentages.get(ingredient_id, 0) < 95:  
                    for alt in self.alternatives.get(ingredient_id, []):
                        alt_id = next((id for id, name in self.ingredient_names.items() if name == alt), None)
                        if alt_id and alt_id in fridge:
                            alt_available_qty = fridge[alt_id]
                            percentages[ingredient_id] = max(percentages[ingredient_id], parse_quantity(required_qty, alt_available_qty))

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
            print("c:",core_complete,"\ns:",secondary_complete,"\no:",optional_complete)
            if core_complete and secondary_complete and optional_complete:
                score1 = self.calculate_score(percentages, core, secondary, optional)
                results.append({
                    "recipe": recipe_data['recipe_name'], 
                    "case": "Complete", 
                    "score1": score1, 
                    "score2": 0, 
                    "total": score1
                })
                print(f"Recipe: {recipe_data['recipe_name']} - Complete, Score: {score1:.2f}")
                continue  

            
            core_available = {ing for ing, perc in percentages.items() if 85 <= min(perc, 100) <= 100}
            secondary_available = {ing for ing, perc in percentages.items() if 65 <= min(perc, 100) <= 100}
            optional_available = {ing for ing, perc in percentages.items() if 45 <= min(perc, 100) <= 100}
            
            missing = set(core) - core_available
            missing.update(set(secondary) - secondary_available)
            missing.update(set(optional) - optional_available)

            total_ingredients = len(core) + len(secondary) + len(optional)
            missing_percentage = (len(missing) / total_ingredients) * 100 if total_ingredients > 0 else 100

            if missing_percentage > 33:
                results.append({
                    "recipe": recipe_data['recipe_name'],
                    "case": "Rejected",
                    "reason": "More than 30% missing ingredients",
                    "total": 0
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
                "recipe": recipe_data['recipe_name'], 
                "case": "Partial", 
                "score1": score1, 
                "score2": score2, 
                "total": score1 + score2
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
        logging.getLogger().setLevel(logging.DEBUG)
        user_id = 3
        recipe_suggester = RecipeSuggestion(db_params, user_id)
        results = recipe_suggester.suggest_recipes()

        complete_recipes = [r for r in results if r['case'] == 'Complete']
        partial_recipes = [r for r in results if r['case'] == 'Partial']
        rejected_recipes = [r for r in results if r['case'] == 'Rejected']

        print("COMPLETE RECIPES:")
        print("-" * 50)
        for recipe in complete_recipes:
            print(f"Recipe: {recipe['recipe']}")
            print(f"Total Score: {recipe['total']:.2f}")
            print("-" * 50)

        print("\nPARTIAL RECIPES:")
        print("-" * 50)
        for recipe in partial_recipes:
            print(f"Recipe: {recipe['recipe']}")
            print(f"Total Score: {recipe['total']:.2f}")
            print(f"Score 1: {recipe['score1']:.2f}")
            print(f"Score 2: {recipe['score2']:.2f}")
            print("-" * 50)

        print("\nREJECTED RECIPES:")
        print("-" * 50)
        for recipe in rejected_recipes:
            print(f"Recipe: {recipe['recipe']}")
            print(f"Reason: {recipe.get('reason', 'Unknown')}")
            print("-" * 50)

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()   