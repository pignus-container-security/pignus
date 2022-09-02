"""Base Entity Meta Model
Base model class for all models requiring meta storage.

"""
from pignus_api.models.base import Base
from pignus_api.models.entity_meta import EntityMeta
from pignus_shared.utils import xlate


class BaseEntityMeta(Base):
    def __init__(self, conn=None, cursor=None):
        """Base Entity Meta model constructor."""
        super(BaseEntityMeta, self).__init__(conn, cursor)
        self.table_name = None
        self.table_name_meta = EntityMeta().table_name
        self.meta = {}

    def __repr__(self):
        if self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        return "<%s>" % self.__class__.__name__

    def get_by_id(self, model_id: int) -> bool:
        """Get a single model object from db based on an object ID with all meta data loaded into
           self.metas.
        """
        if not super(BaseEntityMeta, self).get_by_id(model_id):
            return False
        self.load_meta()
        return True

    def build_from_list(self, raw: list, meta=False) -> bool:
        """Build a model from list, and pull its meta data."""
        super(BaseEntityMeta, self).build_from_list(raw)
        if meta:
            self.load_meta()

    def build_from_dict(self, raw: dict) -> bool:
        """Builds a model by a dictionary. This is expected to be used mostly from a client making
        a request from a web api.
        This extends the original to unpack meta objects.
        """
        super(BaseEntityMeta, self).build_from_dict(raw)
        if 'meta' not in raw:
            return True

        for meta_key, meta_value in raw["meta"].items():
            self.meta[meta_key] = meta_value

        return True

    def save(self) -> bool:
        """Extend the Base model save, settings saves for all model self.metas objects."""
        super(BaseEntityMeta, self).save()
        if not self.metas:
            return True

        if not self.id:
            raise AttributeError('Model %s cant save entity metas with out id' % self)

        for meta_name, meta in self.metas.items():
            if not isinstance(meta, EntityMeta):
                meta_value = meta
                meta = EntityMeta()
                meta.name = meta_name
                meta.value = str(meta_value)

            meta.entity_type = self.table_name
            meta.entity_id = self.id
            if not meta.type:
                meta.type = 'str'
            meta.save()
            self.metas[meta_name] = meta
        return True

    def delete(self) -> bool:
        """Delete a model item and it's meta."""
        super(BaseEntityMeta, self).delete()
        sql = """
            DELETE FROM `%s`
            WHERE
                `entity_id` = %s AND
                `entity_type` = "%s"
            """ % (
            self.table_name_meta,
            self.id,
            xlate.sql_safe(self.table_name))
        self.cursor.execute(sql)
        self.conn.commit()
        return True

    def get_meta(self, meta_name: str):
        """Get a meta key from an entity if it exists, or return None. """
        if meta_name not in self.metas:
            return False
        else:
            return self.metas[meta_name]

    def meta_update(self, meta_name: str, meta_value, meta_type: str = 'str') -> bool:
        """Set a models entity value if it currently exists or not."""
        if meta_name not in self.metas:
            self.metas[meta_name] = EntityMeta(self.conn, self.cursor)
            self.metas[meta_name].name = meta_name
            self.metas[meta_name].type = meta_type
        self.metas[meta_name].value = meta_value
        return True

    def load_meta(self) -> bool:
        """Load the model's meta data."""
        sql = """
            SELECT *
            FROM %s
            WHERE
                `entity_id` = %s AND
                `entity_type` = "%s";
            """ % (
            self.table_name_meta,
            self.id,
            xlate.sql_safe(self.table_name))
        self.cursor.execute(sql)
        meta_raws = self.cursor.fetchall()
        self._load_from_meta_raw(meta_raws)
        return True

    def _load_from_meta_raw(self, meta_raws) -> bool:
        """Create self.metas for an object from raw_metas data."""
        ret_metas = {}
        for meta_raw in meta_raws:
            em = EntityMeta(self.conn, self.cursor)
            em.build_from_list(meta_raw)
            ret_metas[em.name] = em
        self.metas = ret_metas
        return True


# End File: pignus/src/pignus_api/modles/base_entity_meta.py
