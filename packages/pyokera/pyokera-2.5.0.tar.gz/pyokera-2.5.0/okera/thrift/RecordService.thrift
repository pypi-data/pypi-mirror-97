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

namespace py okera.RecordService
namespace cpp recordservice
namespace java recordservice.thrift

//
// This file contains the service definition for the RecordService which consists
// of two thrift services: RecordServicePlanner and RecordServiceWorker.
//

// Version used to negotiate feature support between the server and client. Both
// clients and servers need to maintain backwards compatibility.
typedef string TProtocolVersion

// 128-bit GUID.
struct TUniqueId {
  1: required i64 hi
  2: required i64 lo
}

// Network address which specifies the machine, typically used to schedule where
// tasks run.
struct TNetworkAddress {
  1: required string hostname
  2: required i32 port
}

struct TServerVersion {
  1: optional string version
  2: optional string build_time
  3: optional string build_hash
}

struct TInitApplicationParams {
  1: required string application
}

struct TInitApplicationResult {
  // Protocol version of the server
  1: required TProtocolVersion protocol_version

  // The authenticated user on the network connection
  2: required string authenticated_user
}

// The supported datatypes for attribute values
// NOTE: This should be in sync with AttributeValueType.java
enum TAttributeValueType {
  BOOLEAN,
  STRING
}

/**
 * Types of CRUD and other operations on an object. Reduces the number of RPCs needed to
 * manage a backend object.
 */
enum TObjectOpType {
  CREATE,
  UPDATE,
  DELETE,
  GET,
  LIST,
  SEARCH,
  TEST_CREATE,
  TEST_EDIT,
  TEST_EXISTING
}

// Represents "TEST CONNECTION" status.
// New values can be added when required
enum TTestStatus {
  SUCCESS,
  FAILED
}

/**
 * Represents the various crawler operations.
 */
enum TCrawlerOpType {
  CRAWL,
  RECRAWL,
  DISABLE,
  DISCOVER
}

enum TPrivilegeType {
  GRANT,
  RESTRICT,
}

/**
 * Do not change the order of the enums, add them at the end.
 */
enum TAccessPermissionLevel {
  ALL,
  ALTER,
  CREATE,
  CREATE_AS_OWNER,
  INSERT,
  SELECT,
  SHOW,
  ADD_ATTRIBUTE,
  REMOVE_ATTRIBUTE,
  VIEW_AUDIT,
  VIEW_COMPLETE_METADATA,
  DELETE,
  UPDATE,
  DROP,
  CREATE_ROLE_AS_OWNER,
  MANAGE_GRANTS,
  MANAGE_PERMISSIONS,
  MANAGE_GROUPS,
  CREATE_CRAWLER_AS_OWNER,
  CREATE_DATACONNECTION_AS_OWNER,
  USE
}

/**
 * enum for Access Permission Scope
 */
enum TAccessPermissionScope {
  SERVER,
  URI,
  DATABASE,
  TABLE,
  COLUMN,
  ATTRIBUTE_NAMESPACE,
  ROLE,
  CRAWLER,
  DATACONNECTION,
}

/**
 * Various crawler status. Note this status is preserved per dataset for the crawler.
 */
enum TCrawlStatus {
  /**
   * If crawling was successful for a dataset.
   */
  SUCCESS,
  /**
   * If crawling was failure for a dataset.
   */
  FAILURE,
  /**
   * When submitted for asynchronous crawling, indicates crawling is in progress.
   */
  CRAWLING
}

/**
 * Enum to specify level of match (All, DB, Table or Column) in case of attribute filter.
 */
enum TAttributeMatchLevel {
  /**
   * If SERVER_ONLY, match attributes at SERVER level only
   * This is for future. We don't have attributes at SERVER (CATALOG) level as of now.
   */
  SERVER_ONLY,
  /**
   * If SERVER_PLUS, match attributes at SERVER level and below (i.e. db, table, column)
   * This is for future. We don't have attributes at SERVER (CATALOG) level as of now.
   */
  SERVER_PLUS,
  /**
   * If DATABASE_ONLY, match attributes at DB level only
   */
  DATABASE_ONLY,
  /**
   * If DATABASE_PLUS, match attributes at DB level and below (i.e. Table and Column also)
   */
  DATABASE_PLUS,
  /**
   * If TABLE_ONLY, match attributes at Table level only
   */
  TABLE_ONLY,
  /**
   * If TABLE_PLUS, match attributes at Table level and below (i.e. Column as well)
   */
  TABLE_PLUS,
  /**
   * If COLUMN_ONLY, match attributes at Column level only
   */
  COLUMN_ONLY
}

struct TAttribute {
  1: required string key

  // The datatype for the value of the key
  // If no value_type is specified, STRING is used as default
  2: optional TAttributeValueType value_type

  // The key is unique within a namespace
  // If no namespace is specified, 'default' is used
  3: optional string attribute_namespace

  4: optional string description

  5: optional bool is_system

  6: optional string created_by

  // The application that created the attribute
  // Ex: autotagger, UI
  7: optional string user_agent

  // ID that can be used to lookup this attribute
  // in okera_system.attributes
  8: optional i32 id
}

struct TAttributeValue {
  1: required TAttribute attribute

  2: required string value

