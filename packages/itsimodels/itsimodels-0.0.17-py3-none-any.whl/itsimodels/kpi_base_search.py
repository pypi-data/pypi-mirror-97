from itsimodels.core.base_models import BaseModel, ChildModel
from itsimodels.core.fields import (
    BoolField,
    ListField,
    NumberField,
    StringField
)


class SearchMetric(ChildModel):
    key = StringField(required=True, alias='_key')

    title = StringField(required=True)

    aggregate_statop = StringField(default='avg')

    entity_statop = StringField(default='avg')

    fill_gaps = StringField(default='null_value')

    gap_custom_alert_value = StringField()

    gap_severity = StringField(default='unknown')

    gap_severity_color = StringField(default='')

    gap_severity_color_light = StringField(default='')

    gap_severity_value = StringField(default='-1')

    threshold_field = StringField(default='')

    unit = StringField(default='')


class KpiBaseSearch(BaseModel):
    key = StringField(required=True, alias='_key')

    base_search = StringField(required=True)

    title = StringField(required=True)

    alert_lag = NumberField(default=30)

    alert_period = StringField()

    description = StringField(default='')

    entity_filter_field = StringField(default='', alias='entity_id_fields')

    entity_split_field = StringField(default='', alias='entity_breakdown_id_fields')

    is_filter_entities_to_service = BoolField(default=False, alias='is_service_entity_filter')

    is_split_by_entity = BoolField(default=False, alias='is_entity_breakdown')

    metric_qualifier = StringField(default='')

    metrics = ListField(SearchMetric)

    search_alert_earliest = StringField(default='')
