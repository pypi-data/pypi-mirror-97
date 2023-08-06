from itsimodels.core.base_models import ImageModel
from itsimodels.core.fields import StringField


class GlassTableImage(ImageModel):
    key = StringField(required=True, alias='_key')

    data = StringField()

    name = StringField()

    type = StringField()
