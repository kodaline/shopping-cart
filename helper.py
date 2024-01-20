
import os
import pandas as pd


cart_filepath = os.path.join(
    os.path.dirname(__file__), "shopping_cart.csv"
)


def stringify_items(cart):
    if len(cart) == 0:
        return "Your shopping list is empty."
    
    out = "### Shopping list:"
    for t in cart:
        out += "\n - " + t["description"]

    return out


def get_items():
    if not os.path.exists(cart_filepath):
        return []
    else:
        df = pd.read_csv(cart_filepath)
        return df.to_dict(orient="records")

    
def save_items(cart):
    if len(cart) == 0:
        os.remove(cart_filepath)
    else:
        pd.DataFrame(cart).to_csv(cart_filepath, index=False)