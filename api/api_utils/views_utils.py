def get_category_names(data: dict):
    '''
    возвращает имена всех категорий
    :param data: словарь запроса
    :return: список с именами категорий
    '''
    categories = []

    def recursion(data):
        for key, val in data.items():
            if key == 'name':
                categories.append(val)
            if key == 'children':
                for child in val:
                    recursion(child)

    recursion(data)
    return categories


def validate_data(data: dict):
    '''
    проверяет валидность данных (имени категории)
    :return: True or False
    '''
    i = 0
    cat_prefix = ''
    flag = True

    def recursion(data):
        nonlocal i
        nonlocal cat_prefix
        nonlocal flag
        for key, val in data.items():
            if not flag:
                return
            elif key == 'name':
                check_prefix = cat_prefix.split('.')
                check_val = val.split('.')
                if len(check_val) - len(check_prefix) > 1:
                    # проверяем что перескочили через одного потомка
                    # print(f'len breaks! {i} - {val}')
                    flag = False
                if len(check_val) == len(check_prefix):
                    # проверяем, что братья/сестры
                    if '.'.join(check_val[:-1]) != '.'.join(check_prefix[:-1]):
                        # print(f'equal breaks! {i} - {val}')
                        flag = False
                    # проверяем на уникальность имени
                    if '.'.join(check_val) == '.'.join(check_prefix):
                        # print(f'unique breaks! {i} - {val}')
                        flag = False
                if len(check_val) - len(check_prefix) == 1:
                    # проверяем, что ближайший ребенок
                    if not '.'.join(check_val).startswith('.'.join(check_prefix)):
                        # print(f'starts breaks! {i} - {val}')
                        flag = False
                i += 1
                cat_prefix = val

            elif key == 'children':
                for child in val:
                    recursion(child)
        return flag

    return recursion(data)
