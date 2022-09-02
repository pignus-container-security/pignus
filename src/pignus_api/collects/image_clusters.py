"""Image Cluster Collection
Gets collection of Image Clusters

"""
from pignus_api.collects.base import Base
from pignus_api.models.image_cluster import ImageCluster


class ImageClusters(Base):

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(ImageClusters, self).__init__(conn, cursor)
        self.table_name = ImageCluster().table_name
        self.collect_model = ImageCluster

    def get_by_image_id(self, image_id: int) -> list:
        """Get all Image Cluster's for a given Image ID."""
        sql_args = {
            "image_id": image_id
        }
        sql = """
            SELECT *
            FROM `%s`""" % self.table_name
        sql += """
            WHERE `image_id` = %(image_id)s
            ORDER BY `created_ts` DESC;"""
        self.cursor.execute(sql, sql_args)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        return prestines

    def get_by_image_and_cluster(self, image_id: int, cluster_id: int) -> ImageCluster:
        """Get the Image Cluster record for a given image and cluster, returning just the
        ImageCluster if it exists.
        """
        sql_args = {
            "image_id": image_id,
            "cluster_id": cluster_id
        }
        sql = """
            SELECT *
            FROM `%s`""" % self.table_name
        sql += """
            WHERE
                `image_id` = %(image_id)s AND
                `cluster_id` = %(cluster_id)s
            ORDER BY `created_ts` DESC;"""
        self.cursor.execute(sql, sql_args)
        raws = self.cursor.fetchall()
        if not raws:
            return None
        prestines = self.build_from_lists(raws)
        return prestines[0]

    def get_for_sentry_sync(self, image_id: int):
        sql_args = {
            "image_id": image_id
        }
        sql = """
            SELECT *
            FROM `%s`""" % self.table_name
        sql += """
            WHERE
                image_id = %(image_id)s AND
                (
                    maintained = 1 OR
                    sync_flag = 1
                )
            ORDER BY `created_ts` DESC;"""
        self.cursor.execute(sql, sql_args)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        return prestines

# End File: pignus/src/pignus_api/collections/image_clusters.py
