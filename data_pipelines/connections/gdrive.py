from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from data_pipelines.writers.core import writer_factory
import uuid
import json
import tempfile
import csv
import random
import datetime

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

    def load_file(self, file_path, folder_name, **kwargs):
        file_name = file_path.split("/")[-1]
        folder_id = self._get_folder_id(folder_name)
        file_metadata = {"name": file_name, "parents": [folder_id]}

        media = MediaFileUpload(file_path, resumable=True)
        self.client.files().create(
            body=file_metadata, media_body=media, fields="id"
        ).execute()
        self.log.info(
            f"file created successfully: https://drive.google.com/drive/u/0/folders/{folder_id}/{file_name}"  # noqa: E501
        )

    def load_data(self, data, **kwargs):
        
        curret_date = datetime.datetime.now().strftime("%Y%m%d")

        folder_name = kwargs.get("folder_name")
        file_ext = kwargs.get("file_ext", "json")
        with tempfile.TemporaryDirectory() as temp_dir:

            file_name = f"{curret_date}_{uuid.uuid4()}_data.{file_ext}"
            file_path = f"{temp_dir}/{file_name}"
            writer = writer_factory(file_ext)
            writer.write(data, file_path)
            
            
            #self.log.warning(f"File Extension not Recognized, {file_ext}")

            self.load_file(file_path, folder_name)
                    

if __name__ == "__main__":

    kwargs = {"folder_name": "Testing1"}

    def get_data():
        pets = ["cat", "dog", "mouse", "bird", "rabbit"]
        ages  = [12, 3, 4, 5]
        for i in range(10):
            pet = random.choice(pets)
            age = random.choice(ages)
            yield {
                "pet": pet,
                "age": age
            }
    

    conn = GDriveConn(connection_id="gdrive_default")
    with conn:
        data = get_data()
        conn.load_data(data, file_ext = 'txt', **kwargs)
