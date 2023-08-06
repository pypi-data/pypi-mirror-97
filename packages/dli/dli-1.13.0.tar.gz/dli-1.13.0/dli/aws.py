#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import logging
import operator
import re
from collections import defaultdict
from datetime import timezone, datetime
from typing import Optional, List, Dict, Tuple, Iterator, Union

from botocore.credentials import RefreshableCredentials
from botocore.session import get_session

from boto3 import Session
from dateutil.parser import isoparse

trace_logger = logging.getLogger('trace_logger')


class SplitString:
    """Field that serializes to a title case string and deserializes
    to a lower case string.
    """
    _re_match = re.compile(
        r'^([\sa-zA-z0-9_-]+)'
        '(<=|<|=|>|>=|!=)((?!<=|<|=|>|>=|!=)'
        r'[\sa-zA-z0-9_-]+)$'
    )

    def __init__(self, val):
        matches = SplitString._re_match.match(val)
        self.valid = True
        if not matches or len(matches.groups()) != 3:
            self.valid = False
            raise ValueError(
                f"Requested partition is invalid: {val}. Partition arguments "
                f"must be alphanumeric separated by an operator, and must "
                f"not be wrapped in special characters like single or double "
                f"quotations."
            )
        else:
            self.partition, self.operator, self.value = matches.groups()

    def as_dict(self):
        if self.valid:
            return {
                'partition': str(self.partition),
                'operator': str(self.operator),
                'value': str(self.value)
            }

        return None


def create_refreshing_session(
    dli_client_session, **kwargs
) -> Session:
    """
    :param dli_client_session: We must not be closing over the original
    variable in a multi-threaded env as the state can become shared.
    :param kwargs:
    :return:
    """

    def refresh():
        auth_key = dli_client_session.auth_key
        expiry_time = dli_client_session.token_expires_on.replace(
            tzinfo=timezone.utc
        ).isoformat()

        return dict(
            access_key=auth_key,
            secret_key='noop',
            token='noop',
            expiry_time=expiry_time,
        )

    _refresh_meta = refresh()

    session_credentials = RefreshableCredentials.create_from_metadata(
        metadata=_refresh_meta,
        refresh_using=refresh,
        method='noop'
    )

    session = get_session()
    handler = kwargs.pop("event_hooks", None)
    if handler is not None:
        session.register(f'before-send.s3', handler)

    session._credentials = session_credentials
    return Session(
        botocore_session=session,
        **kwargs
    )


def _get_partitions_in_filepath(filepath: str) -> List[List[str]]:
    splits = filepath.split("/")
    return [x.split("=") for x in splits if "=" in x]


def _operator_lookup(op):
    return {
        '<': operator.lt,
        '>': operator.gt,
        '=': operator.eq,
        '<=': operator.le,
        '>=': operator.ge,
        '!=': operator.ne
    }[op]


def eval_logical(oper, field, val):
    return _operator_lookup(oper)(field, val)


def match_partitions(
    file_path: str,
    partitions: Optional[List[str]],
):
    """
    Return True if the path contains the partition(s) provided.

    :param file_path:
    :param partitions:
    :return:
    """
    # Convert from a list of string to a dictionary of partition, operator &
    # value
    query_partitions = [
        potential.as_dict() for potential in
        [
            SplitString(x)
            for x in partitions
        ] if potential.valid
    ]

    return _meets_partition_params(file_path, query_partitions)


