"""Image Build Model

"""
from pignus_api.models.base_entity_meta import BaseEntityMeta
from pignus_api.models.scan import Scan
from pignus_api.models.image_build_cluster import ImageBuildCluster
from pignus_api.models.entity_meta import EntityMeta
from pignus_api.collects.image_build_clusters import ImageBuildClusters
from pignus_api.collects.operations import Operations
from pignus_api.collects.scans import Scans
from pignus_api.utils import date_utils
from pignus_api.utils import glow
from pignus_shared.models.image_build import FIELD_MAP
from pignus_shared.utils import misc
from pignus_shared.utils import xlate


class ImageBuild(BaseEntityMeta):

    model_name = "image_build"

    def __init__(self, conn=None, cursor=None):
        """
        :unit-test: TestImageBuild::test____init__
        """
        super(ImageBuild, self).__init__(conn, cursor)
        self.table_name = "image_builds"
        self.field_map = FIELD_MAP
        self.scans = []
        self.clusters = {}
        self.operations = []
        self.metas = {}
        self.scan = {}
        self.setup()

    def __repr__(self) -> str:
        """
        :unit-test: TestImageBuild::test____repr__
        """
        if self.digest:
            return "<ImageBuild %s:%s>" % (self.id, self.short_digest())
        else:
            return "<ImageBuild>"

    def get_by_digest(self, digest: str):
        """Gets a container by it's digest."""
        sql = """
            SELECT *
            FROM `image_builds`
            WHERE `digest` = %(digest)s
            LIMIT 1; """
        digest = xlate.sql_safe(digest)
        self.cursor.execute(sql, {"digest": digest})
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

    def short_digest(self):
        """Get the short digest of a ImageBuild. These are often used is Docker.
        :unit-test: TestImageBuild::test__short_digest
        """
        return misc.short_digest(self.digest)

    def get_clusters(self) -> dict:
        """Get all ImageBuild Cluster data"""
        raw_clusters = ImageBuildClusters().get_by_image_build_id(self.id)
        for cluster in raw_clusters:
            self.clusters[cluster.cluster_id] = cluster
        return self.clusters

    def get_last_scan(self):
        """Get the Container's last Scan data.
        @todo: fix scanner_id
        """
        scan = Scan()
        if scan.get_build_last(self.id, scanner_id=1):
            self.scan = scan
            return scan
        else:
            self.scan = False
            return False

    def set_cluster_observed(self, cluster_id: int) -> bool:
        """Update ImageBuildCluster that we have observed the image in the cluster. """
        image_build_cluster = ImageBuildCluster()
        if not self.id:
            raise AttributeError("ImageBuild missing ID, cannot set cluster observed")
        if not image_build_cluster.get_image_build_cluster(self.id, cluster_id):
            image_build_cluster.image_build_id = self.id
            image_build_cluster.cluster_id = cluster_id
            image_build_cluster.first_seen = date_utils.now()
        image_build_cluster.last_seen = date_utils.now()
        image_build_cluster.present = True
        image_build_cluster.save()
        return True

    def get_operations(self) -> list:
        """Get a list of all the Container"s Operations."""
        collect_operations = Operations()
        self.operations = collect_operations.get_by_image_id(self.id)
        return self.operations

    def get_scan(self) -> Scan:
        """Get a list of all the Container"s Operations."""
        scan = Scan()
        if not scan.get_container_last(self.id, scanner_id=1):
            return False
        return scan

    def save(self) -> bool:
        """Delete a User and its ApiKeys."""
        if self.repository:
            self.repository = misc.strip_trailing_slash(self.repository)

        return super(ImageBuild, self).save()

    def delete(self) -> bool:
        """Delete a Container and it"s relationships."""
        self.get_clusters()
        container_clusters = []
        for cluster_name, cluster in self.clusters.items():
            container_clusters.append(cluster.id)
        ImageBuildClusters().delete_by_ids(container_clusters)

        # Delete Image Operations
        self.get_operations()
        for operation in self.operations:
            operation.delete()

        super(ImageBuild, self).delete()
        return True

    def json(self) -> dict:
        """Create a JSON friendly output of the model, converting types to friendlies. Add Scan to
        the return.
        """
        default_scanner = glow.options["DEFAULT_SCANNER"].value
        json_ret = super(ImageBuild, self).json()
        last_scan = Scans().get_last(self.id, scanner_id=default_scanner)
        if last_scan:
            json_ret["scan"] = last_scan.json()
        else:
            json_ret["scan"] = {}

        self.get_clusters()
        # Get the ImageBuild Clusters
        # image_build_clusters = self.get_clusters()
        # json_ret["clusters"] = image_build_clusters

        return json_ret

    def set_pending_operation(self):
        """
        """
        pending_ops = Operations().get_pending_by_build_id(self.id)
        if pending_ops:
            return False
        else:
            self.pending_operation = None
            self.save()
            return True

    def set_meta_maintained(self, set_value: str) -> EntityMeta:
        """
        """
        self.get_meta("maintained-info")
        self.metas["maintained-info"] = self.get_meta("maintained-info")
        if not self.metas["maintained-info"]:
            # Create the notes meta if it doesn't exist
            self.metas["maintained-info"] = EntityMeta()
            self.metas["maintained-info"].create(
                meta_name="maintained-info",
                meta_type='str',
                entity_id=self.id,
                meta_value=set_value)
            self.metas["maintained-info"].save()
        else:
            self.metas["maintained-info"].value = set_value
            self.metas["maintained-info"].save()
        return self.metas["maintained-info"]


# End File: pignus/src/pignus_api/modles/image_build.py
