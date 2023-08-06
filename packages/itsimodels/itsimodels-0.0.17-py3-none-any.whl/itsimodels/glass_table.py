from itsimodels.core.base_models import BaseModel, ChildModel
from itsimodels.core.compat import string_types
from itsimodels.core.fields import (
    BoolField,
    DictField,
    ForeignKey,
    ForeignKeyList,
    ListField,
    NumberField,
    StringField,
    TypeField
)


KPI_SUMMARY_RE = r'`get_full_itsi_summary_kpi\((.+)\)`'


KV_STORE_KEY_RE = r'splunk-enterprise-kvstore://(.+)'


class ValuedModel(ChildModel):

    def to_dict(self, *args, **kwargs):
        obj = super(ValuedModel, self).to_dict(*args, **kwargs)

        # Remove any null values to conform with the UI visualization library
        data = {key: value for key, value in obj.items() if value}

        return data


class DataSourceMeta(ChildModel):
    kpi_id = ForeignKey('itsimodels.service.Kpi', alias='kpiID')

    service_id = ForeignKey('itsimodels.service.Service', alias='serviceID')


class DataSourceOptions(ValuedModel):
    data = DictField()

    query = ForeignKey('itsimodels.service.Kpi', key_regex=KPI_SUMMARY_RE)


class DataSource(ValuedModel):
    meta = TypeField(DataSourceMeta)

    name = StringField()

    options = TypeField(DataSourceOptions)

    primary = StringField()

    type = StringField()


class DefinitionInput(ChildModel):
    options = DictField()

    type = StringField()


class LayoutImage(ChildModel):
    size_type = StringField(alias='sizeType')

    src = ForeignKey('itsimodels.glass_table_image.GlassTableImage', key_regex=KV_STORE_KEY_RE)

    x = NumberField()

    y = NumberField()


class LayoutOptions(ChildModel):
    background_color = StringField(alias='backgroundColor')

    background_image = TypeField(LayoutImage, alias='backgroundImage')

    height = NumberField()

    width = NumberField()


class StructureItem(ChildModel):
    item = StringField()

    position = DictField()

    type = StringField()


class Layout(ChildModel):
    global_inputs = ListField(string_types, alias='globalInputs')

    options = TypeField(LayoutOptions)

    structure = ListField(StructureItem)

    type = StringField()


class VisualizationOptions(ValuedModel):
    background_color = StringField(alias='backgroundColor')

    color = StringField()

    content = StringField()

    fill = StringField()

    font_size = NumberField(alias='fontSize')

    icon = ForeignKey('itsimodels.glass_table_icon.GlassTableIcon', key_regex=KV_STORE_KEY_RE)

    number_precision = NumberField(alias='numberPrecision')

    preserve_aspect_ratio = BoolField(alias='preserveAspectRatio')

    rx = NumberField()

    ry = NumberField()

    show_value = BoolField(alias='showValue')

    src = ForeignKey('itsimodels.glass_table_image.GlassTableImage', key_regex=KV_STORE_KEY_RE)

    stroke = StringField()

    stroke_width = NumberField(alias='strokeWidth')


class Visualization(ValuedModel):
    data_sources = DictField(alias='dataSources')

    options = TypeField(VisualizationOptions)

    primary = StringField()

    type = StringField()


class Definition(ChildModel):
    data_sources = DictField(DataSource, alias='dataSources')

    inputs = DictField(DefinitionInput)

    layout = TypeField(Layout)

    visualizations = DictField(Visualization)


class GlassTable(BaseModel):
    key = StringField(required=True, alias='_key')

    title = StringField(required=True)

    definition = TypeField(Definition)

    description = StringField(default='')

    gt_version = StringField(default='beta')

    latest = StringField(default='now')

    latest_label = StringField(default='Now')

    template_selected_service_id = ForeignKey('itsimodels.service.Service', alias='templateSelectedServiceId')

    template_swappable_service_ids = ForeignKeyList('itsimodels.service.Service', alias='templateSwappableServiceIds')
