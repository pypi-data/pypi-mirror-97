from itsimodels.core.base_models import BaseModel
from itsimodels.core.fields import StringField


class GlassTableIcon(BaseModel):
    key = StringField(required=True, alias='_key')

    category = StringField()

    data = StringField(alias='dataURI')

    default_width = StringField()

    default_height = StringField()

    svg_path = StringField()

    title = StringField()
