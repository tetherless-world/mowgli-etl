import logging
from pathlib import Path

import googleapiclient.discovery
from configargparse import ArgParser
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

from mowgli_etl.cli.commands._command import _Command


class DriveUploadCommand(_Command):
    """
    Command line utility for uploading a single file to Google Drive
    """

    def add_arguments(self, arg_parser: ArgParser, add_parent_arguments):
        arg_parser.add_argument(
            "--file-path", required=True, help="Local path to the file to be uploaded"
        )
        arg_parser.add_argument(
            "--file-id",
            required=True,
            help="Id of the file in Drive that will be overwritten.  Must already exist.",
        )
        arg_parser.add_argument(
            "--service-account-file",
            required=True,
            help="Path to Google Cloud service account file",
        )

    def __call__(self, args):
        service_account_file_path = Path(args.service_account_file)
        assert service_account_file_path.is_file()
        file_path = Path(args.file_path)
        assert file_path.is_file()

        drive_client = self.__create_drive_client(service_account_file_path)
        file = self.__update_file(
            drive_client=drive_client, file_path=file_path, file_id=args.file_id
        )

        self._logger.info("file uploaded %s", file)

    def __create_drive_client(self, service_account_file_path: Path):
        scopes = ["https://www.googleapis.com/auth/drive"]
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file_path, scopes=scopes
        )
        return googleapiclient.discovery.build(
            "drive", "v3", credentials=credentials, cache_discovery=False
        )

    def __update_file(self, *, drive_client, file_path: Path, file_id: str):
        body = {"name": file_path.name}
        media_body = MediaFileUpload(file_path, resumable=True)
        return (
            drive_client.files()
            .update(fileId=file_id, body=body, media_body=media_body)
            .execute()
        )
