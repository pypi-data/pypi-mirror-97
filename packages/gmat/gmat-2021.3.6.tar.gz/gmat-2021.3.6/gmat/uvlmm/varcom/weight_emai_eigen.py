import numpy as np
from scipy import linalg
import logging


def weight_emai_eigen(y, xmat, gmat_eigen_val, gmat_eigen_vec, init=None, maxiter=100, cc=1.0e-8):
    """
    :param y:
    :param xmat:
    :param gmat_eigen_val:
    :param gmat_eigen_vec:
    :param init:
    :param maxiter:
    :param cc:
    :return:
    """
    y_raw = np.array(y)
    y = np.dot(gmat_eigen_vec.T, y)  # transform the phenotypic values
    xmat = np.dot(gmat_eigen_vec.T, xmat)  # transform the fixed effects
    if init is not None:
        var = np.array(init)
    else:
        var = np.array([np.var(y_raw)/2]*2)
    var_update = var*10000
    delta = var_update - var
    fd_mat = np.zeros(2)
    ai_mat = np.zeros((2, 2))
    em_mat = np.zeros((2, 2))
    num_id = gmat_eigen_vec.shape[0]
    for i in range(maxiter):
        logging.info("Iteration: {}".format(i+1))
        vmat = 1.0 / (gmat_eigen_val * var[0] + var[1])
        vx = np.multiply(vmat, xmat)
        xvx = np.dot(xmat.T, vx)
        xvx = linalg.inv(xvx)
        # py
        xvy = np.dot(vx.T, y)
        y_xb = y - np.dot(xmat, np.dot(xvx, xvy))
        py = np.multiply(vmat, y_xb)
        # add_py p_add_py
        add_py = np.multiply(gmat_eigen_val, py)
        xvy = np.dot(vx.T, add_py)
        y_xb = add_py - np.dot(xmat, np.dot(xvx, xvy))
        p_add_py = np.multiply(vmat, y_xb)
        # res_py p_res_py
        res_py = py.copy()
        xvy = np.dot(vx.T, res_py)
        y_xb = res_py - np.dot(xmat, np.dot(xvx, xvy))
        p_res_py = np.multiply(vmat, y_xb)
        # fd
        tr_vd = np.sum(np.multiply(vmat, gmat_eigen_val))
        xvdvx = np.dot(xmat.T, vmat * gmat_eigen_val * vx)
        tr_2d = np.sum(np.multiply(xvdvx, xvx))
        ypvpy = np.sum(np.dot(py.T, add_py))
        fd_mat[0] = 0.5 * (-tr_vd + tr_2d + ypvpy)
        tr_vd = np.sum(vmat)
        xvdvx = np.dot(xmat.T, vmat * vx)
        tr_2d = np.sum(np.multiply(xvdvx, xvx))
        ypvpy = np.sum(np.dot(py.T, res_py))
        fd_mat[1] = 0.5 * (-tr_vd + tr_2d + ypvpy)
        # AI
        ai_mat[0, 0] = np.sum(np.dot(add_py.T, p_add_py))
        ai_mat[0, 1] = ai_mat[1, 0] = np.sum(np.dot(add_py.T, p_res_py))
        ai_mat[1, 1] = np.sum(np.dot(res_py.T, p_res_py))
        ai_mat = 0.5 * ai_mat
        # EM
        em_mat[0, 0] = num_id / (2 * var[0] * var[0])
        em_mat[1, 1] = num_id / (2 * var[1] * var[1])
        for j in range(0, 51):
            gamma = j * 0.02
            wemai_mat = (1 - gamma) * ai_mat + gamma * em_mat
            delta = np.dot(linalg.inv(wemai_mat), fd_mat)
            var_update = var + delta
            if min(var_update) > 0:
                logging.info('EM weight value: {}'.format(gamma))
                break
        # Convergence criteria
        logging.info('Updated variances: {}'.format(var_update))
        cc_val = np.sum(pow(delta, 2)) / np.sum(pow(var_update, 2))
        cc_val = np.sqrt(cc_val)
        var = var_update.copy()
        logging.info("CC: {}".format(cc_val))
        if cc_val < cc:
            break
    return var