def _meets_partition_params(
    file_path: str,
    query_partitions: Optional[List[Dict[str, str]]],
):
    """
    Return True if the path contains the partition(s) provided.

    :param file_path:
    :param query_partitions:
    :return: True if meets the criteria.
    """

    # Copied from Consumption

    if query_partitions is None:
        return True

    # Sanitse the user input.
    for x in query_partitions:
        x['partition'] = x['partition'].strip()

    # Convert Lists of List to Dictionary using dictionary comprehension.
    found_partitions = {
        x[0]: x[1] for x in _get_partitions_in_filepath(file_path)
    }

    filtered = [
        x for x in query_partitions
        if x['partition'] in found_partitions
    ]

    # Example:
    # found_p = dict[(k,v), (k1,v1)] = k:v, k1:v1
    # query_p = [{'partition':'date', 'operator':'<', 'value':'20190102'}]

    for filterable in filtered:
        field = filterable['partition'].strip()
        compare_val = found_partitions[field]
        op = filterable['operator'].strip()
        filter_value = filterable['value'].strip()

        if field.startswith('as_of_'):
            try:
                filter_value_date = isoparse(filter_value)
            except ValueError as e:
                # This means a user has given an invalid date i.e. not in
                # the correct ISO 8601 format for Python datetime.
                raise ValueError(
                    'Was unable to parse the filter value you provided for '
                    'the `as_of_date` into a Python datetime: '
                    f"'{filter_value}', file_path: {file_path}'"
                ) from e

            try:
                compare_val = isoparse(compare_val)
            except ValueError:
                # Can not meet partition params as it not a date
                trace_logger.warning(
                    f'{file_path} is not a valid date.',
                    extra={
                        'file_path': file_path,
                        'filterable': filterable
                    },
                    exc_info=True
                )

                return False

            filter_value = filter_value_date

        match = eval_logical(
            op,
            field=compare_val,
            val=filter_value
        )

        if not match:
            # Short circuit as soon as we fail to match a filter.
            trace_logger.debug(
                f"Excluding file with path '{file_path}' because it "
                f"contains the partitions '{found_partitions}' and the "
                f"user is filtering with '{field}{op}{filter_value}' "
                f"which for this path is {compare_val}'."
            )
            return False

    not_filtered = [
        x for x in query_partitions
        if not x['partition'] in found_partitions
    ]

    if not_filtered:
        # trace_logger.warning(
        #     f"These query partitions '{not_filtered}' were not found as "
        #     f"keys in the S3 path '{file_path}', so we are going to "
        #     'let this file through the filter but either the user has '
        #     'supplied an partition that does not exist or one of the S3 '
        #     'paths does not follow the partition pattern of the first S3 '
        #     'path in this instance.'
        # )
        return False

    return True


def get_most_recent_common_prefix(
    common_prefixes: Iterator[str],
) -> List[str]:
    """
    This filtering logic only applies to Structured datasets. For a
    Structured dataset, we expect the first common prefix on S3 to be an
    `as_of_` representing when the data was published. It is expected to be
    in ISO 8601 format as this can be parsed into a Python DateTime.

    Return only the most recent `as_of` common prefix.

    :param common_prefixes: List of common prefixes for this dataset on S3.
    :return:  The most recent common_prefix for this dataset on S3. We return
        a collection because there is an edge case where there are common
        prefixes on S3 that do not have as_of, in which case
    """

    as_of_to_common_prefix: dict = defaultdict(list)
    as_of_warning_shown = False

    # Accumulate the `as_of_` dates from the common prefixes.
    for common_prefix in common_prefixes:
        partitions = {
            k.lower(): v for k, v in dict(
                _get_partitions_in_filepath(common_prefix)
            ).items()
        }

        # Partition cannot be filtered out if does not have an
        # `as_of_`. Get the first instance of a key that begins
        # with `as_of_`.
        as_of_key = next(
            (k for k, v in partitions.items()
             if k.startswith('as_of_')),
            None
        )

        if not as_of_key:
            # There is not an `as_of_` in this common prefix!
            # Only show the message the first time, otherwise it will
            # spam the logs.
            if not as_of_warning_shown:
                trace_logger.warning(
                    'as_of_ not in partitions but load type is full, '
                    'so not filtering out this common prefix but will '
                    'consider it as having the oldest as_of_ possible.',
                    extra={
                        'common_prefix': common_prefix,
                    }
                )
                as_of_warning_shown = True

            as_of_to_common_prefix[
                datetime.min
            ].append(common_prefix)
        else:
            # For a `load_type` = `Full Load` dataset, we only want
            # to return the data in the most recent `as_of_`
            # directory. We accumulate a dict of `as_of_` to
            # common_prefix, then at the end we know what the most recent
            # `as_of_` is and only return that common prefix.
            as_of_to_common_prefix[
                isoparse(partitions[as_of_key])
            ].append(common_prefix)

    if as_of_to_common_prefix:
        # Return only the most recent common prefix.
        # To sort, we have to action the iterator and therefore the type
        # changes to a List.
        most_recent_as_of = sorted(
            as_of_to_common_prefix.keys()
        )[-1]
        trace_logger.debug(
            'Load type is full, so returning most recent '
            f"as_of_ common prefix: '{most_recent_as_of}'"
        )
        return as_of_to_common_prefix[most_recent_as_of]
    else:
        # Edge case - the `load_type` is `Full Load` but
        # there are zero as_of_ keys, so return and empty list. The
        # code calling this filter will have to return a user
        # friendly error message about there being no files in the
        # dataset.
        # Alternatively, the cache might not be up to date causing
        # the most recent as_of_ to not be in the list.
        trace_logger.warning(
            'Zero as_of_ keys in the partitions but load type is '
            'full. We may have returned some paths that did not '
            'have an as_of_ key in their common_prefix. Alternatively, '
            'we may need to wait for the cache to update.'
        )
        return []


