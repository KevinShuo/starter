# -*- coding: utf-8 -*-
from ..cgt_base import MyCGTeamWork
from ..modules.asset_data import *
from ..info.cgt_account import *

class CGTTaskBase(MyCGTeamWork):
    def __init__(self, project_db: str):
        super().__init__()
        self.project_db = project_db
