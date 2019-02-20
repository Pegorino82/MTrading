import re


def get_parent_names(name: str):
    '''
    генерирует список имен родителей
    :param name: имя категории
    :return: список возможных имен родителей
    '''
    names = []
    for i in range(1, len(name.split('.')[1:]) + 1):
        names.append('.'.join(name.split('.')[:-i]))
    return names


def get_children_names(name: str, names_of_all_children: list):
    '''
    получает имена детей
    :param name: имя категории
    :param names_of_all_children: список всех потомков
    :return: tuple со списком с именами детей и со списком тех, кто не подошел
    '''
    names = []
    excluded = []
    pattern = re.compile(rf'({name}\.[\d]+)')
    for child in names_of_all_children:
        if pattern.fullmatch(child):
            names.append(child)
        else:
            excluded.append(child)
    return names, excluded


def get_siblings_names(name, list_of_names):
    '''
    получает имена братьев/сестер
    :param name: имя категории
    :param list_of_names: список с именами
    :return: tuple со списком с именами братьев/сестер и со списком тех, кто не подошел
    '''
    names = []
    excluded = []
    pattern = re.compile(rf"({'.'.join(name.split('.')[:-1])}\.[\d]+)")
    for sibling in list_of_names:
        if pattern.fullmatch(sibling):
            names.append(sibling)
        else:
            excluded.append(sibling)
    return names, excluded