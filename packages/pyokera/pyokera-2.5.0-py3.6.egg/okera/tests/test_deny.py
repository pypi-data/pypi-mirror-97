# Copyright 2019 Okera Inc. All Rights Reserved.
#
# Some integration tests for DENY policies
#
# pylint: disable=too-many-lines
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-locals

import os
import time
import unittest

import pytest

from okera import _thrift_api
from okera.tests import pycerebro_test_common as common
from okera._thrift_api import TConfigType, TPrivilegeType

TEST_DB = 'deny_test_db'
TEST_TBL = 'tbl'
TEST_ROLE = 'deny_test_role'
TEST_USER = 'deny_test_user'

class DenyTest(common.TestBase):

    @classmethod
    def setUpClass(cls):
        """ Initializes one time state that is shared across test cases. This is used
            to speed up the tests. State that can be shared across (but still stable)
            should be here instead of __cleanup()."""
        super(DenyTest, cls).setUpClass()
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.delete_attribute('deny_test', 'v1')
            conn.create_attribute('deny_test', 'v1')
            conn.delete_attribute('deny_test', 's1')
            conn.create_attribute('deny_test', 's1')

    @staticmethod
    def __cleanup(conn, dbs=None):
        """ Cleanups all the test state used in this test to "reset" the catalog.
            dbs can be specified to do the initialize over multiple databases.
            This can be used for tests that use multiple dbs (but makes the test
            take longer). By default, only load TEST_DB.
        """
        conn.execute_ddl("DROP ROLE IF EXISTS %s" % TEST_ROLE)
        conn.execute_ddl("CREATE ROLE %s" % TEST_ROLE)
        conn.execute_ddl("GRANT ROLE %s to GROUP %s" % (TEST_ROLE, TEST_USER))

        conn.execute_ddl("DROP DATABASE IF EXISTS %s CASCADE" % TEST_DB)
        if not dbs:
            dbs = [TEST_DB]

        for db in dbs:
            conn.execute_ddl("CREATE DATABASE %s" % db)
            conn.execute_ddl("CREATE TABLE %s.%s(col1 int, col2 int, col3 int)" % \
                             (db, TEST_TBL))

            conn.execute_ddl('''
                CREATE EXTERNAL TABLE %s.alltypes(
                  bool_col BOOLEAN,
                  tinyint_col TINYINT,
                  smallint_col SMALLINT,
                  int_col INT,
                  bigint_col BIGINT,
                  float_col FLOAT,
                  double_col DOUBLE,
                  string_col STRING,
                  varchar_col VARCHAR(10),
                  char_col CHAR(5),
                  timestamp_col TIMESTAMP,
                  decimal_col decimal(24, 10))
                ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'
                STORED AS TEXTFILE
                LOCATION 's3://cerebrodata-test/alltypes/'
                ''' % db)

            conn.assign_attribute('deny_test', 'v1', db, 'alltypes', 'int_col')
            conn.assign_attribute('deny_test', 'v1', db, 'alltypes', 'string_col')
            conn.assign_attribute('deny_test', 's1', db, 'alltypes', 'string_col')

    def test_deny_ddl(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self.__cleanup(conn)
            conn.assign_attribute('deny_test', 'v1', TEST_DB, TEST_TBL, 'col1')

            with self.assertRaises(_thrift_api.TRecordServiceException) as ex_ctx:
                conn.execute_ddl(
                    "DENY SELECT ON DATABASE %s FROM ROLE %s" % (TEST_DB, TEST_ROLE))
            self.assertTrue('must specify attribute expression' in str(ex_ctx.exception),
                            msg=str(ex_ctx.exception))

            with self.assertRaises(_thrift_api.TRecordServiceException) as ex_ctx:
                conn.execute_ddl(
                    ("DENY SELECT ON DATABASE %s HAVING ATTRIBUTE %s WHERE %s " +
                     "FROM ROLE %s") % \
                    (TEST_DB, "deny_test.v1", "true", TEST_ROLE))
            self.assertTrue('do not support filters' in str(ex_ctx.exception),
                            msg=str(ex_ctx.exception))

            # This should fail, this user has no privileges
            ctx.enable_token_auth(token_str=TEST_USER)
            with self.assertRaises(_thrift_api.TRecordServiceException) as ex_ctx:
                data = conn.scan_as_json('%s.%s' % (TEST_DB, TEST_TBL))
            self.assertTrue('does not have privilege' in str(ex_ctx.exception),
                            msg=str(ex_ctx.exception))

            # Create a DENY policy
            ctx.disable_auth()
            conn.execute_ddl(
                "DENY SELECT ON DATABASE %s HAVING ATTRIBUTE %s FROM ROLE %s" % \
                (TEST_DB, "deny_test.v1", TEST_ROLE))
            result = conn.execute_ddl("SHOW GRANT ROLE %s" % TEST_ROLE)
            self.assertEqual(len(result), 1)
            self.assertEqual(len(result[0]), 16)
            self.assertTrue(result[0][13])

            # This should fail, this user has no grants, only denys
            ctx.enable_token_auth(token_str=TEST_USER)
            with self.assertRaises(_thrift_api.TRecordServiceException) as ex_ctx:
                data = conn.scan_as_json('%s.%s' % (TEST_DB, TEST_TBL))
            self.assertTrue('does not have privilege' in str(ex_ctx.exception),
                            msg=str(ex_ctx.exception))

            # Grant SELECT on the DB
            ctx.disable_auth()
            conn.execute_ddl(
                "GRANT SELECT ON DATABASE %s TO ROLE %s" % \
                (TEST_DB, TEST_ROLE))

            ctx.enable_token_auth(token_str=TEST_USER)
            data = conn.execute_ddl('describe %s.%s' % (TEST_DB, TEST_TBL))
            print(data)

    def test_restrict_ddl(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self.__cleanup(conn)

            # Negative cases: missing transform and filter
            with self.assertRaises(_thrift_api.TRecordServiceException) as ex_ctx:
                conn.execute_ddl(
                    "RESTRICT SELECT ON DATABASE %s FROM ROLE %s" % (TEST_DB, TEST_ROLE))
            self.assertTrue('RESTRICT privileges must specify' in str(ex_ctx.exception),
                            msg=str(ex_ctx.exception))

            # Having restrict
            conn.execute_ddl(
                "RESTRICT SELECT ON DATABASE %s HAVING ATTRIBUTE %s FROM ROLE %s" % \
                (TEST_DB, "deny_test.v1", TEST_ROLE))
            result = conn.execute_ddl("SHOW GRANT ROLE %s" % TEST_ROLE)
            print(result)
            self.assertEqual(len(result), 1)
            self.assertEqual(len(result[0]), 16)
            self.assertTrue(result[0][13])

            params = _thrift_api.TGetRoleParams()
            params.role_name = TEST_ROLE
            params.include_privilege_props = True
            params.include_role_history = True
            result = conn._underlying_client().GetRole(params)
            role = result.role
            self.assertEqual(len(role.privileges), 1)
            priv = role.privileges[0]
            self.assertEqual(priv.privilege_type, TPrivilegeType.RESTRICT)
            history = result.history
            self.assertTrue(len(history) > 0)

            # History should be ordered (descending chronological order)
            ts = float("inf")
            for e in history:
              self.assertTrue(ts >= e.timestamp_ms)
              ts = e.timestamp_ms

            # Transform restrict
            conn.execute_ddl(
                "RESTRICT SELECT ON DATABASE %s %s FROM ROLE %s" % \
                (TEST_DB, "TRANSFORM deny_test.v1 WITH mask()", TEST_ROLE))
            result = conn.execute_ddl("SHOW GRANT ROLE %s" % TEST_ROLE)
            print(result)
            self.assertEqual(len(result), 2)
            self.assertEqual(len(result[0]), 16)
            self.assertTrue(result[0][13])
            self.assertEqual(len(result[1]), 16)
            self.assertTrue(result[1][13])

            # Filter restrict
            conn.execute_ddl(
                "RESTRICT SELECT ON DATABASE %s WHERE %s FROM ROLE %s" % \
                (TEST_DB, "true", TEST_ROLE))
            result = conn.execute_ddl("SHOW GRANT ROLE %s" % TEST_ROLE)
            self.assertEqual(len(result), 3)
            self.assertEqual(len(result[0]), 16)
            self.assertTrue(result[0][13])
            self.assertEqual(len(result[1]), 16)
            self.assertTrue(result[1][13])
            self.assertEqual(len(result[2]), 16)
            self.assertTrue(result[2][13])

            # Transform and filter
            conn.execute_ddl(
                "RESTRICT SELECT ON DATABASE %s %s WHERE %s FROM ROLE %s" % \
                (TEST_DB, "TRANSFORM deny_test.v1 WITH mask()", "true", TEST_ROLE))
            result = conn.execute_ddl("SHOW GRANT ROLE %s" % TEST_ROLE)
            self.assertEqual(len(result), 4)
            self.assertEqual(len(result[0]), 16)
            self.assertTrue(result[0][13])
            self.assertEqual(len(result[1]), 16)
            self.assertTrue(result[1][13])
            self.assertEqual(len(result[2]), 16)
            self.assertTrue(result[2][13])
            self.assertEqual(len(result[3]), 16)
            self.assertTrue(result[3][13])

            result = conn.execute_ddl_table_output("SHOW GRANT ROLE %s" % TEST_ROLE)
            print(result)

    def test_grant_props(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self.__cleanup(conn)
            props = " POLICYPROPERTIES('name'='me', 'description'='awesome!')"
            conn.execute_ddl("GRANT SELECT ON CATALOG TO ROLE %s %s" % (TEST_ROLE, props))

            params = _thrift_api.TListRolesParams()
            params.role_name_substring = TEST_ROLE
            params.include_privilege_props = True
            roles = conn._underlying_client().ListRoles(params)
            self.assertEqual(len(roles.roles), 1)
            role = roles.roles[0]
            self.assertEqual(len(role.privileges), 1)
            priv = role.privileges[0]
            self.assertEqual(priv.privilege_type, TPrivilegeType.GRANT)
            self.assertEqual(priv.privilege_name, 'server=server1->action=SELECT')
            # ID is auto-generated, it should be there
            self.assertTrue('id' in priv.props)
            id1 = priv.props['id']
            del priv.props['id']
            print(id1)
            self.assertEqual(priv.props, {'name':'me', 'description':'awesome!'})

            # check that getRole API also returns the props
            params = _thrift_api.TGetRoleParams()
            params.role_name = TEST_ROLE
            params.include_privilege_props = True
            role = conn._underlying_client().GetRole(params).role
            self.assertEqual(len(role.privileges), 1)
            priv = role.privileges[0]
            # ID is auto-generated, it should be there
            self.assertEqual(priv.privilege_type, TPrivilegeType.GRANT)
            self.assertTrue('id' in priv.props)
            id2 = priv.props['id']
            del priv.props['id']
            self.assertEqual(priv.privilege_name, 'server=server1->action=SELECT')
            self.assertEqual(priv.props, {'name':'me', 'description':'awesome!'})

            # IDs should match
            self.assertEqual(id1, id2)

            # Another grant, generate new ID
            props = " POLICYPROPERTIES('name'='me2', 'description'='awesome!')"
            conn.execute_ddl("GRANT SELECT ON DATABASE okera_sample TO ROLE %s %s" %\
                (TEST_ROLE, props))
            params = _thrift_api.TListRolesParams()
            params.role_name_substring = TEST_ROLE
            params.include_privilege_props = True
            roles = conn._underlying_client().ListRoles(params)
            self.assertEqual(len(roles.roles), 1)
            role = roles.roles[0]
            self.assertEqual(len(role.privileges), 2)
            priv = role.privileges[0]
            self.assertEqual(priv.privilege_type, TPrivilegeType.GRANT)
            self.assertEqual(priv.privilege_name,
                             'server=server1->db=okera_sample->action=SELECT')
            # ID is auto-generated, it should be there
            self.assertTrue('id' in priv.props)
            id3 = priv.props['id']
            del priv.props['id']
            self.assertEqual(priv.props, {'name':'me2', 'description':'awesome!'})
            self.assertTrue(id1 != id3)

            priv = role.privileges[1]
            self.assertEqual(priv.privilege_type, TPrivilegeType.GRANT)
            self.assertEqual(priv.privilege_name, 'server=server1->action=SELECT')
            # ID is auto-generated, it should be there
            self.assertTrue('id' in priv.props)
            id4 = priv.props['id']
            del priv.props['id']
            self.assertEqual(priv.props, {'name':'me', 'description':'awesome!'})
            self.assertTrue(id1 == id4)

            # Issue an alter
            props = " POLICYPROPERTIES('name'='me3', 'id'='%s')" % id4
            conn.execute_ddl("ALTER %s" % props)

            roles = conn._underlying_client().ListRoles(params)
            self.assertEqual(len(roles.roles), 1)
            role = roles.roles[0]
            self.assertEqual(len(role.privileges), 2)
            priv = role.privileges[1]
            self.assertEqual(priv.privilege_type, TPrivilegeType.GRANT)

            # Should get same ID but different value
            self.assertTrue('id' in priv.props)
            id5 = priv.props['id']
            del priv.props['id']
            self.assertEqual(priv.props, {'name':'me3'})
            self.assertTrue(id4 == id5)

    def test_restrict_filter(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self.__cleanup(conn)

            conn.execute_ddl(
                "RESTRICT SELECT ON DATABASE %s WHERE %s FROM ROLE %s" % \
                (TEST_DB, "int_col = 2", TEST_ROLE))
            conn.execute_ddl(
                "RESTRICT SELECT ON DATABASE %s WHERE %s FROM ROLE %s" % \
                (TEST_DB, "not_a_col = 1", TEST_ROLE))
            data = conn.scan_as_json('%s.alltypes' % TEST_DB)
            self.assertTrue(len(data) == 2)

            # Restricts only, no access granted
            ctx.enable_token_auth(token_str=TEST_USER)
            with self.assertRaises(_thrift_api.TRecordServiceException) as ex_ctx:
                conn.scan_as_json('%s.alltypes' % TEST_DB)
            self.assertTrue('does not have privilege' in str(ex_ctx.exception),
                            msg=str(ex_ctx.exception))

            ctx.disable_auth()
            conn.execute_ddl(
                "GRANT SELECT ON DATABASE %s TO ROLE %s" % \
                (TEST_DB, TEST_ROLE))

            ctx.enable_token_auth(token_str=TEST_USER)
            data = conn.scan_as_json('%s.alltypes' % TEST_DB)
            self.assertTrue(len(data) == 1)
            self.assertTrue(data[0]['int_col'] == 2)

    def test_restrict_redact(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self.__cleanup(conn)

            conn.execute_ddl(
                "RESTRICT SELECT ON DATABASE %s HAVING ATTRIBUTE %s FROM ROLE %s" % \
                (TEST_DB, 'deny_test.v1', TEST_ROLE))
            data = conn.scan_as_json('%s.alltypes' % TEST_DB)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['int_col'], 2)
            self.assertEqual(data[0]['smallint_col'], 1)
            self.assertEqual(data[1]['smallint_col'], 7)

            # Restricts only, no access granted
            ctx.enable_token_auth(token_str=TEST_USER)
            with self.assertRaises(_thrift_api.TRecordServiceException) as ex_ctx:
                conn.scan_as_json('%s.alltypes' % TEST_DB)
            self.assertTrue('does not have privilege' in str(ex_ctx.exception),
                            msg=str(ex_ctx.exception))

            ctx.disable_auth()
            conn.execute_ddl(
                "GRANT SELECT ON DATABASE %s TO ROLE %s" % \
                (TEST_DB, TEST_ROLE))

            ctx.enable_token_auth(token_str=TEST_USER)
            data = conn.scan_as_json('%s.alltypes' % TEST_DB)
            self.assertEqual(len(data), 2)
            print(data)
            self.assertTrue('int_col' not in data[0])
            self.assertTrue('string_col' not in data[0])

    def test_restrict_transform(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self.__cleanup(conn)

            conn.execute_ddl(
                "RESTRICT SELECT ON DATABASE %s TRANSFORM %s WITH %s FROM ROLE %s" % \
                (TEST_DB, 'deny_test.v1', 'tokenize()', TEST_ROLE))
            data = conn.scan_as_json('%s.alltypes' % TEST_DB)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['int_col'], 2)
            self.assertEqual(data[0]['smallint_col'], 1)
            self.assertEqual(data[1]['smallint_col'], 7)

            # Restricts only, no access granted
            ctx.enable_token_auth(token_str=TEST_USER)
            with self.assertRaises(_thrift_api.TRecordServiceException) as ex_ctx:
                conn.scan_as_json('%s.alltypes' % TEST_DB)
            self.assertTrue('does not have privilege' in str(ex_ctx.exception),
                            msg=str(ex_ctx.exception))

            ctx.disable_auth()
            conn.execute_ddl(
                "GRANT SELECT ON DATABASE %s TO ROLE %s" % \
                (TEST_DB, TEST_ROLE))

            ctx.enable_token_auth(token_str=TEST_USER)
            data = conn.scan_as_json('%s.alltypes' % TEST_DB)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['int_col'], 733288971)
            self.assertEqual(data[1]['int_col'], 953486778)
            self.assertEqual(data[0]['smallint_col'], 1)
            self.assertEqual(data[1]['smallint_col'], 7)

    def test_demo_1(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self.__cleanup(conn)

            # Policy grant with tokenize
            conn.execute_ddl(
                "GRANT SELECT ON DATABASE %s EXCEPT TRANSFORM %s WITH %s TO ROLE %s" % \
                (TEST_DB, 'deny_test.s1', 'tokenize()', TEST_ROLE))

            # Should tokenize
            ctx.enable_token_auth(token_str=TEST_USER)
            data = conn.scan_as_json('%s.alltypes' % TEST_DB)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['string_col'], 'yexyi')
            self.assertEqual(data[1]['string_col'], 'gtyjx')

            # Safeguard policy with mask should take precedence
            ctx.disable_auth()
            conn.execute_ddl(
                "RESTRICT SELECT ON CATALOG TRANSFORM %s WITH %s FROM ROLE %s" % \
                ('deny_test.s1', 'mask()', TEST_ROLE))

            # Should mask
            ctx.enable_token_auth(token_str=TEST_USER)
            data = conn.scan_as_json('%s.alltypes' % TEST_DB)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['string_col'], 'XXXXX')
            self.assertEqual(data[1]['string_col'], 'XXXXX')

    def test_demo_2(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self.__cleanup(conn)

            # Safeguard policy with mask should take precedence
            conn.execute_ddl(
                "RESTRICT SELECT ON CATALOG TRANSFORM %s WITH %s FROM ROLE %s" % \
                ('deny_test.s1', 'mask()', TEST_ROLE))

            # Add WHERE filter as a grant
            conn.execute_ddl(
                "GRANT SELECT ON DATABASE %s WHERE %s TO ROLE %s" % \
                (TEST_DB, 'int_col = 2', TEST_ROLE))

            # Should mask and filter
            ctx.enable_token_auth(token_str=TEST_USER)
            data = conn.scan_as_json('%s.alltypes' % TEST_DB)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['string_col'], 'XXXXX')

    def test_demo_3(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self.__cleanup(conn)

            # Add WHERE filter as a grant
            conn.execute_ddl(
                "GRANT SELECT ON DATABASE %s WHERE %s TO ROLE %s" % \
                (TEST_DB, 'true', TEST_ROLE))

            # Should show table
            ctx.enable_token_auth(token_str=TEST_USER)
            data = conn.scan_as_json('%s.alltypes' % TEST_DB)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['string_col'], 'hello')
            tbls = conn.list_datasets(TEST_DB)
            self.assertEqual(len(tbls), 2)

if __name__ == "__main__":
    unittest.main()

