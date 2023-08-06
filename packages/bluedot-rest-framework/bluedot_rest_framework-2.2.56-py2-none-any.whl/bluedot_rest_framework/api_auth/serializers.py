from django.contrib.auth import get_user_model
from rest_framework import serializers
from bluedot_rest_framework.utils.func import get_tree, get_tree_menu
from bluedot_rest_framework.api_auth.models import AuthMenu, AuthGroupMenu


class AuthGroupMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthGroupMenu
        fields = '__all__'


class AuthMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthMenu
        fields = '__all__'


class AuthUserSerializer(serializers.ModelSerializer):

    menu = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = '__all__'

    def get_menu(self, queryset):
        if queryset.is_superuser:
            menu_queryset = AuthMenu.objects.order_by('-sort')
        else:
            group_menu_ids = AuthGroupMenu.objects.filter(
                pk__in=queryset.group_ids).only('menu_ids')
            menu_ids = []
            for item in group_menu_ids:
                for i in item.menu_ids:
                    if i not in menu_ids:
                        menu_ids.append(i)
            menu_queryset = AuthMenu.objects.filter(pk__in=menu_ids)
        data = AuthMenuSerializer(menu_queryset, many=True).data
        return get_tree(data, 0)
