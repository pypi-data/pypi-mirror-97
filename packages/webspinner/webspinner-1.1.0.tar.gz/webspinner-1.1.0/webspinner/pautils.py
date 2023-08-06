"""
webspinner.pautils
------------------
Utilities for working with the parquet data format, especially via pandas.

:copyright: (c) 2021, Alliance for Sustainable Energy, LLC
:license: BSD-3
"""

import pyarrow as pa
import pyarrow.parquet as pq

def to_parquet(df, p):
    """
    Writes df to .parquet. This method is able to handle multi-indexed columns.
    
    Parameters
    ----------
    df : DataFrame
    p : pathlib.Path or str
    """
    table = pa.Table.from_pandas(df)
    pq.write_table(table, str(p))
