"""Migrate DB
Creates all the SQL models needed for Pignus.

"""
import os

from pignus_api.models.option import Option
from pignus_api.models.scanner import Scanner
from pignus_api.models.migration import Migration as MigrationModel

from pignus_api.utils import auth
from pignus_api.utils import glow
from pignus_api.utils import misc_server
# from pignus_api.utils.rbac import Rbac
from pignus_api.version import __version__
from pignus_api.utils import db
from pignus_shared.utils import log


class Migrate:

    def __init__(self):
        self.migration_version = 1
        self.last_migration = None
        self.auth = None
        self.response = {
            "data": {}
        }

    def run(self):
        """Run all initial DB processes. So far that includes
            - Creating the database
            - Creating initial RSA key pair in SSM
            - Rotating an existing RSA key pairs stored in SSM
            - Running all migrations
            - Creating default Options
            - Creating default Scanners
            - Creating default RBAC relationships
            - Creating an admin user if one doesnt exist
        """
        log.info("Running migrations on %s" % glow.db["NAME"])
        self.create_database()
        db_connection = db.connect()
        glow.db["conn"] = db_connection["conn"]
        glow.db["cursor"] = db_connection["cursor"]
        self.setup()
        self.run_sql_migrations()
        self.create_scanners()
        self.create_options()
        # self.create_rbac()
        self.create_user()
        return self.response

    def create_database(self) -> bool:
        """Create the Pignus schema if it does not exist. """
        db_connection = db.connect_no_db(glow.db)
        db.create_mysql_database(db_connection["conn"], db_connection["cursor"])
        return True

    def setup(self) -> bool:
        """After the database has been created, create a connection to it, create the migrations
        table if it doesnt yet exist, and select the last run Migration from that table.
        """
        log.debug("Setting up Migrations")
        MigrationModel().create_table()
        last_migration = MigrationModel()
        last_migration.get_last()
        self.last_migration = last_migration
        return True

    def run_sql_migrations(self) -> bool:
        """Find any migrations files that haven't yet been run according to the
        self.migration_version value.
        """
        log.info("Current migration version: %s" % self.migration_version)
        migrations_files = self._get_migration_files()
        migrations_ran = 0
        for phile in migrations_files:
            migration_number = self._get_migration_number(phile)
            run_migration = self._determine_migration_run()
            if not run_migration:
                continue

            log.info("Applying :%s" % phile)
            migrated = MigrationModel()
            migrated.number = migration_number
            migrated.pignus_version = __version__
            migration_commands = self._break_migrations(phile)

            for migration_command_sql in migration_commands:
                try:
                    # @todo: fix this added dash to the comments.
                    glow.db["cursor"].execute("-- " + migration_command_sql)
                    glow.db["conn"].commit()
                    migrations_ran += 1
                except Exception as e:
                    log.error("Failed to run %s. %s" % (phile, e))
                    migrated.status = False
                    migrated.save()
                    exit(1)
                migrated.status = True
                migrated.save()
        log.info("Ran %s migrations" % migrations_ran)
        return True

    def _break_migrations(self, phile: str) -> list:
        sql = open(phile, 'r').read()
        sql_commands = sql.split("-- ")
        return sql_commands

    def _get_migration_files(self) -> list:
        """Get the migration files, ordered by the way they are intended to be applied."""
        migrations_path = misc_server.get_pignus_migrations_path()
        migrations_files = os.listdir(migrations_path)
        pruned_files = []
        for phile in migrations_files:
            if "migration_" in phile and "_up" in phile:
                pruned_files.append(os.path.join(migrations_path, phile))
        return pruned_files

    def _get_migration_number(self, migration_phile: str) -> int:
        tmp = migration_phile.find("/migration_")
        number = migration_phile[tmp + 11: migration_phile.find("_up.sql")]
        return int(number)

    def _determine_migration_run(self) -> bool:
        """Check the last migration run, and determine if we need to run the migration file in
        question. Returning True if we should run the file.
        """
        if not self.last_migration.number:
            return True
        # If the last migration failed, try to run again.
        if not self.last_migration.number == self.migration_version and self.last_migration.status:
            return True
        if self.last_migration.number >= self.migration_version:
            return False
        return True

    def create_options(self):
        """Create and or update the Options for Pignus. """
        log.info("Setting options")

        # Sync Options
        option_sync_limit = {
            "name": "SYNC_LIMIT",
            "type": "int",
            "default": 10,
        }
        Option().set_default(option_sync_limit)

        # Scan Options
        option_scan_interval = {
            "name": "SCAN_INTERVAL_HOURS",
            "type": "int",
            "default": 72,
        }
        Option().set_default(option_scan_interval)

        option_scan_limit = {
            "name": "SCAN_LIMIT",
            "type": "int",
            "default": 10,
        }
        Option().set_default(option_scan_limit)

        # Cluster Options
        option_cluster_presence_interval = {
            "name": "CLUSTER_PRESENCE_HOURS",
            "type": "int",
            "default": 48,
        }
        Option().set_default(option_cluster_presence_interval)

        option_cluster_supported = {
            "name": "NO_PULL_REPOSITORIES",
            "type": "list",
        }
        Option().set_default(option_cluster_supported)

        option_aws_ecr_create = {
            "name": "AWS_ECR_CREATE",
            "type": "bool",
            "default": True
        }
        Option().set_default(option_aws_ecr_create)

        option_aws_ecr_delete = {
            "name": "AWS_ECR_DELETE",
            "type": "bool",
            "default": True
        }
        Option().set_default(option_aws_ecr_delete)

        option_default_scanner = {
            "name": "DEFAULT_SCANNER",
            "type": "int",
            "default": 1
        }
        Option().set_default(option_default_scanner)

        return True

    def create_scanners(self) -> bool:
        """Create the default scanners. """
        log.info("Creating Scanners")
        scanners = {
            "Trivy": {
                "build_name": "Pignus-Scan-Trivy",
                "parser_name": "parse_trivy.py",
                "enabled": True
            }
        }

        scanners_made = 0
        for scanner_name, scanner_info in scanners.items():
            scanner = Scanner().get_by_name(scanner_name)
            if scanner:
                continue
            scanner = Scanner()
            scanner.name = scanner_name
            scanner.build_name = scanner_info["build_name"]
            scanner.parser_name = scanner_info["parser_name"]
            scanner.enabled = scanner_info["enabled"]
            scanner.save()
            scanners_made += 1
        log.info("Created %s Scanners" % scanners_made)
        return True

    # def create_rbac(self):
    #     log.info("Running RBAC setup/verify")
    #     return Rbac().create_default_rbac_layout()

    def create_user(self):
        log.info("Creating Pignus-Admin user")
        created_user = auth.create_user_and_key("pignus-admin", 1)
        msg = "Created 8 hour Admin Api-Key: %s" % created_user["api_key"]
        self.response["data"]["user"] = msg
        log.info(msg)
        return True

    def create_database_pignus_user(self):
        """Create the Pignus app user. This will have to be done by the Pignus admin user.
        @todo: Finish this, and restrict where the user is allowed to connect from, and not just
        wildcard.
        """
        sql = """
            CREATE USER '%(pignus_app_user)s'@'%' IDENTIFIED BY '%(pignus_app_pass)s';
            GRANT ALL PRIVILEGES ON %(pignus_db_name)s . * TO '%(pignus_app_user)s'@'%'; """
        print(sql)

    # def create_test_data(self) -> bool:
    #     """Creates some basic data for testing."""
    #     fakes = [
    #         {
    #             "name": "cwpp_agent/s1helper",
    #             "tag": "stable-musl",
    #             "repository": "123456789000.dkr.ecr.us-west-2.amazonaws.com",
    #             "digest": "9ba5ec8fe1baa1c9c8be5c9db04e4ca299ce43cdb058e802f15bae3d1b6baf7d"
    #         },
    #         {
    #             "name": "cwpp_agent/s1agent",
    #             "tag": "sp1-21.10.4",
    #             "repository": "1234567890000.dkr.ecr.us-west-2.amazonaws.com",
    #             "digest": "902c6fc64fbea8a34263f94bd44d1d816600b654e2dc41efd4c3aff86b5bbad6"
    #         }
    #     ]
    #     for fake in fakes:
    #         added = image_add.add(fake)
    #         log.info("Added %s" % added["image"])

        return True


if __name__ == "__main__":
    Migrate().run()


# End File: pignus/src/pignus_api/migrate.py
