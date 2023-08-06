from datetime import datetime
from typing import List
from unittest.mock import Mock, PropertyMock

import pytest
from freezegun import freeze_time
from moto import mock_s3

from dli.aws import create_refreshing_session, _meets_partition_params, \
    match_partitions, get_most_recent_common_prefix

path_with_as_of_date = 'prefix/a=2/b=4/c=6/as_of_date=2020-01-23/file.ext'
path_with_as_of_year_month = 'prefix/a=2/b=4/c=6/' \
                             'as_of_year_month=2020-01/file.ext'
paths_and_sizes = [
    'prefix/as_of_date=2020-01-01/file0.ext',
    'prefix/as_of_date=2020-01-02/file1.ext',
    'prefix/as_of_date=2020-01-03/file2.ext',
    'prefix/as_of_date=2020-01-03/file3.ext',
]
paths_without_as_of = [
    'prefix/file0.ext',
    'prefix/file1.ext',
]


@mock_s3
def test_session_refreshes():
    dli_client = Mock()
    # This is how you give an attribute a side effect
    auth_key = PropertyMock(return_value='abc')
    type(dli_client.session).auth_key = auth_key 

    dli_client.session.token_expires_on = datetime(2000, 1, 2, 0, 0, 0)
    session = create_refreshing_session(dli_client.session).resource('s3')

    with freeze_time(datetime(2000, 1, 1, 0, 0, 0)):
        assert auth_key.call_count == 1
        session.meta.client.list_buckets()
        assert auth_key.call_count == 1
        session.meta.client.list_buckets()
        assert auth_key.call_count == 1

    with freeze_time(datetime(2000, 1, 3, 0, 0, 0)):
        dli_client.session.token_expires_on = datetime(2000, 1, 4, 0, 0, 0)
        assert auth_key.call_count == 1
        session.meta.client.list_buckets()
        assert auth_key.call_count == 2
        session.meta.client.list_buckets()
        assert auth_key.call_count == 2


@pytest.mark.parametrize(
    'path,partition_query',
    [
        [
            path_with_as_of_date,
            [{'partition': 'a', 'operator': '>', 'value': '3'}],
        ],

        [
            path_with_as_of_date,
            [{'partition': 'c', 'operator': "<", 'value': '5'}],
        ],

        [
            path_with_as_of_date,
            [{'partition': 'as_of_date', 'operator': '<',
              'value': '2020-01-23'}],
        ],
        [
            path_with_as_of_year_month,
            [{'partition': 'as_of_year_month', 'operator': '<',
              'value': '2020-01'}],
        ],

        [
            path_with_as_of_date,
            [{'partition': 'as_of_date', 'operator': '>',
              'value': '2020-01-23'}],
        ],
        [
            path_with_as_of_year_month,
            [{'partition': 'as_of_year_month', 'operator': '>',
              'value': '2020-01'}],
        ],
    ],
)
def test_fails_partition_params(path: str, partition_query: List):
    assert not _meets_partition_params(path, partition_query)


@pytest.mark.parametrize(
    'path,partition_query',
    [
        [
            path_with_as_of_date,
            [
                {'partition': 'as_of_date', 'operator': '=',
                 'value': '2020-01-23'}
            ]
        ],
        # Left starts with space
        [
            path_with_as_of_date,
            [{'partition': ' as_of_date', 'operator': '=',
              'value': '2020-01-23'}
             ]
        ],
        # Left ends with space
        [
            path_with_as_of_date,
            [{'partition': 'as_of_date ', 'operator': '=',
              'value': '2020-01-23'}
             ]
        ],
        # Left starts and ends with space
        [
            path_with_as_of_date,
            [{'partition': ' as_of_date ', 'operator': '=',
              'value': '2020-01-23'}
             ]
        ],
        # Right starts with space
        [
            path_with_as_of_date,
            [{'partition': 'as_of_date', 'operator': '=',
              'value': ' 2020-01-23'}
             ]
        ],
        # Right ends with space
        [
            path_with_as_of_date,
            [{'partition': 'as_of_date', 'operator': '=',
              'value': '2020-01-23 '}
             ]
        ],
        # Right starts and ends with space
        [
            path_with_as_of_date,
            [{'partition': 'as_of_date', 'operator': '=',
              'value': ' 2020-01-23 '}
             ]
        ],

        # Left starts with space
        [
            path_with_as_of_year_month,
            [{'partition': ' as_of_year_month', 'operator': '=',
              'value': '2020-01'}
             ]
        ],
        # Left ends with space
        [
            path_with_as_of_year_month,
            [{'partition': 'as_of_year_month ', 'operator': '=',
              'value': '2020-01'}
             ]
        ],
        # Left starts and ends with space
        [
            path_with_as_of_year_month,
            [{'partition': ' as_of_year_month ', 'operator': '=',
              'value': '2020-01'}
             ]
        ],
        # Right starts with space
        [
            path_with_as_of_year_month,
            [{'partition': 'as_of_year_month', 'operator': '=',
              'value': ' 2020-01'}
             ]
        ],
        # Right ends with space
        [
            path_with_as_of_year_month,
            [{'partition': 'as_of_year_month', 'operator': '=',
              'value': '2020-01 '}
             ]
        ],
        # Right starts and ends with space
        [
            path_with_as_of_year_month,
            [{'partition': 'as_of_year_month', 'operator': '=',
              'value': ' 2020-01 '}
             ]
        ],
    ]
)
def test_meets_date_supported_partition_params(
        path: str,
        partition_query: List
):
    assert _meets_partition_params(path, partition_query)


