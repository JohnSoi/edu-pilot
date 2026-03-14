from app.repositories.branches import BranchRepository
from app.services.base import BaseService


class BranchService(BaseService):
    _REPOSITORY = BranchRepository