// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

namespace py okera.OkeraRecordService
namespace cpp recordservice
namespace java com.okera.recordservice.ext.thrift

include "RecordService.thrift"

// The supported catalog objects for for which total record count
// can be retrieved. This will be expanded as needed
enum TCatalogObjectType {
  ATTRIBUTE
}

struct TCreateAttributesParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: required list<RecordService.TAttribute> attributes
  2: required string requesting_user
}

struct TCreateAttributesResult {
  1: required list<RecordService.TAttribute> attributes
}

struct TGetAttributesParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: required string requesting_user
  2: optional RecordService.TAttribute filter_attribute
  3: optional i32 offset
  4: optional i32 count

  // If true, only return attributes where this user can edit this attribute
  5: optional bool editable_only
}

struct TGetAttributesResult {
  1: required list<RecordService.TAttribute> attributes
}

struct TGetCountParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: required string requesting_user
  2: required TCatalogObjectType object_type
}

struct TGetCountResult {
  1: required i32 total_count
  2: required bool is_total_count_estimated;
}

struct TAssignAttributesParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: required string requesting_user
  2: required list<RecordService.TAttributeValue> mappings
  3: optional bool if_not_exists

  // If cascade is true, apply the assignment to views dependent on objects
  // referenced in the mappings.
  4: optional bool cascade
}

struct TAssignAttributesResult {
  1: required list<RecordService.TAttributeValue> mappings
}

struct TUnassignAttributesParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: required string requesting_user
  2: required list<RecordService.TAttributeValue> mappings

  // If cascade is true, apply the assignment to views dependent on objects
  // referenced in the mappings.
  3: optional bool cascade
}

struct TSetAttributesParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  // This user needs both ADD_ATTRIBUTE and REMOVE_ATTRIBUTE privileges
  1: required string requesting_user

  // The TAttributeValues that comprise the new attributes set.
  // The database/table/column fields allow a bulk set.
  2: required list<RecordService.TAttributeValue> mappings

  // If cascade is true, apply the assignment to views dependent on objects
  // referenced in the mappings.
  3: optional bool cascade
}

struct TSetAttributesResult {
  // The TAttributeValues that were set
  1: required list<RecordService.TAttributeValue> mappings
}

struct TUpdateAttributeMappingsParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  // This user needs both ADD_ATTRIBUTE and REMOVE_ATTRIBUTE privileges
  1: required string requesting_user

  // The TAttributeValues that are needed to be assigned.
  2: required list<RecordService.TAttributeValue> to_assign

  // The TAttributeValues that are needed to be unassigned.
  3: required list<RecordService.TAttributeValue> to_unassign

  // If cascade is true, apply the update to views dependent on objects
  // referenced in the mappings.
  4: optional bool cascade
}

struct TUpdateAttributeMappingsResult {
  // The numbaer of updated TAttributeValues mappings
  1: required i32 updated_count
}

struct TGetAttributeNamespacesParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: required string requesting_user

  // If true, only return attributes where this user can edit this attribute
  2: optional bool editable_only
}

struct TGetAttributeNamespacesResult {
  1: required list<string> namespaces
}

struct TUnassignAttributesResult {
  1: required i32 unassigned_count
}

struct TDeleteAttributesParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: required string requesting_user
  2: required list<RecordService.TAttribute> attributes

  // By default cascade is true. Meaning all attribute assignments and grants
  // associated to the attribute will be removed. If set to false,
  // only the attributes and assignments will be removed, leaving the grants behind
  3: optional bool cascade
}

struct TDeleteAttributesResult {
  1: required i32 delete_count
  2: required list<RecordService.TAttribute> attributes
}

// Requests access permissions for tables
struct TGetAccessPermissionsParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  // The users (or groups) to query access permissions for.
  1: required list<string> users_or_groups

  // Database to request permissions on
  2: required string database

  // Filter to apply to tables within the database
  3: optional string filter

  // User making the request, if not set, will use the connected user
  4: optional string requesting_user
}

struct TRoleAttributeExpression {
  1: required string role_name
  2: required string expression
}

struct TAccessPermission {
  // The list of users/groups that have this access.
  1: required list<string> users_or_groups

  // For each user/group, the role that granted them this access. Note that it is
  // possible multiple roles granted them this, this returns just one of them.
  2: required list<string> roles

  3: required RecordService.TAccessPermissionLevel level
  4: required bool has_grant
  5: required string database
  6: required string table
  7: required RecordService.TAccessPermissionScope scope

  // The projection that is accessible
  8: optional list<string> projection

  // attribute expression affecting the access permission for the role
  9: optional list<TRoleAttributeExpression> attribute_expression
}

struct TGetAccessPermissionsResult {
  1: required list<TAccessPermission> permissions
  // For every value in users_or_groups from TGetAccessPermissionsParams,
  // a boolean whether it is a user or not
  2: required list<bool> is_user_flags
}

struct TGetGrantableRolesParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: optional string requesting_user

  // If set, checking for grants at this database/table object. If neither is
  // set, it is grants at the catalog scope.
  2: optional string database
  3: optional string table
}

struct TGetGrantableRolesResult {
  1: required list<string> roles
}

