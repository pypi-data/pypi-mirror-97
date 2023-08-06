""" Exporters tasks
"""
from __future__ import absolute_import, unicode_literals

import json
import logging

from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task

import core_exporters_app.commons.constants as exporter_constants
import core_exporters_app.components.exporter.api as exporter_api
from core_explore_common_app.components.result.models import Result
from core_explore_common_app.rest.result.serializers import ResultBaseSerializer
import core_main_app.components.user.api as user_api
from core_exporters_app.exporters.exporter import (
    get_exporter_module_from_url,
    AbstractExporter,
)
from core_exporters_app.settings import COMPRESSED_FILES_EXPIRE_AFTER_SECONDS
from core_exporters_app.system.api import get_older_exported_files
from core_main_app.utils.requests_utils.requests_utils import send_get_request

logger = logging.getLogger(__name__)


@shared_task
def export_files(
    exported_file_id, exporters_list_url, url_base, data_url_list, session_key, user_id
):
    """Asynchronous tasks exporting files

    Args:
        exported_file_id:
        exporters_list_url:
        url_base:
        data_url_list:
        session_key:
        user_id:

    Returns:

    """
    # gets all data from the url list
    result_list = _get_results_list_from_url_list(url_base, data_url_list, session_key)

    transformed_result_list = []
    # Converts all data
    for exporter_id in exporters_list_url:
        # get the exporter with the given id
        exporter_object = exporter_api.get_by_id(exporter_id)
        # get the exporter module
        exporter_module = get_exporter_module_from_url(exporter_object.url)
        # if is a xslt transformation, we have to set the xslt
        if exporter_object.url == exporter_constants.XSL_URL:
            # set the xslt
            exporter_module.set_xslt(exporter_object.xsl_transformation)
        # transform the list of xml files
        transformed_result_list.extend(
            exporter_module.transform(result_list, session_key)
        )

    # Get current user
    user = user_api.get_user_by_id(user_id) if user_id else None

    # Export in Zip
    AbstractExporter.export(exported_file_id, transformed_result_list, user)


@periodic_task(run_every=crontab(minute="*"))
def delete_old_exported_files():
    """Delete older exported files.

    Returns:

    """
    try:
        # remove older exported files from database
        for exported_file in get_older_exported_files(
            seconds=COMPRESSED_FILES_EXPIRE_AFTER_SECONDS
        ):
            logger.info(
                "Periodic task: delete exported file {}.".format(str(exported_file.id))
            )
            exported_file.delete()
    except Exception as e:
        logger.error(
            "An error occurred while deleting exported files ({}).".format(str(e))
        )


def _get_results_list_from_url_list(url_base, url_list, session_key):
    """Gets all data from url

    Args:
        url_base: url of running server
        url_list: url list to request
        session_key: Session key used for requests.get
    Returns:

    """
    result_list = []
    for url in url_list:
        response = send_get_request(url_base + url, cookies={"sessionid": session_key})
        if response.status_code == 200:
            # Build serializer
            results_serializer = ResultBaseSerializer(data=json.loads(response.text))
            # Validate result
            results_serializer.is_valid(True)
            # Append the list returned
            result_list.append(
                Result(
                    title=results_serializer.data["title"],
                    xml_content=results_serializer.data["xml_content"],
                )
            )
    return result_list
