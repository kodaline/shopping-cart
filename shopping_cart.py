from pydantic import BaseModel
from ast import literal_eval
import time

from cat.mad_hatter.decorators import tool, hook
from cat.log import log

from .helper import get_items, save_items, stringify_items


@tool(return_direct=True)
def add_to_shopping_cart(products, cat):
    """Add product or multiple products to the shopping list. User may say "Add to my shopping list potatoes..." or similar. Argument "products" is an array of items.
    """

    products = literal_eval(products)
    shopping_cart = get_items()
    for elem in products:
        shopping_cart.append({
            "created": time.time(),
            "description": str(elem)
        })

    save_items(shopping_cart)

    return f"Shopping list updated with: *{', '.join(products)}*"

@tool(return_direct=True)
def remove_from_shopping_list(products, cat):
    """Remove / delete product or multiple products from the shopping list. "products" is the array of items to remove."""
    shopping_cart = get_items()

    prompt = "Given this list of products:"
    for t_index, t in enumerate(shopping_cart):
        prompt += f"\n {t_index}. {t['description']}"
    prompt += f"\n\nThe products corresponding to `{products}` are items number... (reply ONLY with an array with the number or numbers, no letters or points)"
    try:
        to_remove = cat.llm(prompt)

        index_to_remove = literal_eval(to_remove)
        shopping_cart = [el for idx, el in enumerate(shopping_cart) if idx not in index_to_remove]
        save_items(shopping_cart)
    except Exception as e:
        log(e, "ERROR")
        return f"Sorry there was an error: {e}. Can you ask in a different way?"

    return stringify_items(shopping_cart)


@tool(return_direct=True)
def search_in_shopping_cart(query, cat):
    """Get things in the shopping list. "query" is a string used to filter the list."""

    todos = get_items()
    return stringify_items(todos)