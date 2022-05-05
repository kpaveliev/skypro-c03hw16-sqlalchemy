import json
import datetime

def assign_model(Model_name: str, path: str) -> list:
    """ Create list of model objects from json

    :param model_name: Name of the target model
    :param path: Path to json file
    :return: List of the Model_name objects
    """
    # Load data from the json
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Create list of the objects and append it with the Model_name objects
    objects_list = []
    for item in data:
        item_changed = {}
        for key, data in item.items():
            # Replace MM/DD/YYYY fields with datetime.date objects
            if 'date' in key:
                month, day, year = data.split('/')
                date_new = datetime.date(int(year), int(month), int(day))
                item_changed[key] = date_new
            else:
                item_changed[key] = data

        objects_list.append(Model_name(**item_changed))

    return objects_list


def user_to_dict(instance):
    """
    Serialize implementation
    """
    return {
        "id": instance.id,
        "first_name": instance.first_name,
        "last_name": instance.last_name,
        "age": instance.age,
        "email": instance.email,
        "role": instance.role,
        "phone": instance.phone
    }


if __name__ == '__main__':
    print(assign_model('data/orders.json'))
