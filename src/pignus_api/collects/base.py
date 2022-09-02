"""Base Collection

Testing
11/22 methods currently unit tested.

"""
from datetime import timedelta
import math

import arrow

from pignus_api.utils import glow
from pignus_shared.utils import xlate
from pignus_shared.utils import log


class Base:

    def __init__(self, conn=None, cursor=None):
        """Class constructor, set the db connection vars.
        :unit-test: TestBase.test____init__
        """
        self.conn = conn
        if not self.conn:
            self.conn = glow.db["conn"]
        self.cursor = cursor
        if not self.cursor:
            self.cursor = glow.db["cursor"]

        self.table_name = None
        self.collect_model = None

    def get_by_ids(self, model_ids: list) -> list:
        """Get models instances by their ids from the database.
        :unit-test: TestBase.test__get_by_ids
        """
        if not model_ids:
            return []
        model_ids = list(set(model_ids))
        sql_ids = self.int_list_to_sql(model_ids)
        sql = """
            SELECT *
            FROM %(table_name)s
            WHERE id IN (%(ids)s); """ % {
            'table_name': self.table_name,
            'ids': sql_ids,
        }
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        return prestines

    def get_by_ids_keyed(self, model_ids: list, key_field: str = "id") -> dict:
        """Get models instances by their ids from the database, returned as a dict, keyed off of
        the model id or any model attribute supplied by `key_field`.
        :unit-test: TestBase.test__get_by_ids_keyed
        """
        prestines = self.get_by_ids(model_ids)
        prestine_dict = {}
        for prestine in prestines:
            key = getattr(prestine, key_field)
            prestine_dict[key] = prestine
        return prestine_dict

    def get_all_keyed(self, key_field: str = "id") -> dict:
        """Get all models in a dictionary keyed on the id, or supplied `key_field` value."""
        prestines = self.get_all()
        prestines_dict = {}
        for prestine in prestines:
            key = getattr(prestine, key_field)
            prestines_dict[key] = prestine
        return prestines_dict

    def get_like(self, like: dict) -> list:
        """Run a LIKE query searching for a given value.
        like - a dict containing the field and value to search for.
            example:
                {
                    "field": "name",
                    "value": "hello"
                }
        """
        sql = 'SELECT * FROM `%(table)s` WHERE `%(field)s` LIKE "%%'
        vals = {
            "table": self.table_name,
            "field": xlate.sql_safe(like["field"]),
        }
        sql = sql % vals
        sql += like["value"]
        sql += '%";'
        prestines = self.query(sql)
        ret = {
            'objects': prestines,
            'info': {}
        }
        return ret

    def query(self, sql: str) -> list:
        """Run a ready to go SQL statement against the database and get a list of presitine objects
        returned.
        """
        self.cursor.execute(sql)
        raw = self.cursor.fetchall()
        prestines = []
        for raw_item in raw:
            new_object = self.collect_model(self.conn, self.cursor)
            new_object.build_from_list(raw_item)
            prestines.append(new_object)
        return prestines

    def get_paginated(
        self,
        page: int = 1,
        limit: int = 0,
        order_by: dict = {},
        where_and: list = [],
        per_page: int = 20,
    ) -> list:
        """
        Get paginated collection of models.
        :param limit: The limit of results per page.
        :param offset: The offset to return pages from or the "page" to return.
        :param order_by: A dict with the field to us, and the direction of the order.
            example value for order_by:
            {
                'field': 'last_seen',
                'op' : 'DESC'
            }
        :param where_and: a list of dictionaries, containing fields, values and the operator of AND
            statements to concatenate for the query.
            example value for where_and:
            [
                {
                    'field': 'last_seen',
                    'value': last_online,
                    'op': '>='
                }
            ]
        :returns: A list of model objects, hydrated to the default of the base.build_from_list()
        :unit-test: TestBase.test___generate_paginated_sql
        """
        if limit == 0:
            limit = per_page
        sql = self._generate_paginated_sql(page, where_and, order_by, limit)
        self.cursor.execute(sql)
        raw = self.cursor.fetchall()
        prestines = []
        for raw_item in raw:
            new_object = self.collect_model(self.conn, self.cursor)
            new_object.build_from_list(raw_item)
            prestines.append(new_object)
        ret = {
            'objects': prestines,
            'info': self.get_pagination_info(sql, page, limit)
        }
        return ret

    def _generate_paginated_sql(
        self,
        page: int,
        where_and: list,
        order_by: dict,
        limit: int
    ) -> str:
        """Generate the SQL query for the paginated request.
        :unit-test: TestBase:test___generate_paginated_sql()
        """
        sql_vars = {
            'table_name': self.table_name,
            'where': self._pagination_where_and(where_and),
            'order': self._pagination_order(order_by),
            'limit': limit,
            'offset': self._pagination_offset(page, limit),
        }
        sql = """
            SELECT *
            FROM `%(table_name)s`
            %(where)s
            %(order)s
            LIMIT %(limit)s OFFSET %(offset)s;""" % sql_vars
        return sql

    def get_pagination_info(self, sql: str, current_page: int, per_page: int) -> dict:
        """Get pagination details, supplementary info from the get_paginated method. This contains
        details like total_objects, next_page, previous page and other details needed for properly
        drawing pagination info on a GUI.
        """
        total_objects = self._pagination_total(sql)
        last_page = math.ceil(total_objects / per_page)
        if last_page == 0:
            last_page = 1
        ret = {
            "total_objects": total_objects,
            "current_page": current_page,
            "last_page": last_page,
            "per_page": per_page,
        }
        return ret

    def delete_by_ids(self, model_ids: list):
        """Delete a collection of Models by their ID.
        :unit-test: TestBase.test__delete_by_ids
        """
        model_objs = self.get_by_ids(model_ids)
        for model in model_objs:
            model.delete()
        return True

    def _pagination_offset(self, page: int, per_page: int) -> int:
        """Get the offset number for pagination queries.
        :unit-test: TestBase.test___pagination_offset
        """
        if page == 1:
            offset = 0
        else:
            offset = (page * per_page) - per_page
        return offset

    def _pagination_total(self, sql: str) -> int:
        """Get the total number of pages for a pagination query."""
        total_sql = self._edit_pagination_sql_for_info(sql)
        self.cursor.execute(total_sql)
        raw = self.cursor.fetchone()
        if not raw:
            return 0
        return raw[0]

    def _edit_pagination_sql_for_info(self, original_sql: str):
        """Edit the original pagination query to get the total number of results for pagination
        details.
        :unit-test: TestBase.test___edit_pagination_sql_for_info
        """
        sql = original_sql[original_sql.find("FROM"):]
        sql = "%s %s" % ("SELECT COUNT(*)", sql)
        end_sql = sql.find("LIMIT")
        sql = sql[:end_sql].strip() + ";"
        return sql

    def get_total_pages(self, total, per_page) -> int:
        """Get total number of pages based on a total count and per page value.
        :unit-test: TestBase.test__get_total_pages
        """
        total_pages = total / per_page
        return int(round(total_pages, 0))

    def get_count_total(self) -> int:
        """Get count of total model instances in table."""
        sql = """
            SELECT COUNT(*)
            FROM `%s`;
            """ % self.table_name

        self.cursor.execute(sql)
        raw_scans_count = self.cursor.fetchone()
        return raw_scans_count[0]

    def get_all(self) -> list:
        """Get all of a models instances from the database.
        @note: This should NOT be used unless a model has a VERY limited set of results or all
        models are absolutely required for a task.
        """
        sql = """
            SELECT *
            FROM `%s`;
            """ % self.table_name
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        pretties = []
        for raw in raws:
            model = self.collect_model(self.conn, self.cursor)
            model.build_from_list(raw)
            pretties.append(model)
        return pretties

    def get_count_since(self, seconds_since_created: int) -> int:
        """Get count of model instances in table created in last x seconds. """
        then = arrow.utcnow().datetime - timedelta(seconds=seconds_since_created)
        sql = """
            SELECT COUNT(*)
            FROM `%s`
            WHERE created_ts > "%s";
            """ % (self.table_name, then)
        self.cursor.execute(sql)
        raw_scans_count = self.cursor.fetchone()
        return raw_scans_count[0]

    def get_since(self, seconds_since_created: int) -> list:
        """Get model instances created in last x seconds. """
        then = arrow.utcnow().datetime - timedelta(seconds=seconds_since_created)
        sql = """
            SELECT *
            FROM `%s`
            WHERE created_ts > "%s"
            ORDER BY id DESC;
            """ % (self.table_name, then)
        self.cursor.execute(sql)
        raw = self.cursor.fetchall()
        prestines = []
        for raw_item in raw:
            new_object = self.collect_model(self.conn, self.cursor)
            new_object.build_from_list(raw_item)
            prestines.append(new_object)
        return prestines

    def get_last(self, num_units: int = 10) -> list:
        """Get last `num_units` created models descending. """
        sql = """
            SELECT *
            FROM %s
            ORDER BY created_ts DESC
            LIMIT %s;""" % (self.table_name, num_units)
        self.cursor.execute(sql)
        raw = self.cursor.fetchall()
        prestines = self.build_from_lists(raw)
        return prestines

    def build_from_lists(self, raws: list) -> list:
        """Creates list of hydrated collection objects. """
        prestines = []
        for raw_item in raws:
            new_object = self.collect_model(self.conn, self.cursor)
            new_object.build_from_list(raw_item)
            prestines.append(new_object)
        return prestines

    def int_list_to_sql(self, item_list: list) -> str:
        """Transform a list of ints to a sql safe comma separated string. """
        sql_ids = ""
        for i in item_list:
            sql_ids += "%s," % i
        sql_ids = sql_ids[:-1]
        return sql_ids

    def _pagination_where_and(self, where_and: list) -> str:
        """Create the where clause for pagination when where and clauses are supplied.
        Note: We append multiple statements with an AND in the sql statement.
        :unit-test: TestBase().test___pagination_where_and()
        """
        where = False
        where_and_sql = ""
        for where_a in where_and:
            if not where_a["field"]:
                log.warning("Collections - Invalid where option: %s" % where_a)
                continue
            where = True
            op = "="
            if 'op' in where_a:
                op = where_a['op']
            if isinstance(where_a["value"], str):
                where_a["value"] = '"%s"' % xlate.sql_safe(where_a["value"])
            where_and_sql += '`%s` %s %s AND ' % (
                xlate.sql_safe(where_a['field']),
                op,
                where_a['value'])
            where_and_sql = where_and_sql.strip()

        if where:
            where_and_sql = "WHERE " + where_and_sql
            where_and_sql = where_and_sql[:-4]

        return where_and_sql

    def _pagination_order(self, order: dict) -> str:
        """Create the order clause for pagination using user supplied arguments or defaulting to
        created_desc DESC.
        :unit-test: TestBase.test___pagination_order
        """
        order_sql = "ORDER BY `created_ts` DESC"
        if not order:
            return order_sql
        order_field = order['field']
        order_op = order['op']
        order_sql = 'ORDER BY `%s` %s' % (order_field, order_op)
        return order_sql

    def _get_previous_page(self, page: int) -> int:
        """Get the previous page, or first page if below 1.
        :unit-test: TestBase.test___get_previous_page
        """
        previous = page - 1
        return previous

    def _get_next_page(self, page: int, last_page: int) -> int:
        """Get the next page.
        :unit-test: TestBase.test___get_next_page
        """
        if page == last_page:
            return None
        next_page = page + 1
        return next_page


# End File: pignus/src/pignus_api/collections/base.py
