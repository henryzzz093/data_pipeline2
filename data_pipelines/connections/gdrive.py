from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import uuid
import json
import tempfile

from data_pipelines.connections.core import BaseConn


class GDriveConn(BaseConn):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = None

    def connect(self):
        creds = Credentials.from_authorized_user_info(self.conn_kwargs)
        creds.refresh(Request())
        self.client = build("drive", "v3", credentials=creds)

    def close(self):
        pass

    def get_data(self):
        pass

    def _get_folder_id(self, name):
        folder_id = None
        response = (
            self.client.files()
            .list(
                q="mimeType = 'application/vnd.google-apps.folder'",
                spaces="drive",
                fields="nextPageToken, files(id, name)",
            )
            .execute()
        )
        for item in response.get("files", []):
            if item.get("name") == name:
                return item.get("id")

        if not folder_id:
            folder_metadata = {
                "name": name,
                "mimeType": "application/vnd.google-apps.folder",
            }
            folder = (
                self.client.files()
                .create(body=folder_metadata, fields="id")
                .execute()
            )
            folder_id = folder.get("id")
        return folder_id

    def load_data(self, data, **kwargs):
        folder_name = kwargs.get("folder_name")
        folder_id = self._get_folder_id(folder_name)

        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = f"{uuid.uuid4()}_data.json"
            temp_path = f"{temp_dir}/{file_name}"

            with open(temp_path, "w") as f:
                json.dump(data, f, default=str)

            file_metadata = {"name": file_name, "parents": [folder_id]}

            media = MediaFileUpload(temp_path, resumable=True)
            self.client.files().create(
                body=file_metadata, media_body=media, fields="id"
            ).execute()
        self.log.info(
            f"file created successfully: https://drive.google.com/drive/u/0/folders/{folder_id}"  # noqa: E501
        )


if __name__ == "__main__":

    kwargs = {"folder_name": "Testing1"}

    conn = GDriveConn(connection_id="gdrive_default")
    with conn:
        data = {"test": "Testing Message!"}
        conn.load_data(data, **kwargs)