  // Attributes can be assigned to database/table/column
  // If column specified, table and db are required
  // If table specified db required
  3: optional string database

  4: optional string table

  5: optional string column

  // If this is set to true, the ABAC rules (if any) on
  // the attribute, will be applied to the catalog object
  // By default this is treated as false
  6: optional bool is_active

  7: optional string created_by

  // The application that created the attribute
  // Ex: autotagger, UI
  8: optional string user_agent

  // If generated by a rule, the ID for that rule.
  9: optional i32 rule_id
}

// Types support by the RecordService.
enum TTypeId {
  // Boolean, true or false
  BOOLEAN,

  // 1-byte (signed) integer.
  TINYINT,

  // 2-byte (signed) integer.
  SMALLINT,

  // 4-byte (signed) integer.
  INT,

  // 8-byte (signed) integer.
  BIGINT,

  // ieee floating point number
  FLOAT,

  // ieee double precision floating point number
  DOUBLE,

  // Variable length byte array.
  STRING,

  // Variable length byte array with a restricted maximum length.
  VARCHAR,

  // Fixed length byte array.
  CHAR,

  // Fixed point decimal value.
  DECIMAL,

  // Timestamp with nanosecond precision.
  TIMESTAMP_NANOS,

  // Type for nested schemas. For example, if the data type was:
  // RECORD person {
  //   STRING first_name;
  //   STRING last_name;
  // }
  // This would consist of a schema with 3 columns: person, first_name, last_name.
  // The type of person would be RECORD
  RECORD,

  // Array of another type, which can be any type. This type always has one child.
  ARRAY,

  // A map of STRING to any type. This type always has two children.
  MAP,

  // This would be used only for JDBC and that too for the purpose of translating
  // Java.SQL.Binary/Blob types to Okera types. RS does not support BINARY completely
  // and eventually the BINARY types are treated as STRING. This should not have
  // any impact on the clients until we have coded handlers there. So safe to introduce.
  BINARY,

  // Date value.
  DATE,

  // To be used to bubble up conversion errors.
  UNSUPPORTED,
}

// Type specification, containing the enum and any additional parameters the type
// may need.
struct TColumnType {
  1: required TTypeId type_id

  // Only set if id == DECIMAL
  2: optional i32 precision
  3: optional i32 scale

  // Only set if id == VARCHAR or CHAR
  4: optional i32 len

  // Set iff this type is RECORD, for nested schemas
  5: optional i32 num_children
}

// A description for a column in the schema.
struct TColumnDesc {
  1: required TColumnType type
  2: required string name

  // If true, this column is a partitioning column
  3: optional bool is_partitioning_col

  // If true, this column is not accessible to this user
  4: optional bool hidden

  5: optional string comment

  6: optional list<TAttributeValue> attribute_values
}

// Representation of a RecordServiceSchema.
struct TSchema {
  // Pre-order traversal of the schema.
  1: required list<TColumnDesc> cols
  2: required bool is_count_star = false
  3: optional list<TColumnDesc> nested_cols
}

// Record serialization formats.
enum TRecordFormat {
  // Serialized columnar data. Each column is a contiguous byte buffer to minimize
  // serialization costs.
  // The serialization is optimized for little-endian machines:
  //   BOOLEAN - Encoded as a single byte.
  //   TINYINT, SMALLINT, INT, BIGINT - Encoded as little endian,
  //        2's complement in the size of this type.
  //   DATE - Encoded as 4 bytes little endian, 2's complement as days since epoch.
  //   FLOAT, DOUBLE - Encoded as IEEE
  //   STRING, VCHAR - Encoded as a INT followed by the byte data.
  //   CHAR - The byte data.
  //   DECIMAL - Encoded as the unscaled 2's complement little-endian value.
  //   TIMESTAMP_NANOS - Encoded as a BIGINT (8 bytes) millis since epoch followed
  //        by INT(4 byte) nanoseconds offset.
  //   ARRAY - array<TYPE> is serialized as one column containing the array lengths
  //     followed by all the serialized values of the inner type.
  //     For example, if the data of 4 records: [1,2], [3], NULL, [4,NULL]
  //     The column of lengths would contain:
  //        [0,0,1,0], for the null indicators and
  //        [2,1,2] for the lengths of the arrays.
  //     The array data is the next column, which just contains all the element values:
  //        [0,0,0,0,1] For the null indicators and
  //        [1,2,3,4] For the integer data values.
  //
  //   MAP - Maps are serialized similar to arrays, with one column for the lengths just
  //     as for arrays, followed by the column of strings for the key and the columns
  //     needed to serialize the values.
  //
  // Serialized data excludes NULLs. Values are serialized back to back.
  Columnar,

  // Similar to `Columnar` but optimized to allow cheaper deserialization from numpy.
  // The differences are:
  // 1. Values are dense. NULLs are included in the serialized data. The value
  //    for those bytes is undefined. For example if that data was [1,NULL,2],
  //    with Columnar, the serialized data is just [1,2] for a total of 2 bytes.
  //    With ColumnarNumPy it is [1, undefined byte, 2] for a total of 3 bytes.
  // 2. String serialization is different. In this version, all string lengths
  //    are encoded at the start of the data buffer, followed by all the
  //    string data back to back. The lengths are also dense. For example,
  //    if the data was ['hello', NULL, 'world']:
  //       Columnar: 5hello5world
  //       ColumnarNumPy: 5(undefined 4 bytes)5helloworld
  ColumnarNumPy,

