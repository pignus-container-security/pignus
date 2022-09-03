"""Image Model
Model to describe the parent Image, which has children ImageBuilds, that are unique instances of an
Image with different image digests.

"""
from pignus_api.models.base_entity_meta import BaseEntityMeta
from pignus_api.models.image_build import ImageBuild
from pignus_api.models.image_cluster import ImageCluster
from pignus_api.collects.image_builds import ImageBuilds
from pignus_api.collects.image_clusters import ImageClusters as CollectImageClusters
from pignus_api.collects.operations import Operations
from pignus_api.collects.scans import Scans
from pignus_api.utils import date_utils
from pignus_shared.models.image import FIELD_MAP
from pignus_shared.utils import misc
from pignus_shared.utils import xlate


class Image(BaseEntityMeta):

    model_name = "image"

    def __init__(self, conn=None, cursor=None):
        """Create the Image instance.
        :unit-test: TestImage::test____init__
        """
        super(Image, self).__init__(conn, cursor)
        self.table_name = "images"
        self.field_map = FIELD_MAP
        self.api_writeable_fields = ["name", "repositories", "maintained"]
        self.metas = {}
        self.clusters = {}
        self.builds = {}
        self.scans = []
        self.operations = []
        self.setup()

    def __repr__(self):
        """Set the class representation
        :unit-test: TestImage::__repr__
        """
        if self.id:
            return "<Image %s:%s>" % (self.id, self.name)
        elif self.name:
            return "<Image %s>" % (self.name)
        else:
            return "<Image>"

    def build_from_dict(self, raw: dict) -> bool:
        """Builds a model by a dictionary. This is expected to be used mostly from a client making
        a request from a web api.
        This extends the original to unpack meta objects.
        For Images we need to unpack 'image_builds' and hydrate them to full ImageBuild model
        objects.
        For "clusters" we need to hydrate the date strings into Arrow objects like we do with all
        other date times.
        :unit-test: TestImage::test__build_from_dict
        """
        super(Image, self).build_from_dict(raw)

        # Check if the raw data has fields we can unpack more
        catch_fields = ["builds", "clusters"]
        unpack_more = False
        for catch in catch_fields:
            if catch in raw:
                unpack_more = True
                continue
        if not unpack_more:
            return True

        # Unpack ImageBuilds and make them a model instance
        for build_key, build_raw in raw["builds"].items():
            self.builds[build_key] = ImageBuild()
            self.builds[build_key].build_from_dict(build_raw)

        # Unpack cluster data, hydrating date info
        for cluster_name, cluster_raw in raw["clusters"].items():
            if "last_seen" in cluster_raw:
                self.clusters[cluster_name]["last_seen"] = \
                    date_utils.date_from_json(cluster_raw["last_seen"])
            if "first_seen" in cluster_raw:
                self.clusters[cluster_name]["first_seen"] = \
                    date_utils.date_from_json(cluster_raw["first_seen"])

        return True

    def get_builds(self) -> dict:
        """Get all ImageBuilds for an Image.
        :unit-test: TestImage::test__get_builds
        """
        raw_builds = ImageBuilds().get_by_image_id(self.id)
        for build in raw_builds:
            self.builds[build.digest] = build
        return self.builds

    def get_build(self, digest: str, repository: str) -> ImageBuild:
        """Get a single ImageBuild from an Image by the Image digest.
        :unit-test: TestImage::test__get_build
        """
        image_build = ImageBuild()
        if not image_build.get_by_digest(digest):
            return False
        return image_build

    def get_clusters(self) -> dict:
        """Get all ImageClusters for the Image."""
        image_clusters = CollectImageClusters().get_by_image_id(self.id)
        for image_cluster in image_clusters:
            self.clusters[image_cluster.cluster_id] = image_cluster
        return self.clusters

    def get_cluster(self, cluster_id: int) -> ImageCluster:
        """Get a single Image Cluster data point, given an Image ID and cluster name"""
        image_cluster = CollectImageClusters().get_by_image_and_cluster(self.id, cluster_id)
        if image_cluster and image_cluster not in self.clusters:
            self.clusters[image_cluster.cluster_id] = image_cluster
        return image_cluster

    def check_image_exists(self, image_parsed: dict):
        name = xlate.sql_safe(image_parsed["name"])
        qry = f"""
            SELECT *
            FROM `{self.table_name}`
            WHERE `name`="{name}"
            LIMIT 1;
            """
        print(qry)
        self.cursor.execute(qry)
        x = self.cursor.fetchone()
        return x

    def set_cluster_observed(self, cluster_id: int) -> bool:
        """Update ImageCluster that we have observed the image in the cluster.
        :unit-test: TestImage.test__set_cluster_observed
        """
        image_cluster = ImageCluster()
        if not self.id:
            raise AttributeError("Image missing ID, cannot set cluster observed")
        if not image_cluster.get_image_cluster(self.id, cluster_id):
            image_cluster.first_seen = date_utils.now()
            image_cluster.cluster_id = cluster_id
            image_cluster.image_id = self.id
        image_cluster.last_seen = date_utils.now()
        image_cluster.present = True
        image_cluster.save()
        return True

    def get_operations(self) -> list:
        """Get a list of all the Image's Operations."""
        collect_operations = Operations()
        self.operations = collect_operations.get_by_image_id(self.id)
        return self.operations

    def get_scans(self) -> list:
        """Get a list of all the Image's Scans."""
        collect_scans = Scans()
        self.scans = collect_scans.get_by_image_id(self.id)
        return self.scans

    def json(self, full: bool = True) -> dict:
        """Create a JSON friendly output of the model, converting types to friendlies. This
        instance extends the Base Model's json method and adds "clusters" to the output.
        """
        json_ret = super(Image, self).json()

        if full:
            self.get_builds()
            json_ret["builds"] = self.builds
            for build_digest, image_build in self.builds.items():
                json_ret["builds"][build_digest] = image_build.json()

            self.get_clusters()
            json_ret["clusters"] = {}
            for cluster_id, cluster in self.clusters.items():
                json_ret["clusters"][cluster.cluster_id] = cluster.json()

        self.load_meta()
        json_ret["meta"] = {}
        for meta_name, meta in self.metas.items():
            json_ret["meta"][meta_name] = meta.json()

        return json_ret

    def save(self) -> bool:
        """Save an Image and prune trailing slashes from repositories prior."""
        if self.repositories:
            if isinstance(self.repositories, list):
                tmp_repos = []
                for repo in self.repositories:
                    tmp_repos.append(misc.strip_trailing_slash(repo))
                self.repositories = tmp_repos
            elif isinstance(self.repositories, str):
                self.repositories = misc.strip_trailing_slash(self.repositories)

        return super(Image, self).save()

    def delete(self) -> bool:
        """Delete an Image and it's relationships. Including ImageBuilds, ImageClusters Operations
        and Meta.
        """
        # Delete ImageBuilds
        self.get_builds()
        builds_to_delete = []
        for build_digest, build in self.builds.items():
            builds_to_delete.append(build.id)
        ImageBuilds().delete_by_ids(builds_to_delete)

        # Delete Image Clusters
        self.get_clusters()
        clusters_to_delete = []
        for cluser_name, cluster in self.clusters.items():
            clusters_to_delete.append(cluster.id)
        CollectImageClusters().delete_by_ids(clusters_to_delete)

        # Delete Image Operations
        self.get_operations()
        for operation in self.operations:
            operation.delete()

        # Delete Image Scans
        self.get_scans()
        for scan in self.scans:
            scan.delete()

        self.conn.commit()

        super(Image, self).delete()
        return True

# End File: pignus/src/pignus_api/modles/image.py
