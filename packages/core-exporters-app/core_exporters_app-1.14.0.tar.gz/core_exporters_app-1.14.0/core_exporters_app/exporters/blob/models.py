""" Blob exporter
"""
import logging
import re
from urllib.parse import urlparse

from rest_framework import status

from core_exporters_app.exporters.exporter import (
    AbstractExporter,
    TransformResult,
    TransformResultContent,
)
from core_main_app.settings import INSTALLED_APPS, SERVER_URI
from core_main_app.utils.blob_downloader import BlobDownloader
from core_main_app.utils.file import get_filename_from_response
from core_main_app.utils.requests_utils import requests_utils
from core_main_app.utils.urls import get_blob_download_regex

if "core_federated_search_app" in INSTALLED_APPS:
    import core_federated_search_app.components.instance.api as instance_api

logger = logging.getLogger(__name__)


class BlobExporter(AbstractExporter):
    """BLOB Exporter. Allows to find and download all blobs from an xml content"""

    def __init__(self):
        self.name = "BLOB"
        self.extension = ".blob"

    def transform(self, xml_inputs, session_key):
        """find and download all blobs from an xml content

        Args:
            xml_inputs:
            session_key: session key

        Returns:

        """
        results_transform = []
        for xml_item in xml_inputs:
            # get the sha of the xml
            sha = AbstractExporter.get_sha(xml_item["xml_content"])
            # get the name of the xml document representing the source document name
            document_name_with_sha = AbstractExporter.get_title_document(
                xml_item["title"], xml_item["xml_content"]
            )
            transform_result = TransformResult()
            transform_result.source_document_name = document_name_with_sha
            # Get all url from xml content
            urls = _get_blob_url_list_from_xml(xml_item["xml_content"])
            # Get all blobs from urls
            for url in urls:
                try:
                    # download the blob
                    response = BlobDownloader(url, session_key).get_blob_response()
                    # manage the response
                    if response is not None:
                        if response.status_code == status.HTTP_200_OK:
                            blob_content = response.content
                            # generates the file name
                            blob_name = _get_filename_from_blob(
                                response, blob_content, sha
                            )
                            # generates an content result representing the blob file
                            transform_result_content = TransformResultContent()
                            transform_result_content.file_name = blob_name
                            transform_result_content.content_converted = blob_content
                            # Don't need any additional extension, Is generated with the file name
                            transform_result_content.content_extension = ""
                            # add the blob to the result list
                            transform_result.transform_result_content.append(
                                transform_result_content
                            )
                except Exception as ex:
                    # if something happens while downloading the blob, we don't want to freeze the export
                    # so we log the Url that fails
                    logger.error(
                        "Something went wrong while exporting blob at {0}: {1}".format(
                            url, str(ex)
                        )
                    )

            results_transform.append(transform_result)
        return results_transform


def _get_blob_url_list_from_xml(xml):
    """Returns all blob's url list

    Args:
        xml:

    Returns:

    """
    return re.findall(get_blob_download_regex(), xml)


def _get_filename_from_blob(blob_file_info, blob_file_read, sha_from_xml):
    """Returns the file name like "file_name.sha3.extension"

    Args:
        blob_file_info:
        blob_file_read:
        sha_from_xml:

    Returns:

    """
    file_name = get_filename_from_response(blob_file_info)
    sha = AbstractExporter.get_sha(blob_file_read)
    if file_name:
        # split by all dotes
        file_name_split = file_name.split(".")
        # file name start with the first element
        return_value = file_name_split[0]
        # loop on the list and generate the file name
        for index in range(1, len(file_name_split)):
            # If is the last element, we insert the sha before the extension
            if index == len(file_name_split) - 1:
                return_value += "." + sha_from_xml + "." + sha
            return_value += "." + file_name_split[index]
        # file_name.sha.extension
        return return_value.replace("\r", "")
    else:
        # if header have no filename, we return the sha only
        return sha
