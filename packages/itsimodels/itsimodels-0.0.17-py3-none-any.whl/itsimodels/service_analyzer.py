from itsimodels.core.base_models import BaseModel, ChildModel
from itsimodels.core.fields import (
    BoolField,
    NumberField,
    StringField,
    TypeField
)


class TileSettings(ChildModel):
    is_filter_enabled = BoolField(default=False, alias='isFilterEnabled')

    num_tiles = NumberField(default=50, alias='numTiles')


class ServiceAnalyzer(BaseModel):
    key = StringField(required=True, alias='_key')

    title = StringField(required=True)

    description = StringField(default='')

    earliest_time = StringField()

    kpi_filter_string = StringField(default='', alias='kpiFilterString')

    kpi_tiles_settings = TypeField(TileSettings, alias='kpiTilesSettings')

    latest_time = StringField()

    search_type = StringField(default='aggregate', alias='searchType')

    service_filter_string = StringField(default='', alias='serviceFilterString')

    service_tiles_settings = TypeField(TileSettings, alias='serviceTilesSettings')

    tile_size = StringField(
        choices=('small', 'medium', 'large'),
        default='large',
        alias='tileSize')

    view = StringField(default='view')

    view_type = StringField(
        choices=('tile', 'topology'),
        default='tile',
        alias='viewType')
