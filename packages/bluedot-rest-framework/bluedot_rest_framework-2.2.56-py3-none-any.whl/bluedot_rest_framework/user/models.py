from .abstract_models import AbstractUser


class User(AbstractUser):

    class Meta:
        db_table = 'user'
        swappable = 'FORNTEND_USER_MODEL'
