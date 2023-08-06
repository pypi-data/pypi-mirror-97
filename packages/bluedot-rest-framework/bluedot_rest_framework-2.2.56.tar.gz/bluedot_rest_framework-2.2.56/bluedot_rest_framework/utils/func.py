import hashlib


def get_tree(data, parent):
    result = []
    for item in data:
        if parent == item["parent"]:
            temp = get_tree(data, item["id"])
            if (len(temp) > 0):
                item["children"] = temp
            result.append(item)
    return result


def get_tree_menu(data, parent):
    state = True
    for item in data:
        if parent == item['id']:
            state = False
    return state


def orm_bulk_update(queryset, update_dict):
    if queryset and update_dict:
        for key in update_dict:
            setattr(queryset, key, update_dict[key])
        return queryset.save()


def md5_str(_str):
    md5_obj = hashlib.md5()
    md5_obj.update(_str.encode('utf8'))
    return md5_obj.hexdigest()