  // Identical to Columnar, except with the string encoding from ColumnarNumPy
  Columnar2,

  // Presto's result wire JSON format
  PrestoJson,
}

enum TCompressionCodec {
  LZ4,
  ZSTD,
}

struct TColumnData {
  // One byte for each value.
  1: required binary is_null
  2: required binary data

  // Set iff codec is enabled for the decompressed length of the respective
  // buffers.
  3: optional i32 is_null_decompressed_len
  4: optional i32 data_decompressed_len

  // If set, the number of nulls in is_null.
  5: optional i32 num_nulls
}

// List of column data for the Columnar record format. This is 1:1 with the
// schema. i.e. cols[0] is the data for schema.cols[0].
struct TColumnarRecords {
  1: required list<TColumnData> cols
}

// The type of request specified by the client. Clients can specify read
// requests in multiple ways.
enum TRequestType {
  Sql,
  Path,
}

struct TPathRequest {
  // The URI to read.
  1: required string path

  // Optional query (for predicate push down). The query must be valid SQL with
  // __PATH__ used instead of the table.
  2: optional string query

  // The schema for the files at 'path'. The client can set this if it wants the
  // server to interpret the data with this schema, otherwise the server will infer
  // the schema
  3: optional TSchema schema

  // Only valid if schema is set. Specifies the field delimiter to use for the files
  // in 'path'. Only applicable to some file formats.
  4: optional byte field_delimiter
}

enum TLoggingLevel {
  // The OFF turns off all logging.
  OFF,

  // The ALL has the lowest possible rank and is intended to turn on all logging.
  ALL,

  // The FATAL level designates very severe error events that will presumably lead the
  // application to abort.
  FATAL,

  // The ERROR level designates error events that might still allow the application
  // to continue running.
  ERROR,

  // The WARN level designates potentially harm
  WARN,

  // The INFO level designates informational messages that highlight the progress of the
  // application at coarse-grained level.
  INFO,

  // The DEBUG Level designates fine-grained informational events that are most useful
  // to debug an application.
  DEBUG,

  // The TRACE Level designates finer-grained informational events than the DEBUG
  TRACE,
}

// Log messages return by the RPCs. Non-continuable errors are returned via
// exceptions in the RPCs. These messages contain either warnings or additional
// diagnostics.
struct TLogMessage {
  // User facing message.
  1: required string message

  // Additional detail (e.g. stack trace, object state)
  2: optional string detail

  // Level corresponding to this message.
  3: required TLoggingLevel level

  // The number of times similar messages have occurred. It is up to the service to
  // decide what counts as a duplicate.
  4: required i32 count = 1
}

struct TRequestOptions {
  // If true, fail tasks if an corrupt record is encountered, otherwise, those records
  // are skipped (and warning returned).
  1: optional bool abort_on_corrupt_record = false
}

// Type of sampling to perform
enum TSamplingType {
  // Restrict the data scanned in this table to approximately this value.
  DATA_SET_SIZE,
  LIMIT_NUM_RECORDS,
}

struct TSamplingParams {
  1: required TSamplingType type
  2: required i64 value
}

// Captures optional request metadata for improved diagnostics. This header
// is intended to be embedded in every T*Params object.
// Note for backwards compat with older clients, some information will be
// duplicated with this and what is inside the params as an explicit field.
struct TRequestContext {
  // Optional name. This is not intended to be unique. It should be for example
  // "user-activity-report" (uniqueness if from client_requet_id).
  1: optional string request_name

  // Optional ID, provided by the client, to represent a client request. A single
  // client request (e.g. query) can make multiple RPCs and we want to be able
  // to tie them together.
  2: optional string client_request_id

  // If set, the token for the requesting user. This allows the connected user
  // (via th network auth) to be different than the request user.
  3: optional string auth_token
}

struct TPlanRequestParams {
  // Context metadata for the request.
  100: optional TRequestContext ctx

  // The version of the client
  1: required TProtocolVersion client_version = "1.0"

  2: required TRequestType request_type

  // Optional arguments to the plan request.
  3: optional TRequestOptions options

  // Only one of the below is set depending on request type
  4: optional string sql_stmt
  5: optional TPathRequest path

  // Username for the connecting user. On a secure cluster, this is ignored and
  // instead the authenticated user used.
  6: optional string user

  // A hint for the maximum number of tasks this request will generate. If not
  // set, the server will pick a default. If this value is smaller than the
  // number o fnatural task splits (e.g. HDFS blocks), the server will combine tasks.
  // The combined tasks will have multiple blocks, for example.
  7: optional i32 max_tasks

  // If set, this is the user to run the request as. Note that this can be different
  // than the connected user for proxy access. For example, the connected user can
  // be the userid of the server application, and the requesting user can be the
  // end user.
  8: optional string requesting_user

  // If true, generate only a single task per recordservice worker.
  9: optional bool single_task_per_worker

