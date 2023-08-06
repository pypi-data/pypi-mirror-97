"""
webspinner.connect.aws
----------------------
This module provides utilities for connecting to AWS data sources.

:copyright: (c) 2021, Alliance for Sustainable Energy, LLC
:license: BSD-3
"""

import logging
from urllib.parse import quote_plus

import boto3
# You'll want pyathena >= 1.11.2 if you plan to query Athena tables with 
# missing data
import pyathena
try:
    # Location starting with version 2.X.X
    from pyathena.pandas.cursor import PandasCursor
except ImportError:
    # Location prior to version 2.X.X
    from pyathena.pandas_cursor import PandasCursor
import sqlalchemy as sa

import webspinner

logger = logging.getLogger(__name__)


class AthenaEngine(object):
    """
    Class that connects to Athena using sqlalchemy.

    Attributes
    ----------
    database_name : str
        a.k.a Athena schema_name    
    region_name : str
        AWS region, e.g., 'us-west-2'
    s3_staging_dir : None or str
        s3 path to data in Athena. Starts with 's3://'.
    work_group : None or str
        AWS work group
    """

    def __init__(self, database_name, region_name = None,
                 s3_staging_dir = None, work_group = None):

        # consolidate direct and configured arguments
        kwargs = _get_aws_connection_kwargs(
            s3_staging_dir=s3_staging_dir,
            region_name=region_name, 
            schema_name=database_name, 
            work_group=work_group)
        
        all_kwargs = {}
        for key in ['s3_staging_dir', 'region_name', 'schema_name', 'work_group']:
            if key in kwargs:
                all_kwargs[key] = kwargs[key]
            else:
                all_kwargs[key] = None

        self.database_name = all_kwargs['schema_name']
        self.region_name = all_kwargs['region_name']
        self.s3_staging_dir = all_kwargs['s3_staging_dir']
        self.work_group = all_kwargs['work_group']

        con, _cur, engine = make_athena_connection(
            s3_staging_dir = all_kwargs['s3_staging_dir'],
            region_name = all_kwargs['region_name'],
            schema_name = all_kwargs['schema_name'],
            work_group = all_kwargs['work_group'])
        self._con = con
        self._engine = engine

    @property
    def sa_engine(self):
        """
        Returns
        -------
        sqlalchemy.engine.Engine
        """
        return self._engine

    @property
    def pa_con(self):
        """
        Returns
        -------
        pyathena.connection.Connection
        """
        return self._con