@pytest.mark.parametrize(
    'path,partition_query', [
        [
            path_with_as_of_date,
            [{'partition': 'a', 'operator': '<', 'value': '3'}],
        ],

        [
            path_with_as_of_date,
            [{'partition': 'b', 'operator': '=', 'value': '4'}],
        ],

        [
            path_with_as_of_date,
            [{'partition': 'c', 'operator': ">", 'value': '5'}],
        ],

        [
            path_with_as_of_date,
            [{'partition': 'as_of_date', 'operator': '=',
              'value': '2020-01-23'}],
        ],
        [
            path_with_as_of_year_month,
            [{'partition': 'as_of_year_month', 'operator': '=',
              'value': '2020-01'}],
        ],

        # Combination of all filters.
        [
            path_with_as_of_date,
            [{'partition': 'a', 'operator': '<', 'value': '3'},
             {'partition': 'b', 'operator': '=', 'value': '4'},
             {'partition': 'c', 'operator': ">", 'value': '5'},
             {'partition': 'as_of_date', 'operator': '=',
              'value': '2020-01-23'}],
        ],
        [
            path_with_as_of_year_month,
            [{'partition': 'a', 'operator': '<', 'value': '3'},
             {'partition': 'b', 'operator': '=', 'value': '4'},
             {'partition': 'c', 'operator': ">", 'value': '5'},
             {'partition': 'as_of_year_month', 'operator': '=',
              'value': '2020-01'}],
        ],
    ],
)
def test_meets_partition_params(path: str, partition_query: List):
    assert _meets_partition_params(path, partition_query)

@pytest.mark.parametrize(
    'partition_query', [
        [
            {'partition': 'd', 'operator': '<', 'value': '5'}
        ]
    ],
)
def test_fails_unknown_partition_params(
    partition_query: List
):
    assert not _meets_partition_params(path_with_as_of_date, partition_query)



@pytest.mark.parametrize(
    'path,partitions', [
        [
            path_with_as_of_date, ['a<3']
        ],
        [
            path_with_as_of_date, ['b=4']
        ],
        [
            path_with_as_of_date, ['c>5']
        ],
        [
            path_with_as_of_date, ['as_of_date=2020-01-23']
        ],
        [
            path_with_as_of_year_month, ['as_of_year_month=2020-01']
        ],
        # Combination of all filters.
        [
            path_with_as_of_date,
            ['a<3', 'b=4', 'c>5', 'as_of_date=2020-01-23']
        ],
        [
            path_with_as_of_year_month,
            ['a<3', 'b=4', 'c>5', 'as_of_year_month=2020-01']
        ],
        [
            'prefix/export_region=NorthAmerica/file.ext',
            ['export_region=NorthAmerica']
        ],
        [
            'prefix/export_region=North_America/file.ext',
            ['export_region=North_America']
        ],
        [
            'prefix/export_region=North America/file.ext',
            ['export_region=North America']
        ],
        [
            'prefix/export region=North America/file.ext',
            ['export region=North America']
        ],
    ],
)
def test_match_partitions(path: str, partitions: List[str]):
    assert match_partitions(path, partitions)


@pytest.mark.parametrize('path,partition_query', [
    [path_with_as_of_date, [{
        'partition': 'as_of_date',
        'operator': '=',
        'value': '202-01-23'
    }]],
    [path_with_as_of_year_month, [{
        'partition': 'as_of_year_month',
        'operator': '=',
        'value': '202-01'
    }]],
])
def test_raises_error_with_malformed_date(path: str, partition_query: List):
    with pytest.raises(ValueError):
        _meets_partition_params(path, partition_query)


def test_false_when_as_of_date_is_invalid():
    partition_query = [{
        'partition': 'as_of_date',
        'operator': '=',
        'value': '2020-01-23'
    }]

    invalid_path = 'b=4/c=6/as_of_date=ABC/file.ext'

    assert not _meets_partition_params(invalid_path, partition_query)


def test_load_type_full_returns_data_from_most_recent_as_of_date():
    assert get_most_recent_common_prefix(
        common_prefixes=paths_and_sizes,
    ) == paths_and_sizes[-2:]


def test_load_type_full_but_zero_paths_returns_empty():
    assert get_most_recent_common_prefix(
        common_prefixes=[],
    ) == []


def test_load_type_full_all_paths_without_as_of_date_return_paths():
    assert get_most_recent_common_prefix(
        common_prefixes=paths_without_as_of,
    ) == paths_without_as_of


def test_load_type_full_some_paths_without_as_of_date_return_paths():
    assert get_most_recent_common_prefix(
        common_prefixes=paths_and_sizes + paths_without_as_of,
    ) == paths_and_sizes[-2:]
