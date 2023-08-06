from itsimodels.core.base_models import BaseModel, ChildModel
from itsimodels.core.compat import string_types
from itsimodels.core.fields import (
    BoolField,
    DictField,
    ForeignKey,
    ListField,
    NumberField,
    StringField,
    TypeField
)


class LaneOverlaySettings(ChildModel):
    is_enabled = StringField(default='no', alias='isEnabled')

    overlay_type = StringField(alias='overlayType')

    graph_color = StringField(alias='graphColor')

    graph_type = StringField(alias='graphType')

    entity_count = NumberField(alias='entityCount')

    selection_mode = StringField(alias='selectionMode')

    metric = StringField()

    selected_entities = ListField(alias='selectedEntities')

    search = StringField()


class DeepDiveLaneSettings(ChildModel):
    key = StringField(required=True, alias='id')

    data_gaps = StringField(default='connected', alias='dataGaps')

    data_model_stat_op = StringField(default='count', alias='dataModelStatOp')

    data_model_where_clause = StringField(default='', alias='dataModelWhereClause')

    data_model = DictField(string_types, alias='datamodelModel')

    distribution_stream_mode = StringField(default='quantile', alias='distributionStreamMode')

    entity_add_to_summary = StringField(default='yes', alias='entityAddToSummary')

    exclude_fields = ListField(string_types, alias='excludeFields')

    graph_color = StringField(default='', alias='graphColor')

    graph_series = ForeignKey('itsimodels.service.Kpi', alias='graphSeries')

    graph_type = StringField(default='line', alias='graphType')

    hide_graph = StringField(default='no', alias='hideGraph')

    kpi_add_to_summary = StringField(default='yes', alias='kpiAddToSummary')

    kpi_id = ForeignKey('itsimodels.service.Kpi', alias='kpiId')

    kpi_service_id = ForeignKey('itsimodels.service.Service', alias='kpiServiceId')

    kpi_service_title = StringField(alias='kpiServiceTitle')

    kpi_title = StringField(alias='kpiTitle')

    kpi_unit = StringField(default='', alias='kpiUnit')

    lane_overlay_settings = TypeField(LaneOverlaySettings, alias='laneOverlaySettingsModel')

    lane_size = StringField(default='small', alias='laneSize')

    lane_type = StringField(default='kpi', alias='laneType')

    overwrite_entity_title = StringField(default='no', alias='overwriteEntityTitle')

    overwrite_kpi_title = StringField(default='no', alias='overwriteKpiTitle')

    search = StringField(default='')

    search_source = StringField(alias='searchSource')

    subtitle = StringField(default='')

    threshold_indication_enabled = StringField(default='enabled', alias='thresholdIndicationEnabled')

    threshold_indication_type = StringField(default='stateIndication', alias='thresholdIndicationType')

    title = StringField(default='')

    vertical_axis_boundary_type = StringField(default='value', alias='verticalAxisBoundaryType')

    vertical_axis_scale = StringField(default='linear', alias='verticalAxisScale')

    vertical_axis_static_bounds = ListField(object, alias='verticalAxisStaticBounds')


class DeepDive(BaseModel):
    key = StringField(required=True, alias='_key')

    title = StringField(required=True)

    description = StringField(default='')

    earliest_time = StringField()

    focus_id = StringField()

    # interactable = BoolField(default=True)

    is_named = BoolField(default=True)

    lane_settings = ListField(DeepDiveLaneSettings, alias='lane_settings_collection')

    latest_time = StringField()

    topology_id = ForeignKey('itsimodels.service.Service')
