class Limit:
    """Настройка констант моделей"""

    # Модель Tag
    CHAR_LIMIT_TAG_NAME = 32
    CHAR_LIMIT_TAG_SLUG_NAME = 32
    CHAR_LIMIT_TAG_HEX_COLOR = 7

    # Модель Ingredient
    CHAR_LIMIT_INGREDIENT_NAME = 128
    CHAR_LIMIT_INGREDIENT_MEASUREMENT_UNIT = 32

    # Модель Recipe
    CHAR_LIMIT_RECIPE_TITLE = 255
    MIN_VALUE_RECIPE_TIME_COOKING = 1

    # Модель RecipeIngredient
    MIN_VALUE_RECIPEINGREDIENT_AMOUNT = 1

    VISUAL_CHAR = 32