struct TExecDDLParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: required string ddl

  // User running the request
  2: optional string requesting_user

  // If set, the default db to use when executing the ddl statement. If not
  // set, the default db is 'default'
  3: optional string defaultdb

  // If set, enable support for bucketed join queries.
  4: optional map<string, string> exec_ddl_options
}

// Result for a DDL statement. Note that none of the fields need to be set for
// DDL that does not return a result (e.g. create table).
struct TExecDDLResult {
  // Set if the result is tabular. col_names is the headers of the table
  // and tabular_result contain the results row by row.
  1: optional list<string> col_names
  2: optional list<list<string>> tabular_result

  // Set if the result is not tabular and should just be output in fixed-width font.
  3: optional string formatted_result

  // Warnings generated while processing this request.
  4: optional list<RecordService.TLogMessage> warnings
}

struct TGetRoleProvenanceParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  // The user to query role provenance for
  1: optional string user
}

struct TRoleProvenance {
  // The name of the role
  1: required string role
  // The list of groups granting this role
  2: required list<string> provenance
}

struct TGetRoleProvenanceResult {
  // The requesting user
  1: required string user
  // The groups this user belongs to
  2: required list<string> groups
  // The roles and provenance this user belongs to
  3: required list<TRoleProvenance> roles

  // Return a set of groups which have access to datasets where this user is admin.
  4: optional set<string> groups_administered
  // Return a set of databases for which this user is admin on at least one datasets
  5: optional set<string> databases_administered

  // Returns the set of attribute namespaces this user has edit and create permissions on
  6: optional set<string> editable_attribute_namespaces
  7: optional set<string> creatable_attribute_namespaces
}

struct TGetAuthenticatedUserResult {
  // Returns the authenticated user name
  1: required string user

  // If set, the credentials used to authenticate this user will expire in
  // this number of milliseconds.
  // If not set, the credentials will not expire.
  2: optional i64 expires_in_ms
}

struct TGetRegisteredObjectsParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: required string prefix_path
  // The user running the request. Can be unset if this should just be the connected
  // user.
  2: optional string requesting_user

  // If true, also return views that are in the catalog over these paths
  3: optional bool include_views
}

struct TGetRegisteredObjectsResult {
  // The list of objects, as fully qualified names. e.g. 'db' or 'db.table' by path.
  1: required map<string, set<string>> object_names
}

struct TGetDatasetsParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  // The user running the request. Can be unset if this should just be the connected
  // user.
  1: optional string requesting_user

  // Returns datasets only in this database
  2: optional list<string> databases

  // If set, only return datasets where the requesting user has these levels of
  // access.
  3: optional list<RecordService.TAccessPermissionLevel> access_levels

  // If set, only match datasets which contain this string
  4: optional string filter

  // List of fully qualified dataset names to return metadata for. Cannot be used
  // with databases and filter.
  10: optional list<string> dataset_names

  // If true, also return the schema for the dataset
  5: optional bool with_schema

  // If true, only return the names of the datasets, with no other metadata
  11: optional bool names_only

  // If true, only do whatever calculation is necessary for the count
  19: optional bool count_only

  // If set, return the full details for the first `full_details_count` and just
  // the names for the remainder. Cannot be used with `names_only`. If not set,
  // returns the full details for all returned datasets.
  13: optional i32 full_details_count

  // Attribute key-namespace-value. Cannot be used with 'dataset_names'
  // If set, only datasets which have these attributes will be returned
  14: optional RecordService.TAttributeValue attribute_value

  // If set, the set of groups to return permissions for. This means that for each dataset
  // returned, the server will return the groups in this list that have some access to
  // those datasets.
  // If not set, the server does not return any group related access information.
  6: optional set<string> groups_to_return_permissions_for

  // Offset and count for pagination. The first `offset` datasets are skipped (after
  // matching filters) and at most `count` are returned. Not that this is not
  // transactional, if datasets get added or removed while paging through them, results
  // will be inconsistent
  7: optional i32 offset
  8: optional i32 count

  // Returns the total matched datasets. This is expected to be used with pagination
  // to return the total count.
  9: optional bool return_total

  15: optional string client_request_id

  // List of attributes (namespace:key) to be filtered (Exact Match).
  // This param is added for advanced filters to have Multi-Tag filter with a mechanism
  // to specify the level of match (DB, Table or Column. Please refer 'attr_match_level.')
  // Note: There is an existing Single-Tag filter (please refer 'attribute_value') which
  // would be deprecated in future.
  16: optional list<RecordService.TAttribute> attributes

  // It specifies level of match (All, DB, Table or Column) in case of attribute filter.
  // If not specified, match attributes at all levels
  // If DATABASE_ONLY, match attributes at DB level only
  // If DATABASE_PLUS, match attributes at DB level and below (i.e. Table and Column also)
  // If TABLE_ONLY, match attributes at Table level only
  // If TABLE_PLUS, match attributes at Table level and below (i.e. Column as well)
  17: optional RecordService.TAttributeMatchLevel attr_match_level

  // Filter to get all the datasets associated with the specified connection.
  // Cannot be used with other filters like dbname pattern, databases, attributes etc.
  18: optional string connection_name
}

struct TGetDatasetsResult {
  1: required list<RecordService.TTable> datasets

