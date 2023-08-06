from datetime import datetime, date
import logging
from sqlalchemy import Column, Table, MetaData
from sqlalchemy.types import Integer, DateTime, String, Text, Float, Date
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.engine import Engine
from typing import List, Tuple, Callable, Iterable
import json

logger = logging.getLogger(__name__)

TABLE_NAME = 'great_players'
TEST_DATA_INITIAL = [
    {'first_name': 'Novak',
     'last_name': 'Djokovic',
     'playing_style_desc': 'aggressive/baseline',
     'win_percentage': 83.0,
     'high_rank': 1,
     'turned_pro': datetime(2003, 1, 1),
     'date_of_birth': date(1987, 3, 22)},
    {'first_name': 'Rafael',
     'last_name': 'Nadal',
     'playing_style_desc': 'aggressive/baseline',
     'win_percentage': 83.2,
     'high_rank': 1,
     'turned_pro': datetime(2001, 1, 1),
     'date_of_birth': date(1986, 6, 3)},
    {'first_name': 'Roger',
     'last_name': 'Federer',
     'playing_style_desc': 'aggressive/all-court',
     'win_percentage': 81.2,
     'high_rank': 1,
     'turned_pro': datetime(1998, 1, 1),
     'date_of_birth': date(1981, 8, 8)}
]
TEST_DATA_APPEND_MULTIPLE_ROWS = [
    {'first_name': 'Stefanos',
     'last_name': 'Tsitsipas',
     'playing_style_desc': 'aggressive/all-court',
     'win_percentage': 67.6,
     'high_rank': 5,
     'turned_pro': datetime(2016, 1, 1),
     'date_of_birth': date(1998, 8, 12)},
    {'first_name': 'Alexander',
     'last_name': 'Zverev',
     'playing_style_desc': 'aggressive/baseline',
     'win_percentage': 65.8,
     'high_rank': 3,
     'turned_pro': datetime(2013, 1, 1),
     'date_of_birth': date(1997, 4, 12)},
    {'first_name': 'Dominic',
     'last_name': 'Thiem',
     'playing_style_desc': 'aggressive/baseline',
     'win_percentage': 65.1,
     'high_rank': 3,
     'turned_pro': datetime(2011, 1, 1),
     'date_of_birth': date(1993, 10, 3)}
]
TEST_DATA_APPEND_MULTIPLE_ROWS_WITH_DELETE = TEST_DATA_APPEND_MULTIPLE_ROWS[1:]
TEST_DATA_APPEND_SINGLE_ROW = [
    {'first_name': 'Andy',
     'last_name': 'Murray',
     'playing_style_desc': 'defensive/baseline',
     'win_percentage': 77.1,
     'high_rank': 1,
     'turned_pro': datetime(2005, 1, 1),
     'date_of_birth': date(1987, 5, 15)}
]
TEST_DATA_UPDATE_SINGLE_ROW = [
    {'first_name': 'Andy',
     'last_name': 'Murray',
     'playing_style_desc': 'defensive/baseline',
     'win_percentage': 77.4,
     'high_rank': 1,
     'turned_pro': datetime(2005, 1, 1),
     'date_of_birth': date(1987, 5, 15)}
]

TEST_TABLE_METADATA = Table(TABLE_NAME,
                            MetaData(),
                            Column('first_name', String(256), primary_key=True),
                            Column('last_name', String(256), primary_key=True),
                            Column('playing_style_desc', Text),
                            Column('win_percentage', Float),
                            Column('high_rank', Integer),
                            Column('turned_pro', DateTime),
                            Column('date_of_birth', Date))


FIRST_UPDATE, SECOND_UPDATE, THIRD_UPDATE, FOURTH_UPDATE, FIFTH_UPDATE = tuple(range(5))
ALL_UPDATES = (FIRST_UPDATE, SECOND_UPDATE, THIRD_UPDATE, FOURTH_UPDATE, FIFTH_UPDATE)


def get_expected_dolt_diffs(update_num: int):
    """
    The fixture fixtures.dolt.create_dolt_test_data_with_commits writes writes a sequence of four updates, this function
    returns the expected results at each of those updates.
    :return:
    """
    assert update_num in ALL_UPDATES, 'update must be one of {}'.format(update_num)

    diffs = {
        FIRST_UPDATE: ([], TEST_DATA_INITIAL),
        SECOND_UPDATE: ([], TEST_DATA_APPEND_SINGLE_ROW),
        THIRD_UPDATE: ([], TEST_DATA_APPEND_MULTIPLE_ROWS),
        FOURTH_UPDATE: ([], TEST_DATA_UPDATE_SINGLE_ROW),
        FIFTH_UPDATE: ([{'first_name': 'Stefanos', 'last_name': 'Tsitsipas'}], [])
    }

    return diffs[update_num]


def get_expected_data(update_num: int) -> Tuple[list, list]:
    """
    The fixture fixtures.dolt.create_dolt_test_data_with_commits writes writes a sequence of four updates, this function
    returns the expected results at each of those updates.
    :return:
    """
    assert update_num in ALL_UPDATES, 'update must be one of {}'.format(update_num)

    cumulative = {
        FIRST_UPDATE: ([], TEST_DATA_INITIAL),
        SECOND_UPDATE: ([], TEST_DATA_INITIAL + TEST_DATA_APPEND_SINGLE_ROW),
        THIRD_UPDATE: ([], TEST_DATA_INITIAL + TEST_DATA_APPEND_SINGLE_ROW + TEST_DATA_APPEND_MULTIPLE_ROWS),
        FOURTH_UPDATE: ([], TEST_DATA_INITIAL + TEST_DATA_APPEND_MULTIPLE_ROWS + TEST_DATA_UPDATE_SINGLE_ROW),
        FIFTH_UPDATE:
            ([{'first_name': 'Stefanos', 'last_name': 'Tsitsipas'}],
             TEST_DATA_INITIAL + TEST_DATA_APPEND_MULTIPLE_ROWS_WITH_DELETE + TEST_DATA_UPDATE_SINGLE_ROW)
    }

    return cumulative[update_num]


