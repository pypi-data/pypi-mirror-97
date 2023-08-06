# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""OArepo Micro API utilities."""
from invenio_indexer.utils import default_record_to_index


def record_to_index_from_index_name(record):
    """Get index/doc_type given a record.

    It tries to extract from `record['index_name']` the index and doc_type.
    If it fails, return the default values using default Invenio record_to_index.
    :param record: The record object.
    :returns: Tuple (index, doc_type).
    """
    index = getattr(record, 'index_name', None)
    if index:
        return index, '_doc'

    return default_record_to_index(record)