  // If 'groups_to_return_permissions_for' is specified in the request, for each
  // dataset in 'datasets', the list of groups with some access to the dataset.
  // i.e. 'groups_with_access[i]' are the groups that have access to 'datasets[i]'
  3: optional list<set<string>> groups_with_access

  // For each dataset in `datasets`, true, if this user is admin on it.
  5: optional list<bool> is_admin

  // For each dataset in `datasets`, true, if it is a public dataset.
  7: optional list<bool> is_public

  // List of datasets that failed to load. The server returns as many of the fields
  // as possible, but some may be unset as they could not load.
  // This list is always disjoint with `datasets.
  2: optional list<RecordService.TTable> failed_datasets

  // Map of databases that failed to load to the error.
  4: optional map<string, RecordService.TRecordServiceException> failed_databases

  // Set if `return_total` was set in the request.
  6: optional i32 total_count
}

// This currently just contains the fields to make this compatible with hive.
struct TUdf {
  1: required string database
  2: required string fn_signature
  3: required string class_name

  // The list of resources required to run this UDF. This can be for example, the list
  // of jars that need to be added that are required for the UDF.
  4: optional list<string> resource_uris
}

struct TGetUdfsParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  // List of databases to return UDFs for. If not set, returns it for all databases.
  1: optional list<string> databases

  // User running the request
  2: optional string requesting_user
}

struct TGetUdfsResult {
  1: list<TUdf> udfs
}

struct TAddRemovePartitionsParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: required bool add           // Otherwise remove
  2: optional list<RecordService.TPartition> partitions

  // User running the request
  3: optional string requesting_user
}

struct TAddRemovePartitionsResult {
  // Number of partitions added or removed
  1: required i32 count
}

enum TListFilesOp {
  LIST,
  READ,
  WRITE,
  GET,
  DELETE,
}

struct TListFilesParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: required TListFilesOp op

  // Either the name of a dataset[db.table] or a fully qualified path
  2: optional string object

  // If set, continue the current list for this request. The other fields
  // are ignored in that case and the parameters from the initial request are used.
  3: optional binary next_key

  // User running the request
  4: optional string requesting_user

  // For underlying file systems that support multiple versions of the same file,
  // the version id to use.
  5: optional string version_id

  // If true, list the files with posix semantics
  6: optional bool posix_semantics

  // If true, only perform authorization for the specified parameters but don't
  // execute the operation.
  7: optional bool authorize_only
}

struct TFileDesc {
  1: required string path
  2: required bool is_directory
  3: optional i64 modified_time_ms
  4: optional i64 len
}

struct TListFilesResult {
  // These can either be signed or paths, depending on the operation. For listing,
  // it is the paths, for the read/write ops, these are signed urls.
  // Either one of these will be set depending on if posix_semantics is set in
  // the request.
  1: optional list<string> files
  3: optional list<TFileDesc> file_descs

  2: optional bool done
}

enum TConfigType {
  AUTOTAGGER_REGEX,
  SYSTEM_CONFIG,
  PROCESS_TRANSIENT_CONFIG,
}

struct TConfigUpsertParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: required TConfigType config_type

  // If empty, null, or not set, this is an insert
  2: optional list<string> key

  3: optional map<string, string> params

  // User making the request, if not set, will use the connected user
  4: optional string requesting_user
}

struct TConfigDeleteParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: required TConfigType config_type
  2: required list<string> key

  // User making the request, if not set, will use the connected user
  3: optional string requesting_user
}

struct TConfigChangeResult {
  1: optional i32 result
  2: optional list<string> warnings
}

enum TInfoType {
  RESERVED_KEYWORDS,
}

struct TGetInfoParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: required TInfoType info
}

struct TGetInfoResult {
  1: optional string result_json
}

struct TLogInfoParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: required TInfoType info

  2: optional string info_json
}

struct TLogInfoResult {
}

struct TAuditQueryParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  1: optional string requesting_user
  2: optional string query
  3: optional string client

  // Datasets accessed by this query. Each dataset should be fully qualified
  // (i.e. db.table)
  4: optional set<string> accessed_datasets

  // Unset if successful
  5: optional string failure_message

  // Standard metrics
  6: optional i64 start_unix_time_ms
  7: optional i64 end_unix_time_ms
  8: optional i64 records_returned

  //
  // Optional metrics
  //
  9: optional i64 bytes_scanned
  // Total time measured by the server ( 7. - 6. is closer to client measured time)
  10: optional i64 server_total_time_ms
  11: optional i64 queue_time_ms
  12: optional i64 planning_time_ms
  13: optional i64 execution_time_ms

  // Optional rewrite info
  14: optional string rewritten_query

  15: optional string client_request_id
}

struct TAuditQueryResult {
}

enum TAuthorizeQueryClient {
  OKERA,
  APACHE_SPARK,
  DATABRICKS_SPARK,
  HIVE,
  IMPALA,
  PRESTO,

  OKERA_CACHE_KEY,
  REST_API,

  // Postgres dialect, not necessarily postgres database
  POSTGRES,
  ATHENA,
  BIG_QUERY,
  SNOWFLAKE,

  // Flag for performance testing
  TEST_ACK,

  // PowerBI/AAS dialect
  DAX,
  MYSQL,
  REDSHIFT,
  DREMIO,
}

