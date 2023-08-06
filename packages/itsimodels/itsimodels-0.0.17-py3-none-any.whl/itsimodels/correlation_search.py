from itsimodels.core.fields import StringField
from itsimodels.core.base_models import DynamicModel


class CorrelationSearch(DynamicModel):
    key = StringField(required=True)

    name = StringField(required=True)
