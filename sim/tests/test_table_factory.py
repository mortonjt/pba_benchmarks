"""
Unit tests for table factory
"""

import unittest
import numpy.testing as npt
import numpy as np
from sim.table_factory import (getParams, init_data,
                               build_correlation_matrix)
from sim.generators.ecological import *


class TestParams(unittest.TestCase):
    def test_get(self):
        params = getParams(dims=[1], sts=[5], interactions=['amensal'])
        self.assertEquals(params,
                          {'amensal_related_1d_st_5':
                           {'data': [],
                            'dim': 1,
                            'func': amensal_1d,
                            'name': 'amensal',
                            'strength': 0.5,
                            'truth': []}})

        params = getParams(dims=[1, 2], sts=[5], interactions=['amensal'])
        self.assertEquals(params,
                          {'amensal_related_1d_st_5':
                           {'data': [],
                            'dim': 1,
                            'func': amensal_1d,
                            'name': 'amensal',
                            'strength': 0.5,
                            'truth': []},
                           'amensal_related_2d_st_5':
                           {'data': [],
                            'dim': 2,
                            'func': amensal_nd,
                            'name': 'amensal',
                            'strength': 0.5,
                            'truth': []}})

    def test_init(self):
        for interaction in ['amensal',
                            'commensal',
                            'mutual',
                            'parasite',
                            'competition',
                            'obligate_syntroph',
                            'partial_obligate_syntroph']:

            params = getParams(dims=[1, 2], sts=[5],
                               interactions=[interaction])
            params = init_data(params, num_groups=2, num_samps=2)
            for k in params.keys():
                if '1d' in k:
                    npt.assert_array_equal(params[k]['truth'],
                                           np.array([[0., 1., 0., 0.],
                                                     [0., 0., 0., 0.],
                                                     [0., 0., 0., 1.],
                                                     [0., 0., 0., 0.]]))
                else:
                    npt.assert_array_equal(params[k]['truth'],
                                           array([[0., 0., 1., 0., 0., 0.],
                                                  [0., 0., 1., 0., 0., 0.],
                                                  [0., 0., 0., 0., 0., 0.],
                                                  [0., 0., 0., 0., 0., 1.],
                                                  [0., 0., 0., 0., 0., 1.],
                                                  [0., 0., 0., 0., 0., 0.]]))

    def test_build_correlation_matrix(self):
        for interaction in ['amensal',
                            'commensal',
                            'mutual',
                            'parasite',
                            'competition']:

            params = getParams(dims=[1, 2], sts=[5],
                               interactions=[interaction])
            params = init_data(params, num_groups=2, num_samps=2)
            corr_mat = build_correlation_matrix(params)
            exp = np.array([[0., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
                            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                            [0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
                            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                            [0., 0., 0., 0., 0., 0., 1., 0., 0., 0.],
                            [0., 0., 0., 0., 0., 0., 1., 0., 0., 0.],
                            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                            [0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
                            [0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
                            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])
            npt.assert_array_equal(corr_mat, exp)

if __name__ == "__main__":
    unittest.main()