struct TAuthorizeQueryParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  // If set, the SQL query to authorize and rewrite
  1: optional string sql

  // If set, the dataset to authorize. If the user has partial access to this
  // dataset, a SQL query for the view over it is returned.
  2: optional RecordService.TDatabaseName db
  3: optional string dataset

  // User making the request, if not set, will use the connected user
  4: optional string requesting_user

  // If true, this request should use session local tables as part of authorizing
  // the query.
  5: optional bool use_session_local_tables

  // If set, the client making the request
  6: optional TAuthorizeQueryClient client

  // If set, the query being executed should only be recorded for audit purposes,
  // no authorization is necessary.
  7: optional bool audit_only = false

  // If true, also generate a plan that's able to execute the rewritten SQL by
  // ODAS workers, i.e. the same result structure as would come from PlanRequest()
  13: optional bool plan_request

  // The privilege level for this request. If not set, SELECT is assumed.
  8: optional RecordService.TAccessPermissionLevel privilege_level

  // If set, this is the records to authorize. This is used for privilege_levels like
  // create to authorize the data. The records must be json serialized.
  // This is a batched API and each element of this array is a json object aka record.
  9: optional list<string> records

  // If true, returrn the result records as a list of json records. Otherwise, this
  // just returns the list of booleans or records that pass the filter.
  15: optional bool return_records

  // If set, rewrite this query using common table expression cte. This can only be
  // used if 'sql' is set.
  10: optional bool cte_rewrite

  // If set, the tables referenced for cte_rewrite. If not set, the server will try
  // to figure it out.
  11: optional set<string> referenced_tables

  // If set, the Okera database to use to get connection info. This is used when
  // rewriting for RDBMS pushdown.
  // TODO: this is not the right way, we need another connection id identifier
  // when that is all complete.
  12: optional string connection_db

  14: optional string client_request_id

  // If set, the filter that should be added (AND semantics) to any configured by
  // policies.
  16: optional string request_filter

  // If true, ignore authorizing the query if the table is unknown
  17: optional bool ignore_unknown_tables

  // If set, the default database to use when analyzing the queries
  18: optional string default_db
}

enum TCompoundOp {
  AND,
  OR
}

struct TAuthorizeQueryFilters {
  1: required list<string> filters
  2: required TCompoundOp op
}

struct TColumnAccess {
  // If true, the user has access to this column, false means no access
  1: bool accessible
}

struct TAuthorizeQueryResult {
  1: optional string result_sql
  // Schema for result sql
  3: optional RecordService.TSchema result_schema

  // The plan, if requested and runnable by ODAS workers
  9: optional RecordService.TPlanRequestResult plan

  // Only set if the request specified db/dataset name. If true, then this user
  // has full access to this dataset.
  2: optional bool full_access

  // Set if this request cannot be bypassed and must go through the workers to
  // generate the results. Examples where this is true is if the query queries
  // a JDBC data source or uses a function that is unique to us.
  4: optional bool requires_worker

  // Set if request was a dataset and the user has access to all columns.
  // This will return the full metadata, to enable the caller to access directly.
  5: optional RecordService.TTable table

  // Set if access to this dataset requires a filter. This will also be part
  // of result_sql but broken out to facilitate composition
  6: optional string filter

  // Pre-composed filters that need to be added to access the dataset. The
  // result in 'filter' is the toSQL() version of this. Splitting this up
  // is convenient for callers so they don't need to parse SQL.
  13: optional TAuthorizeQueryFilters filters

  // Set if this filter can be expressed as a set of values with "in" semantics.
  // e.g. if the filter is a = 1 or a = 2 or a in [3, 4], this would return
  // { a: [1, 2, 3, 4] }
  8: optional map<string, set<string>> filtered_values

  // if data_payload_json was set, for each record, true if the record passed the
  // filter and false otherwise.
  7: optional list<bool> filtered_records

  // Set if return_records is true. This returns the results post transformations
  // and filters.
  12: optional list<string> result_records

  // For rewritten queries, example JDBC pushdown queries, we need to
  // also pass the jdbc_connection_id of the data source we are connecting to execute
  // the full pushdown query. This value will be set in the SessionState along with the
  // temporary jdbc view with the CTE query in it.
  10: optional i32 jdbc_connection_id

  // If set, the tables referenced for cte_rewrite. This is passed to the caller (proxy),
  // in order to populate the audit logs with this info.
  // TODO: Remove this
  11: optional set<string> referenced_tables

  // If set, the columns, specified as the field path, that this user is allowed to
  // see. If not set, the user can see all columns
  14: optional map<string, TColumnAccess> column_access
}

struct TRefreshCredentialsParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  // Task to refresh credentials for
  1: required binary task

  // Optional duration to resign this task for. If not specified, the server will
  // pick.
  2: optional i64 duration_sec
}

struct TRefreshCredentialsResult {
  // Result signed task
  1: required binary task

  // Unix timestamp that this task will expire in
  2: required i64 expire_time_unix_sec
}

/**
 * Represents one data registration connection management request.
 */