def get_common_prefixes(
    resource,
    bucket,
    prefix: str,
) -> Iterator[str]:
    """
    Abstract over the S3 location and return a list of the common prefixes
    (the top-level of directories under the dataset's S3 prefix..

    :param prefix: e.g. as_of_date=2019
    :param bucket: e.g. consumption-performance-test
    :param resource:

    :return: Iterator of paths for the top-level of directories under the
        dataset's S3 prefix.
    """
    trace_logger.debug(
        'get_common_prefixes - start paginating s3 list from prefix '
        f"'{prefix}' to delimiter '/'",
        extra={
            'Bucket': bucket.name,
            'Prefix': prefix,
        }
    )

    delimiter = '/'
    start_after = None  # Used for pagination of S3 results.
    max_loops = 1000000  # Used to prevent infinite loops.
    i = 0

    while i < max_loops and True:
        i += 1  # Counter to prevent infinite loops.
        response: Dict[str, str]

        if start_after:
            trace_logger.debug(
                f'next page of s3 list results (start_after {start_after})...',
                extra={
                    'Bucket': bucket.name,
                    'Prefix': prefix,
                    'Delimiter': delimiter,
                    'start_after': start_after,
                }
            )
            response = resource.meta.client.list_objects_v2(
                Bucket=bucket.name,
                Prefix=prefix,
                Delimiter=delimiter,
                StartAfter=start_after,
            )
        else:
            # Initial loop
            trace_logger.debug(
                'start paginating s3 list...',
                extra={
                    'Bucket': bucket.name,
                    'Prefix': prefix,
                    'Delimiter': delimiter,
                }
            )
            response = resource.meta.client.list_objects_v2(
                Bucket=bucket.name,
                Prefix=prefix,
                Delimiter=delimiter,
                # No StartAfter param in initial loop.,
            )

        # Type could be horrible as it comes from a response.
        common_prefixes: Union[
            str,
            Dict[str, str],
            List[Dict[str, str]]
        ] = response.get('CommonPrefixes', [])

        last_prefix = None
        if common_prefixes:
            if isinstance(common_prefixes, str):
                trace_logger.warning(
                    'common prefix came back as a single string '
                    'instead of a list of dict which was unexpected '
                    'but was handled'
                )
                last_prefix = common_prefixes
                yield common_prefixes
            if isinstance(common_prefixes, Dict):
                trace_logger.warning(
                    'common prefix came back as a single dict '
                    'instead of a list of dict which was unexpected '
                    'but was handled',
                    extra={
                        'response first N chars': str(response)[:1000]
                    }
                )
                last_prefix = common_prefixes.get(
                    'Prefix',
                    None
                )
                yield common_prefixes.get('Prefix', '')
            elif isinstance(common_prefixes, List):
                # Example of common_prefixes structure:
                #  [
                #     {
                #         "Prefix":
                #             "short_code/as_of_date=2020-09-22/"
                #     },
                #     {
                #         "Prefix":
                #             "short_code/as_of_date=2020-09-23/"
                #     }
                # ]
                for current_common_prefix in common_prefixes:
                    last_prefix = current_common_prefix.get(
                        'Prefix',
                        None
                    )
                    yield last_prefix
            else:
                trace_logger.error(
                    'type error for common_prefixes',
                    extra={
                        'common_prefixes': common_prefixes,
                        'type common_prefixes': type(common_prefixes),
                        'response first N chars': str(response)[:1000]
                    }
                )
                raise Exception(
                    'type error for common_prefixes - '
                    f'type: {type(common_prefixes)}, '
                    f'common_prefixes: {common_prefixes}'
                )
        else:
            trace_logger.debug(
                'Zero common_prefixes',
                extra={
                    'response first N chars': str(response)[:1000],
                }
            )
            last_prefix = None

        if response.get('IsTruncated') and last_prefix:
            start_after = last_prefix
            trace_logger.debug(
                'Truncated response, so more results on the next '
                'page',
                extra={
                    'start_after': start_after,
                    'response first N chars': str(response)[:1000],
                }
            )
        else:
            break