  // If true, this will return tasks where each tasks contains data that is only
  // for a single partition. It is possible to have many tasks for the same partition
  // (i.e. if the partition is big and should split) but no task will contain data
  // that spans partitions.
  10: optional bool preserve_partitions

  // This value determines the maximum partition_split optimization value.
  // If the number of partitions are > this value, the partition split optimization
  // will be kicked off. With this optimization, the workers would enumerate through the
  // files instead of the planner.
  11: optional i32 partition_split_threshold

  // If set, the worker cluster to use for this request
  12: optional string cluster_id

  // If set, enable bucketed join if backend can support it.
  13: optional bool enable_bucketed_joins

  // If set, the sampling that should be applied automatically for all tables in
  // this query.
  14: optional TSamplingParams sampling_params

  // Optional ID, provided by the client, to represent a client request. A single
  // client request (e.g. query) can make multiple RPCs and we want to be able
  // to tie them together.
  15: optional string client_request_id

  // If true, allow executing restricted(eg., JDBC table scan) tasks on external workers
  16: optional bool allow_external_restricted_tasks

  // If set, indicates the minimum task size (bytes) for planning the tasks.
  // Note, the purpose of this is for testing and we should not rely on this value
  // passed from client to control this. We already have TaskCombiner that automates this.
  17: optional i32 min_task_size

  // If true, allow the planner to defer task signing. This means not all the tasks
  // generated will contain signed urls. The server can decide how many to sign.
  18: optional bool defer_task_url_signing
}

struct TTask {
  // The list of hosts where this task can run locally.
  1: required list<TNetworkAddress> local_hosts

  // An opaque blob that is produced by the RecordServicePlanner and passed to
  // the RecordServiceWorker.
  2: required binary task

  // Unique ID generated by the planner. Used only for diagnostics (e.g. server
  // log messages).
  3: required TUniqueId task_id

  // If true, the records returned by this task are ordered, meaning in the case
  // of failures, the client can continue from the current record. If false, the
  // client needs to recompute from the beginning.
  4: required bool results_ordered

  // A unit-less estimate of the computation required to execute the task. This
  // should only be used to compare task sizes returned from a single PlanRequest()
  // to give an estimate of how large tasks are. Within a single request if the
  // size of one task is 3x bigger than another task, we expect it to take 3 times
  // as long.
  5: required i64 task_size = 1

  // Only set if preserve_partitions is set to true in TPlanRequestParams, in which
  // case it contains the partitions values for this task as formatted in storage.
  // e.g. year=2001/month=2/day=1. This does *not* include the base dir.
  6: optional string partition_path

  // If true, allow this task to run on external odas worker.
  7: optional bool allow_external_task_execution

  // If set, the unix time that this task will expire. The client is expected to
  // call RefreshCredentials() if the expiry is close.
  // If not set, it indicates this task has no need to be refreshed. i.e. not using
  // signed urls.
  8: optional i64 expire_unix_sec
}

struct TPlanRequestResult {
  1: required list<TTask> tasks
  2: required TSchema schema

  // Unique ID generated by the planner. Used only for diagnostics (e.g. server
  // log messages).
  3: required TUniqueId request_id

  // The list of all hosts running workers.
  4: required list<TNetworkAddress> hosts

  // List of warnings generated during planning the request. These do not have
  // any impact on correctness.
  5: required list<TLogMessage> warnings

  // The wire formats the server supports when returning records. If unset,
  // the server only supports the default, TRecordFormat.Columnar.
  6: optional set<TRecordFormat> supported_result_formats
}

struct TGetSchemaResult {
  1: required TSchema schema
  2: required list<TLogMessage> warnings
}

struct TExecTaskParams {
  // Context metadata for the request.
  100: optional TRequestContext ctx

  // This is produced by the RecordServicePlanner and must be passed to the worker
  // unmodified.
  1: required binary task

  // Logging level done by the service the service Service level logging for this task.
  2: optional TLoggingLevel logging_level

  // Maximum number of records that can be returned per fetch. The server can return
  // fewer. If unset, service picks default.
  3: optional i32 fetch_size

  // The format of the records to return. Only the corresponding field is set
  // in TFetchResult. If unset, the server picks the default.
  4: optional TRecordFormat record_format

  // The memory limit for this task in bytes. If unset, the service manages it
  // on its own.
  5: optional i64 mem_limit

  // The offset to start returning records. This is only valid for tasks where
  // results_ordered is true. This can be used to improve performance when there
  // are failures. The client can run the task against another daemon with the
  // offset set to the number of records already seen.
  // The offset is the record ordinal, that is, the first offset records are not
  // returned to the client.
  6: optional i64 offset

  // The maximum number of records to return for this task.
  7: optional i64 limit

  // Codecs supported by the client
  8: optional set<TCompressionCodec> supported_compression_codecs

  9: optional string client_request_id

  // The memory limit for the default RequestPool (default-pool) in bytes. If unset, the
  // server manages it on its own.
  10: optional i64 default_pool_mem_limit
}

struct TExecTaskResult {
  1: required TUniqueId handle

  // Schema of the records returned from Fetch().
  2: required TSchema schema
}

struct TFetchParams {
  1: required TUniqueId handle
}

struct TFetchResult {
  // If true, all records for this task have been returned. It is still valid to
  // continue to fetch, but they will return 0 records.
  1: required bool done

