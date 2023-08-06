from .abstract_models import AbstractMaterial


class Material(AbstractMaterial):
    class Meta:
        db_table = 'material'
