PRIZES = {
    "vingummi-bamser": {
        "name": "Vingummi Bamser",
        "price": 10,
    },
    "stor-slikkepind": {
        "name": "Stor Slikkepind",
        "price": 250,
    },
    "squishy": {
        "name": "Squishy",
        "price": 100,
    },
    "dumpling": {
        "name": "Dumpling",
        "price": 250,
    },
}


state = {
    "active": False,
    "side": None,
    "starting_balance": 0,
    "remaining_balance": 0,
    "prizes": [],
}


def start_order(side):
    if state["active"]:
        return False, "Der er allerede en aktiv ekspedition."

    state["active"] = True
    state["side"] = side
    state["starting_balance"] = 0
    state["remaining_balance"] = 0
    state["prizes"] = []

    return True, f"Ny ekspedition startet på {side} side."


def register_ticket_balance(amount):
    if not state["active"]:
        return False, "Der er ingen aktiv ekspedition."

    state["starting_balance"] += amount
    state["remaining_balance"] += amount

    return True, f"{amount} billetter blev registreret."


def add_prize(slug):
    if not state["active"]:
        return False, "Der er ingen aktiv ekspedition."

    prize = PRIZES.get(slug)

    if prize is None:
        return False, "Gevinsten findes ikke."

    if state["remaining_balance"] < prize["price"]:
        return (
            False,
            f"Der er ikke nok billetter til {prize['name']}. "
            f"Gevinsten koster {prize['price']} billetter.",
        )

    state["prizes"].append(
        {
            "slug": slug,
            "name": prize["name"],
            "price": prize["price"],
        }
    )

    state["remaining_balance"] -= prize["price"]

    return True, f"{prize['name']} blev tilføjet."


def finish_order():
    if not state["active"]:
        return False, "Der er ingen aktiv ekspedition."

    remaining_balance = state["remaining_balance"]

    state["active"] = False
    state["side"] = None
    state["starting_balance"] = 0
    state["remaining_balance"] = 0
    state["prizes"] = []

    return (
        True,
        f"Ekspeditionen blev afsluttet. "
        f"Resterende saldo var {remaining_balance} billetter.",
    )