"""Image Cluster model

"""
from pignus_api.models.base import Base
from pignus_api.utils import date_utils


class ImageCluster(Base):

    model_name = "image_cluster"

    def __init__(self, conn=None, cursor=None):
        super(ImageCluster, self).__init__(conn, cursor)
        self.name = "image_cluster"
        self.table_name = "image_clusters"
        self.field_map = [
            {
                "name": "image_id",
                "type": "int",
                "extra": "NOT NULL"
            },
            {
                "name": "cluster_id",
                "type": "int",
                "extra": "NOT NULL"
            },
            {
                "name": "last_seen",
                "type": "datetime",
                "extra": "NOT NULL"
            },
            {
                "name": "first_seen",
                "type": "datetime",
                "extra": "NOT NULL"
            },
            {
                "name": "present",
                "type": "bool"
            }
        ]
        self.setup()

    def __repr__(self):
        """Image Cluster representation.
        :unit-test: TestImageCluster::test____repr__
        """
        if self.id:
            return "<ImageCluster %s>" % self.id
        else:
            return "<ImageCluster>"

    def get_image_cluster(self, image_id: int, cluster_id: int):
        sql_args = {
            "image_id": image_id,
            "cluster_id": cluster_id,
        }
        sql = """
            SELECT *
            FROM `image_clusters`
            WHERE
                `image_id` = %(image_id)s AND
                `cluster_id` = %(cluster_id)s
            ORDER BY `created_ts` DESC LIMIT 1;"""
        self.cursor.execute(sql, sql_args)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

    def json(self) -> dict:
        """Create a JSON friendly output of the model, converting types to friendlies. This
        instance extends the Base Model"s json method and adds "clusters" to the output.
        """
        json_ret = {
            "cluster_id": self.cluster_id,
            "image_id": self.image_id,
            "last_seen": date_utils.json_date(self.last_seen),
            "first_seen": date_utils.json_date(self.first_seen),
            "present": self.present
        }
        return json_ret

# End File: pignus/src/pignus_api/modles/image_cluster.py
