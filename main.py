import requests, json, csv
from logger import logger

base_url = "https://jsonplaceholder.typicode.com/"
stat_file = "stat.csv"


def decorator_save_json_to_file(fun):
    def wrapper(*args):
        data = fun(*args)
        file_name = "./" + args[0] + ".json"
        if not data:
            logger.warning(f"No data to save into file {file_name}")
        else:
            with open(file_name, "w") as file:
                json.dump(data, file, indent=4)
            logger.debug(f"Data were saved into file {file_name}")
            return data

    return wrapper


@decorator_save_json_to_file
def get_data(path):
    response = requests.get(base_url + path)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Error code: {response.status_code}. Error message:  {response.text}")
        return None


def count_posts_by_user(posts):
    user_counts = {}
    if not posts:
        return {}
    for post in posts:
        user_id = post["userId"]
        user_counts[user_id] = user_counts[user_id] + 1 if user_id in user_counts else 0
    return user_counts


def print_stat(posts, users):
    user_counts = count_posts_by_user(posts)
    if users:
        logger.info("Print statistics about posts by users:")
        for user in users:
            user_id = user["id"]
            logger.info(
                f"Id: {user_id}, Name: {user["name"]},  Username:  {user["username"]},  Posts:  {user_counts[user_id] if user_id in user_counts else 0}")


def save_stat(posts, users):
    user_counts = count_posts_by_user(posts)
    with open(stat_file, "w", newline='') as file:
        writer = csv.writer(file)
        row = ["id", "name", "username", "posts"]
        writer.writerow(row)
        if users:
            for user in users:
                row = get_stat_row(user, user_counts)
                writer.writerow(row)
    logger.debug(f"Posts by user were saved to file {stat_file}")


def get_stat_row(user, user_counts):
    row = []
    user_id = user["id"]
    row.append(user_id)
    row.append(user["name"])
    row.append(user["username"])
    row.append(user_counts[user_id] if user_id in user_counts else 0)
    return row


users = get_data("users")
posts = get_data("posts")
print_stat(posts, users)
save_stat(posts, users)
