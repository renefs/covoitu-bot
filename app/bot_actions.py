import pickle
from app import logger, redis_connection


def get_help(chat_id):
    payload = {
        "chat_id": chat_id,
        "text": "Ayuda: \n"
        + "- /add: Añade 1 a tu cuenta\n"
        + "- /remove: Resta 1 a tu cuenta\n"
        + "- /show: Muestra todas las cuentas\n"
        + "- /kill <nombre>: Elimina a un usuario\n"
        + "- /set <nombre> <valor>: Establece el valor de un usuario\n"
        + "- /clear estoy totalmente seguro, dale: Borra todos los datos\n",
    }
    logger.info("Help requested")
    return payload


def get_clear(chat_id, received_text):
    try:
        user_to_kill = received_text.split(" ", 1)[1]
    except IndexError:
        user_to_kill = None
    if user_to_kill == "estoy totalmente seguro, dale":
        p_mydict = pickle.dumps({})
        redis_connection.set("data", p_mydict)
        text = "Hala, todo borrado! Te habrás quedado a gusto..."
    else:
        text = (
            "No se ha borrado nada. Si quieres borrar todo, "
            + "tienes que escribir: "
            + "'estoy totalmente seguro, dale' después de /clear"
        )
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    logger.info(text)
    return payload


def get_set(chat_id, received_text):
    try:
        user_to_set = received_text.split(" ")[1]
        value = received_text.split(" ")[2]
        value = int(value)
        if value < 0:
            user_to_set = None
    except (IndexError, ValueError):
        user_to_set = None
    if user_to_set:
        redis_data = redis_connection.get("data")
        if not redis_data:
            user_counts = {}
        else:
            user_counts = pickle.loads(redis_data)
        # Remove the user with name user_to_set from the dict
        user_set = False
        for user_id in user_counts:
            user = user_counts[user_id]
            if user["name"] == user_to_set:
                user["count"] = value
                user_set = True
                break
        if not user_set:
            text = "El usuario no existe, así que no se cambió nada 💃"
        else:
            p_mydict = pickle.dumps(user_counts)
            redis_connection.set("data", p_mydict)
            text = f"Se ha establecido {user_to_set} a {value}. WoW!"
    else:
        text = "No se ha podido establecer nada. Algo mal habrás hecho... "

    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    logger.info(text)

    return payload


def get_kill(chat_id, received_text):
    user_to_kill = received_text.split(" ")[1]
    redis_data = redis_connection.get("data")
    if not redis_data:
        user_counts = {}
    else:
        user_counts = pickle.loads(redis_data)
    # Remove the user with name user_to_kill from the dict
    for user_id in user_counts:
        user = user_counts[user_id]
        if user["name"] == user_to_kill:
            user_counts.pop(user_id)
            break
    p_mydict = pickle.dumps(user_counts)
    redis_connection.set("data", p_mydict)
    text = f"Se ha eliminado a {user_to_kill}. Adieu!"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    logger.info(text)
    return payload


def get_show(chat_id):
    display_text = "🚙 Cuentas:\n"
    redis_data = redis_connection.get("data")
    if not redis_data:
        user_counts = {}
    else:
        user_counts = pickle.loads(redis_data)

    for user_id in user_counts:
        user = user_counts[user_id]
        user_name = user["name"]
        display_text += f"- @{user_name}: {user['count']}\n"

    if len(user_counts.items()) == 0:
        display_text = "No hay datos aún"

    payload = {
        "chat_id": chat_id,
        "text": display_text,
    }
    logger.info("Show requested")
    return payload


def get_remove(chat_id, username, user_id, user_first_name):
    redis_data = redis_connection.get("data")
    if not redis_data:
        user_counts = {}
    else:
        user_counts = pickle.loads(redis_data)
    user_name = username or user_first_name

    current_value = user_counts.get(user_id, {"count": 0, "name": user_name}).get(
        "count", 0
    )

    user_counts[user_id] = {
        "count": current_value - 1 if current_value > 0 else 0,
        "name": user_name,
    }
    text = f"Se ha restado 1 a la cuenta de @{user_name}. "
    payload = {
        "chat_id": chat_id,
        "text": text + f"Total: {user_counts[user_id]['count']}",
    }
    p_mydict = pickle.dumps(user_counts)
    redis_connection.set("data", p_mydict)
    logger.info(text)
    return payload


def get_add(chat_id, username, user_id, user_first_name):
    redis_data = redis_connection.get("data")
    if not redis_data:
        user_counts = {}
    else:
        user_counts = pickle.loads(redis_data)
    user_name = username or user_first_name

    current_value = user_counts.get(user_id, {"count": 0, "name": user_name}).get(
        "count", 0
    )

    user_counts[user_id] = {
        "count": current_value + 1,
        "name": user_name,
    }
    text = f"Se ha añadido 1 a la cuenta de @{user_name}. "
    payload = {
        "chat_id": chat_id,
        "text": text + f"Total: {user_counts[user_id]['count']}",
    }
    p_mydict = pickle.dumps(user_counts)
    redis_connection.set("data", p_mydict)
    logger.info(text)
    return payload
