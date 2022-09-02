"""Image Build Cluster Model

"""
from pignus_api.models.base import Base


class ImageBuildCluster(Base):

    model_name = "image_build_cluster"

    def __init__(self, conn=None, cursor=None):
        super(ImageBuildCluster, self).__init__(conn, cursor)
        self.table_name = 'image_build_clusters'
        self.field_map = [
            {
                "name": "image_build_id",
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
        return "<ImageBuildCluster>"

    def get_image_build_cluster(self, image_build_id: int, cluster: str) -> bool:
        """Gets the ImageBuildCluster with a image_build_id and a cluster. """
        sql_args = {
            "image_build_id": image_build_id,
            "cluster_id": cluster
        }
        sql = """
            SELECT *
            FROM `image_build_clusters`
            WHERE
                `image_build_id` = %(image_build_id)s AND
                `cluster_id` = %(cluster_id)s
            LIMIT 1;
            """
        self.cursor.execute(sql, sql_args)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

    def get_cluster_last_check_in(self, cluster_id: int):
        sql_args = {
            "cluster": cluster_id
        }
        sql = """
            SELECT `last_seen`
            FROM `image_build_clusters`
            WHERE
                `cluster_id` = %(cluster_id)s
            ORDER BY `last_seen` DESC
            LIMIT 1;
            """
        self.cursor.execute(sql, sql_args)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        return raw[0]


# End File: pignus/src/pignus_api/modles/image_build_cluster.py
