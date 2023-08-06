import pandas as pd
from numpy import array
import time

__all__ = [
  "wait_until",
  "gen_create_sql_query_payload",
  "gen_sql_query_payload",
  "gen_sql_result_payload",
  "gen_delete_statement_payload",
  "data_factory"
]

def wait_until(somepredicate, timeout, period=1, *args, **kwargs):
  mustend = time.time() + timeout
  while time.time() < mustend:
    if somepredicate(*args, **kwargs): return True
    time.sleep(period)
  raise RuntimeError(f'Executeing query exceed {timeout} seconds, please call query.wait_for_finish(timeout=int) to set a longer waiting time') 

def gen_create_sql_query_payload(sql, cache_refresh, cache_ttl, workspace_id):
    return {
        'operationName': 'createSqlQuery',
        'query': """
            mutation createSqlQuery($data: SqlQueryCreateInput!, $where: SqlQueryWhereInput!) {
                createSqlQuery(data: $data, where: $where) {
                    id
                    status
                    error
                    location
                    statementId
                    rowCount
                }
            }
        """,
        'variables': {
            'data': {
                'sql': sql,
                'cacheRefresh': cache_refresh,
                'cacheTTL': cache_ttl,
                'source': 'NOTEBOOK'
            },
            'where': {
                'workspaceId': workspace_id
            }
        }
    }

def gen_sql_query_payload(sql_query_id):
    return {
        'operationName': 'sqlQuery',
        'query': """
            query sqlQuery($where: SqlQueryWhereUniqueInput!) {
                sqlQuery(where: $where) {
                    id
                    status
                    error
                    location
                    statementId
                    rowCount
                }
            }
        """,
        'variables': {
            'where': {
                'id': sql_query_id
            }
        }
    }

def gen_sql_result_payload(sql_query_id, limit, offset):
    return {
        'operationName': 'sqlResultPagination',
        'query': """
            query sqlResultPagination($where: SqlResultPaginationWhereInput!) {
                sqlResultPagination(where: $where) {
                    result
                    columns
                    rowCount
                }
            }
        """,
        'variables': {
            'where': {
                'id': sql_query_id,
                'limit': limit,
                'offset': offset,
                'source': 'NOTEBOOK'
            }
        }
    }

def gen_delete_statement_payload(statement_id):
    return {
        'operationName': 'deleteStatement',
        'query': """
            mutation deleteStatement($where: StatementWhereUniqueInput!) {
                deleteStatement(where: $where) {
                    id
                }
            }
        """,
        'variables': {
            'where': {
                'id': statement_id
            }
        }
    }

def data_factory(data_format='list', **options):
    def get_df(columns, data):
        data_list = get_list(columns, data)
        return pd.DataFrame(data_list[1:], columns=data_list[0])
    def get_np(columns, data):
        return array(data)
    def get_list(columns, data, with_column=True):
        if (with_column == True):
            column_names = list(map(lambda column: column['name'], columns))
            return [column_names] + data
        return data
    
    if (data_format == 'list'):
        return get_list(**options)
    if (data_format == 'df'):
        return get_df(**options)
    if (data_format == 'np'):
        return get_np(**options)
    raise RuntimeError(f'Unexpected data_format {data_format}')
