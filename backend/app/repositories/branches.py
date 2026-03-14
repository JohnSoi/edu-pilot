from .base import BaseRepository
from app.models import Branches


class BranchRepository(BaseRepository):
    _MODEL: Branches = Branches
