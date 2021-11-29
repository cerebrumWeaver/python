import json


with open('./static/data3.json', 'r', encoding='utf-8') as f:
    json_object = json.loads(f.read())

all_keys = []
all_values = []


# 返回json所有：键-值对 列表型元组
def find_keys_values(json_object):
    keys_list = list(json_object.keys())  # 1.先找到json包含的所有键
    values_list = []
    for key_list in keys_list:
        values_list.append(json_object[key_list])  # 2.遍历键找到对应的值，并存入列表中
# if type(json_object[key_list]) is not dict:
    all_keys.append(keys_list)
    all_values.append(values_list)
    return keys_list, values_list


# 字典递归
def dict_to_dict(json_object, *controller):
    values_list = None
    # if len(controller) > 0 and controller[0] == 'list_on':
    #     if type(json_object) is str:
    #         pass
        # else:
        #     dict_to_dict(json_object)
    # if type(json_object) is not str and type(json_object) is not list:
    if type(json_object) is dict:
        keys_list, values_list = find_keys_values(json_object)
    if values_list is not None:
        for value_list in values_list:
            if type(value_list) is dict:
                dict_to_dict(value_list)
            elif type(value_list) is str:
                pass
            elif type(value_list) is list:
                for _value_list in value_list:
                    dict_to_dict(_value_list, 'list_on')


# print(find_keys_values(json_object))
dict_to_dict(json_object)


def values_extend_keys(keys, values):
    result = f'{keys}: {values}'
    return result


print(all_keys, len(all_keys))
print(all_values, len(all_values))
print('------------------------------------------------------------------------------')
all_keys_list = []
all_values_list = []


for keys in all_keys:
    for key in keys:
        all_keys_list.append(key)
#         print(key)
print('------------------------------------------------------------------------------')

for values in all_values:
    for value in values:
        all_values_list.append(value)
#         print(value)
new_map = map(lambda x, y: f'{x}:{y}', all_keys_list, all_values_list)

print('------------------------------------------------------------------------------')
for i in list(new_map):
    print(i)
# print(list(new_map))
