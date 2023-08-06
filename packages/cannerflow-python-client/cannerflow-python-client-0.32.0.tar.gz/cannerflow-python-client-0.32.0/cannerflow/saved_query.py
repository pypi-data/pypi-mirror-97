__all__ = ["SavedQuery"]

class SavedQuery(object):
    def __init__(
        self,
        workspace_id,
        request
    ):
        self.workspace_id = workspace_id
        self.request = request
    def getPayload(self):
        return {
            'operationName': 'sqls',
            'query': """
                query sqls($where: SqlWhereInput!) {
                    sqls(where: $where) {
                        id
                        sql
                        title
                        description
                        workspaceId
                    }
                }
            """,
            'variables': {
                'where': {
                    'workspaceId': self.workspace_id
                }
            }
        }
    def fetch(self):
        return self.request.post(self.getPayload()).get('sqls')
    def list_title(self):
        data = self.fetch()
        return list(map(lambda x: x['title'], data))
    def get(self, title):
        queries = self.fetch()
        query = next(q for q in queries if q.get('title') == title)
        return  query