  // The approximate completion progress [0, 1]
  2: required double task_progress

  // The number of records in this batch.
  3: required i32 num_records

  // The encoding format.
  4: required TRecordFormat record_format

  // TRecordFormat.Columnar/ColumnarNumPy/Columnar2
  5: optional TColumnarRecords columnar_records

  // If set, the codec that was used to compress the results. Only applies for
  // columnar_records.
  6: optional TCompressionCodec compression_codec

  // TRecordFormat.PrestoJson
  7: optional binary presto_json_result
}

struct TStats {
  // [0 - 1]
  1: required double task_progress

  // The number of records read before filtering.
  2: required i64 num_records_read

  // The number of records returned to the client.
  3: required i64 num_records_returned

  // The number of records that were skipped (due to data errors).
  4: required i64 num_records_skipped

  // Time spent in the record service serializing returned results.
  5: required i64 serialize_time_ms

  // Time spent in the client, as measured by the server. This includes
  // time in the data exchange as well as time the client spent working.
  6: required i64 client_time_ms

  //
  // HDFS specific counters
  //

  // Time spent in decompression.
  7: optional i64 decompress_time_ms

  // Bytes read from HDFS
  8: optional i64 bytes_read

  // Bytes read from the local data node.
  9: optional i64 bytes_read_local

  // Throughput of reading the raw bytes from HDFS, in bytes per second
  10: optional double hdfs_throughput
}

struct TTaskStatus {
  1: required TStats stats

  // Errors due to invalid data
  2: required list<TLogMessage> data_errors

  // Warnings encountered when running the task. These should have no impact
  // on correctness.
  3: required list<TLogMessage> warnings
}

enum TErrorCode {
  // The request is invalid or unsupported by the Planner service.
  INVALID_REQUEST,

  // The handle is invalid or closed.
  INVALID_HANDLE,

  // The task is malformed.
  INVALID_TASK,

  // Service is busy and not unable to process the request. Try later.
  SERVICE_BUSY,

  // The service ran out of memory processing the task.
  OUT_OF_MEMORY,

  // The task was cancelled.
  CANCELLED,

  // Internal error in the service.
  INTERNAL_ERROR,

  // The server closed this connection and any active requests due to a timeout.
  // Clients will need to reconnect.
  CONNECTION_TIMED_OUT,

  // Error authenticating.
  AUTHENTICATION_ERROR,

  // Request is valid but unsupported.
  // TODO: clean up server response codes. It currently overlaps with INVALID_REQUEST.
  UNSUPPORTED_REQUEST,
}

exception TRecordServiceException {
  1: required TErrorCode code

  // The error message, intended for the client of the RecordService.
  2: required string message

  // The detailed error, intended for troubleshooting of the RecordService.
  3: optional string detail
}

// TODO: argument this response with the description, units, etc.
struct TMetricResponse {
  // Set if the metric is defined. This is the human readable string of the value.
  1: optional string metric_string
}

// Serialized delegation token.
struct TDelegationToken {
  // Identifier/password for authentication. Do not log the password.
  // Identifier is opaque but can be logged.
  1: required string identifier
  2: required string password

  // Entire serialized token for cancel/renew. Do not log this. It contains
  // the password.
  3: required binary token
}

typedef list<string> TDatabaseName

struct TDatabase {
  1: TDatabaseName name

  // Optional, unschemaed metadata
  2: optional map<string, string> metadata

  3: optional list<TAttributeValue> attribute_values

  // optional location for database and its tables
  4: optional string location

  /**
   * Description of the database
   */
  5: optional string description

  /**
   * Number of datasets (tables) in the database
   * 'Count' would be the number of datasets (tables) user has access to
   */
  6: optional i64 datasets_count

  /**
   * Privilege level e.g. CREATE, ALTER, INSERT, SELECT etc
   * Indicates the permissions the requesting user has on this database
   */
  7: optional list<TAccessPermissionLevel> access_levels

  8: optional bool has_grant

  // Indicates if the datasets count returned is an estimate.
  9: optional bool is_datasets_count_estimated
}

struct TSortColOrder {
  // sort column name
  1: string col

  // asc(1) or desc(0)
  2: i32    order
}

struct TTable {
  1: required string name
  9: optional TDatabaseName db

  2: optional string owner
  3: optional TSchema schema

  // Description attached to table
  4: optional string description

  // Time this dataset was created, in unix time
  5: optional i64 created_time_unix_epoch

  // Time ddl was executed on this dataset.
  7: optional i64 last_ddl_time_unix_epoch

  // Information string on the primary storage system for this table. This is
  // not interpreted and just presented to the user. Examples are "hdfs', 'kinesis'.
  6: optional string primary_storage

  // If this is an external view, the view string for this table
  8: optional string view_string

  // If set, the path in the storage system where this table is located.
  10: optional string location

  // If set, this dataset is invalid for some reason and could not be fully loaded.
  11: optional string loading_error_msg

  // If set, the underlying table format (i.e. storage format). This may not be
  // set if not applicable to this table type or the metadata is hidden.
  12: optional string table_format

  // Optional, unschemaed metadata
  13: optional map<string, string> metadata

  // Optional, serde metadata
  14: optional map<string, string> serde_metadata

