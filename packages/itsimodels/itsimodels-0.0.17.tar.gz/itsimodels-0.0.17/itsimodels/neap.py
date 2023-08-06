from itsimodels.core.base_models import BaseModel, ChildModel
from itsimodels.core.fields import (
    BoolField,
    DictField,
    ListField,
    NumberField,
    StringField
)


class FactorWeight(ChildModel):
    factor_name = StringField()

    factor_weight = NumberField()


class Rule(ChildModel):
    key = StringField(alias='_key')

    actions = ListField(object)

    activation_criteria = DictField()

    description = StringField()

    priority = NumberField()

    title = StringField()


class NotableEventAggregationPolicy(BaseModel):
    key = StringField(required=True, alias='_key')

    title = StringField(required=True)

    breaking_criteria = DictField(object)

    description = StringField(default='')

    disabled = BoolField(default=True)

    entity_factor_enabled = BoolField(default=True)

    filter_criteria = DictField(object)

    group_assignee = StringField()

    group_custom_instruction = StringField()

    group_dashboard = StringField()

    group_dashboard_context = StringField()

    group_description = StringField()

    group_instruction = StringField()

    group_severity = StringField()

    group_status = StringField()

    group_title = StringField()

    priority = StringField()

    rules = ListField(Rule)

    service_topology_enabled = BoolField(default=True)

    smart_breaking_criteria = DictField(object, alias='ace_breaking_criteria')

    smart_enabled = BoolField(default=False, alias='ace_enabled')

    smart_factor_fields = ListField(object, alias='ace_factor_fields')

    smart_factor_weights = ListField(FactorWeight, alias='ace_factor_weights')

    smart_field_analysis_end_time = NumberField(alias='ace_field_analysis_end_time')

    smart_field_analysis_start_time = NumberField(alias='ace_field_analysis_start_time')

    smart_group_assignee = StringField(alias='ace_group_assignee')

    smart_group_dashboard = StringField(alias='ace_group_dashboard')

    smart_group_dashboard_context = StringField(alias='ace_group_dashboard_context')

    smart_group_description = StringField(alias='ace_group_description')

    smart_group_instruction = StringField(alias='ace_group_instruction')

    smart_group_severity = StringField(alias='ace_group_severity')

    smart_group_status = StringField(alias='ace_group_status')

    smart_group_title = StringField(alias='ace_group_title')

    smart_split_by_field = StringField(default='', alias='ace_split_by_field')

    split_by_field = StringField(default='')

    sub_group_limit = StringField(default='')
