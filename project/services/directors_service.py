from project.dao.directors import DirectorDAO
from project.exceptions import ItemNotFound
from project.schemas.director import DirectorSchema
from project.services.base import BaseService


class DirectorService(BaseService):
    def get_item_by_id(self, pk):
        director = DirectorDAO(self._db_session).get_by_id(pk)
        if not director:
            raise ItemNotFound
        return DirectorSchema().dump(director)

    def get_all_directors(self):
        director = DirectorDAO(self._db_session).get_all()
        return DirectorSchema(many=True).dump(director)