def is_hidden_file(path: str, content_type: str) -> bool:
    """
    [DL-4545][DL-4536][DL-5209] Do not read into files or
    directories that are cruft from Spark which Spark will ignore
    on read, e.g. files/dirs starting with `.` or `_` are hidden
    to Spark.

    Skip as_of_*=latest as it is a Spark temporary folder.

    :param content_type: Structured/Unstructured
    :param path: e.g. as_of_date=2019, .latest, as_of_date=latest
    :return: True if the path matches the criteria of a hidden file.
    """
    return (
        path.startswith('.') or
        path.startswith('_') or
        (
            path == 'metadata' and
            content_type != "Unstructured"
        ) or
        (
            path.startswith('as_of_') and
            path.endswith('=latest')
        )
    )


def __to_s3_proxy_path_and_size(
    object_summary,
    absolute_path: bool,
    organisation_short_code: str,
) -> Tuple[str, int]:
    if absolute_path:
        path = f"s3://{organisation_short_code}/{object_summary.key}"
        return path, object_summary.size
    else:
        return object_summary.key, object_summary.size


def get_s3_list(
    bucket,
    prefix: str,
    absolute_path: bool,
    organisation_short_code: str,
) -> Iterator[Tuple[str, int]]:
    """
    S3 list everything in this bucket under this prefix.

    :param bucket:
    :param prefix: e.g. abc/as_of_date=2019, abc/as_of_date
    :param absolute_path: True returns absolute path to the file on S3 proxy.
    :param organisation_short_code:
    :return: S3 proxy path and size.
    """

    trace_logger.debug(f"Get S3 list for prefix '{prefix}'.")

    object_summaries = bucket.objects.filter(
        # Prefix searches for exact matches and folders
        Prefix=prefix
    )

    # Convert each object_summary into an S3 proxy path.
    for object_summary in object_summaries:
        if not object_summary.key.endswith('/'):
            yield __to_s3_proxy_path_and_size(
                object_summary=object_summary,
                absolute_path=absolute_path,
                organisation_short_code=organisation_short_code
            )