struct TDataRegConnectionParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  /**
   * The requesting user.
   */
  1: required string requesting_user
  /**
   * Type of operation for the data registration connection management.
   */
  2: required RecordService.TObjectOpType op_type
  /**
   * The connection object to be managed. Note, for list/search operations, this can be
   * set as a empty object.
   */
  3: required RecordService.TDataRegConnection connection
  /**
   * Valid list of connection names which can be used to retrieve multiple connection
   * objects. If this list and the `connection_pattern` are empty, all data registration
   * connections are returned from the storage.
   */
  4: optional list<string> connection_names
  /**
   * A connection pattern (string) for which matching data registration connection
   * records are returned. If the `connection_names` list is provided, it takes precedence
   * over this search pattern.
   */
  5: optional string connection_pattern
}

/**
 * Represents data registration connection management response.
 */
struct TDataRegConnectionResult {
  /**
   * Returns the list of connections as response. Below are some sample responses:<br/><br/>
   * <i>ManageDataRegConnection::CREATE</i>: A single record list with the
   * created data registration connection.<br/><br/>
   * <i>ManageDataRegConnection::UPDATE</i>:
   * A single record list with the updated data registration connection.<br/><br/>
   * <i>ManageDataRegConnection::DELETE</i>: this will be an empty list.<br/><br/>
   * <i>ManageDataRegConnection::GET</i> (by connection name):
   * A single data registration connection record list.<br/><br/>
   * <i>ManageDataRegConnection::LIST</i> (by `connection_names`):
   * List of the filtered data registration connections.<br/><br/>
   * <i>ManageDataRegConnection::LIST</i> (by `connection_pattern`):
   * List of the matching data registration connections.
   */
  1: required list<RecordService.TDataRegConnection> connections
  /**
   * Optionally return the total number of records found by the filter or search criteria.
   */
  2: optional i32 count
}

/**
 * Represent the Discovery APIs for crawling a source using a specific connection.
 * For JDBC, use this to peek, the catalogs, schemas, tables, and columns.
 */
struct TDiscoverCrawlerParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  /**
   * The requesting user.
   */
  1: optional string requesting_user
  /**
   * The connection for which this crawler discovery needs to happen.
   */
  2: required RecordService.TDataRegConnection connection
  /**
   * If connection is of type JDBC, option to browse the catalog.
   */
  3: optional string jdbc_catalog
  /**
   * If connection is of type JDBC, option to browse the schema under the catalog.
   */
  4: optional string jdbc_schema
}

/**
 * Represents crawler management response.
 */
struct TDiscoverCrawlerResult {
  /**
   * If crawler type is S3/ADLS, the list of paths discovered under the path identified in
   * the connection passed in the <i>TDiscoverCrawlerParams</i> request.
   * If crawler type is JDBC, the list of JDBC discovered datasets. Based on the call,
   * this object will vary in information.<br/><br/>
   * For example,<br/>
   * If the <i>TDiscoverCrawlerParams</i> does not specify a JDBC catalog, this will
   * return the list of the catalog names under the JDBC data source identified by<br/>
   * the connection and no other information.<br/><br/>
   * If the <i>TDiscoverCrawlerParams</i> specifies a jdbc_catalog
   * and empty list of `jdbc_schemas`,<br/>
   * the response will be a list of JDBC schema names under the JDBC catalog specified.<br/><br/>
   * If the <i>TDiscoverCrawlerParams</i> specifies a jdbc_catalog
   * and also specifies a list of `jdbc_schemas`,<br/>
   * the response will be a list of JDBC tables info (in form of list of <i>TJDBCDataset</i>).<br/><br/>
   * Caution: this can be a slow responding API, if 100s of schemas are specified in the
   * `jdbc_schemas` list or if the JDBC data source has 1000s of tables under the schema.
   */
  1: required list<RecordService.TCrawlerDiscoveryDataset> crawler_discover_datasets
  /**
   * Optionally return the total number of datasets being discovered.<br/>
   * Note, this can be tentative as and when objects are discovered for crawling.
   */
  2: optional i32 count
}

/**
 * Represents crawler management request.
 */
struct TCrawlerParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  /**
   * The requesting user.
   */
  1: required string requesting_user
  /**
   * Type of operation on the data registration crawler.
   * Below are some combinations supported for
   * <i>ManageCrawler</i> service call, with operation:<br/><br/>
   * For <i>ManageCrawler::CRAWL</i> operation: Crawl the datasets
   * in the `crawl_datasets` list (or)<br/> for all the datasets
   * discovered for the crawler (if `is_crawl_all` is true).<br/><br/>
   * For <i>ManageCrawler::RECRAWL</i> operation: Recrawl the datasets
   * in the `crawl_datasets` list (or)<br/> for all the datasets
   * discovered for the crawler (if `is_crawl_all` is true).<br/>
   * Note, this will delete all the previous crawler dataset status.<br/> Not the
   * registered datasets, but just the status.<br/><br/>
   * For <i>ManageCrawler::DISABLE</i> operation:
   * this will disable the datasets crawling for the `crawl_datasets` list (or)<br/>
   * for all datasets under the crawler.<br/><br/>
   * For <i>ManageCrawler::DELETE</i> operation,
   * this will delete crawler along with all datasets crawling under this.<br/>
   */
  2: required RecordService.TCrawlerOpType op_type
  /**
   * The connection for which this crawler is setup.
   */
  3: required RecordService.TDataRegConnection connection
  /**
   * The list of <i>TDataRegCrawlDataset</i> objects representing the datasets to be crawled.
   */
  4: optional list<RecordService.TDataRegCrawlDataset> crawl_datasets
  /**
   * Specify whether to crawl all datasets for the crawler.<br/>
   */
  5: optional bool is_crawl_all = false
  /**
   * Specify if crawling should be processed asynchronously.<br/>
   * Note, for crawling more than 20 datasets, automatically, the crawler will be
   * processed asynchronous.
   */
  6: optional bool is_asynchronous = false
}

