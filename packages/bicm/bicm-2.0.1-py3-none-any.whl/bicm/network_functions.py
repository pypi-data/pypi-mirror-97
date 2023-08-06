"""
This module contains several functions for bipartite networks.
"""

import numpy as np
import scipy.sparse
from numba import jit


@jit(nopython=True)
def bicm_from_fitnesses(x, y):
    """
    Rebuilds the average probability matrix of the bicm from the fitnesses

    :param x: the fitness vector of the rows layer
    :type x: numpy.ndarray
    :param y: the fitness vector of the columns layer
    :type y: numpy.ndarray
    """
    avg_mat = np.zeros((len(x), len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            xy = x[i] * y[j]
            avg_mat[i, j] = xy / (1 + xy)
    return avg_mat


def sample_bicm(avg_mat):
    """
    Build a biadjacency matrix sampling from the probability matrix of a BiCM.
    """
    if not isinstance(avg_mat, np.ndarray):
        avg_mat = np.array(avg_mat)
    dim1, dim2 = avg_mat.shape
    return np.array(avg_mat > np.reshape(np.random.sample(dim1 * dim2), (dim1, dim2)), dtype=int)


def sample_bicm_edgelist(x, y):
    """
    Build an edgelist sampling from the fitnesses of a BiCM.
    """
    edgelist = []
    for i in range(len(x)):
        for j in range(len(y)):
            xy = x[i] * y[j]
            if np.random.uniform() < xy / (1 + xy):
                edgelist.append((i, j))
    return edgelist


def sample_bicm_edgelist_names(dict_x, dict_y):
    """
    Build an edgelist from the BiCM keeping the names of the nodes as contained in the BiCM fitnesses' dictionaries.
    """
    edgelist = []
    for xx in dict_x:
        for yy in dict_y:
            xy = dict_x[xx] * dict_y[yy]
            if np.random.uniform() < xy / (1 + xy):
                edgelist.append((xx, yy))
    return edgelist


@jit(nopython=True)
def edgelist_from_biadjacency_fast(biadjacency):
    """
    Build the edgelist of a bipartite network from its biadjacency matrix.
    """
    edgelist = []
    for i in range(biadjacency.shape[0]):
        for j in range(biadjacency.shape[1]):
            if biadjacency[i, j] == 1:
                edgelist.append((i, j))
    return edgelist


def edgelist_from_biadjacency(biadjacency):
    """
    Build the edgelist of a bipartite network from its biadjacency matrix.
    Accounts for sparse matrices and returns a structured array.
    """
    if scipy.sparse.isspmatrix(biadjacency):
        coords = biadjacency.nonzero()
        if np.sum(biadjacency.data != 1) > 0:
            raise ValueError('Only binary matrices')
        return np.array(list(zip(coords[0], coords[1])), dtype=np.dtype([('rows', int), ('columns', int)])),\
               np.array(biadjacency.sum(1)).flatten(), np.array(biadjacency.sum(0)).flatten()
    else:
        if np.sum(biadjacency[biadjacency != 0] != 1) > 0:
            raise ValueError('Only binary matrices')
        return np.array(edgelist_from_biadjacency_fast(biadjacency),
                        dtype=np.dtype([('rows', int), ('columns', int)])),\
               np.sum(biadjacency, axis=1), np.sum(biadjacency, axis=0)


def biadjacency_from_edgelist(edgelist, fmt='array'):
    """
    Build the biadjacency matrix of a bipartite network from its edgelist.
    Returns a matrix of the type specified by ``fmt``, by default a numpy array.
    """
    edgelist, rows_deg, cols_deg, rows_dict, cols_dict = edgelist_from_edgelist_bipartite(edgelist)
    if fmt == 'array':
        biadjacency = np.zeros((len(rows_deg), len(cols_deg)), dtype=int)
        for edge in edgelist:
            biadjacency[edge[0], edge[1]] = 1
    elif fmt == 'sparse':
        biadjacency = scipy.sparse.coo_matrix((np.ones(len(edgelist)), (edgelist['rows'], edgelist['columns'])))
    elif not isinstance(format, str):
        raise TypeError('format must be a string (either "array" or "sparse")')
    else:
        raise ValueError('format must be either "array" or "sparse"')
    return biadjacency, rows_deg, cols_deg, rows_dict, cols_dict


def edgelist_from_edgelist_bipartite(edgelist):
    """
    Creates a new edgelist with the indexes of the nodes instead of the names.
    Method for bipartite networks.
    Returns also two dictionaries that keep track of the nodes.
    """
    edgelist = np.array(list(set([tuple(edge) for edge in edgelist])))
    out = np.zeros(np.shape(edgelist)[0], dtype=np.dtype([('source', object), ('target', object)]))
    out['source'] = edgelist[:, 0]
    out['target'] = edgelist[:, 1]
    edgelist = out
    unique_rows, rows_degs = np.unique(edgelist['source'], return_counts=True)
    unique_cols, cols_degs = np.unique(edgelist['target'], return_counts=True)
    rows_dict = dict(enumerate(unique_rows))
    cols_dict = dict(enumerate(unique_cols))
    inv_rows_dict = {v: k for k, v in rows_dict.items()}
    inv_cols_dict = {v: k for k, v in cols_dict.items()}
    edgelist_new = [(inv_rows_dict[edge[0]], inv_cols_dict[edge[1]]) for edge in edgelist]
    edgelist_new = np.array(edgelist_new, dtype=np.dtype([('rows', int), ('columns', int)]))
    return edgelist_new, rows_degs, cols_degs, rows_dict, cols_dict


def adjacency_list_from_edgelist_bipartite(edgelist, convert_type=True):
    """
    Creates the adjacency list from the edgelist.
    Method for bipartite networks.
    Returns two dictionaries, each containing an adjacency list with the rows as keys and the columns as keys, respectively.
    If convert_type is True (default), then the nodes are enumerated and the adjacency list is returned as integers.
    Returns also two dictionaries that keep track of the nodes and the two degree sequences.
    """
    if convert_type:
        edgelist, rows_degs, cols_degs, rows_dict, cols_dict = edgelist_from_edgelist_bipartite(edgelist)
    adj_list = {}
    inv_adj_list = {}
    for edge in edgelist:
        adj_list.setdefault(edge[0], set()).add(edge[1])
        inv_adj_list.setdefault(edge[1], set()).add(edge[0])
    if not convert_type:
        rows_degs = np.array([len(adj_list[k]) for k in adj_list])
        rows_dict = {k: k for k in adj_list}
        cols_degs = np.array([len(inv_adj_list[k]) for k in inv_adj_list])
        cols_dict = {k: k for k in inv_adj_list}
    return adj_list, inv_adj_list, rows_degs, cols_degs, rows_dict, cols_dict


def adjacency_list_from_adjacency_list_bipartite(old_adj_list):
    """
    Creates the adjacency list from another adjacency list, converting the data type to integers.
    Method for bipartite networks.
    Returns two dictionaries, each representing an adjacency list with the rows or columns as keys, respectively.
    Original keys are treated as rows, values as columns.
    The nodes are enumerated and the adjacency list contains the related integers.
    Returns also two dictionaries that keep track of the nodes and the two degree sequences.
    """
    rows_dict = dict(enumerate(np.unique(list(old_adj_list.keys()))))
    cols_dict = dict(enumerate(np.unique([el for l in old_adj_list.values() for el in l])))
    inv_rows_dict = {v: k for k, v in rows_dict.items()}
    inv_cols_dict = {v: k for k, v in cols_dict.items()}
    adj_list = {}
    inv_adj_list = {}
    for k in old_adj_list:
        adj_list.setdefault(inv_rows_dict[k], set()).update({inv_cols_dict[val] for val in old_adj_list[k]})
        for val in old_adj_list[k]:
            inv_adj_list.setdefault(inv_cols_dict[val], set()).add(inv_rows_dict[k])
    rows_degs = np.array([len(adj_list[k]) for k in range(len(adj_list))])
    cols_degs = np.array([len(inv_adj_list[k]) for k in range(len(inv_adj_list))])
    return adj_list, inv_adj_list, rows_degs, cols_degs, rows_dict, cols_dict


def adjacency_list_from_biadjacency(biadjacency, return_inverse=True, return_degree_sequences=True):
    """
    Creates the adjacency list from a biadjacency matrix, given in sparse format or as a list or numpy array.
    Returns the adjacency list as a dictionary, with the rows as keys and as values lists with indexes of the columns.
    If return_inverse is True, the inverse adjacency list is also returned.
    If return_degree_sequences is True, the two degree sequences are also returned.
    """
    if scipy.sparse.isspmatrix(biadjacency):
        if np.sum(biadjacency.data != 1) > 0:
            raise ValueError('Only binary matrices')
        coords = biadjacency.nonzero()
    else:
        biadjacency = np.array(biadjacency)
        if np.sum(biadjacency[biadjacency != 0] != 1) > 0:
            raise ValueError('Only binary matrices')
        coords = np.where(biadjacency != 0)
    adj_list = {}
    inv_adj_list = {}
    for edge_i in range(len(coords[0])):
        adj_list.setdefault(coords[0][edge_i], set()).add(coords[1][edge_i])
        inv_adj_list.setdefault(coords[1][edge_i], set()).add(coords[0][edge_i])
    return_args = [adj_list]
    if return_inverse:
        return_args.append(inv_adj_list)
    if return_degree_sequences:
        rows_degs = np.array([len(adj_list[k]) for k in range(len(adj_list))])
        cols_degs = np.array([len(inv_adj_list[k]) for k in range(len(inv_adj_list))])
        return_args.append(rows_degs)
        return_args.append(cols_degs)
    if len(return_args) > 1:
        return tuple(return_args)
    else:
        return adj_list


def edgelist_from_adjacency_list_bipartite(adj_list):
    """
    Creates the edgelist from an adjacency list given as a dictionary.
    Returns the edgelist as a numpy array, with the keys as first elements of the couples and the values second.
    :param dict adj_list: the adjacency list to be converted.
    """
    edgelist = []
    for k in adj_list:
        for k_neighbor in adj_list[k]:
            edgelist.append((k, k_neighbor))
    return np.array(edgelist)


def biadjacency_from_adjacency_list(adj_list, fmt='array'):
    """
    Creates the biadjacency matrix from an adjacency list given as a dictionary.
    Returns the biadjacency as a numpy array by default, or sparse scipy matrix if fmt='sparse'.
    The biadjacency comes with the keys as rows of the matrix and the values as columns.
    :param dict adj_list: the adjacency list to be converted. Must contain integers that will be used as indexes.
    :param str fmt: the desired format of the output biadjacency matrix, either 'array' or 'sparse', optional
    """
    assert np.isin(fmt, ['array', 'sparse']), 'fmt must be either array or sparse'
    assert isinstance(list(adj_list.keys())[0], (int, float, complex)), 'Adjacency list must be numeric'
    rows_index = [k for k, v in adj_list.items() for _ in range(len(v))]
    cols_index = [i for ids in adj_list.values() for i in ids]
    biad_mat = scipy.sparse.csr_matrix(([1] * len(rows_index), (rows_index, cols_index)))
    if fmt == 'sparse':
        return biad_mat
    else:
        return biad_mat.toarray()


def adjacency_matrix_from_adjacency_list(adj_list, fmt='array'):
    """
    Creates the adjacency matrix from an adjacency list given as a dictionary.
    Returns the adjacency as a numpy array by default, or sparse scipy matrix if fmt='sparse'.
    :param dict adj_list: the adjacency list to be converted. Must contain integers that will be used as indexes.
    :param str fmt: the desired format of the output adjacency matrix, either 'array' or 'sparse', optional
    """
    assert np.isin(fmt, ['array', 'sparse']), 'fmt must be either array or sparse'
    assert isinstance(list(adj_list.keys())[0], (int, float, complex)), 'Adjacency list must be numeric'
    rows_index = [k for k, v in adj_list.items() for _ in range(len(v))]
    cols_index = [i for ids in adj_list.values() for i in ids]
    biad_mat = scipy.sparse.csr_matrix(([1] * len(rows_index), (rows_index, cols_index)))
    biad_mat = biad_mat + biad_mat.T
    if fmt == 'sparse':
        return biad_mat
    else:
        return biad_mat.toarray()
