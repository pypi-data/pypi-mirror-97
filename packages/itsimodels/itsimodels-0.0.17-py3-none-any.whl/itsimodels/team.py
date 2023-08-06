from itsimodels.core.base_models import BaseModel, ChildModel
from itsimodels.core.fields import ForeignKey, ListField, StringField


GLOBAL_TEAM_KEY = 'default_itsi_security_group'


class TeamRelative(ChildModel):
    key = ForeignKey('itsimodels.team.Team', required=True, alias='_key')


class Team(BaseModel):
    key = StringField(required=True, alias='_key')

    title = StringField(required=True)

    description = StringField()

    inherit_from = ForeignKey('itsimodels.team.Team')

    children = ListField(TeamRelative)

    parents = ListField(TeamRelative)
