"""
Sure Independence Screening

https://orfe.princeton.edu/~jqfan/papers/06/SIS.pdf

"""
import logging
from itertools import combinations
from typing import Optional, Dict, List

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import get_scorer

from maml.apps.symbolic._selectors import BaseSelector, DantzigSelector

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _get_coeff(x, y):
    coeff, _, _, _ = np.linalg.lstsq(x, y, rcond=-1)
    return coeff


def _eval(x, y, coeff, metric):
    metric_func = get_scorer(metric)
    lr = LinearRegression(fit_intercept=False)
    lr.coef_ = coeff  # type: ignore
    lr.intercept_ = 0
    return metric_func(lr, x, y)


def _best_combination(x, y, find_sel, find_sel_new, metric: str = "neg_mean_absolute_error"):
    if len(find_sel_new) == 1:
        comb_best = np.append(find_sel, find_sel_new)
        coeff_best = _get_coeff(x[:, comb_best], y)
        score_best = _eval(x[:, comb_best], y, coeff_best, metric)
        return comb_best, coeff_best, score_best
    combs = combinations(np.append(find_sel, find_sel_new), len(find_sel) + 1)
    coeff_best = _get_coeff(x[:, find_sel], y)
    score_best = _eval(x[:, find_sel], y, coeff_best, metric)
    comb_best = find_sel
    for ind_comb in combs:
        d = x[:, ind_comb]
        coeff = _get_coeff(d, y)
        score = _eval(d, y, coeff, metric)
        if score > score_best:
            score_best = score
            comb_best = ind_comb
            coeff_best = coeff
    return comb_best, coeff_best, score_best


class SIS:
    """
    Sure independence screening method.
    The method consists of two steps:
        1. Screen
        2. Select

    """

    def __init__(self, gamma=0.1, selector: Optional[BaseSelector] = None, verbose: bool = True):
        """
        Sure independence screening

        Args:
            gamma (float): ratio between selected features and original feature sizes
            selector (BaseSelector): selector after the screening
            verbose (bool): whether to output information along the way

        """
        self.gamma = gamma
        self.selector = selector
        self.verbose = verbose

    def run(self, x, y, select_options=None):
        """
        Run the SIS with selector
        Args:
            x (np.ndarray): MxN input data array
            y (np.ndarray): M output targets
            select_options (dict): options in the optimizations provided
                to scipy.optimize.minimize. If the selector is using cvxpy
                optimization package, this option is fed into cp.Problem.solve

        Returns: selected feature indices

        """
        screened_indices = self.screen(x, y)
        if self.verbose:
            logger.info(f"After the screening step, {len(screened_indices)}/{x.shape[1]} features remains")
        x_screen = x[:, screened_indices]

        final_selected = self.select(x_screen, y, select_options)

        if self.verbose:
            logger.info(f"After the selection step, {len(final_selected)}/{x.shape[1]} features remains")
        return screened_indices[final_selected]

    def screen(self, x, y):
        """
        Simple screening method by comparing the correlation between features
        and the target

        Args:
            x (np.ndarray): input array
            y (np.ndarray): target array

        Returns: top indices

        """
        n = x.shape[1]
        omega = x.T.dot(y)
        sorted_omega = np.argsort(omega)[::-1]
        d = int(n * self.gamma)
        top_indices = sorted_omega[:d]
        return top_indices

    def select(self, x, y, options=None):
        """
        Select features using selectors
        Args:
            x (np.ndarray): input array
            y (np.ndarray): target array
            options (dict): options for the optimization

        Returns:

        """
        return self.selector.select(x, y, options)

    def compute_residual(self, x, y):
        """
        Compute residual
        Args:
            x (np.ndarray): input array
            y (np.ndarray): target array

        Returns: residual vector

        """
        return self.selector.compute_residual(x, y)

    def set_selector(self, selector: BaseSelector):
        """
        Set new selector
        Args:
            selector (BaseSelector): a feature selector

        Returns:

        """
        self.selector = selector

    def set_gamma(self, gamma):
        """
        Set gamma

        Args:
            gamma(float): new gamma value

        """
        self.gamma = gamma

    def update_gamma(self, step: float = 0.5):
        """
        Update the sis object so that sis.select
        return at least one feature

        Args:
            step(float): ratio to update the parameters

        """
        self.set_gamma(self.gamma * (1 + step))


class ISIS:
    """Iterative SIS"""

    def __init__(self, sis: SIS = SIS(gamma=0.1, selector=DantzigSelector(0.1)), l0_regulate: bool = True):
        """

        Args:
            sis(SIS): sis object
            l0_regulate(bool): Whether to regulate features in each iteration, default True
        """
        self.sis = sis
        self.selector = sis.selector
        self.l0_regulate = l0_regulate
        self.coeff = []  # type: ignore
        self.find_sel = []  # type: ignore

    def run(
        self,
        x,
        y,
        max_p: int = 10,
        metric: str = "neg_mean_absolute_error",
        options: Optional[Dict] = None,
        step: float = 0.5,
    ):
        """
        Run the ISIS
        Args:
            x:
            y:
            max_p(int): Number of feature desired
            metric (str): scorer function, used with
                sklearn.metrics.get_scorer
            options:
            step(float): step to update gamma with

        Returns:
            find_sel(np.array): np.array of index of selected features
            coeff(np.array): np.array of coeff of selected features

        """
        assert max_p <= x.shape[1]
        findex = np.array(np.arange(0, x.shape[1]))
        find_sel = self.sis.select(x, y, options)
        self.coeff = _get_coeff(x[:, find_sel], y)
        if len(find_sel) >= max_p:
            self.coeff = _get_coeff(x[:, find_sel[:max_p]], y)
            return find_sel[:max_p]
        new_findex = np.array(list(set(findex) - set(find_sel)))
        new_y = self.sis.compute_residual(x, y)
        new_x = x[:, new_findex]
        while len(find_sel) < max_p:
            find_sel_new: List[int] = []
            try:
                find_sel_new = self.sis.run(new_x, new_y, options)
            except ValueError:
                while len(find_sel_new) == 0:
                    self.sis.update_gamma(step)
                    find_sel_new = self.sis.run(new_x, new_y)
            if self.l0_regulate:
                find_sel, _, _ = _best_combination(x, y, find_sel, new_findex[find_sel_new], metric)
            else:
                find_sel = np.append(find_sel, new_findex[find_sel_new])
            new_findex = np.array(list(set(findex) - set(find_sel)))
            new_y = self.sis.compute_residual(new_x, new_y)
            new_x = x[:, new_findex]
        self.coeff = _get_coeff(x[:, find_sel], y)
        self.find_sel = find_sel
        return find_sel

    def evaluate(self, x: np.ndarray, y: np.ndarray, metric: str = "neg_mean_absolute_error") -> float:
        """
        Evaluate the linear models using x, and y test data
        Args:
            x (np.ndarray): MxN input data array
            y (np.ndarray): M output targets
            metric (str): scorer function, used with
                sklearn.metrics.get_scorer
        Returns:
        """
        return _eval(x[:, self.find_sel], y, self.coeff, metric)