  // Set iff this table is clustered
  15: optional list<string> cluster_by_cols
  16: optional i32 num_buckets

  // list of attribute values if any assigned to this table
  17: optional list<TAttributeValue> attribute_values

  // If set to true, access to this dataset should be direct
  18: optional bool direct_access

  // The SerDe library used for this dataset, if any
  19: optional string serialization_lib

  // input format definition used in the storage of this table
  20: optional string input_format

  // output format definition used in the storage of this table
  21: optional string output_format

  // compressed or not, in storage, if this information available and applicable
  22: optional bool compressed

  // sort order of the data in each cluster in cluster_by_cols
  23: optional list<TSortColOrder> sort_cols

  // if this is a view (external or not), the view definition for it
  24: optional string view_expanded_text
}

struct TPartition {
  1: required list<string> partition_values
  2: optional string location
}

/**
 * Represents a Data Registration Connection record.
 */
struct TDataRegConnection {
  /**
   * The unique name of the data registration connection.<br/>
   * All interactions with data registration connection object will be based on this.
   */
  1: required string name

  /**
   * The connection type like JDBC/S3/ADLS etc.
   * Valid values are:
   * <br>
   * JDBC, S3, ADLS
   * </br>
   */
  2: optional string type

  /**
   * If S3/ADLS as data source, the cloud path of the data source (S3/ADLS).<br/>
   * For JDBC, optionally this will be the credentials file path.
   */
  3: optional string data_source_path

  /**
   * For JDBC type, this will be the jdbc driver name.
   * Refer to common DbInfo.Engine enum values (case sensitive).<br/>
   * Valid values are:
   * <p>
   * mysql, postgresql, snowflake, awsathena, redshift,
   * sqlserver, jtds:sqlserver, jtds:sybase, oracle:thin
   * </p>
   */
  4: optional string jdbc_driver

  /**
   * If JDBC as type, a valid connection host.
   */
  5: optional string host

  /**
   * If JDBC as type, a valid connection port.
   */
  6: optional i32 port

  /**
   * TO BE DEPRECATED
   * If JDBC as type, user name to connect to the JDBC data source.
   */
  7: optional string user_name

  /**
   * TO BE DEPRECATED
   * If JDBC as type, password to connect to the JDBC data source.<br/>
   * This will be stored in the secrets manager.
   */
  8: optional string password

  /**
   * If JDBC as type, the user secrets key.
   * This will be stored in the secrets manager.
   */
  17: optional string user_key

  /**
   * If JDBC as type, the password secrets key.<br/>
   * This will be stored in the secrets manager.
   */
  18: optional string password_key

  /**
   * If JDBC as type, default catalog for the initial connection.
   */
  9: optional string default_catalog

  /**
   * If JDBC as type, default schema for the initial connection.
   */
  10: optional string default_schema

  /**
   * Connection properties map. Additional properties are to be stored here.<br/>
   * For example, if the connection supports SSL, <br/>
   * then this properties map can be used to specify the connection parameter as,<br/>
   * {'SSL':'true'}<br/>
   */
  11: optional map<string, string> connection_properties

  /**
   * Set if this connection is active/inactive. Use this to set a connection state.
   */
  12: optional bool is_active = true

  /**
   * Created by user. This is a read-only value and has no effect on create
   * or update of the connection.<br/>
   * This will be automatically set by the backend.
   */
  13: optional string created_by

  /**
   * Created at time since epoch (milliseconds).
   * This is a read-only value.
   */
  14: optional i64 created_at

  /**
   * Updated by user.  This is a read-only value.
   */
  15: optional string updated_by

  /**
   * Updated at time since epoch (milliseconds).
   * This is a read-only value.
   */
  16: optional i64 updated_at

  /**
   * The "test connection" status
   */
  19: optional string test_status

  /**
   * The "test connection" error details
   */
  20: optional string test_error_details

  /**
   * tested at time since epoch (milliseconds).
   * This is a read-only value.
   */
  21: optional i64 tested_at

  /**
   * Privilege level e.g. CREATE, ALTER, INSERT, SELECT etc
   * Indicates the permissions the requesting user has on this Connection
   */
  22: optional list<TAccessPermissionLevel> access_levels
}

/**
 * Represents one dataset for data registration.
 */
struct TDataRegCrawlDataset {
  /**
   * The connection object associated with the dataset crawler.
   */
  1: required TDataRegConnection connection
  /**
   * The Okera target database name where the crawled dataset should be registered.
   **/
  2: required string target_db
  /**
   * Same as <i>TDataRegConnection.data_source_path</i>.
   */
  3: optional string data_source_path
  /**
   * The JDBC catalog name (database) for the crawler dataset.
   */
  4: optional string jdbc_catalog
  /**
   * The JDBC schema name for the crawler dataset.
   */
  5: optional string jdbc_schema
  /**
   * The JDBC table name for the crawler dataset.
   */
  6: optional string jdbc_table
  /**
   * The crawler status. Valid values from <i>RecordService.TCrawlStatus</i>
   */
  7: optional string status
  /**
   * The crawler error message if there is an error crawling dataset.
   */
  8: optional string error_message
  /**
   * The verbose error details if there is an error crawling dataset.
   */
  9: optional string error_details
  /**
   * The dataset crawler state, by default active, use this flag to disable the crawling
   * for this dataset.
   */
  10: optional bool is_active = true
  /**
   * Created by user. This is a read-only value and has no effect on create
   * or update of the connection.<br/>
   * This will be automatically set by the backend.
   */
  11: optional string created_by
  /**
   * Created at time since epoch (milliseconds).
   * This is a read-only value.
   */
  12: optional i64 created_at
  /**
   * Updated by user.  This is a read-only value.
   */
  13: optional string updated_by
  /**
   * Updated at time since epoch (milliseconds).
   * This is a read-only value.
   */
  14 : optional i64 updated_at
}

