"""Images Collection.
Gets collection of Images

"""
from pignus_api.collects.base_entity_metas import BaseEntityMetas
from pignus_api.collects.image_builds import ImageBuilds
from pignus_shared.utils import xlate
from pignus_api.models.image import Image


class Images(BaseEntityMetas):
    """Collection class for gathering groups of device macs."""

    collection_name = "images"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(Images, self).__init__(conn, cursor)
        self.table_name = Image().table_name
        self.collect_model = Image
        self.per_page = 20

    def get_by_ids(
            self,
            model_ids: list,
            get_builds: bool = False,
            get_clusters: bool = False) -> list:
        """Get models instances by their ids from the database.
        :unit-test: TestBase.test__get_by_ids
        """
        if not model_ids:
            return []
        model_ids = list(set(model_ids))
        sql_ids = self.int_list_to_sql(model_ids)
        sql = """
            SELECT *
            FROM `%(table_name)s`
            WHERE id IN (%(ids)s); """ % {
            'table_name': self.table_name,
            'ids': sql_ids,
        }
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(
            raws,
            get_builds=get_builds,
            get_clusters=get_clusters)
        return prestines

    def build_from_lists(
            self,
            raws: list,
            get_builds: bool = False,
            get_clusters: bool = False) -> list:
        """Creates list of hydrated collection images, with the optional ability to collect their
        cluster and container children.
        """
        images = super(Images, self).build_from_lists(raws)
        for image in images:
            if get_builds:
                image.get_builds()
            if get_clusters:
                image.get_clusters()
        return images

    def get_maintained(self) -> list:
        """Get Images for that are currently maintained. """
        sql = """
            SELECT *
            FROM `%s`""" % self.table_name
        sql += """
            WHERE `maintained`=1
            ORDER BY `updated_ts` DESC;"""
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        return prestines

    def get_count_maintained(self) -> int:
        """Get count of Images that are maintained"""
        sql = """
            SELECT COUNT(*)
            FROM `images`
            WHERE `maintained` = 1;
            """
        self.cursor.execute(sql)
        raw_scans_count = self.cursor.fetchone()
        return raw_scans_count[0]

    def get_for_sentry_sync_flagged(self) -> list:
        """Get Images for the Sentry Sync process, that are flagged for sync for they can be
        prioritized.
        """
        image_ids = ImageBuilds().get_image_ids_for_sentry_sync_flagged()
        if not image_ids:
            return []
        images = self.get_by_ids(image_ids)
        return images

    def get_for_sentry_sync(self) -> list:
        """Get Images for the Sentry Sync process. """
        image_ids = ImageBuilds().get_image_ids_for_sentry_sync()
        if not image_ids:
            return []
        images = self.get_by_ids(image_ids)
        return images

    def get_for_sentry_scan(self) -> list:
        """Get Images for the Sentry Scan process. """
        image_ids = ImageBuilds().get_image_ids_for_sentry_scan()
        if not image_ids:
            return []
        images = self.get_by_ids(image_ids)
        return images

    def get_for_sentry_rectify(self) -> list:
        """Get Images for the Sentry Rectify process. """
        raw_image_ids = ImageBuilds().get_image_ids_for_sentry_rectify_sync()
        raw_image_ids += ImageBuilds().get_image_ids_for_sentry_rectify_scan()
        # raw_image_ids += ImageBuilds().get_image_ids_for_sentry_rectify_clusters()

        clean_image_ids = []
        for image in raw_image_ids:
            if image not in clean_image_ids:
                clean_image_ids.append(image)
        if not clean_image_ids:
            return []
        images = self.get_by_ids(clean_image_ids)
        return images

    def search_by_name(self, image_name: str, page: int = 1) -> dict:
        """Search for Images by its name."""
        sql = """
            SELECT *
            FROM `images`
            WHERE
                `name` LIKE "%%%(image_name)s%%"
            ORDER BY `updated_ts`
            LIMIT %(per_page)s OFFSET %(offset)s;
            """ % {
            "image_name": xlate.sql_safe(image_name),
            "per_page": self.per_page,
            "offset": self._pagination_offset(page, self.per_page)
        }
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        ret = {
            "objects": prestines,
            "info": self.get_pagination_info(sql, page, self.per_page)
        }
        return ret

    def get_by_cluster(self, cluster_id: str) -> list:
        """Get Images currently present in a given cluster"""
        sql = """
            SELECT `image_id`
            FROM `image_clusters`
            WHERE
                `cluster_id` = "%(cluster_id)s" AND
                `present` = 1
            ORDER BY `updated_ts`;
            """ % {
            "cluster_id": xlate.sql_safe(cluster_id),
        }
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        image_ids = []
        for raw in raws:
            image_ids.append(raw[0])

        images = self.get_by_ids(image_ids, get_clusters=True)
        return images

    def get_by_cluster_paginated(
        self,
        cluster_id: int,
        page: int = 1,
        limit: int = 0,
        per_page: int = 20
    ) -> list:
        """Get Images currently present in a given cluster, in a paginated return."""
        if limit == 0:
            limit = per_page
        sql = """
            SELECT i.*
            FROM `image_clusters` ic
            JOIN `images` i
                ON ic.`image_id` = i.`id`
            WHERE
                ic.`cluster_id` = %(cluster_id)s AND
                ic.`present` = 1
            ORDER BY i.`updated_ts`
            LIMIT %(limit)s OFFSET %(offset)s;
            """ % {
            "cluster_id": xlate.sql_safe(cluster_id),
            "limit": limit,
            "offset": self._pagination_offset(page, limit)
        }
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)

        ret = {
            "objects": prestines,
            "info": self.get_pagination_info(sql, page, limit)
        }
        return ret

    def search_by_cve(self, cve_number: str, page: int = 1) -> list:
        """Search for Images by a CVE number."""
        sql = """
            SELECT *
            FROM `images`
            WHERE
                (
                `cve_critical_nums` LIKE "%%%(cve_number)s%%" OR
                `cve_high_nums` LIKE "%%%(cve_number)s%%" OR
                `cve_medium_nums` LIKE "%%%(cve_number)s%%" OR
                `cve_low_nums` LIKE "%%%(cve_number)s%%"
            )
            AND
            `maintained` = 1
            ORDER BY `updated_ts`
            LIMIT %(per_page)s OFFSET %(offset)s;
            """ % {
            "cve_number": xlate.sql_safe(cve_number),
            "per_page": self.per_page,
            "offset": self._pagination_offset(page, self.per_page)
        }
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        ret = {
            "objects": prestines,
            "info": self.get_pagination_info(sql, page, self.per_page)
        }
        return ret

    def missing_auth(self, aws_account: str) -> list:
        """Get Images missing auth on the remote aws account."""
        sql = """
            SELECT distinct(`entity_id`)
            FROM `entity_metas`
            WHERE
                `entity_type` = "images" AND
                `name` = "ecr-fail-%(aws_account)s";
            """ % {"aws_account": xlate.sql_safe(aws_account)}
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()

        image_ids = []
        for raw in raws:
            image_ids.append(raw[0])

        prestines = self.get_by_ids(image_ids, get_builds=False, get_clusters=False)
        ret = {
            "objects": prestines,
            "info": {},
        }
        return ret

    def get_cve_severity(
        self,
        severity: str,
        scanner_id: int = None,
        page: int = 1,
        limit: int = 0,
        per_page: int = 20
    ) -> list:
        """Get Images with a CVE of a given severity.
        @params


        """
        if limit == 0:
            limit = 20

        if severity.upper() == "CRITICAL":
            severity = severity.upper()
            sql = """
                SELECT DISTINCT(image_id)
                FROM `scans` AS s
                JOIN `images` AS i
                    ON s.image_id = i.id

                WHERE
                    i.`maintained` = 1 AND
                    s.`scanner_id` = %(scanner_id)s
                ORDER BY s.updated_ts DESC
                LIMIT %(limit)s OFFSET %(offset)s
            """ % {
                "scanner_id": xlate.sql_safe(scanner_id),
                "limit": xlate.sql_safe(limit),
                "offset": self._pagination_offset(page, limit)
            }
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        image_ids = []
        for raw in raws:
            image_ids.append(raw[0])

        images = self.get_by_ids(image_ids)
        ret = {
            "objects": images,
            "info": self.get_pagination_info(sql, page, limit)
        }

        return ret


# End File: pignus/src/pignus_api/collections/images.py