class AthenaConnection(object):
    """
    Class that provides context management for AthenaEngine.sa_engine 
    connections.

    Per https://docs.sqlalchemy.org/en/13/core/connections.html, it appears this
    class is redundant and should be deprecated in favor of:

    with athena_engine.sa_engine.connect() as con:
        ...
    """

    def __init__(self, athena_engine):
        """
        Parameters
        ----------
        athena_engine : AthenaEngine
        """
        assert isinstance(athena_engine, AthenaEngine)
        self._engine = athena_engine
        self._connection = None
    
    def __enter__(self):
        """
        Returns
        -------
        sqlalchemy.engine.Connection
        """
        self._connection = self._engine.sa_engine.connect()
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the connection.
        """
        self._connection.close()


def make_athena_connection(s3_staging_dir = None,
                           region_name = None, 
                           schema_name = None,
                           work_group = None):

    """
    Function that connects to an Athena database.

    Parameters
    ----------
    s3_staging_dir : str
        s3 path to data in Athena. Starts with 's3://'.
    region_name : str
        AWS region, e.g., 'us-west-2'
    schema_name : str
        name of the Athena database schema (a.k.a. database_name in AthenaEngine)
    work_group : None or str
        name of the AWS work_group

    Returns
    -------
    con : pyathena.connection.Connection
    cur : pyathena.cursor.Cursor
    engine : sqlalchemy.engine.Engine
    """
    # consolidate direct and configured arguments
    kwargs = _get_aws_connection_kwargs(
        s3_staging_dir=s3_staging_dir,
        region_name=region_name, 
        schema_name=schema_name, 
        work_group=work_group)
    
    con = pyathena.connect(**kwargs)
    cur = con.cursor()

    engine = None 
    if kwargs['schema_name'] is not None:
        assert kwargs['region_name'] is not None, kwargs
        conn_str = make_athena_connection.CONNECTION_STRING.format(
            region_name = kwargs['region_name'],
            database_name = kwargs['schema_name'])
        sep = '?'
        if kwargs['s3_staging_dir'] is not None:
            conn_str += '{sep}s3_staging_dir={s3_staging_dir}'.format(
                sep = sep, s3_staging_dir = kwargs['s3_staging_dir'])
            sep = '&'
        if kwargs['work_group'] is not None:
            conn_str += '{sep}work_group={work_group}'.format(
                sep = sep, work_group = kwargs['work_group'])
        logger.debug(f"Connecting to AWS Athena with connection string:{conn_str}")
        engine = sa.create_engine(conn_str)

    return con, cur, engine
make_athena_connection.CONNECTION_STRING = 'awsathena+rest://:@athena.{region_name}.amazonaws.com:443/{database_name}'


def _get_aws_connection_kwargs(s3_staging_dir = None, region_name = None, 
                               schema_name = None, work_group = None):

    result = {}
    keys_and_vals = [
        ('s3_staging_dir', s3_staging_dir),
        ('region_name', region_name),
        ('schema_name', schema_name),
        ('work_group', work_group)]

    # first get configured values
    if webspinner.WEBSPINNER_CONFIGURATION is not None:
        if 'AWS' in webspinner.WEBSPINNER_CONFIGURATION:
            for key, _ignore in keys_and_vals:
                if key in webspinner.WEBSPINNER_CONFIGURATION['AWS']:
                    val = webspinner.WEBSPINNER_CONFIGURATION['AWS'][key]
                    if val is not None:
                        result[key] = quote_plus(val) if key == 's3_staging_dir' else val
                    
    # now override with supplied values
    for key, val in keys_and_vals:
        if (key not in result) or (val is not None):
            # missing parameters are added, even if they are none
            # non-null passed-in values override default configuration
            result[key] = quote_plus(val) if (val is not None) and (key == 's3_staging_dir') else val

    return result


def read_athena_sql(sql, con, max_tries=5):
    """
    Equivalent to calling pd.read_sql(sql, con), but uses code that is more 
    computationally efficient.

    Parameters
    ----------
    sql : str
        SQL text to execute
    con : pyathena.connection.Connection
        con returned from make_athena_connection
    max_tries : int
        maximum number of times to try downloading data

    Returns
    -------
    pandas.DataFrame
        
    Raises
    ------
    WebspinnerRuntimeError
        If cannot download data within max_tries
    """

    for i in range(max_tries):
        try:
            logger.debug(f"SQL to be executed on Athena:\n{sql}")
            cursor = con.cursor(PandasCursor)
            return cursor.execute(sql).as_pandas()
        except Exception as sqlerr:
            # help diagnose new-to-us exception types
            cause = sqlerr.__cause__ if hasattr(sqlerr, '__cause__') else 'no __cause__ attr'
            logger.debug(f"Athena query\n{sql}\nfailed due to an "
                         f"exception of type {type(sqlerr)}:\n{sqlerr}\n"
                         f"Listed __cause__ is: {cause}")

            # don't retry if this is a basic SQL error
            if hasattr(sqlerr, '__cause__') and (sqlerr.__cause__ is not None):
                if hasattr(sqlerr.__cause__, 'operation_name'):
                    check_error = sqlerr.__cause__.operation_name
                    if check_error == 'StartQueryExecution':
                        logger.error(f"Athena query\n{sql}\nfailed due to an "
                            f"exception of type {type(sqlerr)}:\n{sqlerr}")
                        raise

            # don't retry if we're getting a value error (e.g., could not convert string to float)
            if type(sqlerr) == ValueError:
                logger.error(f"Athena query\n{sql}\n failed due to an "
                             f"exception of type {type(sqlerr)}:\n{sqlerr}")
                raise

            logger.warning(f'Iteration {i+1} of trying to execute SQL '
                f'statement on Athena failed, because {sqlerr}')

    # Failed to download data within max_tries. Raise an exception
    raise webspinner.WebspinnerRuntimeError(f'Executing SQL query:\n{sql}\n'
            f'on Athena failed {i+1} times.')


def download_s3_file(bucket_name, s3_filename, dest_filename):
    """
    Download a file from AWS S3

    Parameters
    ----------
    bucket_name : str
        AWS S3 bucket. Must already have configured access to AWS with permissions
        that provide access to the bucket.
    s3_filename : str
        path to the file to be downloaded, as it appears in the AWS bucket
    dest_filename : str or pathlib.Path
        local path to where the file is to be copied

    Raises
    ------
    WebspinnerRuntimeError
        If the file download fails for any reason
    """

    try:
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, s3_filename, str(dest_filename))
    except Exception as e:
        raise webspinner.WebspinnerRuntimeError("Unable to download "
            f"{s3_filename!r} from bucket {bucket_name!r} to {dest_filename}, "
            f"because {e}")
