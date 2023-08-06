from itsimodels.core.base_models import BaseModel
from itsimodels.core.fields import BoolField, StringField, TypeField
from itsimodels.service import KpiTimePolicies


class KpiThresholdTemplate(BaseModel):
    key = StringField(required=True, alias='_key')

    title = StringField(required=True)

    adaptive_thresholds_is_enabled = BoolField(default=False)

    anomaly_detection_training_window = StringField()

    description = StringField(default='')

    time_policies = TypeField(KpiTimePolicies, alias='time_variate_thresholds_specification')

    use_time_policies = BoolField(default=False, alias='time_variate_thresholds')
