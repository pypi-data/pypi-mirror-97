


class ParquetHandler(object):
    def __init__(self, request, ):
        self.request = request

    def get_result(self, workspace_id, object_name):
        signed_url = self.request.get(f'/api/getSignedUrl?workspaceId={workspace_id}&objectName={object_name}')
        data = self.request.get()
