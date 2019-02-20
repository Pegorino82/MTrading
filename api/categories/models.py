from django.db import models
from api_utils.db_parsers import get_parent_names, get_children_names, get_siblings_names


class Category(models.Model):
    name = models.CharField(
        max_length=64,
        null=False,
        unique=True,
        db_index=True)

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def get_parents(cls, id_):
        parents_list = []
        category_name = Category.objects.get(pk=id_).name
        parents_names = get_parent_names(category_name)
        for name in parents_names:
            parent = Category.objects.filter(name=name).first()
            if parent:
                parents_list.append(parent)

        return parents_list

    @classmethod
    def get_children(cls, id_):
        children_list = []
        category_name = Category.objects.get(pk=id_).name
        children = Category.objects.filter(name__startswith=category_name + '.')
        names_list = [child.name for child in children]
        _, excluded = get_children_names(category_name, names_list)
        for child in children.exclude(name__in=excluded):
            children_list.append(child)

        return children_list

    @classmethod
    def get_siblings(cls, id_):
        siblings_list = []
        category_name = Category.objects.get(pk=id_).name
        prepare_queryset = Category.objects.filter(name__startswith='.'.join(category_name.split('.')[:-1])) \
            .exclude(name=category_name)
        prepare_list = [sibling.name for sibling in prepare_queryset]
        _, excluded = get_siblings_names(category_name, prepare_list)
        for sibling in prepare_queryset.exclude(name__in=excluded):
            siblings_list.append(sibling)

        return siblings_list