/**
 * Represents crawler management response.
 */
struct TCrawlerResult {
  /**
   * The collective crawler status for all the datasets submitted for crawling.<br/><br/>
   * If crawling synchronously, this would return
   * <i>TCrawlStatus.SUCCESS</i> or <i>TCrawlStatus.FAILURE</i><br/>
   * based on if crawling on all datasets succeeded (or)
   * if there was failure for crawling on at least one dataset.<br/><br/>
   * If crawling asynchronously, this would return <i>TCrawlStatus.CRAWLING</i><br/>
   * indicating the crawling will be processed asynchronously.
   */
  1: required RecordService.TCrawlStatus status
  /**
   * Optionally return the total number of datasets being crawled.<br/> Note, this can be
   * tentative as and when objects are discovered for crawling.
   */
  2: optional i32 count
}

/**
 * Represents crawler dataset management request. This is mostly to list and optionally
 * manage crawler datasets.
 */
struct TCrawlDatasetParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  /**
   * The requesting user.
   */
  1: required string requesting_user
  /**
   * Type of operation on the data registration crawler datasets.
   * Below are some combinations supported for
   * <i>ManageCrawlerDataset</i> service call, with operation:<br/><br/>
   * For <i>ManageCrawlerDataset::LIST</i> operation::
   * the `crawl_datasets` would be empty, to get the list of dataset crawler status.
   * Note, connection is required for the <i>LIST</i> of crawler datasets operation.<br/><br/>
   * For <i>ManageCrawlerDataset::DISABLE</i> operation:
   * this will disable the datasets in the `crawl_datasets` list<br/><br/>
   * Note, <i>CREATE/UPDATE/DELETE/GET/SEARCH</i> operations on crawler datasets
   * would not work for this call.
   */
  2: required RecordService.TObjectOpType op_type
  /**
   * The connection using which we would want to list the crawler datasets.
   */
  3: required RecordService.TDataRegConnection connection
  /**
   * The list of <i>TDataRegCrawlDataset</i> objects representing the crawler datasets.
   */
  4: optional list<RecordService.TDataRegCrawlDataset> crawl_datasets
}

/**
 * Represents crawler dataset management response.
 */
struct TCrawlDatasetResult {
  /**
   * Type of operation on the data registration crawler datasets.
   * Below are some combinations supported for
   * <i>ManageCrawlerDataset</i> service call, with operation:<br/><br/>
   * For <i>ManageCrawlerDataset::LIST</i> operation::
   * the `crawl_datasets` would be the list of dataset crawler.
   * Note, connection is required for the <i>LIST</i> of crawler datasets operation.<br/><br/>
   * For <i>ManageCrawlerDataset::DISABLE</i> operation: NO-OP for success,
   * TRecordServiceException for failure.<br/>
   */
  1: optional list<RecordService.TDataRegCrawlDataset> crawl_datasets
  /**
   * Optionally return the total number of datasets being crawled.<br/> Note, this can be
   * tentative as and when objects are discovered for crawling.
   */
  2: optional i32 count
}

/**
 * Represents a struct to List catalogs.
 */
struct TListCatalogsParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  /**
   * The requesting user.
   */
  1: optional string requesting_user
}

/**
 * Represents a struct to List databases.
 */
struct TListDatabasesParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  /**
   * The requesting user.
   */
  1: optional string requesting_user
  /**
   * List of db names to be filtered (Exact Match).
   */
  2: optional list<string> db_names
  /**
   * match only those databases that match the pattern string.
   */
  3: optional string db_name_pattern
  /**
   * List of attributes to be filtered (Exact Match).
   */
  4: optional list<RecordService.TAttribute> attributes
  /**
   * List of permission levels to be filtered
   */
  5: optional list<RecordService.TAccessPermissionLevel> access_levels
  /**
   * This field represents sorting information (list of columns and sort order)
   */
  6: optional list<RecordService.TSortColOrder> sorting_info
  /**
   * Flag to indicate wheter to ignore internal dbs or not
   */
  7: optional bool ignore_internal_dbs = true
  /**
   * How many objects to return at most (count per page)
   */
  8: optional i64 limit = 10
  /**
   * It specifies the token corresponding to the page to be displayed.
   * If not defined, it indicates 'first page'
   */
  9: optional string page_token
  /**
   * It specifies level of match (All, DB, Table or Column) in case of attribute filter.
   * If not specified, match attributes at all levels
   * If DATABASE_ONLY, match attributes at DB level only
   * If DATABASE_PLUS, match attributes at DB level and below (i.e. Table and Column also)
   * If TABLE_ONLY, match attributes at Table level only
   * If TABLE_PLUS, match attributes at Table level and below (i.e. Column as well)
   * and so on
   */
  10: optional RecordService.TAttributeMatchLevel attr_match_level
}

