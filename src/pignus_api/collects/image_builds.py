"""ImageBuilds Collection.
Gets collection of ImageBuilds
"""
from pignus_api.collects.base_entity_metas import BaseEntityMetas
from pignus_api.models.image_build import ImageBuild
from pignus_api.utils import date_utils
from pignus_api.utils import glow


class ImageBuilds(BaseEntityMetas):

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
        collections target model.
        """
        super(ImageBuilds, self).__init__()
        self.table_name = ImageBuild().table_name
        self.collect_model = ImageBuild
        self.scan_interval_hours = glow.options.get("SCAN_INTERVAL_HOURS").value
        self.cluster_interval_hours = glow.options.get("CLUSTER_PRESENCE_HOURS").value

    def get_by_image_id(self, image_id: int) -> list:
        """Get all ImageBuilds belonging to a given Image id."""
        sql_args = {
            "image_id": image_id
        }
        sql = """
            SELECT *
            FROM `image_builds`
            WHERE `image_id` = %(image_id)s
            ORDER BY `created_ts` DESC;"""
        self.cursor.execute(sql, sql_args)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        # for build in prestines:
        #     build.get_last_scan()
        return prestines

    # def get_image_ids_for_sentry_sync_flagged(self) -> list:
    #     """Get all ImageBuilds that are maintained and flagged for scan."""
    #     sql = """
    #         SELECT distinct(`image_id`)
    #         FROM `image_builds`
    #         WHERE
    #             `maintained` = 1 AND
    #             `sync_flag` = 1
    #         ORDER BY `image_id` ASC;
    #     """
    #     self.cursor.execute(sql)
    #     raws = self.cursor.fetchall()
    #     if not raws:
    #         return []
    #     image_ids = []
    #     for raw in raws:
    #         image_ids.append(raw[0])
    #     return image_ids

    def get_for_sentry_sync(self) -> list:
        """Get all ImageBuilds for sentry sync. Current logic states that we collect ImageBuilds
        that are maintained and flagged for sync.
        """
        since = date_utils.date_hours_ago(self.cluster_interval_hours)
        sql = """
            SELECT *
            FROM `image_builds`
            WHERE
                `maintained` = 1 AND
                `scan_enabled` = 1 AND
                (`scan_last_ts` IS NULL OR`sync_last_ts` <= "%s")
            ORDER BY `image_id` ASC;
            """ % (since)
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        if not raws:
            return []
        return self.build_from_lists(raws)

    def get_image_ids_for_sentry_rectify_sync(self) -> list:
        """Get all ImageBuilds that are maintained and flagged for sync"""
        sql = """
            SELECT distinct(`image_id`)
            FROM `image_builds`
            WHERE
                `maintained` = 1 AND
                `pending_operation` = "sync"
            """
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        if not raws:
            return []
        image_ids = []
        for raw in raws:
            image_ids.append(raw[0])
        return image_ids

    def get_image_ids_for_sentry_rectify_scan(self) -> list:
        sql = """
            SELECT DISTINCT(`image_id`)
            FROM `image_builds`
            WHERE `pending_operation` = "scan";
            """
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        image_ids = []
        for raw in raws:
            image_ids.append(raw[0])
        return image_ids

    def get_image_ids_for_sentry_rectify_clusters(self) -> list:
        """Get Image IDs for Sentry the Rectify Cluster's operation. We're looking for
        ImageBuilds that are currently marked as being present in a cluster, but their
        last seen value for that cluster is before our `cluster_presence_interval_hours` value.
        """
        interval = 24
        # since = date_utils.date_hours_ago(self.cluster_interval_hours)
        since = date_utils.date_hours_ago(interval)
        sql = """
            SELECT DISTINCT(`image_id`)
            FROM `image_builds`
            WHERE
                `present` = 1 AND
                `last_seen` <= "%s"
            """ % since
        self.cursor.execute(sql)
        raw_build_ids = self.cursor.fetchall()

        build_ids = []
        for raw in raw_build_ids:
            build_ids.append(raw[0])

        image_builds = self.get_by_ids(build_ids)

        image_ids = []
        for image_build in image_builds:
            image_ids.append(image_build.image_id)
        return image_ids

    def get_image_ids_missing_auth(self) -> list:
        """Get all ImageBuilds with Ecr sync fails."""
        sql = """
            SELECT distinct(c.image_id)
            FROM `entity_metas` em
            JOIN `image_builds` c
                ON em.entity_id = c.id
            WHERE
                em.`entity_type` = "image_build" AND
                em.`name` = "sync-error" AND
                em.`value` = "ecr-auth"; """
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        if not raws:
            return []
        image_ids = []
        for raw in raws:
            image_ids.append(raw[0])
        return image_ids

    def get_count_maintained(self) -> int:
        """Get count of ImageBuilds that are maintained"""
        sql = """
            SELECT COUNT(*)
            FROM `image_builds` where `maintained` = 1;
            """
        self.cursor.execute(sql)
        raw_scans_count = self.cursor.fetchone()
        return raw_scans_count[0]

# End File: pignus/src/pignus_api/collections/image_builds.py