def get_dolt_update_row_statement(table: Table):
    """
    Helper function used to form a update query for building test data.
    :return:
    """
    update = TEST_DATA_UPDATE_SINGLE_ROW[0]
    update_statement = (table
                        .update()
                        .values(win_percentage=update['win_percentage'])
                        .where(table.c.first_name == update['first_name'])
                        .where(table.c.last_name == update['last_name']))

    return update_statement


def get_dolt_drop_pk_query(table: Table):
    """
    Helper function used to form a delete query for building test data.
    :return:
    """
    first_name, last_name = 'Stefanos', 'Tsitsipas'
    delete_statement = (table
                        .delete()
                        .where(table.c.first_name == first_name)
                        .where(table.c.last_name == last_name))

    return delete_statement


def get_data_for_comparison(engine: Engine):
    with engine.connect() as conn:
        result = conn.execute(TEST_TABLE_METADATA.select())
        return [dict(row) for row in result]


DROP_TEST_TABLE = 'DROP TABLE {table_name}'.format(table_name=TABLE_NAME)


def by_first_last(dic: dict) -> tuple:
    return dic['first_name'], dic['last_name']


def assert_rows_equal(left: List[dict],
                      right: List[dict],
                      comparator: Callable[[dict], tuple] = by_first_last,
                      datetime_strict: bool = True):
    assert len(left) == len(right)
    failed = False

    if len(left) == 0 and len(right) == 0:
        return True

    l, r = sorted(left, key=comparator), sorted(right, key=comparator)

    for left_row, right_row in zip(l, r):
        for left_column, left_value in left_row.items():
            if left_column in right_row:
                right_value = right_row[left_column]

                # datetime coercion
                #   - Oracle connector returns both dates and timestamps as datetime, and coerces a datetime in SQL
                #     Alchemy to DATE (this seems like a bug as it is destructive). For now this code effectively
                #     ensures that type discrepancy can be account for by passing datetime_strict = False.
                if not datetime_strict:
                    left_value, right_value = coerce_date(left_value, right_value)

                if not isinstance(left_value, type(right_value)):
                    failed = True
                    logger.error('left value is of type {}, right value is of type {}'.format(type(left_value),
                                                                                              type(right_value)))

                if isinstance(left_value, float):
                    left_value, right_value = round(left_value, 4), round(right_value, 4)

                if left_value != right_value:
                    failed = True
                    logger.error('left value {} for column {} is not equal to {}'.format(left_value,
                                                                                         left_column,
                                                                                         right_value))
            else:
                failed = True
                logger.error('{} column is in left, but not right'.format(left_column))

    if failed:
        raise AssertionError('Errors found')
    else:
        return True


def coerce_date(left_value, right_value):
    if isinstance(left_value, datetime) and isinstance(right_value, datetime):
        return left_value, right_value

    if isinstance(left_value, datetime) and isinstance(right_value, date):
        left_value = date(left_value.year, left_value.month, left_value.day)

    elif isinstance(left_value, date) and isinstance(right_value, datetime):
        right_value = date(right_value.year, right_value.month, right_value.day)

    return left_value, right_value


TEST_DATA_WITH_ARRAYS = [
    {'id': 1,
     'ints': [1, 2],
     'floats': [1.1, 2.2],
     'dates': [datetime(2020, 1, 1), datetime(2019, 1, 1)],
     'json_data': json.dumps({"id": 1})},
    {'id': 2,
     'ints': [None, 2],
     'floats': [1.1, None],
     'dates': [datetime(2020, 1, 1), None],
     'json_data': json.dumps({})}
]

TABLE_WITH_ARRAYS_NAME = 'test_array_types'

POSTGRES_TABLE_WITH_ARRAYS = Table(TABLE_WITH_ARRAYS_NAME,
                                   MetaData(),
                                   Column('id', Integer, primary_key=True),
                                   Column('ints', ARRAY(Integer)),
                                   Column('floats', ARRAY(Float)),
                                   Column('dates', ARRAY(DateTime)),
                                   Column('json_data', JSON))

DOLT_TABLE_WITH_ARRAYS = Table(TABLE_WITH_ARRAYS_NAME,
                               MetaData(),
                               Column('id', String(32), primary_key=True),
                               Column('ints', LONGTEXT),
                               Column('floats', LONGTEXT),
                               Column('dates', LONGTEXT),
                               Column('json_data', LONGTEXT))


def deserialize_longtext(data: Iterable[dict]):
    """
    This function transforms array types serialized as LONGTEXT back to Python data structures. We currently do not
    support this as we do not support array types. An appropriate serialization scheme needs to be chosen to make this
    work, with JSON arrays being the current favorite.
    :param data:
    :return:
    """
    data_copy = []
    for row in data:
        row_copy = {}
        for col, val in row.items():
            if col == 'id':
                row_copy[col] = int(val)
            if col == 'ints':
                row_copy[col] = [int(el) if el != 'NULL' else None for el in val.split(',')]
            if col == 'floats':
                row_copy[col] = [float(el) if el != 'NULL' else None for el in val.split(',')]
            if col == 'dates':
                row_copy[col] = [datetime.strptime(el, '%Y-%m-%d %H:%M:%S') if el != 'NULL' else None
                                 for el in val.split(',')]
            if col == 'json_data':
                row_copy[col] = val

        data_copy.append(row_copy)

    return data_copy
