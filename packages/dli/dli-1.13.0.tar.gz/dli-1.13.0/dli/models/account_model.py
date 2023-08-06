#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
from dli.models import AttributesDict


class AccountModel(AttributesDict):
    @classmethod
    def _from_v2_response(cls, data):
        id_ = data.pop('id')
        attributes = data.pop('attributes')
        attributes.pop('ui_settings', None)
        return cls(id=id_, **attributes)