def filter_non_hidden_common_prefixes(
    common_prefixes: Iterator[str],
    prefix: str,
    content_type: str,
) -> Iterator[str]:
    """
    Filter out S3 paths that are hidden directories. This function is intended
    for use with common prefixes.

    :param common_prefixes: Iterator of paths for the top-level of
        directories under the dataset's S3 prefix.
    :param prefix: e.g. abc/as_of_date=2019, abc/as_of_date
    :param content_type: Structured/Unstructured
    :return:
    """

    def shorten(common_prefix: str):
        """
        Path is made by stripping the common prefix of the prefix
        and the delimiter, which S3 returns.

        :param common_prefix: e.g. abc/as_of_date=2019/
        :return: as_of_date=2019
        """

        top_level_path = common_prefix
        if common_prefix.startswith(prefix):
            top_level_path = common_prefix[len(prefix):]
        if common_prefix.endswith('/'):
            top_level_path = top_level_path[:-1]
        return top_level_path

    yield from (
        common_prefix for common_prefix in common_prefixes
        if not is_hidden_file(shorten(common_prefix), content_type)
    )


def get_s3_list_filter_out_hidden(
    resource,
    bucket,
    prefix: str,
    content_type: str,
    load_type: str,
    absolute_path: bool,
    organisation_short_code: str,
) -> Iterator[Tuple[str, int]]:
    """
    Top-level common prefix filtering. We need to prevent reading into
    hidden folders. In the case of Bilateral the latest folders are
    growing linearly and for us to do an iterative list and post filter
    out folders we do not want is taking too long on prod. We need to
    filter out at the common prefix level!

    :param resource:
    :param bucket:
    :param prefix: e.g. abc/as_of_date=2019, abc/as_of_date
    :param content_type: Structured/Unstructured
    :param load_type: Either None, "Incremental Load" or "Full Load". None
        should have the same behaviour as "Incremental Load".
    :param absolute_path: True returns absolute path to the file on S3 proxy.
    :param organisation_short_code:
    :return: S3 proxy path and size.
    """

    common_prefixes: Iterator[str] = get_common_prefixes(
        resource=resource,
        bucket=bucket,
        prefix=prefix,
    )

    non_hidden_common_prefixes = filter_non_hidden_common_prefixes(
        common_prefixes=common_prefixes,
        prefix=prefix,
        content_type=content_type,
    )

    unique_non_hidden_common_prefixes = set([])

    trace_logger.debug(
        f"load_type from Catalogue: '{load_type}'",
        extra={
            'load_type': load_type,
        }
    )

    if load_type == 'Full Load':
        # For a Structured dataset, we expect the first common prefix on S3
        # to be an `as_of` representing when the data was published.
        #
        # If the dataset's load type is "Full Load"
        # then return only data from the most recent `as_of` common prefix.
        # Else (if the dataset's load type is "Incremental Load" or None),
        # then we return data from all as_of common prefixes.
        unique_non_hidden_common_prefixes.update(get_most_recent_common_prefix(
            common_prefixes=non_hidden_common_prefixes
        ))
    else:
        for common_prefix in non_hidden_common_prefixes:
            # We do not need the entire path of each non-hidden
            # common prefix. We only need to know the prefix and the
            # partition name of the common prefix (if exists) knowing
            # it will not be a `.` or `_`. We do not want to keep the
            # unique value of the partition as that will cause use to
            # make an S3 call for each unique partition.
            # e.g. for common_prefix
            #     abc/as_of_date=2020
            # we only store
            #     abc/as_of_date
            # and so all the as_of_dates are collected in a single
            # S3 list operation with prefix starting abc/as_of_date.
            if '=' in common_prefix:
                prefix_plus_partition, _ = common_prefix.split('=', 1)
            else:
                # Edge case where the top-level is not partitioned.
                prefix_plus_partition = common_prefix

            unique_non_hidden_common_prefixes.add(prefix_plus_partition)

    for non_hidden_common_prefix in unique_non_hidden_common_prefixes:
        # Now loop over the unique prefix plus partition to get a list
        # of the contents.
        # e.g. for
        #   abc/as_of_date
        # the S3 list could return:
        #   abc/as_of_date=2019/file.parquet
        #   abc/as_of_date=2020/file.parquet
        yield from get_s3_list(
            bucket=bucket,
            prefix=non_hidden_common_prefix,
            absolute_path=absolute_path,
            organisation_short_code=organisation_short_code,
        )