/**
 * Represents List Catalogs Response
 */
struct TListCatalogsResult {
  /**
   * List of Catalogs
   */
  1: required list<RecordService.TOkeraCatalog> catalogs
}

/**
 * Represents List Databases Response
 */
struct TListDatabasesResult {
  /**
   * List of Databases
   */
  1: required list<RecordService.TDatabase> databases
  /**
   * Pointer to next page. null if this is the last page
   */
  2: optional string prev_page_token
  /**
   * Pointer to previous page. null if this is the first page
   */
  3: optional string next_page_token
  /**
   * Number of databases the requesting user has access to.
   */
  4: optional i64 total_count
}

/**
 * Represents a struct of parameters to List roles.
 * Each parameter can be set (except for some mutually exclusive ones, see below)
 * and reduces the result set.
 */
struct TListRolesParams {
  // Context metadata for the request.
  100: optional RecordService.TRequestContext ctx

  // User running the request
  1: optional string requesting_user

  // Substring match against role name
  2: optional string role_name_substring

  // Substring to match against granted group names
  3: optional string group_name_substring

  /**
   * SCOPE FILTERS
   * Note: only *one* of options 4,5 can be set.
   */
  // If set, only return roles having at least one privilege with a
  // scope in this list.
  4: optional list<RecordService.TAccessPermissionScope> scopes
  // If set, only return roles having at least one privilege granted
  // directly to an object in this list of fully-qualified catalog object names.
  // e.g. for a database: ["okera_sample"], or for a table: ["okera_sample.sample"]
  5: optional list<string> catalog_object_names

  // If set, only return roles that have been granted to this user
  6: optional string target_user

  // How many roles to return at most
  7: optional i64 limit = 10

  // If set, return a specific page of results. If not set, return the first page.
  8: optional string page_token

  // If set, return only the roles that are manageable, ie user in question has
  // any permission on these roles.
  9: optional bool manageable_only

  // If true, return kv properties associated with each grant
  10: optional bool include_privilege_props

  // If set, return only the roles having at least one privilege granted
  // with access levels in this list
  11: optional list<RecordService.TAccessPermissionLevel> levels
}

// Represents a result set for a ListRoles call
struct TListRolesResult {
  // The list of roles matching the request filters
  1: required list<RecordService.TRole> roles

  // The identifier for the previous page of results
  2: optional string prev_page_token

  // The identifier for the next page of results
  3: optional string next_page_token

  // The total count across all pages. Not set if count is unknown.
  4: optional i64 total_count
}

// Represent parameters for a GetRole call
struct TGetRoleParams {
  // Context metadata for the request
  100: optional RecordService.TRequestContext ctx

  // The name of the role to retrieve
  1: required string role_name

  // User running the request
  2: optional string requesting_user

  // If true, return kv properties associated with each grant
  3: optional bool include_privilege_props

  // If true, return the history for this role
  4: optional bool include_role_history
}

// Represents a history event for an object
struct THistoryEvent {
  // Millis since unix epoch
  1: required i64 timestamp_ms
  2: required string user
  3: required string operation
  4: optional string detail
}

// Represents a result for a GetRole call
struct TGetRoleResult {
  // The role requested
  1: required RecordService.TRole role

  // Returned iff include_role_history is set.
  2: optional list<THistoryEvent> history
}

// KV get/put
struct TKvStoreGetParams {
  100: optional RecordService.TRequestContext ctx

  1: required string key
}

struct TKvStoreGetResult {
  1: optional string value
}

struct TKvStorePutParams {
  100: optional RecordService.TRequestContext ctx

  1: required string key
  2: optional string value
}

struct TKvStorePutResult {
}

struct TGetUserAttributesParams {
  // Context metadata for the request
  100: optional RecordService.TRequestContext ctx

  // The effective user who submitted this request.
  2: optional string requesting_user

  // Whether to return user attributes for all users.
  // Only valid for admins.
  3: optional bool all_users

  // A specific user to return user attributes for.
  // Only admins can set it to a user other than themselves.
  4: optional string user
}

struct TUserAttributeValue {
  // The actual value
  1: required string value
  // The source it come from (e.g. LDAP, Script, etc)
  2: required string source
}

struct TGetUserAttributesResult {
  // A map representing the requested user attributes
  1: required map<string, map<string, TUserAttributeValue>> attributes
}

