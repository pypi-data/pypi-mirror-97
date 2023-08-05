#!/usr/bin/env python
#
# test_main_non_numeric.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import             warnings
import             os
import textwrap as tw
import os.path  as op
import multiprocessing as mp
from unittest import mock
from io import StringIO

import pytest

from collections import OrderedDict

import pandas as pd
import numpy  as np
import           h5py

from pandas.testing import assert_frame_equal

import funpack.importing      as importing
import funpack.exporting      as exporting
import funpack.exporting_hdf5 as exporting_hdf5
import funpack.exporting_tsv  as exporting_tsv
import funpack.datatable      as datatable
import funpack.custom         as custom
import funpack.util           as util
import funpack.main           as main

from . import (gen_DataTable,
               clear_plugins,
               patch_base_tables,
               patch_logging,
               tempdir,
               gen_test_data,
               gen_tables,
               gen_DataTableFromDataFrame)


@patch_logging
def test_main_write_non_numerics():

    data = tw.dedent("""
    eid,1-0.0,2-0.0,3-0.0,4-0.0
    1,11,a,31,ff
    2,12,b,32,gg
    3,13,c,33,hh
    4,14,d,34,ii
    5,15,e,35,jj
    """)
    expn = tw.dedent("""
    eid\t1-0.0\t3-0.0
    1\t11\t31
    2\t12\t32
    3\t13\t33
    4\t14\t34
    5\t15\t35
    """)
    expnn = tw.dedent("""
    eid\t2-0.0\t4-0.0
    1\ta\tff
    2\tb\tgg
    3\tc\thh
    4\td\tii
    5\te\tjj
    """)

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write(data)

        data  = pd.read_csv(StringIO(data),  index_col=0)
        expn  = pd.read_csv(StringIO(expn),  index_col=0, sep='\t')
        expnn = pd.read_csv(StringIO(expnn), index_col=0, sep='\t')

        base = ' -nb -ow out.csv data.txt'

        # default: both numeric and non-
        # numeric columns output to main file
        main.main(base.split())
        assert_frame_equal(pd.read_csv('out.csv', index_col=0), data)

        # --suppress_non_numerics - outfile
        # only contains numeric cols
        main.main(('-esn' + base).split())
        assert_frame_equal(pd.read_csv('out.csv', index_col=0), expn)

        # --write_non_numerics - non-numerics
        # saved to both main and auxillary
        # output files
        main.main(('-wnn' + base).split())
        assert_frame_equal(pd.read_csv('out.csv',              index_col=0), data)
        assert_frame_equal(pd.read_csv('out_non_numerics.csv', index_col=0), expnn)

        # --suppress + --write - non-numerics
        # saved to  auxillary output file
        main.main(('-esn -wnn' + base).split())
        assert_frame_equal(pd.read_csv('out.csv',              index_col=0), expn)
        assert_frame_equal(pd.read_csv('out_non_numerics.csv', index_col=0), expnn)
