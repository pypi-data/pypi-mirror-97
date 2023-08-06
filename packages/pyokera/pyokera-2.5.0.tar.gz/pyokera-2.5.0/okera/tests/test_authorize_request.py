# Copyright 2019 Okera Inc. All Rights Reserved.

# pylint: disable=too-many-lines
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-lines
#
# Tests for AuthorizeQuery() API
#

import json
import os
import unittest

from okera._thrift_api import TAccessPermissionLevel
from okera._thrift_api import TAuthorizeQueryParams
from okera._thrift_api import TAuthorizeQueryClient
from okera._thrift_api import TErrorCode
from okera._thrift_api import TRecordServiceException
from okera._thrift_api import TRequestContext

from okera.tests import pycerebro_test_common as common

TEST_USER = 'testuser'
SKIP_LEVELS = ["smoke", "dev", "all", "checkin"]

class AuthorizeQueryTest(common.TestBase):
    def authorize_query_audit_only(self, conn, query, user=None, db=None, dataset=None):
        request = TAuthorizeQueryParams()
        request.sql = query
        request.requesting_user = user
        request.use_session_local_tables = False
        request.audit_only = True
        if db:
            request.db = [db]
        if dataset:
            request.dataset = dataset
        result = conn.service.client.AuthorizeQuery(request)
        self.assertTrue(result is not None)
        self.assertTrue(result.table is None)
        return result

    def authorize_query(self, conn, query, user=None, use_tmp_tables=False, client=None,
                        return_full_result=False, cte=False, token=None):
        request = TAuthorizeQueryParams()
        request.sql = query
        request.requesting_user = user
        request.use_session_local_tables = use_tmp_tables
        request.client = client
        request.cte_rewrite = cte
        if token:
            request.ctx = TRequestContext()
            request.ctx.auth_token = token

        result = conn.service.client.AuthorizeQuery(request)
        if client == TAuthorizeQueryClient.TEST_ACK:
            return ''
        if return_full_result:
            return ' '.join(result.result_sql.split())
        self.assertTrue(result.table is None)
        if result.requires_worker:
            return None
        self.assertTrue(result.result_schema is not None or cte)
        return ' '.join(result.result_sql.split())

    # Returns * if the user can directly access the table, the rewritten query if
    # that's required or None if the user must go to ODAS.
    def authorize_table(self, conn, db, table, user=None, use_tmp_tables=False):
        request = TAuthorizeQueryParams()
        request.db = [db]
        request.dataset = table
        request.requesting_user = user
        request.use_session_local_tables = use_tmp_tables
        result = conn.service.client.AuthorizeQuery(request)
        self.assertTrue(result.result_sql is not None or result.table is not None)
        if result.full_access:
            # Full access should return full table metadata
            self.assertTrue(result.table is not None)
            return '*'
        if result.requires_worker:
            return None
        self.assertTrue(result.result_schema is not None)
        return ' '.join(result.result_sql.split())

    @staticmethod
    def cache_key(conn, query, user=None):
        request = TAuthorizeQueryParams()
        request.sql = query
        request.requesting_user = user
        request.client = TAuthorizeQueryClient.OKERA_CACHE_KEY
        result = conn.service.client.AuthorizeQuery(request)
        if result.result_sql is None:
            return None
        return ' '.join(result.result_sql.split())

    @staticmethod
    def cte_rewrite(conn, query, user=None,
                    generate_plan=False, client=None):
        request = TAuthorizeQueryParams()
        request.sql = query
        request.requesting_user = user
        request.cte_rewrite = True
        request.plan_request = generate_plan
        request.client = client
        result = conn.service.client.AuthorizeQuery(request)
        if result.result_sql is None:
            return None, None
        result_sql = ' '.join(result.result_sql.split())
        return result_sql, result.plan, result.referenced_tables

    @staticmethod
    def get_filter(conn, db, tbl, user, level=None, records=None, return_records=False):
        request = TAuthorizeQueryParams()
        request.db = [db]
        request.dataset = tbl
        request.requesting_user = user
        request.privilege_level = level
        request.records = records
        request.client = TAuthorizeQueryClient.REST_API
        request.return_records = return_records
        return conn.service.client.AuthorizeQuery(request)

    def test_sql(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self.assertEqual("SELECT 1", self.authorize_query(conn, "select 1"))
            self.assertEqual(
                "SELECT 1", self.authorize_query(conn, "select 1", None, True))
            self.assertEqual(
                "SELECT 1", self.authorize_query(conn, "select 1",
                                                 client=TAuthorizeQueryClient.IMPALA,
                                                 cte=True))

            self.assertEqual(
                "SELECT 'okera' as user",
                self.authorize_query(conn, "select * from okera_sample.whoami"))
            self.assertEqual(
                "SELECT 'okera' as user",
                self.authorize_query(
                    conn, "select * from okera_sample.whoami", None, True))
            self.assertEqual(
                "SELECT 'okera' as `user`",
                self.authorize_query(
                    conn, "select * from okera_sample.whoami",
                    client=TAuthorizeQueryClient.IMPALA, cte=True))

            self.assertEqual(
                "SELECT 'okera' as user",
                self.authorize_query(conn, "select user from okera_sample.whoami"))
            self.assertEqual(
                "SELECT 'okera' as user",
                self.authorize_query(
                    conn, "select user from okera_sample.whoami", None, True))
            self.assertEqual(
                "SELECT 'okera' as `user`",
                self.authorize_query(
                    conn, "select user from okera_sample.whoami",
                    client=TAuthorizeQueryClient.IMPALA, cte=True))

            # Rewrite does not make sense for this table as it is an okera specific
            # construct.
            self.assertEqual(
                None,
                self.authorize_query(conn, "select * from okera_sample.sample"))
            self.assertEqual(
                None,
                self.authorize_query(
                    conn, "select * from okera_sample.sample", None, True))
            # FIXME
            #self.assertEqual(
            #    None,
            #    self.authorize_query(
            #        conn, "select * from okera_sample.sample", None, True,
            #        client=TAuthorizeQueryClient.IMPALA, cte=True))

            self.assertEqual(
                "SELECT int_col FROM rs.alltypes_s3",
                self.authorize_query(conn, "select int_col from rs.alltypes_s3"))
            self.assertEqual(
                "SELECT int_col FROM rs.alltypes_s3_tmp",
                self.authorize_query(
                    conn, "select int_col from rs.alltypes_s3", None, True))
            self.assertEqual(
                "select int_col from `rs`.`alltypes_s3`",
                self.authorize_query(conn, "select int_col from rs.alltypes_s3",
                                     client=TAuthorizeQueryClient.IMPALA, cte=True))

            self.assertEqual(
                "SELECT bool_col, tinyint_col, smallint_col, int_col, bigint_col, " +\
                "float_col, double_col, string_col, varchar_col, char_col, " +\
                "timestamp_col, decimal_col FROM all_table_types.s3",
                self.authorize_query(conn, "select * from all_table_types.s3"))
            self.assertEqual(
                "SELECT bool_col, tinyint_col, smallint_col, int_col, bigint_col, " +\
                "float_col, double_col, string_col, varchar_col, char_col, " +\
                "timestamp_col, decimal_col FROM all_table_types.s3_tmp",
                self.authorize_query(conn, "select * from all_table_types.s3",
                                     None, True))
            self.assertEqual(
                "select * from `all_table_types`.`s3`",
                self.authorize_query(conn, "select * from all_table_types.s3",
                                     client=TAuthorizeQueryClient.IMPALA, cte=True))

            # Now run as testuser
            self.assertEqual(
                "SELECT 'testuser' as user",
                self.authorize_query(
                    conn, "select * from okera_sample.whoami", TEST_USER))
            self.assertEqual(
                "SELECT 'testuser' as user",
                self.authorize_query(
                    conn, "select * from okera_sample.whoami", TEST_USER, True))
            self.assertEqual(
                "SELECT 'testuser' as `user`",
                self.authorize_query(
                    conn, "select * from okera_sample.whoami", TEST_USER,
                    client=TAuthorizeQueryClient.IMPALA, cte=True))

            self.assertEqual(
                "SELECT int_col FROM rs.alltypes_s3",
                self.authorize_query(
                    conn, "select int_col from rs.alltypes_s3", TEST_USER))
            self.assertEqual(
                "SELECT int_col FROM rs.alltypes_s3_tmp",
                self.authorize_query(
                    conn, "select int_col from rs.alltypes_s3", TEST_USER, True))
            self.assertEqual(
                "WITH okera_rewrite_rs__alltypes_s3 AS (" + \
                "SELECT `int_col`, `float_col`, `string_col` " + \
                "FROM `rs`.`alltypes_s3`) " + \
                "select int_col from okera_rewrite_rs__alltypes_s3",
                self.authorize_query(
                    conn, "select int_col from rs.alltypes_s3", TEST_USER,
                    client=TAuthorizeQueryClient.IMPALA, cte=True))

            # * should expand to a subset of the columns
            self.assertEqual(
                "SELECT int_col, float_col, string_col FROM rs.alltypes_s3",
                self.authorize_query(conn, "select * from rs.alltypes_s3", TEST_USER))
            self.assertEqual(
                "SELECT int_col, float_col, string_col FROM rs.alltypes_s3_tmp",
                self.authorize_query(
                    conn, "select * from rs.alltypes_s3", TEST_USER, True))
            self.assertEqual(
                "WITH okera_rewrite_rs__alltypes_s3 AS " + \
                "(SELECT `int_col`, `float_col`, `string_col` " + \
                "FROM `rs`.`alltypes_s3`) select * from okera_rewrite_rs__alltypes_s3",
                self.authorize_query(conn, "select * from rs.alltypes_s3", TEST_USER,
                                     client=TAuthorizeQueryClient.IMPALA, cte=True))

            # Selecting a column wit no access should fail
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                self.authorize_query(
                    conn, "select bool_col from rs.alltypes_s3", TEST_USER)
            self.assertTrue('does not have privileges' in str(ex_ctx.exception))
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                self.authorize_query(
                    conn, "select bool_col from rs.alltypes_s3", TEST_USER, True)
            self.assertTrue('does not have privileges' in str(ex_ctx.exception))
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                self.authorize_query(
                    conn, "select bool_col from rs.alltypes_s3", TEST_USER,
                    client=TAuthorizeQueryClient.IMPALA, cte=True)
            self.assertTrue('does not have privileges' in str(ex_ctx.exception))

    def test_implicit_string_cast(self):
        db = "implicit_string_test_db"
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self._recreate_test_db(conn, db)
            self._recreate_test_role(conn, 'implicit_cast_role', ['implicit_cast_user'])
            conn.execute_ddl("CREATE ATTRIBUTE IF NOT EXISTS test.string_col")
            conn.execute_ddl("""CREATE TABLE %s.t(
                s1 STRING ATTRIBUTE test.string_col,
                s2 VARCHAR(10) ATTRIBUTE test.string_col,
                s3 CHAR(5) ATTRIBUTE test.string_col)""" % db)
            conn.execute_ddl(
                """GRANT SELECT ON DATABASE %s TRANSFORM test.string_col
                WITH sha2() TO ROLE %s""" % (db, 'implicit_cast_role'))
            self.assertEqual(
                "SELECT CAST(sha2(s1) AS STRING) as s1, " +
                "CAST(sha2(s2) AS VARCHAR(10)) as s2, " +
                "CAST(sha2(s3) AS CHAR(5)) as s3 FROM implicit_string_test_db.t",
                self.authorize_query(conn, "SELECT * FROM %s.t" % db,
                                     'implicit_cast_user', False,
                                     return_full_result=True))
            self.assertEqual(
                "SELECT s1, s2, s3 FROM implicit_string_test_db.t",
                self.authorize_query(conn, "SELECT * FROM %s.t" % db,
                                     'okera', False, return_full_result=True))

    def test_audit_only(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self.authorize_query_audit_only(conn, 'select * from bar1')
            self.authorize_query_audit_only(conn, 'select * from bar2', user='user1')
            self.authorize_query_audit_only(
                conn, 'select * from bar3',
                user='user2', db='xyz', dataset='abc.def')
            self.authorize_query_audit_only(
                conn, 'select * from bar4', user='user3',
                db='xyz,abc', dataset='abc.def,foo.bar')

    def test_table(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self.assertEqual(None, self.authorize_table(conn, "okera_sample", "sample"))
            self.assertEqual(
                None, self.authorize_table(conn, "okera_sample", "sample", None, True))

            self.assertEqual(
                None, self.authorize_table(conn, "okera_sample", "sample", TEST_USER))
            self.assertEqual(
                None,
                self.authorize_table(conn, "okera_sample", "sample", TEST_USER, True))

            self.assertEqual('*', self.authorize_table(conn, "rs", "alltypes_s3"))
            self.assertEqual(
                '*',
                self.authorize_table(conn, "rs", "alltypes_s3", None, True))
            self.assertEqual(
                "SELECT int_col, float_col, string_col FROM rs.alltypes_s3",
                self.authorize_table(conn, "rs", "alltypes_s3", TEST_USER))
            self.assertEqual(
                "SELECT int_col, float_col, string_col FROM rs.alltypes_s3_tmp",
                self.authorize_table(conn, "rs", "alltypes_s3", TEST_USER, True))

            # This is a view, we want to "flatten"
            self.assertEqual(
                "SELECT 'okera' as user",
                self.authorize_table(conn, "okera_sample", "whoami"))
            self.assertEqual(
                "SELECT 'okera' as user",
                self.authorize_table(conn, "okera_sample", "whoami", None, True))
            self.assertEqual(
                "SELECT 'testuser' as user",
                self.authorize_table(conn, "okera_sample", "whoami", TEST_USER))
            self.assertEqual(
                "SELECT 'testuser' as user",
                self.authorize_table(conn, "okera_sample", "whoami", TEST_USER, True))

            # Do some more interesting view
            self.assertEqual(
                "SELECT bool_col, tinyint_col, smallint_col, int_col, bigint_col, " +
                "float_col, double_col, string_col, varchar_col, char_col, " +
                "timestamp_col, decimal_col FROM abac_db.all_types",
                self.authorize_table(conn, "abac_db", "all_types_view", TEST_USER, True))

            self.assertEqual(
                "SELECT user, mask_ccn(ccn) FROM rs.ccn",
                self.authorize_table(conn, "rs", "ccn_masked", TEST_USER, True))
            self.assertEqual(
                "SELECT int_col, float_col, string_col FROM rs.alltypes_s3_tmp",
                self.authorize_table(conn, "rs", "alltypes_s3", TEST_USER, True))

            # No access
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                self.authorize_table(conn, "nytaxi", "parquet_data", TEST_USER)
            self.assertTrue('does not have permissions' in str(ex_ctx.exception))

            with self.assertRaises(TRecordServiceException) as ex_ctx:
                self.authorize_table(conn, "nytaxi", "parquet_data", TEST_USER, True)
            self.assertTrue('does not have permissions' in str(ex_ctx.exception))

    def test_view(self):
        ctx = common.get_test_context()
        db = 'authorize_view_db'
        role = "authorize_view_test_role"
        testuser = "authorize_view_testuser"

        with common.get_planner(ctx) as conn:
            conn.execute_ddl("DROP ROLE IF EXISTS " + role)
            conn.execute_ddl("CREATE ROLE " + role)
            conn.execute_ddl("GRANT ROLE " + role + " TO GROUP " + testuser)
            conn.execute_ddl("DROP DATABASE IF EXISTS %s CASCADE" % db)
            conn.execute_ddl("CREATE DATABASE %s" % db)

            # Test complex type view
            self.assertEqual(
                "SELECT id, s1.f1, s1.f2 FROM authdb.struct_t WHERE s1.f2 > 1",
                self.authorize_table(conn, 'authdb', 'struct_t_where_clause_view',
                                     None, True))

            # Join with no aliases
            conn.execute_ddl(("create view %s.v as " +
                              "select a.*,b.* from okera_sample.sample a " +
                              "join okera_sample.users b on a.record = b.ccn") % db)
            self.assertEqual(
                "SELECT a.record as record, b.uid as uid, b.dob as dob, " +
                "b.gender as gender, b.ccn as ccn FROM okera_sample.sample a " +
                "INNER JOIN okera_sample.users b ON a.record = b.ccn",
                self.authorize_table(conn, db, "v", None, True))

            # Join with alias on one side
            conn.execute_ddl("DROP VIEW %s.v" % db)
            conn.execute_ddl(("create view %s.v as " +
                              "select a.record as r, b.* from okera_sample.sample a " +
                              "join okera_sample.sample b on a.record = b.record") % db)
            self.assertEqual(
                "SELECT a.record as r, b.record as record " +
                "FROM okera_sample.sample a INNER JOIN okera_sample.sample b " +
                "ON a.record = b.record",
                self.authorize_table(conn, db, "v", None, True))

            # Join with alias on both sides
            conn.execute_ddl("DROP VIEW %s.v" % db)
            conn.execute_ddl(("create view %s.v as " +
                              "select a.record as r, b.record as r2 " +
                              "from okera_sample.sample a " +
                              "join okera_sample.sample b on a.record = b.record") % db)
            self.assertEqual(
                "SELECT a.record as r, b.record as r2 " +
                "FROM okera_sample.sample a INNER JOIN okera_sample.sample b " +
                "ON a.record = b.record",
                self.authorize_table(conn, db, "v", None, True))

            conn.execute_ddl("DROP VIEW %s.v" % db)
            conn.execute_ddl(("create view %s.v as " +
                              "select * from okera_sample.sample " +
                              "where record is not null") % db)
            self.assertEqual(
                "SELECT record FROM okera_sample.sample WHERE record IS NOT NULL",
                self.authorize_table(conn, db, "v", None, True))

            conn.execute_ddl("DROP VIEW %s.v" % db)
            conn.execute_ddl(("create view %s.v as " +
                              "select * from okera_sample.sample " +
                              "where record > 'A' and record < 'z'") % db)
            self.assertEqual(
                "SELECT record FROM okera_sample.sample WHERE (record > 'A') " +
                "AND (record < 'z')",
                self.authorize_table(conn, db, "v", None, True))

            conn.execute_ddl("DROP VIEW %s.v" % db)
            conn.execute_ddl(("create view %s.v as " +
                              "select record as r from okera_sample.sample " +
                              "where record > 'A' and record < 'z'") % db)
            self.assertEqual(
                "SELECT record as r FROM okera_sample.sample WHERE (record > 'A') " +
                "AND (record < 'z')",
                self.authorize_table(conn, db, "v", None, True))

            # View with join
            conn.execute_ddl("DROP VIEW %s.v" % db)
            conn.execute_ddl(("create view %s.v as " +
                              "select record as r from okera_sample.sample a " +
                              "join okera_sample.users b on a.record = b.ccn") % db)
            self.assertEqual(
                "SELECT record as r FROM okera_sample.sample a INNER JOIN " +
                "okera_sample.users b ON a.record = b.ccn",
                self.authorize_table(conn, db, "v", None, True))

            conn.execute_ddl("DROP VIEW %s.v" % db)
            conn.execute_ddl(("create view %s.v as " +
                              "select a.record from okera_sample.sample a " +
                              "join okera_sample.users b on a.record = b.ccn") % db)
            self.assertEqual(
                "SELECT a.record as record FROM okera_sample.sample a INNER JOIN " +
                "okera_sample.users b ON a.record = b.ccn",
                self.authorize_table(conn, db, "v", None, True))

            # Some existing views
            self.assertEqual(
                "SELECT uid, dob, gender, mask_ccn(ccn) FROM okera_sample.users",
                self.authorize_table(conn, "okera_sample", "users_ccn_masked",
                                     None, True))
            self.assertEqual(
                "SELECT name, phone, email, userid, lastlogin, creditcardnumber, " + \
                "loc, ipv4_address, ipv6_address FROM abac_db.user_account_data",
                self.authorize_table(conn, "abac_db", "user_account_data_view",
                                     None, True))

            self.assertEqual(
                "SELECT n_nationkey, n_name FROM tpch.nation WHERE n_nationkey < 5",
                self.authorize_table(conn, "rs", "nation_projection", None, True))

            # Try as testuer, should compose
            conn.execute_ddl(
                "GRANT SELECT ON TABLE rs.nation_projection WHERE %s TO ROLE %s" %\
                ("n_name > 'M'", role))
            self.assertEqual(
                "SELECT n_nationkey, n_name FROM tpch.nation WHERE (n_nationkey < 5) " +\
                "AND (n_name > 'M')",
                self.authorize_table(conn, "rs", "nation_projection", testuser, True))

            self.assertEqual(
                "SELECT t1.n_nationkey as n_nationkey, t1.n_name as n_name, " + \
                "t1.n_regionkey as n_regionkey, t1.n_comment as n_comment, " + \
                "t2.n_nationkey as n_nationkey2 FROM tpch.nation t1 " +\
                "INNER JOIN tpch.nation t2 ON t1.n_nationkey = t2.n_nationkey",
                self.authorize_table(conn, "tpch", "nation_join", None, True))

            # FIXME: broken, missing group by
            #self.assertEqual(
            #    "SELECT n_nationkey, count(*) as _c1 FROM tpch.nation",
            #    self.authorize_table(conn, "tpch", "nation_agg", None, True))

    def test_table_subquery(self):
        ctx = common.get_test_context()
        role = "subquery_test_role"
        testuser = "subquery_testuser"
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl("DROP ROLE IF EXISTS " + role)
            conn.execute_ddl("CREATE ROLE " + role)
            conn.execute_ddl("GRANT ROLE " + role + " TO GROUP " + testuser)

            def grant(filter):
                conn.execute_ddl(
                    "GRANT SELECT ON TABLE rs.alltypes_s3 WHERE %s TO ROLE %s" %\
                    (filter, role))
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                grant("int_col in (SELECT bigint_col FROM rs.alltypes_s3)")
                conn.scan_as_json("rs.alltypes_s3", requesting_user=testuser)
            self.assertTrue('Policy filter contains a subquery' in str(ex_ctx.exception))

    def test_tmp_views(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            # Get the full schema as okera
            full_schema = conn.list_datasets("rs", name="alltypes_s3")[0].schema
            self.assertEqual(12, len(self._visible_cols(full_schema.cols)))

            # Get the schemas a testuser, this should be a subset
            ctx.enable_token_auth(token_str=TEST_USER)
            partial_schema = conn.list_datasets("rs", name="alltypes_s3")[0].schema
            self.assertEqual(3, len(self._visible_cols(partial_schema.cols)))

            # Reading the tmp version should have. It doesn't exist yet.
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                conn.scan_as_json("rs.alltypes_s3_tmp")
            self.assertTrue('does not have privileges' in str(ex_ctx.exception))

            # Authorize this query, this will temporarily add the temp table and it
            # will have the full schema.
            self.authorize_table(conn, "rs", "alltypes_s3", TEST_USER, True)
            result = conn.list_datasets("rs", name="alltypes_s3_tmp")[0]

            # Note: this returns all the columns, which the user is not normally
            # able to see.
            self.assertEqual(12, len(self._visible_cols(result.schema.cols)))
            self.assertEqual(full_schema, result.schema)

            self.assertEqual("rs", result.db[0])
            self.assertEqual("alltypes_s3_tmp", result.name)

            self.assertEqual(
                '*',
                self.authorize_table(conn, "rs", "alltypes_s3_tmp", TEST_USER, True))

            # Do it again
            self.assertEqual(
                '*',
                self.authorize_table(conn, "rs", "alltypes_s3_tmp", TEST_USER, True))

        # Recreate the connection, the temp tables are gone
        with common.get_planner(ctx) as conn:
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                self.authorize_table(conn, "rs", "alltypes_s3_tmp", TEST_USER, True)
            self.assertTrue('Table does not exist' in str(ex_ctx.exception),
                            msg=str(ex_ctx.exception))

    def test_auth_token_header(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                self.assertEqual(
                    "SELECT 'okera' as `user`",
                    self.authorize_query(
                        conn, "select * from okera_sample.whoami", token='bad-token'))
            self.assertTrue('Invalid token' in str(ex_ctx.exception),
                            msg=str(ex_ctx.exception))

    def test_filter_clause(self):
        role = "filter_test_role"
        testuser = "filter_testuser"
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl("DROP ROLE IF EXISTS " + role)
            conn.execute_ddl("CREATE ROLE " + role)
            conn.execute_ddl("GRANT ROLE " + role + " TO GROUP " + testuser)

            def grant(filter):
                conn.execute_ddl(
                    "GRANT SELECT ON TABLE rs.alltypes WHERE %s TO ROLE %s" %\
                    (filter, role))

            def revoke(filter):
                conn.execute_ddl(
                    "REVOKE SELECT ON TABLE rs.alltypes WHERE %s FROM ROLE %s" %\
                    (filter, role))

            grant('int_col = 1')
            filter = self.get_filter(conn, 'rs', 'alltypes', testuser)
            self.assertEqual('int_col = 1', filter.filter)
            self.assertEqual(['1'], filter.filtered_values['int_col'])

            # Two row filters, bad
            grant('int_col = 2')
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                self.get_filter(conn, 'rs', 'alltypes', testuser)
            self.assertTrue("Access to 'rs.alltypes' is protected by multiple filters" \
                in str(ex_ctx.exception))

            revoke('int_col = 1')
            revoke('int_col = 2')

            # Try some other filters
            grant('int_col = bool_col')
            filter = self.get_filter(conn, 'rs', 'alltypes', testuser)
            self.assertEqual('int_col = bool_col', filter.filter)
            self.assertEqual(None, filter.filtered_values)
            revoke('int_col = bool_col')

            grant('int_col = 1 or int_col = 2')
            filter = self.get_filter(conn, 'rs', 'alltypes', testuser)
            self.assertEqual('int_col IN (1, 2)', filter.filter)
            self.assertEqual(['1', '2'], filter.filtered_values['int_col'])
            revoke('int_col = 1 or int_col = 2')

            grant('int_col = 1 and int_col = 2')
            filter = self.get_filter(conn, 'rs', 'alltypes', testuser)
            self.assertEqual('FALSE', filter.filter)
            self.assertEqual(None, filter.filtered_values)
            revoke('int_col = 1 and int_col = 2')

            grant('int_col in(1, 2, 3)')
            filter = self.get_filter(conn, 'rs', 'alltypes', testuser)
            self.assertEqual('int_col IN (1, 2, 3)', filter.filter)
            self.assertEqual(['1', '2', '3'], filter.filtered_values['int_col'])
            revoke('int_col in(1, 2, 3)')

            grant('int_col in(1, 2, 3) or int_col = 4')
            filter = self.get_filter(conn, 'rs', 'alltypes', testuser)
            self.assertEqual('int_col IN (1, 2, 3, 4)', filter.filter)
            self.assertEqual(['1', '2', '3', '4'], filter.filtered_values['int_col'])
            revoke('int_col in(1, 2, 3) or int_col = 4')

            grant('int_col in(1, 2, 3) or float_col = 4')
            filter = self.get_filter(conn, 'rs', 'alltypes', testuser)
            self.assertEqual('int_col IN (1, 2, 3) OR float_col = 4', filter.filter)
            self.assertEqual(None, filter.filtered_values)
            revoke('int_col in(1, 2, 3) or float_col = 4')

    def test_nea_poc(self):
        admin = "nea_test_admin"
        full_reader = "nea_test_full_reader"
        partial_reader = "nea_test_reader"
        insert_reader = "nea_test_insert_reader"
        inserter = "nea_test_inserter"
        updater = "nea_test_updater"

        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            # Set up roles and groups
            conn.execute_ddl("DROP ROLE IF EXISTS %s_role" % admin)
            conn.execute_ddl("CREATE ROLE %s_role" % admin)
            conn.execute_ddl("GRANT ROLE %s_role TO GROUP %s" % (admin, admin))
            conn.execute_ddl("DROP ROLE IF EXISTS %s_role" % full_reader)
            conn.execute_ddl("CREATE ROLE %s_role" % full_reader)
            conn.execute_ddl("GRANT ROLE %s_role TO GROUP %s" % \
                (full_reader, full_reader))
            conn.execute_ddl("DROP ROLE IF EXISTS %s_role" % partial_reader)
            conn.execute_ddl("CREATE ROLE %s_role" % partial_reader)
            conn.execute_ddl("GRANT ROLE %s_role TO GROUP %s" % \
                (partial_reader, partial_reader))
            conn.execute_ddl("DROP ROLE IF EXISTS %s_role" % insert_reader)
            conn.execute_ddl("CREATE ROLE %s_role" % insert_reader)
            conn.execute_ddl("GRANT ROLE %s_role TO GROUP %s" % \
                (insert_reader, insert_reader))
            conn.execute_ddl("DROP ROLE IF EXISTS %s_role" % inserter)
            conn.execute_ddl("CREATE ROLE %s_role" % inserter)
            conn.execute_ddl("GRANT ROLE %s_role TO GROUP %s" % (inserter, inserter))
            conn.execute_ddl("DROP ROLE IF EXISTS %s_role" % updater)
            conn.execute_ddl("CREATE ROLE %s_role" % updater)
            conn.execute_ddl("GRANT ROLE %s_role TO GROUP %s" % (updater, updater))

            tbl = 'okera_system.audit_logs'
            conn.execute_ddl(
                "GRANT ALL ON TABLE %s TO ROLE %s_role" % (tbl, admin))
            conn.execute_ddl(
                "GRANT SELECT ON TABLE %s TO ROLE %s_role" % (tbl, full_reader))
            conn.execute_ddl(
                "GRANT SELECT ON TABLE %s WHERE v1 TO ROLE %s_role" % \
                (tbl, partial_reader))
            conn.execute_ddl(
                "GRANT SELECT ON TABLE %s WHERE v1 TO ROLE %s_role" % \
                (tbl, insert_reader))
            conn.execute_ddl(
                "GRANT INSERT ON TABLE %s WHERE v1 TO ROLE %s_role" % \
                (tbl, insert_reader))
            conn.execute_ddl(
                "GRANT INSERT ON TABLE %s WHERE v2 TO ROLE %s_role" % \
                (tbl, inserter))
            conn.execute_ddl(
                "GRANT UPDATE ON TABLE %s WHERE v3 TO ROLE %s_role" % \
                (tbl, updater))
            conn.execute_ddl(
                "GRANT DELETE ON TABLE %s WHERE v4 TO ROLE %s_role" % \
                (tbl, updater))

            def get(user, level):
                r = self.get_filter(conn, 'okera_system', 'audit_logs', user, level)
                return r.filter

            def fail(user, level):
                with self.assertRaises(TRecordServiceException) as ex_ctx:
                    get(user, level)
                    self.fail()
                self.assertTrue("does not have permissions" in str(ex_ctx.exception))

            #
            # SELECT
            #
            self.assertEqual(None, get(admin, TAccessPermissionLevel.SELECT))
            self.assertEqual(None, get(full_reader, TAccessPermissionLevel.SELECT))
            self.assertEqual("v1", get(partial_reader, TAccessPermissionLevel.SELECT))
            self.assertEqual("v1", get(insert_reader, TAccessPermissionLevel.SELECT))
            fail(inserter, TAccessPermissionLevel.SELECT)
            fail(updater, TAccessPermissionLevel.SELECT)

            #
            # INSERT
            #
            self.assertEqual(None, get(admin, TAccessPermissionLevel.INSERT))
            fail(full_reader, TAccessPermissionLevel.INSERT)
            fail(partial_reader, TAccessPermissionLevel.INSERT)
            self.assertEqual("v1", get(insert_reader, TAccessPermissionLevel.INSERT))
            self.assertEqual("v2", get(inserter, TAccessPermissionLevel.INSERT))
            fail(updater, TAccessPermissionLevel.INSERT)

            #
            # UPDATE
            #
            self.assertEqual(None, get(admin, TAccessPermissionLevel.UPDATE))
            fail(full_reader, TAccessPermissionLevel.UPDATE)
            fail(partial_reader, TAccessPermissionLevel.UPDATE)
            fail(insert_reader, TAccessPermissionLevel.UPDATE)
            fail(inserter, TAccessPermissionLevel.UPDATE)
            self.assertEqual("v3", get(updater, TAccessPermissionLevel.UPDATE))

            #
            # DELETE
            #
            self.assertEqual(None, get(admin, TAccessPermissionLevel.DELETE))
            fail(full_reader, TAccessPermissionLevel.DELETE)
            fail(partial_reader, TAccessPermissionLevel.DELETE)
            fail(insert_reader, TAccessPermissionLevel.DELETE)
            fail(inserter, TAccessPermissionLevel.DELETE)
            self.assertEqual("v4", get(updater, TAccessPermissionLevel.DELETE))

    def test_measure_speed_of_light(self):
        """ This is not a real test and just verifies the ack in the planner FE
            to measure connection/plumbing related latency.
            On a typical dev setup:

            Iterations 2000
            Mean 0.4550884962081909 ms
            50%: 0.3914833068847656 ms
            90%: 0.5025863647460938 ms
            95%: 0.6008148193359375 ms
            99%: 0.7925033569335938 ms
            99.5%: 0.8821487426757812 ms

            TODO: move this to a proper benchmarking harness.
        """
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            def get():
                self.authorize_query(conn, "select 1",
                                     client=TAuthorizeQueryClient.TEST_ACK)
            common.measure_latency(2000, get)

    def test_measure_get_filter_nea(self):
        """ Measure time to return a filter.
            On a typical dev setup:

            Iterations 1000
            Mean 5.3225297927856445 ms
            50%: 5.099773406982422 ms
            90%: 5.945682525634766 ms
            95%: 6.330013275146484 ms
            99%: 8.286476135253906 ms
            99.5%: 8.737564086914062 ms

            TODO: move this to a proper benchmarking harness.
        """
        partial_reader = "nea_test_reader"
        tbl = 'okera_system.audit_logs'

        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl("DROP ROLE IF EXISTS %s_role" % partial_reader)
            conn.execute_ddl("CREATE ROLE %s_role" % partial_reader)
            conn.execute_ddl("GRANT ROLE %s_role TO GROUP %s" % \
                (partial_reader, partial_reader))
            conn.execute_ddl(
                "GRANT SELECT ON TABLE %s WHERE v1 TO ROLE %s_role" % \
                (tbl, partial_reader))

            def get():
                self.get_filter(conn, 'okera_system', 'audit_logs', 'nea_test_reader',
                                TAccessPermissionLevel.SELECT)
            common.measure_latency(1000, get)

    def test_records_filter(self):
        all_user = "filter_test_user1"
        user1 = "filter_test_user2"

        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            # Set up roles and groups
            conn.execute_ddl("DROP ROLE IF EXISTS %s_role" % all_user)
            conn.execute_ddl("CREATE ROLE %s_role" % all_user)
            conn.execute_ddl("GRANT ROLE %s_role TO GROUP %s" % (all_user, all_user))
            conn.execute_ddl("DROP ROLE IF EXISTS %s_role" % user1)
            conn.execute_ddl("CREATE ROLE %s_role" % user1)
            conn.execute_ddl("GRANT ROLE %s_role TO GROUP %s" % (user1, user1))

            def grant(filter, user):
                conn.execute_ddl(
                    "GRANT INSERT ON TABLE okera_system.audit_logs %s TO ROLE %s_role" % \
                    (filter, user))
                conn.execute_ddl(
                    "GRANT SELECT ON TABLE okera_system.audit_logs %s TO ROLE %s_role" % \
                    (filter, user))

            def filter(user, records, return_records=False):
                serialized = []
                for record in records:
                    serialized.append(json.dumps(record))
                r = self.get_filter(conn, 'okera_system', 'audit_logs', user,
                                    TAccessPermissionLevel.INSERT, serialized,
                                    return_records)
                if return_records:
                    result = []
                    for r in r.result_records:
                      result.append(json.loads(r))
                    return result
                else:
                    return r.filtered_records

            # Set up grants
            grant("", all_user)
            grant("WHERE user='1'", user1)

            # Check records
            self.assertEqual([True], filter(all_user, [{'user':'1'}]))
            self.assertEqual([{'user':'1'}], filter(all_user, [{'user':'1'}], True))

            self.assertEqual([True, True], filter(all_user,
                                                  [{'user':'1'},
                                                   {'user':'2'}]))
            self.assertEqual([{'user':'1'}, {'user':'2'}],
                             filter(all_user, [{'user':'1'}, {'user':'2'}], True))

            self.assertEqual([True], filter(user1, [{'user':'1'}]))
            self.assertEqual([{'user':'1'}], filter(user1, [{'user':'1'}], True))

            self.assertEqual([False], filter(user1, [{'abc':'1'}]))
            self.assertEqual([], filter(user1, [{'abc':'1'}], True))

            self.assertEqual([True], filter(user1, [{'abc':'1', 'user':'1'}]))
            self.assertEqual([{'abc':'1', 'user':'1'}],
                             filter(user1, [{'abc':'1', 'user':'1'}], True))

            self.assertEqual([True, False], filter(user1,
                                                   [{'user':'1'},
                                                    {'user':'2'}]))
            self.assertEqual([{'user':'1'}], filter(user1,
                                                   [{'user':'1'},
                                                    {'user':'2'}], True))

    @unittest.skip("Not a test")
    def test_measure_records_filter_nea(self):
        """ This is not a real test and must be run after the record filter test above
            for setup.
            On a typical dev setup:

            Iterations 1000
            Mean 7.501605033874512 ms
            50%: 7.327556610107422 ms
            90%: 7.956743240356445 ms
            95%: 8.310794830322266 ms
            99%: 9.598255157470703 ms
            99.5%: 9.94420051574707 ms

            TODO: move this to a proper benchmarking harness.
        """
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            def get():
                records = [{'user':'1'}, {'user':'2'}]
                serialized = []
                for record in records:
                    serialized.append(json.dumps(record))
                self.get_filter(conn, 'okera_system', 'audit_logs', 'filter_test_user2',
                                TAccessPermissionLevel.INSERT, serialized)
            common.measure_latency(1000, get)

    def test_require_worker(self):
        # Test tables are atypical and always require the worker to evaluate
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            for user in [None, TEST_USER]:
                self.assertEqual(
                    None, self.authorize_table(conn, "all_table_types", "local_fs", user))
                self.assertEqual(
                    '*',
                    self.authorize_table(
                        conn, "all_table_types", "external_view_only", user))
                self.assertEqual(
                    '*',
                    self.authorize_table(
                        conn, "all_table_types", "dbfs_invalid_table", user))
                if user is None:
                    self.assertEqual(
                        None,
                        self.authorize_table(
                            conn, "okera_system", "audit_logs", user))

                self.assertEqual(
                    None,
                    self.authorize_table(
                        conn, "all_table_types", "single_file_table", user))
                self.assertEqual(
                    None,
                    self.authorize_table(
                        conn, "all_table_types", "http_table", user))

    def test_authorize_table_filter(self):
        role = "filter_test_role"
        testuser = "filter_testuser"
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl("DROP ROLE IF EXISTS " + role)
            conn.execute_ddl("CREATE ROLE " + role)
            conn.execute_ddl("GRANT ROLE " + role + " TO GROUP " + testuser)
            conn.execute_ddl('GRANT SELECT ON TABLE %s WHERE %s TO ROLE %s' %\
                             ('abac_db.all_types', 'find_in_set(string_col, "1,2") > 0',
                              role))
            self.assertTrue(
                self.authorize_table(conn, "abac_db", "all_types", testuser) is not None)

    def test_impala_rewrite(self):
        ctx = common.get_test_context()
        cases = [
            ("SELECT 1",
             "SELECT 1",
             "SELECT 1"),
            ("select count(*), count(int_col) from rs.alltypes_s3",
             "SELECT `count`(*), `count`(`int_col`) FROM `rs`.`alltypes_s3`",
             "select count(*), count(int_col) from `rs`.`alltypes_s3`"),
            ("SELECT count(int_col) as `a.c1` FROM rs.alltypes_s3",
             "SELECT `count`(`int_col`) as `a.c1` FROM `rs`.`alltypes_s3`",
             "SELECT count(int_col) as `a.c1` FROM `rs`.`alltypes_s3`"),
            ("SELECT * FROM okera_sample.users_ccn_masked",
             "SELECT `uid`, `dob`, `gender`, default.`mask_ccn`(`ccn`) " +
             "FROM `okera_sample`.`users`",
             "SELECT * FROM `okera_sample`.`users_ccn_masked`")
        ]

        with common.get_planner(ctx) as conn:
            for sql, rewritten, cte_rewritten in cases:
                self.assertEqual(
                    rewritten,
                    self.authorize_query(conn, sql, client=TAuthorizeQueryClient.IMPALA,
                                         cte=False))

                self.assertEqual(
                    cte_rewritten,
                    self.authorize_query(conn, sql, client=TAuthorizeQueryClient.IMPALA,
                                         cte=True))

    def test_cannot_cache(self):
        cases = [
            'SELECT 1',
            'SELECT user()',
            'SELECT rand()',
            'SELECT rand() + 1',
            'SELECT * FROM okera_sample.sample where rand() > 1',
        ]

        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            for sql in cases:
                self.assertEqual(None, self.cache_key(conn, sql))

    def test_can_cache(self):
        cases = [
            ("SELECT 1 from okera_sample.sample", "SELECT 1 FROM okera_sample.sample"),
            ("SELECT user() from okera_sample.sample",
             "SELECT 'okera' FROM okera_sample.sample"),
            ("SELECT upper(user()) from okera_sample.sample",
             "SELECT 'OKERA' FROM okera_sample.sample"),
            ('SELECT * FROM okera_sample.sample',
             'SELECT record FROM okera_sample.sample'),
            ('SELECT * FROM okera_sample.sample where record is not null',
             'SELECT record FROM okera_sample.sample WHERE record IS NOT NULL'),
        ]

        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            for sql, key in cases:
                self.assertEqual(key, self.cache_key(conn, sql))

    @unittest.skip("AuthorizeQuery by passing referenced tables will be deprecated.")
    def test_cte_rewrite(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            sql, _, _ = self.cte_rewrite(conn, "SELECT * FROM rs.alltypes_s3",
                                         ['rs.alltypes_s3'])
            print(sql)
            self.assertEqual('SELECT * FROM rs.alltypes_s3', sql)

            sql, _, _ = self.cte_rewrite(conn, "SELECT * FROM rs.alltypes_s3",
                                         ['rs.alltypes_s3'], "testuser")
            print(sql)
            self.assertEqual(
                'WITH okera_rewrite_rs__alltypes_s3 AS ' +
                '(SELECT int_col, float_col, string_col FROM rs.alltypes_s3) ' +
                'SELECT * FROM okera_rewrite_rs__alltypes_s3', sql)

            with self.assertRaises(TRecordServiceException) as ex_ctx:
                self.cte_rewrite(conn, "SELECT * FROM rs.nonexistent", ['rs.nonexistent'])
            self.assertTrue('Referenced table does not exist' in str(ex_ctx.exception))

    @unittest.skip("BigQuery test data is not loaded.")
    def test_cte_big_query(self):
        self.maxDiff = None
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl("DROP ATTRIBUTE IF EXISTS bigquery_test.attr")
            conn.execute_ddl("CREATE ATTRIBUTE bigquery_test.attr")

            def rewrite(sql, user=None):
                sql, _, _ = self.cte_rewrite(conn, sql, user=user,
                                             client=TAuthorizeQueryClient.PRESTO)
                return sql

            sql = rewrite("SELECT * FROM jdbc_test_bigquery.customers")
            print(sql)
            self.assertEqual(
                'WITH okera_rewrite_jdbc_test_bigquery__customers AS '\
                '(SELECT dob, country_code, mac, customer_name, customer_id, ip, '\
                'customer_unique_id, customer_unique_name, email FROM demo.customers) '\
                'SELECT * FROM okera_rewrite_jdbc_test_bigquery__customers `customers`',
                sql)

            # Column level permissions
            self._recreate_test_role(conn, 'bigquery_test_role', ['bq_testuser'])
            conn.execute_ddl(
                'GRANT SELECT(name, userid) ' +
                'ON TABLE jdbc_test_bigquery.user_account_data ' +
                'TO ROLE bigquery_test_role')
            sql = rewrite("SELECT * FROM jdbc_test_bigquery.user_account_data",
                          user='bq_testuser')
            print(sql)
            self.assertEqual(
                'WITH okera_rewrite_jdbc_test_bigquery__user_account_data AS '\
                '(SELECT name, userid FROM demo.user_account_data) '\
                'SELECT * FROM '\
                'okera_rewrite_jdbc_test_bigquery__user_account_data `user_account_data`',
                sql)

            # Try count(*)
            result = conn.scan_as_json(
                "SELECT count(*) FROM jdbc_test_bigquery.user_account_data",
                requesting_user='bq_testuser')
            self.assertEqual([{'count(*)': 100}], result)

            # Row level permissions
            self._recreate_test_role(conn, 'bigquery_test_role', ['bq_testuser'])
            conn.execute_ddl(
                'GRANT SELECT ON TABLE jdbc_test_bigquery.customers ' +
                "WHERE country_code = 'AL'" +
                'TO ROLE bigquery_test_role')
            sql = rewrite("SELECT * FROM jdbc_test_bigquery.customers",
                          user='bq_testuser')
            self.assertEqual(
                'WITH okera_rewrite_jdbc_test_bigquery__customers AS '\
                '(SELECT dob, country_code, mac, customer_name, customer_id, ip, '\
                'customer_unique_id, customer_unique_name, email FROM demo.customers '\
                'WHERE country_code = \'AL\') '\
                'SELECT * FROM okera_rewrite_jdbc_test_bigquery__customers `customers`',
                sql)

            result = conn.scan_as_json("SELECT * FROM jdbc_test_bigquery.customers",
                                       requesting_user='bq_testuser')
            self.assertEqual(85, len(result))

            # Loop over all OOB deindentification functions
            conn.execute_ddl('ALTER TABLE jdbc_test_bigquery.customers ' +
                             'ADD COLUMN ATTRIBUTE email bigquery_test.attr')

            for udf, expected in [('mask', 'okera_udfs.mask(email)'),
                                  ('mask_ccn', "okera_udfs.mask_ccn(email)"),
                                  ('null', "CAST(NULL AS STRING)"),
                                  ('sha2', "CAST(to_base64(sha1(email)) AS STRING)"),
                                  ('tokenize', "okera_udfs.tokenize(email)"),
                                  ('zero', "''")]:
                self._recreate_test_role(conn, 'bigquery_test_role', ['bq_testuser'])
                conn.execute_ddl(
                    ('GRANT SELECT ON TABLE jdbc_test_bigquery.customers ' +
                     'TRANSFORM bigquery_test.attr WITH `%s`() ' +
                     'TO ROLE bigquery_test_role') % udf)
                sql = rewrite("SELECT * FROM jdbc_test_bigquery.customers",
                              user='bq_testuser')
                print(sql)
                self.assertEqual(
                    ('WITH okera_rewrite_jdbc_test_bigquery__customers AS '\
                     '(SELECT dob, country_code, mac, customer_name, customer_id, ip, '\
                     'customer_unique_id, customer_unique_name, '\
                     '%s as email FROM demo.customers) '\
                     'SELECT * FROM '\
                     'okera_rewrite_jdbc_test_bigquery__customers `customers`')
                    % expected, sql)

    @unittest.skip("Athena test data is not loaded.")
    def test_cte_athena(self):
        self.maxDiff = None
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl("DROP ATTRIBUTE IF EXISTS athena_test.attr")
            conn.execute_ddl("CREATE ATTRIBUTE athena_test.attr")

            def rewrite(sql, user=None):
                sql, _, _ = self.cte_rewrite(conn, sql, user=user,
                                             client=TAuthorizeQueryClient.PRESTO)
                return sql

            sql = rewrite("SELECT * FROM jdbc_test_athena.alltypes_s3")
            print(sql)
            self.assertEqual(
                'WITH okera_rewrite_jdbc_test_athena__alltypes_s3 AS '
                '(SELECT "bool_col", "tinyint_col", "smallint_col", "int_col", '
                '"bigint_col", "float_col", "double_col", "string_col", "varchar_col", '
                '"char_col", "timestamp_col", "decimal_col" FROM '
                '"AwsDataCatalog"."okera_test"."alltypes_s3") '
                'SELECT * FROM okera_rewrite_jdbc_test_athena__alltypes_s3 "alltypes_s3"',
                sql)

            # Column level permissions
            self._recreate_test_role(conn, 'athena_test_role', ['athena_testuser'])
            conn.execute_ddl(
                'GRANT SELECT(bool_col, tinyint_col) ' +
                'ON TABLE jdbc_test_athena.alltypes_s3 ' +
                'TO ROLE athena_test_role')
            sql = rewrite("select * from jdbc_test_athena.alltypes_s3",
                          user='athena_testuser')
            print(sql)
            self.assertEqual(
                'WITH okera_rewrite_jdbc_test_athena__alltypes_s3 AS '
                '(SELECT "bool_col", "tinyint_col" FROM '
                '"AwsDataCatalog"."okera_test"."alltypes_s3") '
                'SELECT * FROM okera_rewrite_jdbc_test_athena__alltypes_s3 '
                '"alltypes_s3"',
                sql)

            # Try count(*)
            result = conn.scan_as_json(
                "SELECT count(*) as cnt FROM jdbc_test_athena.alltypes_s3",
                requesting_user='athena_testuser')
            self.assertEqual([{'cnt': 2}], result)

            # Row level permissions
            self._recreate_test_role(conn, 'athena_test_role', ['athena_testuser'])
            conn.execute_ddl(
                'GRANT SELECT ON TABLE jdbc_test_athena.alltypes_s3 ' +
                "WHERE string_col = 'hello'" +
                'TO ROLE athena_test_role')
            sql = rewrite("SELECT * FROM jdbc_test_athena.alltypes_s3",
                          user='athena_testuser')
            self.assertEqual(
                'WITH okera_rewrite_jdbc_test_athena__alltypes_s3 AS '
                '(SELECT "bool_col", "tinyint_col", "smallint_col", "int_col", '
                '"bigint_col", "float_col", "double_col", "string_col", "varchar_col", '
                '"char_col", "timestamp_col", "decimal_col" FROM '
                '"AwsDataCatalog"."okera_test"."alltypes_s3" '
                'WHERE "string_col" = \'hello\') '
                'SELECT * FROM okera_rewrite_jdbc_test_athena__alltypes_s3 "alltypes_s3"',
                sql)

            sql = rewrite("SELECT * FROM jdbc_test_athena.alltypes_s3",
                          user='athena_testuser')
            self.assertEqual(1, len(result))

            # Loop over all OOB deindentification functions
            conn.execute_ddl('ALTER TABLE jdbc_test_athena.alltypes_s3 ' +
                             'ADD COLUMN ATTRIBUTE string_col athena_test.attr')

            for udf, expected in [('mask', 'CAST(\'XXXXXXXX\' AS VARCHAR(255))'),
                                  ('mask_ccn', 'CAST((\'XXXX-XXXX-XXXX\' || substr(("string_col"), length(("string_col"))-3) AS VARCHAR(255))'),
                                  ('null', "CAST(CAST(NULL AS STRING) AS VARCHAR(255))"),
                                  ('sha2', 'CAST(from_base(substr(to_hex(sha256(to_utf8(cast(("string_col") as varchar)))), 1, 15), 16) AS VARCHAR(255))'),
                                  ('tokenize', 'CAST(to_hex(sha1(to_utf8(cast(("string_col") as varchar)))) AS VARCHAR(255))'),
                                  ('zero', "CAST('' AS VARCHAR(255))")]:
                self._recreate_test_role(conn, 'athena_test_role', ['athena_testuser'])
                conn.execute_ddl(
                    ('GRANT SELECT ON TABLE jdbc_test_athena.alltypes_s3 ' +
                     'TRANSFORM athena_test.attr WITH `%s`() ' +
                     'TO ROLE athena_test_role') % udf)
                sql = rewrite("SELECT string_col FROM jdbc_test_athena.alltypes_s3",
                              user='athena_testuser')
                print(udf, sql)
                self.assertEqual(
                    ('WITH okera_rewrite_jdbc_test_athena__alltypes_s3 AS '
                    '(SELECT %s as "string_col" FROM '
                    '"AwsDataCatalog"."okera_test"."alltypes_s3") '
                    'SELECT "string_col" FROM '
                    'okera_rewrite_jdbc_test_athena__alltypes_s3 "alltypes_s3"')
                    % expected, sql)

    @unittest.skipIf(common.TEST_LEVEL in SKIP_LEVELS, "Skipping at unit/all level")
    def test_cte_get_referenced_tables(self):
        self.maxDiff = None
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl("DROP ATTRIBUTE IF EXISTS snowflake_test.attr")
            conn.execute_ddl("CREATE ATTRIBUTE snowflake_test.attr")

            def rewrite(sql, user=None):
                sql, plan, referenced_tables = self.cte_rewrite(
                    conn, sql, client=TAuthorizeQueryClient.PRESTO, user=user)
                return sql, plan, referenced_tables

            test_sql = """select * from jdbc_test_snowflake.all_types a
                          join jdbc_test_snowflake.all_types b ON a.string = b.string"""
            sql, _, referenced_tables = rewrite(test_sql)
            self.assertTrue(sql is not None)
            self.assertTrue(len(referenced_tables) == 1)
            self.assertTrue("jdbc_test_snowflake.all_types" in referenced_tables)

            test_sql = """select * from jdbc_test_snowflake.all_types a
                          join jdbc_test_snowflake.all_types2 b ON a.string = b.string"""
            sql, _, referenced_tables = rewrite(test_sql)
            self.assertTrue(sql is not None)
            self.assertTrue(len(referenced_tables) == 2)
            self.assertTrue("jdbc_test_snowflake.all_types" in referenced_tables)
            self.assertTrue("jdbc_test_snowflake.all_types2" in referenced_tables)

    @unittest.skipIf(common.TEST_LEVEL in SKIP_LEVELS, "Skipping at unit/all level")
    def test_cte_snowflake_pushdown(self):
        self.maxDiff = None
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl("DROP ATTRIBUTE IF EXISTS snowflake_test.attr")
            conn.execute_ddl("CREATE ATTRIBUTE snowflake_test.attr")

            def rewrite(sql, user=None):
                sql, _, _ = self.cte_rewrite(conn, sql,
                                             client=TAuthorizeQueryClient.PRESTO,
                                             user=user)
                return sql

            for test_sql in ['SELECT * FROM jdbc_test_snowflake.all_types',
                             'SELECT * FROM "jdbc_test_snowflake"."all_types"']:
                print("Original SQL:\n " + test_sql)
                sql = rewrite(test_sql)
                print("Rewritten SQL:\n " + sql)
                self.assertEqual(
                    'WITH okera_rewrite_jdbc_test_snowflake__all_types AS ' \
                    '(SELECT "VARCHAR" as "varchar", "STRING" as "string", ' \
                    '"TEXT" as "text", "SMALLINT" as "smallint", "INT" as "int", ' \
                    '"BIGINT" as "bigint", "INTEGER" as "integer", ' \
                    '"DOUBLE" as "double", "NUMERIC" as "numeric", ' \
                    '"NUMBER" as "number", "DECIMAL" as "decimal", ' \
                    '"TIMESTAMP" as "timestamp", "CHAR" as "char", ' \
                    '"BOOLEAN" as "boolean", "BINARY" as "binary", ' \
                    '"VARBINARY" as "varbinary", "REAL" as "real" ' \
                    'FROM "DEMO_DB"."JDBC_TEST"."ALL_TYPES") ' \
                    'SELECT * FROM okera_rewrite_jdbc_test_snowflake__all_types ' \
                    '"all_types"', sql)
                result = conn.scan_as_json(test_sql, client=TAuthorizeQueryClient.PRESTO)
                print(result)
                self.assertEqual(2, len(result))

            # Column level permissions
            self._recreate_test_role(conn, 'sf_test_role', ['sf_testuser'])
            conn.execute_ddl(
                'GRANT SELECT(`real`, `text`) ' +
                'ON TABLE jdbc_test_snowflake.all_types ' +
                'TO ROLE sf_test_role')
            sql = rewrite("SELECT * FROM jdbc_test_snowflake.all_types",
                          user='sf_testuser')
            print(sql)
            self.assertEqual(
                'WITH okera_rewrite_jdbc_test_snowflake__all_types AS (' +
                'SELECT "TEXT" as "text", "REAL" as "real" ' +
                'FROM "DEMO_DB"."JDBC_TEST"."ALL_TYPES") ' +
                'SELECT * FROM okera_rewrite_jdbc_test_snowflake__all_types ' +
                '"all_types"', sql)
            result = conn.scan_as_json("SELECT * FROM jdbc_test_snowflake.all_types",
                                       requesting_user='sf_testuser')
            self.assertEqual(
                result,
                [{'text': None, 'real': None}, {'text': 'testtext', 'real': 10.0}])


            # Try count(*)
            test_sql = "SELECT count(*) FROM jdbc_test_snowflake.all_types"
            sql = rewrite(test_sql, user='sf_testuser')
            print("Rewritten SQL:\n " + sql)
            self.assertEqual(
                'WITH okera_rewrite_jdbc_test_snowflake__all_types ' +
                'AS (SELECT "TEXT" as "text", "REAL" as "real" ' +
                'FROM "DEMO_DB"."JDBC_TEST"."ALL_TYPES") ' +
                'SELECT "count"(*) FROM okera_rewrite_jdbc_test_snowflake__all_types ' +
                '"all_types"', sql)
            result = conn.scan_as_json(test_sql, requesting_user='sf_testuser')
            self.assertEqual([{'count(*)': 2}], result)

            # Row level permissions
            self._recreate_test_role(conn, 'sf_test_role', ['sf_testuser'])
            conn.execute_ddl(
                'GRANT SELECT ON TABLE jdbc_test_snowflake.all_types ' +
                "WHERE `text` = 'testtext'" +
                'TO ROLE sf_test_role')

            for test_sql in ['SELECT * FROM jdbc_test_snowflake.all_types']:
                print("Original SQL:\n " + test_sql)
                sql = rewrite(test_sql, user='sf_testuser')
                print("Rewritten SQL:\n " + sql)
                self.assertEqual(
                    'WITH okera_rewrite_jdbc_test_snowflake__all_types ' +
                    'AS (SELECT "VARCHAR" as "varchar", "STRING" as "string", ' +
                    '"TEXT" as "text", "SMALLINT" as "smallint", ' +
                    '"INT" as "int", "BIGINT" as "bigint", ' +
                    '"INTEGER" as "integer", "DOUBLE" as "double", ' +
                    '"NUMERIC" as "numeric", "NUMBER" as "number", ' +
                    '"DECIMAL" as "decimal", "TIMESTAMP" as "timestamp", ' +
                    '"CHAR" as "char", "BOOLEAN" as "boolean", ' +
                    '"BINARY" as "binary", "VARBINARY" as "varbinary", ' +
                    '"REAL" as "real" ' +
                    'FROM "DEMO_DB"."JDBC_TEST"."ALL_TYPES" ' +
                    'WHERE "TEXT" = \'testtext\') ' +
                    "SELECT * FROM okera_rewrite_jdbc_test_snowflake__all_types " +
                    "\"all_types\"", sql)
                result = conn.scan_as_json(test_sql, requesting_user='sf_testuser',
                                           client=TAuthorizeQueryClient.PRESTO)
                self.assertEqual(1, len(result))

            # Loop over all OOB deindentification functions
            conn.execute_ddl('ALTER TABLE jdbc_test_snowflake.all_types ' +
                             'ADD COLUMN ATTRIBUTE `text` snowflake_test.attr')

            for test_sql in ['SELECT * FROM jdbc_test_snowflake.all_types']:
                for udf, expected in [('mask', 'okera_udfs.public.mask("TEXT")'),
                                      ('mask_ccn', 'okera_udfs.public.mask_ccn("TEXT")'),
                                      ('null', 'CAST(NULL AS STRING)'),
                                      ('sha2', 'CAST("sha2"("TEXT") AS STRING)'),
                                      ('tokenize',
                                       'okera_udfs.public.tokenize' + \
                                       '("TEXT", last_query_id())'),
                                      ('zero', "''")]:
                    self._recreate_test_role(conn, 'sf_test_role', ['sf_testuser'])
                    conn.execute_ddl(
                        ('GRANT SELECT ON TABLE jdbc_test_snowflake.all_types ' +
                         'TRANSFORM snowflake_test.attr WITH `%s`() ' +
                         'TO ROLE sf_test_role') % udf)
                    print("Original SQL:\n " + test_sql)
                    sql = rewrite(test_sql, user='sf_testuser')
                    print("Rewritten SQL:\n " + sql)
                    self.assertEqual(
                        ('WITH okera_rewrite_jdbc_test_snowflake__all_types AS ' +
                         '(SELECT "VARCHAR" as "varchar", ' +
                         '"STRING" as "string", %s as "text", ' +
                         '"SMALLINT" as "smallint", ' +
                         '"INT" as "int", "BIGINT" as "bigint", ' +
                         '"INTEGER" as "integer", ' +
                         '"DOUBLE" as "double", "NUMERIC" as "numeric", ' +
                         '"NUMBER" as "number", "DECIMAL" as "decimal", ' +
                         '"TIMESTAMP" as "timestamp", "CHAR" as "char", ' +
                         '"BOOLEAN" as "boolean", "BINARY" as "binary", ' +
                         '"VARBINARY" as "varbinary", "REAL" as "real" ' +
                         'FROM "DEMO_DB"."JDBC_TEST"."ALL_TYPES") ' +
                         'SELECT * FROM okera_rewrite_jdbc_test_snowflake__all_types ' +
                         '"all_types"') %
                        expected, sql)
                    result = conn.scan_as_json(test_sql, requesting_user='sf_testuser',
                                               client=TAuthorizeQueryClient.PRESTO)
                    self.assertEqual(2, len(result))

            for test_sql in [
                    'select * from "jdbc_test_snowflake"."all_types" a ' +
                    'join "jdbc_test_snowflake"."all_types" b ON a.string = b.string',
                    'select * from jdbc_test_snowflake.all_types a ' +
                    'join jdbc_test_snowflake.all_types b ON a.string = b.string']:
                print("Original SQL:\n " + test_sql)
                sql = rewrite(test_sql, user='sf_testuser')
                print("Rewritten SQL:\n " + sql)
                self.assertEqual(
                    'WITH okera_rewrite_jdbc_test_snowflake__all_types ' +
                    'AS (SELECT "VARCHAR" as "varchar", "STRING" as "string", ' +
                    '\'\' as "text", "SMALLINT" as "smallint", "INT" as "int", ' +
                    '"BIGINT" as "bigint", "INTEGER" as "integer", ' +
                    '"DOUBLE" as "double", "NUMERIC" as "numeric", ' +
                    '"NUMBER" as "number", "DECIMAL" as "decimal", ' +
                    '"TIMESTAMP" as "timestamp", "CHAR" as "char", ' +
                    '"BOOLEAN" as "boolean", "BINARY" as "binary", ' +
                    '"VARBINARY" as "varbinary", "REAL" as "real" ' +
                    'FROM "DEMO_DB"."JDBC_TEST"."ALL_TYPES") ' +
                    'SELECT * FROM (okera_rewrite_jdbc_test_snowflake__all_types ' +
                    '"a" INNER JOIN okera_rewrite_jdbc_test_snowflake__all_types "b" ' +
                    'ON ("a"."string" = "b"."string"))', sql)

            test_sql = '''
  SELECT  SUM(1) sum_number_of_reco, DATE_ADD('DAY', CAST((-1 * ((1 + MOD((MOD((MOD((MOD(DATE_DIFF('DAY', CAST('1995-01-01' AS DATE),
        CAST(CAST(superstore.date AS DATE) AS DATE)), 7) + ABS(7)), 7) + 7), 7) + ABS(7)), 7)) - 1)) AS BIGINT),
        CAST(DATE_TRUNC('day', CAST(superstore.date AS DATE)) AS timestamp)) twk_order_date_ok, YEAR(CAST(superstore.date AS DATE)) yr_order_date_nk,
        DAY_OF_WEEK(CAST(superstore.date AS DATE)) day_of_week, DAY_OF_MONTH(CAST(superstore.date AS DATE)) day_of_month,
        DAY_OF_YEAR(CAST(superstore.date AS DATE)) day_of_year, WEEK_OF_YEAR(CAST(superstore.date AS DATE)) week_of_year,
        YEAR_OF_WEEK(CAST(superstore.date AS DATE)) year_of_week
  FROM jdbc_test_snowflake.all_types2 superstore
  GROUP BY 2, 3, 4, 5, 6, 7, 8'''
            print("Original SQL:\n " + test_sql)
            sql = rewrite(test_sql)
            print("Rewritten SQL:\n " + sql)
            result = conn.scan_as_json(test_sql, client=TAuthorizeQueryClient.PRESTO)
            self.assertEqual(2, len(result))

            for test_sql in [
                    'select * from okera.jdbc_test_snowflake.all_types a',
                    'select * from "okera"."jdbc_test_snowflake"."all_types" a']:
                print("Original SQL:\n " + test_sql)
                sql = rewrite(test_sql)
                print("Rewritten SQL:\n " + sql)
                result = conn.scan_as_json(test_sql, client=TAuthorizeQueryClient.PRESTO)
                self.assertEqual(2, len(result))

            test_sql = '''
    SELECT DATE_FORMAT(date, '%Y-%m-%d') as date_val FROM jdbc_test_snowflake.all_types2
            '''
            print("Original SQL:\n " + test_sql)
            sql = rewrite(test_sql)
            print("Rewritten SQL:\n " + sql)
            result = conn.scan_as_json(test_sql, client=TAuthorizeQueryClient.PRESTO)
            self.assertEqual(2, len(result))
            print(result)
            self.assertEqual(None, result[0]["date_val"])
            self.assertEqual('2017-02-28', result[1]["date_val"])

            test_sql = '''
    SELECT to_unixtime(date) as date_val FROM jdbc_test_snowflake.all_types2
            '''
            print("Original SQL:\n " + test_sql)
            sql = rewrite(test_sql)
            print("Rewritten SQL:\n " + sql)
            result = conn.scan_as_json(test_sql, client=TAuthorizeQueryClient.PRESTO)
            self.assertEqual(2, len(result))
            print(result)
            self.assertEqual(None, result[0]["date_val"])
            self.assertEqual(1488240000000, result[1]["date_val"])

            test_sql = '''
    with date_test as (
      select decimal, from_unixtime(1582985586) as x from jdbc_test_snowflake.all_types2
    )
    select
      current_date as c1,
      current_time  as c2,
      current_timestamp as c3,
      DATE(x) as c4,
      localtime as c5,
      now() as c6,
      to_unixtime(x) as c7,
      date_trunc('year', x) as c8,
      date_add('month', 2, x) as c9,
      date_diff('day', x, from_unixtime(1583995586)) as c10,
      date_format(x, 'YYYY-MM-DD') as c11,
      date_parse('2020-02-29 12:05:30', 'YYYY-MM-DD HH:mi:ss') as c12,
      extract(year FROM x) as c13,
      format_datetime(x, 'YYYY-MM-DD') as c14,
      parse_datetime('2020-02-29', 'YYYY-MM-DD') as c15,
      day(x) as c16,
      day_of_month(x) as c17,
      day_of_week(x) as c18,
      day_of_year(x) as c19,
      dow(x) as c20,
      doy(x) as c21,
      hour(x) as c22,
      minute(x) as c23,
      month(x) as c24,
      quarter(x) as c25,
      second(x) as c26,
      week(x) as c27,
      week_of_year(x) as c28,
      year(x) as c29,
      year_of_week(x) as c30,
      yow(x) as c31
    from date_test
    limit 1'''
            print("Original SQL:\n " + test_sql)
            sql = rewrite(test_sql)
            print("Rewritten SQL:\n " + sql)
            result = conn.scan_as_json(test_sql, client=TAuthorizeQueryClient.PRESTO)
            self.assertEqual(1, len(result))
            # TODO: Assert some values. Since these are some current context, it would be
            # hard to assert the correctness.
            print(result)


    def snowflake_verify_policy_on_column(self, conn, column):
        print('\n::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        print('snowflake_verify_policy_on_column test for "%s" column\n' % column)

        def get_cast_type(col_upper):
            if col_upper in ['DOUBLE', 'REAL']:
                return 'DOUBLE'
            if col_upper in ['NUMERIC', 'DECIMAL']:
                return 'DECIMAL(10,2)'
            if col_upper in ['VARCHAR']:
                return 'VARCHAR(20)'
            if col_upper in ['CHAR']:
                return 'VARCHAR(10)'
            if col_upper in ['BIGINT', 'SMALLINT', 'INT', 'INTEGER', 'NUMBER']:
                return 'BIGINT'
            return 'STRING'

        def get_function_tuple_by_column(col_upper):
            if (col_upper in ['BIGINT', 'SMALLINT', 'INT', 'INTEGER', 'DOUBLE',
                              'NUMBER', 'REAL']):
                return [('null', 'CAST(NULL AS %s)' % get_cast_type(col_upper)),
                        ('sha2', '"sha2"("%s")' % col_upper),
                        ('tokenize', 'okera_udfs.public.tokenize("%s", last_query_id())' %
                         col_upper),
                        ('zero', "0")]
            if (col_upper in ['NUMERIC', 'DECIMAL']):
                return [('null', 'CAST(NULL AS %s)' % get_cast_type(col_upper)),
                        # FIXME: Okera issue with sha for numeric
                        #('sha2', '"sha2"("%s")' % col_upper),
                        ('tokenize', 'okera_udfs.public.tokenize("%s", last_query_id())' %
                         col_upper),
                        ('zero', "0")]
            if (col_upper in ['BOOLEAN']):
                return [('null', 'CAST(NULL AS %s)' % col_upper),
                        # FIXME: Okera issue with sha for numeric
                        #('sha2', '"sha2"("%s")' % col_upper),
                        ('tokenize', 'okera_udfs.public.tokenize("%s", last_query_id())' %
                         col_upper),
                        ('zero', "0")]
            if (col_upper in ['TIMESTAMP']):
                return [('null', 'CAST(CAST(NULL AS TIMESTAMP) AS TIMESTAMP)'),
                        # FIXME: Okera issue with sha for timestamp
                        # ('sha2', '"sha2"("%s")' % col_upper),
                        # FIXME: SF issue with tokenize for timestamp
                        # ('tokenize', 'okera_udfs.public.tokenize("%s", last_query_id())'
                        # % col_upper),
                        ('zero', "CAST(0 AS TIMESTAMP)")]
            if (col_upper in ['DATE']):
                return [('null', 'CAST(CAST(NULL AS TIMESTAMP) AS DATE)'),
                        # FIXME: Okera issue with sha for timestamp
                        # ('sha2', '"sha2"("%s")' % col_upper),
                        # FIXME: SF issue with tokenize for DATE
                        # ('tokenize', 'okera_udfs.public.tokenize("%s", last_query_id())'
                        # % col_upper),
                        # FIXME: SF issue with CAST(0 AS DATE)
                        # ('zero', "CAST(0 AS DATE)")
                        ]
            if (col_upper in ['VARCHAR', 'CHAR']):
                return [('mask', 'okera_udfs.public.mask("%s")' % col_upper),
                        ('mask_ccn', 'okera_udfs.public.mask_ccn("%s")' % col_upper),
                        ('null', 'CAST(NULL AS STRING)'),
                        # FIXME: SF issue varchar with sha2 has a string too long error.
                        #('sha2', 'CAST("sha2"("%s") AS %s)' %
                        # (col_upper, get_cast_type(col_upper))),
                        ('tokenize', 'okera_udfs.public.tokenize("%s", last_query_id())' %
                         col_upper),
                        ('zero', "''")]
            if (col_upper in ['BINARY', 'VARBINARY']):
                return [('null', 'CAST(NULL AS STRING)'),
                        ('sha2', 'CAST("sha2"("%s") AS STRING)' % col_upper),
                        # FIXME: SF issue fails for mask(BINARY)
                        # ('mask', 'okera_udfs.public.mask("%s")' % col_upper),
                        # FIXME: SF issue fails for mask(BINARY)
                        # ('mask_ccn', 'okera_udfs.public.mask_ccn("%s")' % col_upper),
                        # FIXME: SF issue fails for tokenize(BINARY)
                        # ('tokenize', 'okera_udfs.public.tokenize("%s", last_query_id())'
                        # % col_upper),
                        ('zero', "''")]
            return [('mask', 'okera_udfs.public.mask("%s")' % col_upper),
                    ('mask_ccn', 'okera_udfs.public.mask_ccn("%s")' % col_upper),
                    ('null', 'CAST(NULL AS STRING)'),
                    ('sha2', 'CAST("sha2"("%s") AS STRING)' % col_upper),
                    ('tokenize', 'okera_udfs.public.tokenize("%s", last_query_id())' %
                     col_upper),
                    ('zero', "''")]

        # Loop over all OOB deindentification functions
        conn.execute_ddl('ALTER TABLE jdbc_test_snowflake.all_types2 ' +
                         'ADD COLUMN ATTRIBUTE `%s` snowflake_test.attr' % column)

        col_upper = column.upper()
        test_sql = 'SELECT * FROM jdbc_test_snowflake.all_types2'
        self._recreate_test_role(conn, 'sf_test_role', ['sf_testuser'])
        for udf, expected in get_function_tuple_by_column(col_upper):
            conn.execute_ddl(
                ('GRANT SELECT ON TABLE jdbc_test_snowflake.all_types2 ' +
                 'TRANSFORM snowflake_test.attr WITH `%s`() ' +
                 'TO ROLE sf_test_role') % udf)
            print("\nTest: UDF / expected:\n " + udf + " / " + expected)
            print("Original SQL:\n " + test_sql)
            sql, _, _ = self.cte_rewrite(conn, test_sql,
                                         client=TAuthorizeQueryClient.PRESTO,
                                         user='sf_testuser')
            print("Rewritten SQL:\n " + sql)
            self.assertTrue('%s' % expected in sql)
            self.assertTrue('as "%s"' % column in sql)
            result = conn.scan_as_json(test_sql, requesting_user='sf_testuser',
                                       client=TAuthorizeQueryClient.PRESTO)
            self.assertEqual(2, len(result))
            print("The output:")
            print(result)
            # cleanup for next test.
            conn.execute_ddl(
                'REVOKE SELECT ON TABLE jdbc_test_snowflake.all_types2 ' +
                'TRANSFORM snowflake_test.attr WITH `%s`() FROM ROLE sf_test_role' %
                udf)

        if column in ['date']:
            # FIXME: date is not present in all_types table, we need another table
            # with data and should complete the referential integrity testing.
            print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
            return

        conn.execute_ddl('ALTER TABLE jdbc_test_snowflake.all_types ' +
                         'ADD COLUMN ATTRIBUTE `%s` snowflake_test.attr' % column)

        self._recreate_test_role(conn, 'sf_test_role', ['sf_testuser'])
        test_sql = 'SELECT a.* FROM jdbc_test_snowflake.all_types2 a JOIN ' + \
                   'jdbc_test_snowflake.all_types b ON (a.%s = b.%s)' % \
                   (column, column)
        for udf, expected in get_function_tuple_by_column(col_upper):
            conn.execute_ddl(
                ('GRANT SELECT ON TABLE jdbc_test_snowflake.all_types2 ' +
                 'TRANSFORM snowflake_test.attr WITH `%s`() ' +
                 'TO ROLE sf_test_role') % udf)
            conn.execute_ddl(
                ('GRANT SELECT ON TABLE jdbc_test_snowflake.all_types ' +
                 'TRANSFORM snowflake_test.attr WITH `%s`() ' +
                 'TO ROLE sf_test_role') % udf)

            print("\nTest: UDF / expected:\n " + udf + " / " + expected)
            print("Original SQL:\n " + test_sql)
            sql, _, _ = self.cte_rewrite(conn, test_sql,
                                         client=TAuthorizeQueryClient.PRESTO,
                                         user='sf_testuser')
            print("Rewritten SQL:\n " + sql)
            self.assertTrue('%s' % expected in sql)
            self.assertTrue('as "%s"' % column in sql)
            result = conn.scan_as_json(test_sql, requesting_user='sf_testuser',
                                       client=TAuthorizeQueryClient.PRESTO)
            # If everything is null, joins will evaluate to no rows.
            if udf == 'null':
                self.assertEqual(0, len(result))
            elif udf == 'zero':
                # There are 2 rows in each table and join on zeros for both would result
                # in 4 rows (cartisan product).
                self.assertEqual(4, len(result))
            else:
                # There are 2 rows in each table but one row is all nulls.
                self.assertEqual(1, len(result))
            print("The output:")
            print(result)
            # Cleanup for next test.
            conn.execute_ddl(
                'REVOKE SELECT ON TABLE jdbc_test_snowflake.all_types2 ' +
                'TRANSFORM snowflake_test.attr WITH `%s`() FROM ROLE sf_test_role' %
                udf)
            conn.execute_ddl(
                'REVOKE SELECT ON TABLE jdbc_test_snowflake.all_types ' +
                'TRANSFORM snowflake_test.attr WITH `%s`() FROM ROLE sf_test_role' %
                udf)
        print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')

    @unittest.skipIf(common.TEST_LEVEL in SKIP_LEVELS, "Skipping at unit/all level")
    def test_cte_snowflake_privacy_functions(self):
        self.maxDiff = None
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self._recreate_test_role(conn, 'sf_test_role', ['sf_testuser'])
            for column in ['varchar', 'string', 'text', 'smallint', 'bigint', 'int',
                           'integer', 'double', 'numeric', 'number', 'decimal', 'real',
                           'char', 'boolean', 'binary', 'varbinary',
                           'timestamp', 'date']:
                conn.execute_ddl("DROP ATTRIBUTE IF EXISTS snowflake_test.attr")
                conn.execute_ddl("CREATE ATTRIBUTE snowflake_test.attr")
                self.snowflake_verify_policy_on_column(conn, column)

    @unittest.skipIf(common.TEST_LEVEL not in "all", "Skipping at unit/all level")
    def test_cte_snowflake_aliases(self):
        self.maxDiff = None
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl("DROP ATTRIBUTE IF EXISTS snowflake_test.attr")
            conn.execute_ddl("CREATE ATTRIBUTE snowflake_test.attr")

            self._recreate_test_role(conn, 'sf_test_role', ['sf_testuser'])
            conn.execute_ddl(
                'GRANT SELECT ON TABLE jdbc_test_snowflake.all_types ' +
                "WHERE `text` = 'testtext'" +
                'TO ROLE sf_test_role')

            def rewrite(sql, user=None):
                sql, _, _ = self.cte_rewrite(conn, sql,
                                             client=TAuthorizeQueryClient.PRESTO,
                                             user=user)
                return sql

            test_sql = 'SELECT 1 AS "number_of_records", ' \
                       '"all_types"."bigint" AS "BigInt", ' \
                       '"all_types"."binary" AS "Binary", ' \
                       '"all_types"."boolean" AS "Boolean", ' \
                       '"all_types"."char" AS "Char", ' \
                       '"all_types"."decimal" AS "Decimal", ' \
                       '"all_types"."double" AS "Double", ' \
                       '"all_types"."int" AS "Int", ' \
                       '"all_types"."integer" AS "Integer", ' \
                       '"all_types"."number" AS "Number", ' \
                       '"all_types"."numeric" AS "Numeric", ' \
                       '"all_types"."real" AS "Real", ' \
                       '"all_types"."smallint" AS "Smallint", ' \
                       '"all_types"."string" AS "String", ' \
                       '"all_types"."text" AS "Text", ' \
                       '"all_types"."timestamp" AS "Timestamp", ' \
                       '"all_types"."varbinary" AS "Varbinary", ' \
                       '"all_types"."varchar" AS "Varchar" ' \
                       'FROM "jdbc_test_snowflake"."all_types" "all_types" ' \
                       'LIMIT 1000'
            print("Original SQL:\n " + test_sql)
            sql = rewrite(test_sql, user='sf_testuser')
            print("Rewritten SQL:\n " + sql)
            self.assertEqual(
                'WITH okera_rewrite_jdbc_test_snowflake__all_types AS ' \
                '(SELECT "VARCHAR" as "varchar", "STRING" as "string", ' \
                '"TEXT" as "text", "SMALLINT" as "smallint", "INT" as "int", ' \
                '"BIGINT" as "bigint", "INTEGER" as "integer", "DOUBLE" as "double", ' \
                '"NUMERIC" as "numeric", "NUMBER" as "number", ' \
                '"DECIMAL" as "decimal", "TIMESTAMP" as "timestamp", "CHAR" as "char", ' \
                '"BOOLEAN" as "boolean", "BINARY" as "binary", ' \
                '"VARBINARY" as "varbinary", ' \
                '"REAL" as "real" FROM "DEMO_DB"."JDBC_TEST"."ALL_TYPES" ' \
                'WHERE "TEXT" = \'testtext\') ' \
                'SELECT 1 "number_of_records", "all_types"."bigint" "BigInt", ' \
                '"all_types"."binary" "Binary", "all_types"."boolean" "Boolean", ' \
                '"all_types"."char" "Char", "all_types"."decimal" "Decimal", ' \
                '"all_types"."double" "Double", "all_types"."int" "Int", ' \
                '"all_types"."integer" "Integer", "all_types"."number" "Number", ' \
                '"all_types"."numeric" "Numeric", "all_types"."real" "Real", ' \
                '"all_types"."smallint" "Smallint", "all_types"."string" "String", ' \
                '"all_types"."text" "Text", "all_types"."timestamp" "Timestamp", ' \
                '"all_types"."varbinary" "Varbinary", "all_types"."varchar" "Varchar" ' \
                'FROM okera_rewrite_jdbc_test_snowflake__all_types "all_types" ' \
                'LIMIT 1000', sql)
            result = conn.scan_as_json(test_sql, requesting_user='sf_testuser',
                                       client=TAuthorizeQueryClient.PRESTO)
            self.assertEqual(1, len(result))

            test_sql = 'SELECT "jdbc_test_snowflake"."all_types"."string" ' \
                           'AS "String", ' \
                           'count(distinct "jdbc_test_snowflake"."all_types"."bigint") ' \
                           'AS "count" ' \
                           'FROM "jdbc_test_snowflake"."all_types" ' \
                           'GROUP BY "jdbc_test_snowflake"."all_types"."string" ' \
                           'ORDER BY "jdbc_test_snowflake"."all_types"."string" ASC'
            print("Original SQL:\n " + test_sql)
            sql = rewrite(test_sql, user='sf_testuser')
            print("Rewritten SQL:\n " + sql)
            self.assertEqual(
                'WITH okera_rewrite_jdbc_test_snowflake__all_types AS ' \
                '(SELECT "STRING" as "string", ' \
                '"BIGINT" as "bigint" ' \
                'FROM "DEMO_DB"."JDBC_TEST"."ALL_TYPES" ' \
                'WHERE "TEXT" = \'testtext\') ' \
                'SELECT "all_types"."string" "String", '\
                '"count"(DISTINCT "all_types"."bigint") ' \
                '"count" ' \
                'FROM okera_rewrite_jdbc_test_snowflake__all_types "all_types" ' \
                'GROUP BY "all_types"."string" ' \
                'ORDER BY "all_types"."string" ASC', sql)
            result = conn.scan_as_json(test_sql, requesting_user='sf_testuser',
                                       client=TAuthorizeQueryClient.PRESTO)
            self.assertEqual(1, len(result))

            conn.execute_ddl(
                'GRANT SELECT ON DATABASE sf_tpcds_1gb '
                'TO ROLE sf_test_role')

            test_sql = 'SELECT "Date Dim"."d_year" AS "d_year", "Item"."i_brand" ' \
                'AS "i_brand", '\
                '"Item"."i_brand_id" AS "i_brand_id", ' \
                'sum("sf_tpcds_1gb"."store_sales"."ss_ext_sales_price") AS "sum" ' \
                'FROM "sf_tpcds_1gb"."store_sales" LEFT JOIN ' \
                '"sf_tpcds_1gb"."date_dim" "Date Dim" ON ' \
                '"sf_tpcds_1gb"."store_sales"."ss_sold_date_sk" = ' \
                '"Date Dim"."d_date_sk" LEFT JOIN ' \
                '"sf_tpcds_1gb"."item" "Item" ' \
                'ON "sf_tpcds_1gb"."store_sales"."ss_item_sk" = "Item"."i_item_sk" ' \
                'WHERE ("Item"."i_manufact_id" = 128 AND "Date Dim"."d_moy" = 11) ' \
                'GROUP BY "Date Dim"."d_year", "Item"."i_brand", "Item"."i_brand_id" ' \
                'ORDER BY "Date Dim"."d_year" ASC, "sum" ASC, "Item"."i_brand_id" ASC, ' \
                '"Item"."i_brand" ASC'
            print("Original SQL:\n " + test_sql)
            sql = rewrite(test_sql, user='sf_testuser')
            print("Rewritten SQL:\n " + sql)
            result = conn.scan_as_json(test_sql, requesting_user='sf_testuser',
                                       client=TAuthorizeQueryClient.PRESTO)
            self.assertEqual(83, len(result))

            # Grant an abac transform
            conn.execute_ddl("DROP ATTRIBUTE IF EXISTS sf_test.attr")
            conn.execute_ddl("CREATE ATTRIBUTE sf_test.attr")
            conn.execute_ddl(
                "ALTER TABLE sf_tpcds_1gb.store_sales ADD COLUMN ATTRIBUTE " +
                "ss_item_sk sf_test.attr")
            conn.execute_ddl(
                "ALTER TABLE sf_tpcds_1gb.item ADD COLUMN ATTRIBUTE " +
                "i_item_sk sf_test.attr")
            conn.execute_ddl(
                'REVOKE SELECT ON DATABASE sf_tpcds_1gb '
                'FROM ROLE sf_test_role')
            conn.execute_ddl(
                'GRANT SELECT ON DATABASE sf_tpcds_1gb '
                'TRANSFORM sf_test.attr WITH sha2()'
                'TO ROLE sf_test_role')
            sql = rewrite(test_sql, user='sf_testuser')
            print("Rewritten SQL:\n " + sql)
            result = conn.scan_as_json(test_sql, requesting_user='sf_testuser',
                                       client=TAuthorizeQueryClient.PRESTO)
            self.assertEqual(83, len(result))

            # Query is valid in case insensitive with upper case Item as table
            # alias and lower case item used later.
            test_sql = '''
SELECT "Date Dim".d_year AS d_year,
       item.i_brand_id AS i_brand_id,
       item.i_brand AS i_brand,
       sum(ss_ext_sales_price) AS "SUM"
FROM   sf_tpcds_1gb.store_sales
       LEFT JOIN sf_tpcds_1gb.date_dim "Date Dim"
              ON sf_tpcds_1gb.store_sales.ss_sold_date_sk = "Date Dim".d_date_sk
       LEFT JOIN sf_tpcds_1gb.item Item
              ON sf_tpcds_1gb.store_sales.ss_item_sk = item.i_item_sk
WHERE  ( item.i_manufact_id = 128 AND "Date Dim".d_moy = 11 )
GROUP  BY "Date Dim".d_year, item.i_brand_id, item.i_brand
ORDER  BY "Date Dim".d_year ASC, "SUM" DESC, item.i_brand_id ASC, item.i_brand asc
limit 10'''
            print("Original SQL:\n " + test_sql)
            sql = rewrite(test_sql, user='sf_testuser')
            print("Rewritten SQL:\n " + sql)
            result = conn.scan_as_json(test_sql, requesting_user='sf_testuser',
                                       client=TAuthorizeQueryClient.PRESTO)
            self.assertEqual(10, len(result))

    @unittest.skipIf(common.TEST_LEVEL not in "all", "Skipping at unit/all level")
    def test_snowflake_tpcds_pushdown(self):
        self.maxDiff = None
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl("DROP ATTRIBUTE IF EXISTS snowflake_test.attr")
            conn.execute_ddl("CREATE ATTRIBUTE snowflake_test.attr")

            self._recreate_test_role(conn, 'sf_test_role', ['sf_testuser'])
            conn.execute_ddl(
                'GRANT SELECT ON DATABASE sf_tpcds_1gb '
                'TO ROLE sf_test_role')

            blacklist_files = [
                # Cumulative window frame unsupported for function "max"
                'query51.sql',
                'query54.sql',
                'query57.sql',
            ]

            tpcds_query_files_path = os.environ["OKERA_HOME"] + \
                '/integration/tests/benchmark/resources/snowflake_tpcds/'

            # Set this to a value to test just that file and alphabetically after that.
            from_file = None

            success = 0
            for file in sorted(os.listdir(tpcds_query_files_path)):
                print("Total files processed so far: " + str(success))
                # Skip non-avro files.
                if not file.endswith(".sql"):
                    continue
                elif file in blacklist_files:
                    continue
                elif from_file is not None and file < from_file:
                    continue
                else:
                    test_file = '%s/%s' % (tpcds_query_files_path, file)
                    with open(test_file, 'r') as sql_f:
                        test_sql = sql_f.read().strip()
                        test_sql = test_sql.replace("{database}", "sf_tpcds_1gb")
                        test_sql = test_sql.replace(";", "")
                        if 'limit ' not in test_sql.lower():
                            test_sql = test_sql + " LIMIT 1 "
                        print("\n" + test_file)
                        print("\n" + test_sql + "\n")
                        success += 1
                        result = conn.scan_as_json(test_sql,
                                                   requesting_user='sf_testuser',
                                                   client=TAuthorizeQueryClient.PRESTO)
                        self.assertTrue(result is not None)
            print("Total files success: " + str(success))
            print("Total files blacklisted: " + str(len(blacklist_files)))

    def test_cte_snowflake_error(self):
        self.maxDiff = None
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl("DROP ATTRIBUTE IF EXISTS snowflake_test.attr")
            conn.execute_ddl("CREATE ATTRIBUTE snowflake_test.attr")

            self._recreate_test_role(conn, 'sf_test_role', ['sf_testuser'])
            conn.execute_ddl(
                'GRANT SELECT ON TABLE jdbc_test_snowflake.all_types ' +
                "WHERE `text` = 'testtext'" +
                'TO ROLE sf_test_role')

            def rewrite(sql, user=None):
                return self.cte_rewrite(conn, sql, client=TAuthorizeQueryClient.PRESTO,
                                        generate_plan=True, user=user)
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                rewrite("select not_a_col from jdbc_test_snowflake.all_types")
            print(ex_ctx.exception.detail)
            self.assertTrue('invalid identifier' in ex_ctx.exception.detail,
                            msg=ex_ctx.exception.detail)

    @unittest.skipIf(common.TEST_LEVEL not in "all", "Skipping at unit/all level")
    def test_cte_snowflake_if_condition(self):
        self.maxDiff = None
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self._recreate_test_role(conn, 'sf_test_role', ['sf_testuser'])
            conn.execute_ddl(
                'GRANT SELECT ON TABLE jdbc_test_snowflake.all_types ' +
                'TO ROLE sf_test_role')

            def rewrite(sql, user=None):
                return self.cte_rewrite(conn, sql, client=TAuthorizeQueryClient.PRESTO,
                                        generate_plan=True, user=user)
            sql_statement = "select if(smallint=1, 10, 20) as x from jdbc_test_snowflake.all_types"
            rewritten_sql = rewrite(sql_statement, 'sf_testuser')
            assert 'iff(' in rewritten_sql[0].lower()

            result = conn.scan_as_json(sql_statement,
                                       requesting_user='sf_testuser',
                                       client=TAuthorizeQueryClient.PRESTO)
            assert len(result) == 2
            assert result[0]['x'] == 20
            assert result[1]['x'] == 10

    def test_cte_non_jdbc(self):
        # Plan generation against non-pushdown-able queries should fail
        # TODO: add cross JDBC datasource join queries.

        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            def rewrite(sql, client, user=None):
                return self.cte_rewrite(conn, sql, client=client,
                                        generate_plan=True, user=user)
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                rewrite("select * from okera_sample.sample",
                        client=TAuthorizeQueryClient.PRESTO)
            self.assertEqual(TErrorCode.UNSUPPORTED_REQUEST, ex_ctx.exception.code)

            # TODO: this should work, see impala-recordservice-server.cc:AuthorizeQuery
            # for details.
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                rewrite("select * from okera_sample.sample",
                        client=TAuthorizeQueryClient.OKERA)
            self.assertEqual(TErrorCode.INVALID_REQUEST, ex_ctx.exception.code)

    def test_cte_jdbc(self):
        # Note the SQL is in the dialect of the RDBMS engine, not OkeraQL
        ctx = common.get_test_context()
        role1 = 'jdbc_rewrite_test_role1'
        role2 = 'jdbc_rewrite_test_role2'
        testuser1 = 'jdbc_rewrite_test_user1'
        testuser2 = 'jdbc_rewrite_test_user2'
        db = 'jdbc_test_redshift'
        with common.get_planner(ctx) as conn:
            self._recreate_test_role(conn, role1, [testuser1])
            self._recreate_test_role(conn, role2, [testuser2])

            def rewrite(sql, user=None):
                return self.cte_rewrite(conn, sql, client=TAuthorizeQueryClient.PRESTO,
                                        generate_plan=True, user=user)

            sql, plan, ref_tables = rewrite(
                'SELECT * FROM "jdbc_test_redshift"."all_types_1" limit 10')
            print(sql)
            self.assertEqual('WITH okera_rewrite_jdbc_test_redshift__all_types_1 AS ' \
                '(SELECT "varchar", "text", "smallint", "int", "bigint", ' \
                '"double", "numeric", "decimal", "timestamp", "char", "bool", "real" ' \
                'FROM "dev"."public"."all_types_1") ' \
                'SELECT * FROM okera_rewrite_jdbc_test_redshift__all_types_1 ' \
                '"all_types_1" LIMIT 10',
                             sql)
            self.assertTrue(plan is not None)
            self.assertTrue('jdbc_test_redshift.all_types_1' in ref_tables)


            sql, plan, ref_tables = rewrite(
                "SELECT * FROM jdbc_test_redshift.all_types_1 limit 10")
            self.assertEqual('WITH okera_rewrite_jdbc_test_redshift__all_types_1 AS ' \
                '(SELECT "varchar", "text", "smallint", "int", "bigint", "double", ' \
                '"numeric", "decimal", "timestamp", "char", "bool", "real" ' \
                'FROM "dev"."public"."all_types_1") ' \
                'SELECT * FROM okera_rewrite_jdbc_test_redshift__all_types_1 ' \
                '"all_types_1" LIMIT 10',
                             sql)
            self.assertTrue(plan is not None)
            self.assertTrue('jdbc_test_redshift.all_types_1' in ref_tables)
            result = conn.scan_as_json(
                "SELECT * FROM jdbc_test_redshift.all_types_1 limit 10",
                client=TAuthorizeQueryClient.PRESTO)
            self.assertEqual(10, len(result))
            self.assertEqual(12, len(result[0]))
            self.assertEqual(1, result[0]['smallint'])
            self.assertEqual('hello', result[0]['text'])

            # Try with testuser1, which can only access one column
            conn.execute_ddl(
                "GRANT SELECT(`TEXT`) ON TABLE %s.all_types_1 TO ROLE %s" % \
                (db, role1))
            sql, plan, _ = rewrite(
                "SELECT * FROM jdbc_test_redshift.all_types_1 limit 10", user=testuser1)
            self.assertEqual(
                'WITH okera_rewrite_jdbc_test_redshift__all_types_1 AS (' +
                'SELECT "text" FROM "dev"."public"."all_types_1") ' +
                'SELECT * FROM okera_rewrite_jdbc_test_redshift__all_types_1 ' +
                '"all_types_1" LIMIT 10',
                sql)
            self.assertTrue(plan is not None)
            result = conn.scan_as_json(
                "SELECT * FROM jdbc_test_redshift.all_types_1 limit 10",
                client=TAuthorizeQueryClient.PRESTO,
                requesting_user=testuser1)
            self.assertEqual(10, len(result))
            self.assertEqual(1, len(result[0]))
            self.assertEqual('hello', result[0]['text'])

            # Try with testuser2, which has a row filter that removes all rows
            conn.execute_ddl(
                "GRANT SELECT ON TABLE %s.all_types_1 WHERE `int` = 0 TO ROLE %s" % \
                (db, role2))
            sql, plan, _ = rewrite(
                "SELECT * FROM jdbc_test_redshift.all_types_1 limit 10", user=testuser2)
            print(sql)
            self.assertEqual(
                'WITH okera_rewrite_jdbc_test_redshift__all_types_1 AS ' +
                '(SELECT "varchar", ' +
                '"text", "smallint", "int", ' +
                '"bigint", "double", ' +
                '"numeric", "decimal", ' +
                '"timestamp", "char", "bool", ' +
                '"real" FROM "dev"."public"."all_types_1" ' +
                'WHERE "int" = 0) ' +
                'SELECT * FROM okera_rewrite_jdbc_test_redshift__all_types_1 ' +
                '"all_types_1" LIMIT 10',
                sql)
            self.assertTrue(plan is not None)
            result = conn.scan_as_json(
                "SELECT * FROM jdbc_test_redshift.all_types_1 limit 10",
                client=TAuthorizeQueryClient.PRESTO,
                requesting_user=testuser2)
            self.assertTrue(len(result) == 0)

    @unittest.skipIf(common.TEST_LEVEL in SKIP_LEVELS, "Skipping at unit/all level")
    def test_cte_redshift(self):
        # Note the SQL is in the dialect of the RDBMS engine, not OkeraQL
        ctx = common.get_test_context()
        role = 'jdbc_rewrite_test_role'
        testuser = 'jdbc_rewrite_test_user'
        db = 'jdbc_test_redshift'

        with common.get_planner(ctx) as conn:
            self._recreate_test_role(conn, role, [testuser])
            conn.execute_ddl(
                ("GRANT SELECT ON DATABASE %s TRANSFORM abac.test_col WITH zero() " +
                 "TO ROLE %s") % (db, role))

            def scan(sql, col):
                row_root = conn.scan_as_json(sql, client=TAuthorizeQueryClient.PRESTO)
                row_user = conn.scan_as_json(
                    sql, client=TAuthorizeQueryClient.PRESTO, requesting_user=testuser)
                v_root = None
                v_user = None
                if row_root:
                    v_root = row_root[0][col]
                if row_user:
                    v_user = row_user[0][col]
                return v_root, v_user

            sql = "SELECT * FROM jdbc_test_redshift.all_data_types limit 1"
            self.assertEqual((None, None), scan(sql, 'varchar'))

            sql = "SELECT * FROM jdbc_test_redshift.all_types limit 1"
            self.assertEqual((None, ''), scan(sql, 'varchar'))

            sql = "SELECT * FROM jdbc_test_redshift.all_types_1 limit 1"
            self.assertEqual(('test', ''), scan(sql, 'varchar'))

            sql = "SELECT * FROM jdbc_test_redshift.drug_detail limit 1"
            self.assertEqual(("Dr. Reddy's Laboratories Limited", ''),
                             scan(sql, 'manufacturer'))

            sql = "SELECT * FROM jdbc_test_redshift.fact_ae limit 1"
            self.assertEqual(("patient_id", ''), scan(sql, 'patient_id'))

            # TODO: Table is wide and ooms the worker scanning it
            #self.assertEqual(("patient_id", ''),
            #                 scan("SELECT * FROM fact_ae_wide limit 1", 'patient_id'))
            sql = "SELECT * FROM jdbc_test_redshift.healthcare_data limit 1"
            self.assertEqual(("918", ''), scan(sql, 'participants'))

            sql = "SELECT * FROM jdbc_test_redshift.patient limit 1"
            self.assertEqual(("pjaxon0@ifeng.com", ''), scan(sql, 'email'))

            sql = "SELECT * FROM jdbc_test_redshift.user_account_data limit 1"
            self.assertEqual(("auctor.odio@amet.ca", ''), scan(sql, 'email'))

            sql = "SELECT * FROM jdbc_test_redshift.zd1278 limit 1"
            self.assertEqual((None, None), scan(sql, 'src_pcntr_ds'))

    def test_cte_dremio(self):
        self.maxDiff = None
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl("DROP ATTRIBUTE IF EXISTS dremio_test.attr")
            conn.execute_ddl("CREATE ATTRIBUTE dremio_test.attr")

            def rewrite(sql, user=None):
                sql, _, _ = self.cte_rewrite(conn, sql, user=user,
                                             client=TAuthorizeQueryClient.PRESTO)
                return sql

            sql = rewrite("SELECT * FROM jdbc_test_dremio.alltypes_parquet")
            print(sql)
            self.assertEqual(
                'WITH okera_rewrite_jdbc_test_dremio__alltypes_parquet AS '
                '(SELECT "id", "bool_col", "tinyint_col", "smallint_col", "int_col", '
                '"bigint_col", "float_col", "double_col", "date_string_col", "string_col", '
                '"timestamp_col" FROM '
                '"okera.cerebrodata-test"."alltypes_parquet") '
                'SELECT * FROM okera_rewrite_jdbc_test_dremio__alltypes_parquet "alltypes_parquet"',
                sql)

            # Column level permissions
            self._recreate_test_role(conn, 'dremio_test_role', ['dremio_testuser'])
            conn.execute_ddl(
                'GRANT SELECT(bool_col, tinyint_col) ' +
                'ON TABLE jdbc_test_dremio.alltypes_parquet ' +
                'TO ROLE dremio_test_role')
            sql = rewrite("select * from jdbc_test_dremio.alltypes_parquet",
                          user='dremio_testuser')
            print(sql)
            self.assertEqual(
                'WITH okera_rewrite_jdbc_test_dremio__alltypes_parquet AS '
                '(SELECT "bool_col", "tinyint_col" FROM '
                '"okera.cerebrodata-test"."alltypes_parquet") '
                'SELECT * FROM okera_rewrite_jdbc_test_dremio__alltypes_parquet '
                '"alltypes_parquet"',
                sql)

            # Try count(*)
            result = conn.scan_as_json(
                "SELECT count(*) as cnt FROM jdbc_test_dremio.alltypes_parquet",
                requesting_user='dremio_testuser')
            self.assertEqual([{'cnt': 8}], result)

            # Row level permissions
            self._recreate_test_role(conn, 'dremio_test_role', ['dremio_testuser'])
            conn.execute_ddl(
                'GRANT SELECT ON TABLE jdbc_test_dremio.alltypes_parquet ' +
                "WHERE smallint_col = 1 " +
                'TO ROLE dremio_test_role')
            sql = rewrite("SELECT * FROM jdbc_test_dremio.alltypes_parquet",
                          user='dremio_testuser')
            self.assertEqual(
                'WITH okera_rewrite_jdbc_test_dremio__alltypes_parquet AS '
                '(SELECT "id", "bool_col", "tinyint_col", "smallint_col", "int_col", '
                '"bigint_col", "float_col", "double_col", "date_string_col", "string_col", '
                '"timestamp_col" FROM '
                '"okera.cerebrodata-test"."alltypes_parquet" '
                'WHERE "smallint_col" = 1) '
                'SELECT * FROM okera_rewrite_jdbc_test_dremio__alltypes_parquet "alltypes_parquet"',
                sql)

            result = conn.scan_as_json(
                "SELECT * FROM jdbc_test_dremio.alltypes_parquet",
                requesting_user='dremio_testuser')
            self.assertEqual(4, len(result))

            # Loop over all OOB deindentification functions
            conn.execute_ddl('ALTER TABLE jdbc_test_dremio.alltypes_parquet ' +
                             'ADD COLUMN ATTRIBUTE string_col dremio_test.attr')

            for udf, expected in [('mask', 'lpad(\'\', length(("string_col")), \'X\')'),
                                  ('mask_ccn', '(\'XXXX-XXXX-XXXX-\' || substr(("string_col"), length(("string_col"))-3))'),
                                  ('null', "CAST(NULL AS VARCHAR)"),
                                  ('sha2', 'CAST(SHA1(("string_col")) AS STRING)'),
                                  ('tokenize', 'SHA1(("string_col"))'),
                                  ('zero', "''")
                                  ]:
                self._recreate_test_role(conn, 'dremio_test_role', ['dremio_testuser'])
                conn.execute_ddl(
                    ('GRANT SELECT ON TABLE jdbc_test_dremio.alltypes_parquet ' +
                     'TRANSFORM dremio_test.attr WITH `%s`() ' +
                     'TO ROLE dremio_test_role') % udf)
                sql = rewrite("SELECT string_col FROM jdbc_test_dremio.alltypes_parquet",
                              user='dremio_testuser')
                print(udf, sql)
                self.assertEqual(
                    ('WITH okera_rewrite_jdbc_test_dremio__alltypes_parquet AS '
                    '(SELECT %s as "string_col" FROM '
                    '"okera.cerebrodata-test"."alltypes_parquet") '
                    'SELECT "string_col" FROM '
                    'okera_rewrite_jdbc_test_dremio__alltypes_parquet "alltypes_parquet"')
                    % expected, sql)

if __name__ == "__main__":
    unittest.main()