// Okera extensions to the RecordServicePlanner API
service OkeraRecordServicePlanner extends RecordService.RecordServicePlanner {
  // Returns the access permissions for tables.
  TGetAccessPermissionsResult GetAccessPermissions(1: TGetAccessPermissionsParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns role provenance for a user
  TGetRoleProvenanceResult GetRoleProvenance(1: TGetRoleProvenanceParams params)
    throws(1:RecordService.TRecordServiceException ex);

  // Returns the roles that is grantable for this user on this object
  TGetGrantableRolesResult GetGrantableRoles(1: TGetGrantableRolesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Executes a ddl command against the server, returning the results (if it produces
  // results).
  list<string> ExecuteDDL(1:TExecDDLParams ddl)
      throws(1:RecordService.TRecordServiceException ex);

  TExecDDLResult ExecuteDDL2(1:TExecDDLParams ddl)
      throws(1:RecordService.TRecordServiceException ex);

  // This will register aliases for 'user'. When the 'user' access path, it will
  // resolve to 'table'. If view is non-empty, a view will created for the user and
  // whenever the user access 'path' or 'table', it will resolve to the view.
  string RegisterAlias(1:string user, 2:string table, 3:string path, 4:string view)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the authenticated user from the user's token.
  TGetAuthenticatedUserResult AuthenticatedUser(1:string token)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the datasets. This is similar to RecordServicePlanner.GetTables() but
  // version2, which matches more advanced usage patterns better.
  TGetDatasetsResult GetDatasets(1:TGetDatasetsParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the UDFs that have been registered. Note that this does not include
  // builtins, only functions explicilty registered by the user.
  TGetUdfsResult GetUdfs(1:TGetUdfsParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Adds or remove partitions in bulk
  TAddRemovePartitionsResult AddRemovePartitions(1:TAddRemovePartitionsParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the list of files specified in the params. This provides a file system
  // like interface.
  TListFilesResult ListFiles(1:TListFilesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the catalog objects registered for a given path prefix
  TGetRegisteredObjectsResult GetRegisteredObjects(1: TGetRegisteredObjectsParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Creates the attributes
  TCreateAttributesResult CreateAttributes(1:TCreateAttributesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the list of attributes for the given filter
  // If no filter specified, returns the first 25 attributes sorted alphabetically
  TGetAttributesResult GetAttributes(1: TGetAttributesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the count of total records for the given object type
  // If the count is greater than max allowed, an estimated count is returned
  TGetCountResult GetRecordCount(1: TGetCountParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Assigns attributes to objects. The object can be database/table/column
  TAssignAttributesResult AssignAttributes(1: TAssignAttributesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Removes attribute values from objects. The object can be database/table/column
  TUnassignAttributesResult UnassignAttributes(1: TUnassignAttributesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Deletes the list of attributes
  TDeleteAttributesResult DeleteAttributes(1: TDeleteAttributesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns a list of unique attribute namespaces
  TGetAttributeNamespacesResult GetAttributeNamespaces(
      1: TGetAttributeNamespacesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Idempotently sets attributes to objects
  TSetAttributesResult SetAttributes(1: TSetAttributesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Updates attributes mappings
  TUpdateAttributeMappingsResult UpdateAttributeMappings(
      1: TUpdateAttributeMappingsParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // CRUD for a configuration
  TConfigChangeResult UpsertConfig(1: TConfigUpsertParams params)
      throws(1:RecordService.TRecordServiceException ex);
  TConfigChangeResult DeleteConfig(1: TConfigDeleteParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Get system information from the server
  TGetInfoResult GetInfo(1: TGetInfoParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Log diagnostic information from the client. This does not change any server
  // state or behavior.
  TLogInfoResult LogInfo(1: TLogInfoParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Authorizes a query, returning the appropriate query for this requesting user
  // or an error
  TAuthorizeQueryResult AuthorizeQuery(1: TAuthorizeQueryParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Refresh the credentials for this task.
  // Note that the user does not need to be authencited to call this API and the
  // payload in params provides trust.
  TRefreshCredentialsResult RefreshCredentials(1: TRefreshCredentialsParams params)
      throws(1:RecordService.TRecordServiceException ex);

  /**
   * A service to manage data registration connections.
   */
  TDataRegConnectionResult ManageDataRegConnection(1: TDataRegConnectionParams params)
      throws(1:RecordService.TRecordServiceException ex);

  /**
   * A service to discover crawler.
   */
  TDiscoverCrawlerResult DiscoverCrawler(1: TDiscoverCrawlerParams params)
      throws(1:RecordService.TRecordServiceException ex);

  /**
   * A service to manage crawler.
   */
  TCrawlerResult ManageCrawler(1: TCrawlerParams params)
      throws(1:RecordService.TRecordServiceException ex);

  /**
   * A service to manage crawler dataset.
   */
  TCrawlDatasetResult ManageCrawlerDataset(1: TCrawlDatasetParams params)
      throws(1:RecordService.TRecordServiceException ex);

  /**
   * Generate an audit entry
   */
  TAuditQueryResult AuditQuery(1: TAuditQueryParams params)
      throws(1:RecordService.TRecordServiceException ex);

  /**
   * A service to list the catalogs
   */
  TListCatalogsResult ListCatalogs(1: TListCatalogsParams params)
      throws(1:RecordService.TRecordServiceException ex);

  /**
   * A service to list the Databases
   */
  TListDatabasesResult ListDatabases(1: TListDatabasesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  TListRolesResult ListRoles(1: TListRolesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  TGetRoleResult GetRole(1: TGetRoleParams params)
      throws(1:RecordService.TRecordServiceException ex);

  TKvStoreGetResult GetFromKvStore(1: TKvStoreGetParams params)
      throws(1:RecordService.TRecordServiceException ex);

  TKvStorePutResult PutToKvStore(1: TKvStorePutParams params)
      throws(1:RecordService.TRecordServiceException ex);

  TGetUserAttributesResult GetUserAttributes(1: TGetUserAttributesParams params)
      throws(1:RecordService.TRecordServiceException ex);
}
