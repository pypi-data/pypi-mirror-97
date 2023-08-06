""" Auto discovery of exporters.
"""
import logging
import re

from django.contrib.admindocs.views import simplify_regex
from django.urls import URLResolver, URLPattern
from django.urls.resolvers import RegexPattern
from mongoengine.errors import ValidationError

import core_exporters_app.components.exporter.api as exporters_api
import core_main_app.commons.exceptions as main_exception
import core_main_app.system.api as system_api
from core_exporters_app.components.exporter.models import Exporter
from core_exporters_app.exporters import urls

logger = logging.getLogger(__name__)


def __assemble_endpoint_data__(pattern, prefix="", filter_path=None):
    """Create a dictionary for matched API urls.

    Args:
        pattern: pattern to parse.
        prefix: API path prefix (used by recursion).
        filter_path:

    Returns:

    """
    path = simplify_regex(prefix + pattern.pattern.regex.pattern)

    if filter_path is not None:
        if re.match("^/?%s(/.*)?$" % re.escape(filter_path), path) is None:
            return None

    path = path.replace("<", "{").replace(">", "}")

    return {
        "url": path,
        "view": pattern.lookup_str,
        "name": pattern.default_args["name"],
        "enable_by_default": pattern.default_args["enable_by_default"],
    }


def __flatten_patterns_tree__(patterns, prefix="", filter_path=None):
    """Use recursion to flatten url tree.

    Args:
        patterns: urlpatterns list
        prefix (optional): Prefix for URL pattern
        filter_path:

    Returns:

    """
    pattern_list = []

    for pattern in patterns:
        if isinstance(pattern, URLPattern):
            if isinstance(pattern.pattern, RegexPattern):
                endpoint_data = __assemble_endpoint_data__(
                    pattern, prefix, filter_path=filter_path
                )

                if endpoint_data is None:
                    continue

                pattern_list.append(endpoint_data)

        elif isinstance(pattern, URLResolver):
            if isinstance(pattern.pattern, RegexPattern):
                pref = prefix + pattern.pattern.regex.pattern
                pattern_list.extend(
                    __flatten_patterns_tree__(
                        pattern.url_patterns, pref, filter_path=filter_path
                    )
                )

    return pattern_list


def discover_exporter():
    """Exporters discover

    Returns:

    """
    patterns = __flatten_patterns_tree__(urls.urlpatterns)
    try:
        for pattern in patterns:
            try:
                try:
                    exporters_api.get_by_url(pattern["view"])
                except main_exception.DoesNotExist:
                    # If there is no exporter with the given url, it is added
                    exporter_added = Exporter(
                        name=pattern["name"],
                        url=pattern["view"],
                        enable_by_default=pattern["enable_by_default"],
                    )
                    # If an exporter was added and is a default one, it is added in all templates
                    if exporter_added.enable_by_default is True:
                        exporter_added.templates = system_api.get_all_templates()
                    exporters_api.upsert(exporter_added)
            except Exception as e:
                logger.error(
                    "Impossible to load the following exporter, class %s not found, exception: %s"
                    % (pattern["view"], str(e))
                )
    except ValidationError as e:
        raise Exception(
            "A validation error occurred during the exporter discovery: %s" % str(e)
        )
    except Exception as e:
        raise e