/**
 * Represents the discovered JDBC dataset for the JDBC crawler. Note, this always
 * is from the JDBC data source and should not be invoked multiple times.
 */
struct TJDBCDataset {
  /**
   * represents a JDBC catalog name (database).
   */
  1: required string jdbc_catalog
  /**
   * represents a JDBC schema name.
   */
  2: optional string jdbc_schema
  /**
   * represents a JDBC table name.
   */
  3: optional string jdbc_table
  /**
   * A list of columns discovered for a JDBC data source table (dataset).
   */
  4: optional TSchema schema
}

/**
 * Represents one discovered dataset for the crawler. Note, this will not be persisted
 * in the Okera catalog. It is always from the S3/ADLS or JDBC data source.
 */
struct TCrawlerDiscoveryDataset {
  /**
   * The connection information of the discovered dataset.
   */
  1: required TDataRegConnection connection
  /**
   * If crawler type is S3/ADLS, The list of sub folders for the given path.
   */
  2: optional list<string> data_source_paths
  /**
   * If crawler type is JDBC, the list of jbdc discovered datasets.
   */
  3: optional list<TJDBCDataset> jdbc_datasets
}

// Returns the databases in the catalog
struct TGetDatabasesParams {
  // Context metadata for the request.
  100: optional TRequestContext ctx

  1: optional string filter

  // If set, return only databases specified in this set and return detailed
  // information about them.
  3: optional list<string> db_names

  2: optional string requesting_user

  4: optional bool ignore_internal_dbs = true

  // If set, only return database where the requesting user has these levels of
  // access.
  5: optional list<TAccessPermissionLevel> access_levels
}

struct TGetDatabasesResult {
  1: required list<TDatabase> databases
}

// Returns the tables in the catalog
struct TGetTablesParams {
  // Context metadata for the request.
  100: optional TRequestContext ctx

  1: required TDatabaseName database

  // Only one of name or filter can be set.
  // - If name is set, returns the details of this dataset.
  // - If filter is set, returns basic metadata about all the datasets with
  //   name that match filter (i.e. matches with SQL 'LIKE' semantics)
  2: optional string name
  3: optional string filter

  4: optional string requesting_user

  // If set, only return datasets where the requesting user has these levels of
  // access.
  5: optional list<TAccessPermissionLevel> access_levels

  6: optional string client_request_id
}

struct TGetTablesResult {
  1: required list<TTable> tables
}

struct TGetPartitionsParams {
  // Context metadata for the request.
  100: optional TRequestContext ctx

  1: required TDatabaseName database
  2: required string table
  3: optional string requesting_user
}

struct TGetPartitionsResult {
  1: optional list<TPartition> partitions
}

struct TOkeraCatalog {
  /**
   * Catalog name
   */
  1: required string name

  /**
   * Privilege levels e.g. CREATE, ALTER, INSERT, SELECT etc
   * Indicates the permissions the requesting user has on this catalog
   */
  2: optional map<TAccessPermissionScope, list<TAccessPermissionLevel>> access_levels

  3: optional bool has_grant
}

/**
 * Represents a privilege in an authorization policy.
 */
struct TPrivilege {
  /**
   * A human readable name for this privilege. The combination of role_id +
   * privilege_name is guaranteed to be unique.
   */
  1: required string privilege_name

  /**
   * The level of access this privilege provides.
   */
  2: required TAccessPermissionLevel privilege_level

  /**
   * The scope of the privilege.
   */
  3: required TAccessPermissionScope scope

  /**
   * If true, GRANT OPTION was specified.
   */
  4: required bool has_grant_opt

  /**
   * The ID of the role this privilege belongs to.
   */
  5: optional i32 role_id

  /**
   * Set if scope is SERVER, URI, DATABASE, or TABLE
   */
  6: optional string server_name

  /**
   * Set if scope is DATABASE or TABLE
   */
  7: optional string db_name

  /**
   * Unqualified table name. Set if scope is TABLE.
   */
  8: optional string table_name

  /**
   * Set if scope is URI
   */
  9: optional string uri

  /**
   * Time this privilege was created (in milliseconds since epoch).
   */
  10: optional i64 create_time_ms

  /**
   * Set if scope is COLUMN
   */
  11: optional string column_name

  /**
   * Attribute expression
   */
  12: optional string attribute_expression

  /**
   * Transformations required for this grant
   */
  13: optional string transform_expression

  /**
   * Row filters required for this grant
   */
  14: optional string filter

  /**
   * Namespace for the attribute to grant on. Set if scope is ATTRIBUTE_NAMESPACE
   */
  15: optional string attribute_namespace

