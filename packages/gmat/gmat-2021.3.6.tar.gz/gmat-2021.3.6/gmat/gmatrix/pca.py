import numpy as np
import pandas as pd
from scipy import linalg
import logging
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def pca(agmat_file, pca_num=10, keep_file=None):
    """
    Principal component analysis
    :param agmat_file: the prefix of file for the additive genomic relationship matrix from the agmat function (id_id_val)
    :param pca_num: the number of pca to output. Default is 10.
    :param keep_file: the file for a subset of individuals. Default is None, all the individuals will be used.
    :return: the eigenvectors (*.eigenvec) and  all the eigenvalues (*.eigenval)
    """
    id_agmat = np.array(pd.read_csv(agmat_file + '.id', header=None, dtype=np.str).iloc[:, 0])
    id_keep = np.array(id_agmat)
    if keep_file is not None:
        id_keep = np.array(pd.read_csv(keep_file, header=None, dtype=np.str).iloc[:, 0])
        id_del = set(id_keep) - set(id_agmat)
        if len(id_del) != 0:
            logging.error('These individuals are not in the agmat_file: {}'.format(id_del))
            sys.exit()
    id_dct = dict(zip(id_keep, range(len(id_keep))))
    ag = np.zeros((len(id_keep), len(id_keep)))
    with open(agmat_file + '.agrm.id_fmt') as fin:
        for line in fin:
            arr = line.split()
            ag[id_dct[arr[0]], id_dct[arr[1]]] = ag[id_dct[arr[1]], id_dct[arr[0]]] = float(arr[2])
    eigenvals, eigenvecs = linalg.eigh(ag)
    eigenvals = np.flip(eigenvals)
    all_sum = np.sum(eigenvals)
    eigenvals_ratio = eigenvals / all_sum
    eigenvals_accum = []
    accum_sum = 0
    for val in eigenvals:
        accum_sum += val
        eigenvals_accum.append(accum_sum / all_sum)
    eigenvals_df = pd.DataFrame({"val": eigenvals, "ratio": eigenvals_ratio, "accum": eigenvals_accum})
    eigenvals_df.to_csv(agmat_file + '.eigenvals', sep=' ', header=False, index=False)
    eigenvecs_df = pd.concat([pd.DataFrame({'id': id_keep}), pd.DataFrame(eigenvecs[:, range(-1, -pca_num-1, -1)])], axis=1)
    eigenvecs_df.to_csv(agmat_file + '.eigenvecs', sep=' ', header=False, index=False)
    plt.figure(figsize=(3.5, 3.5), dpi=600)
    plt.rc('font', family='Times New Roman')
    plt.xlabel('PC1', fontsize=10)
    plt.ylabel('PC2', fontsize=10)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.scatter(eigenvecs[:, -1], eigenvecs[:, -2], s=1.2, c='black')
    plt.tight_layout()
    plt.savefig(agmat_file + '.pca2D.png')
    plt.figure(figsize=(3.5, 3.5), dpi=600)
    plt.rc('font', family='Times New Roman')
    ax = plt.axes(projection='3d')
    ax.set_xlabel('PC1', fontsize=10)
    ax.set_ylabel('PC2', fontsize=10)
    # ax.set_zlabel('PC3', fontsize=10)
    ax.xaxis.set_tick_params(labelsize=8)
    ax.yaxis.set_tick_params(labelsize=8)
    ax.zaxis.set_tick_params(labelsize=8)
    ax.scatter(eigenvecs[:, -1], eigenvecs[:, -2], eigenvecs[:, -3], s=1.2, c='black')
    ax.set_in_layout(True)
    plt.savefig(agmat_file + '.pca3D.png')
    return 0
