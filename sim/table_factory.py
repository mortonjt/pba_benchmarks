from __future__ import division
import numpy as np
from scipy.stats.distributions import lognorm
from scipy.linalg import block_diag
import itertools

import matplotlib.pyplot as plt
from sim.generators.ecological import *

"""
These tables are modeled after TableFactory_3613.py
"""

def getParams(dims=[1, 2], sts=[5, 3, 2],
              interactions=['amensal',
                            'commensal',
                            'mutual',
                            'parasite',
                            'competition',
                            'obligate_syntroph',
                            'partial_obligate_syntroph'],
              seed=0):
    """
    Creates the set of parameters required to construct the
    contingency table and the true correlation matrix

    Parameters
    ----------
    dims : list, int (optional)
       list of number of individuals per group
    sts : list, int (optional)
       list of interaction strengths
    interactions: list, str (optional)
       list of interaction types
    seed : int (optional)
       numpy initial random seed

    Returns
    -------
    dict of dicts:
       First set of keys - type of group interaction and strength
       Second set of keys - attributes for group
           strength : float
              strength of interaction
           func : function
              generator function
           dim : int
              number of individual per interaction
           data : np.array
              count table
           truth : np.array
              adjancency matrix
           name : str
              name of the interaction
    Notes
    -----
    The cartesian product of dims, sts and intereactions will be
    exploited.  So all possible combinations of dims, sts and
    interactions will be used
    """

    # Initalize all of the parameters
    np.random.seed(seed)
    params = \
        {"%s_related_%dd_st_%d" % (z, x, y): {
            # strength of interaction
            "strength": y/10,
            # generator function
            "func": eval('%s_%sd' % (z, ['1', 'n'][x-1])),
            # number of interactions
            "dim": x,
            # simulated data
            "data": [],
            # true correlation matrix
            "truth": [],
            "name": z
        } for (x, y, z) in itertools.product(dims,
                                             sts,
                                             interactions)}
    return params


def init_data(params, num_groups=30, num_samps=50):
    """
    Fills in the contingency tables and correlation matrices
    for each interaction group

    Parameters
    ----------
    params : dict of dicts:
       First set of keys - type of group interaction and strength
       Second set of keys - attributes for group
           strength : float
              strength of interaction
           func : function
              generator function
           dim : int
              number of individual per interaction
           data : np.array
              count table
           truth : np.array
              adjancency matrix
           name : str
              name of the interaction
    num_groups : int
        number of groups of interactions
    num_samps : int
        number of samples

    Returns
    -------
    dict of dicts:
       First set of keys - type of group interaction and strength
       Second set of keys - attributes for group
           strength : float
              strength of interaction
           func : function
              generator function
           dim : int
              number of individual per interaction
           data : np.array
              count table
           truth : np.array
              adjancency matrix
           name : str
              name of the interaction
    """
    D, S = num_groups, num_samps
    # Start filling in some tables
    for k in params.keys():
        x = params[k]['dim']+1

        os = lognorm.rvs(3, 0, size=(x*D, S))
        strength = params[k]['strength']
        params[k]['data'] = np.zeros((S, x*D))
        params[k]['truth'] = np.zeros((x*D, x*D))
        func = params[k]['func']
        for i in range(D):
            idx = range(x*i, x*i+x)
            if params[k]['name'] == 'partial_obligate_syntroph':
                if '1d' in k:
                    obs_otu = func(*list(os[idx]))
                else:
                    obs_otu = func(os[idx])
            else:
                if '1d' in k:
                    obs_otu = func(*(list(os[idx])+[strength]))
                else:
                    obs_otu = func(os[idx], strength)

            params[k]['data'][:, idx] = np.vstack(obs_otu).T

            if params[k]['name'] in {'commensal', 'mutual',
                                     'obligate_syntroph',
                                     'partial_obligate_syntroph'}:
                params[k]['truth'][idx[:-1], idx[-1]] = 1
            if params[k]['name'] in {'amensal', 'parasite', 'competition'}:
                params[k]['truth'][idx[:-1], idx[-1]] = -1

    return params


def build_contingency_table(params):
    """
    Parameters
    ----------
    params : dict of dicts:
       First set of keys - type of group interaction and strength
       Second set of keys - attributes for group
           strength : float
              strength of interaction
           func : function
              generator function
           dim : int
              number of individual per interaction
           data : np.array
              count table
           truth : np.array
              adjancency matrix
           name : str
              name of the interaction

    Returns
    -------
    np.array
        The observed contingency table
    """
    return np.hstack([params[k]['data'] for k in params.keys()])


def build_correlation_matrix(params):
    """
    Parameters
    ----------
    params : dict of dicts:
       First set of keys - type of group interaction and strength
       Second set of keys - attributes for group
           strength : float
              strength of interaction
           func : function
              generator function
           dim : int
              number of individual per interaction
           data : np.array
              count table
           truth : np.array
              adjancency matrix
           name : str
              name of the interaction

    Returns
    -------
    np.array
        The truth correlation matrix
    """
    return block_diag(*[params[k]['truth'] for k in params.keys()])