  /**
   * Role to grant on. Set if scope is ROLE
   */
  16: optional string role

  /**
   * Crawler to grant on. Set if scope is CRAWLER
   */
  17: optional string crawler

  /**
   * Additional KV properties associated with this role.
   */
  18: optional map<string, string> props

  /**
   * If not set, assume GRANT.
   */
  19: optional TPrivilegeType privilege_type

  /**
   * Data connection to grant on. Set if scope is DATACONNECTION
   */
  20: optional string data_connection
}

/**
 * Represents a role in an authorization policy.
 */
struct TRole {
  /**
   * Case-insensitive role name
   */
  1: required string role_name

  /**
   * Unique ID of this role.
   */
  2: required i32 role_id

  /**
   * List of groups this role has been granted to.
   */
  3: required list<string> grant_groups

  /**
   * Privileges that have been granted to this role
   */
  4: optional list<TPrivilege> privileges

  /**
   * Privilege level e.g. CREATE, ALTER, INSERT, SELECT etc
   * Indicates the permissions the requesting user has on this role
   */
  5: optional list<TAccessPermissionLevel> access_levels

  /**
   * Whether or not this is a user role (i.e. the internally created
   * per-user role, _okera_internal_role_<user>)
   */
  6: optional bool is_user_role
}


// This service is responsible for planning requests.
service RecordServicePlanner {
  // Returns the version of the server. Throws exception if there are too
  // many connections for the planner.
  TProtocolVersion GetProtocolVersion() throws(1:TRecordServiceException ex);

  // Returns the version information of the server.
  TServerVersion GetServerVersion() throws(1:TRecordServiceException ex);

  // Initializes the application state for this connection to share connectionn
  // wide (i.e. across all requests) metadata
  TInitApplicationResult InitApplication(1:TInitApplicationParams params)
      throws(1:TRecordServiceException ex);

  // Deprecated version of InitApplication (subset of the API to set the name of
  // the application.)
  void SetApplication(1:string app) throws(1:TRecordServiceException ex);

  // Plans the request. This generates the tasks and the list of machines
  // that each task can run on.
  TPlanRequestResult PlanRequest(1:TPlanRequestParams params)
      throws(1:TRecordServiceException ex);

  // Returns the schema for a plan request.
  TGetSchemaResult GetSchema(1:TPlanRequestParams params)
      throws(1:TRecordServiceException ex);

  // Queries the server for a metric by key.
  TMetricResponse GetMetric(1:string key)

  // Returns the databases in the catalog.
  TGetDatabasesResult GetDatabases(1:TGetDatabasesParams params)
      throws(1:TRecordServiceException ex);

  // Returns the tables in this database.
  TGetTablesResult GetTables(1:TGetTablesParams params)
      throws(1:TRecordServiceException ex);

  // Returns the partitions in this table.
  TGetPartitionsResult GetPartitions(1:TGetPartitionsParams params)
      throws(1:TRecordServiceException ex);

  // Gets a delegation for user. This creates a token if one does not already exist
  // for this user. renewer, if set, is the user than can renew this token (in addition
  // to the 'user').
  // Returns an opaque delegation token which can be subsequently used to authenticate
  // with the RecordServicePlanner and RecordServiceWorker services.
  TDelegationToken GetDelegationToken(1:string user, 2:string renewer)
      throws(1:TRecordServiceException ex);

  // Cancels the delegation token.
  void CancelDelegationToken(1:TDelegationToken delegation_token)
      throws(1:TRecordServiceException ex);

  // Renews the delegation token. Duration set by server configs.
  void RenewDelegationToken(1:TDelegationToken delegation_token)
      throws(1:TRecordServiceException ex);
}

// This service is responsible for executing tasks generated by the RecordServicePlanner
service RecordServiceWorker {
  // Returns the version of the server. Throws exception if there are too
  // many connections for the worker.
  TProtocolVersion GetProtocolVersion() throws(1:TRecordServiceException ex)

  // Returns the version information of the server.
  TServerVersion GetServerVersion() throws(1:TRecordServiceException ex)

  // Initializes the application state for this connection to share connectionn
  // wide (i.e. across all requests) metadata
  TInitApplicationResult InitApplication(1:TInitApplicationParams params)
      throws(1:TRecordServiceException ex);

  // Deprecated version of InitApplication (subset of the API to set the name of
  // the application.)
  void SetApplication(1:string app) throws(1:TRecordServiceException ex);

  // Begin execution of the task in params. This is asynchronous.
  TExecTaskResult ExecTask(1:TExecTaskParams params)
      throws(1:TRecordServiceException ex);

  // Returns the next batch of records
  TFetchResult Fetch(1:TFetchParams params)
      throws(1:TRecordServiceException ex);

  // Closes the task specified by handle. If the task is still running, it is
  // cancelled. The handle is no longer valid after this call.
  void CloseTask(1:TUniqueId handle);

  // Returns status for the task specified by handle. This can be called for tasks that
  // are not yet closed (including tasks in flight).
  TTaskStatus GetTaskStatus(1:TUniqueId handle)
      throws(1:TRecordServiceException ex);

  // Queries the server for a metric by key.
  TMetricResponse GetMetric(1:string key)
}

