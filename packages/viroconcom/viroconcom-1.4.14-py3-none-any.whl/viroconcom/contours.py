#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Contours.
"""
import warnings
import math
from abc import ABC, abstractmethod
from multiprocessing import Pool, TimeoutError

import numpy as np
import scipy.stats as sts
import scipy.ndimage as ndi
import networkx as nx
from sklearn.neighbors import NearestNeighbors

from ._n_sphere import NSphere

__all__ = ["Contour", "IFormContour", "ISormContour", "DirectSamplingContour",
           "HighestDensityContour", "sort_points_to_form_continous_line"]


class Contour(ABC):
    """
    Abstract base class for contours.

    Attributes
    ----------
    distribution : MultivariateDistribution
        The distribution to calculate the contour of.
    coordinates : list of lists of ndarrays
        Contains the coordinates of points on the contour.
        If the distribution is unimodal the outer list contains only one element,
        else the outer list divides possible multiple contour parts.
        The inner list contains multiple numpy arrays of the same length, one per dimension.
        The values of the arrays are the coordinates in the corresponding dimension.

    """

    def __init__(self, mul_var_distribution, return_period=50, state_duration=3,
                 timeout=None, *args, **kwargs):
        """

        Parameters
        ----------
        mul_var_distribution : MultivariateDistribution
            The distribution to be used to calculate the contour.
        Raises
        ------
        TimeoutError
            If the calculation takes too long and the given value for timeout is exceeded.
        """
        self.distribution = mul_var_distribution
        self.coordinates = None

        self.state_duration = state_duration
        self.return_period = return_period
        self.alpha = state_duration / (return_period * 365.25 * 24)

        if timeout:
            # Use multiprocessing to define a timeout
            pool = Pool(processes=1)
            res = pool.apply_async(self._setup, args, kwargs)
            try:
                computed = res.get(timeout=timeout)
            except TimeoutError:
                err_msg = "The calculation takes too long. " \
                          "It takes longer than the given value for" \
                          " a timeout, which is '{} seconds'.".format(timeout)
                raise TimeoutError(err_msg)
            # Save the results separated
            self._save(computed)
        else:
            computed = self._setup(*args, **kwargs)
            self._save(computed)

    @abstractmethod
    def _setup(self, *args, **kwargs):
        """Calculate the contours coordinates."""

    @abstractmethod
    def _save(self, computed):
        """Save the contours coordinates."""


class IFormContour(Contour):
    def __init__(self, mul_var_distribution, return_period=50, state_duration=3,
                 n_points=180, timeout=None):
        """
        Contour based on the inverse first-order reliability method.

        This method was proposed by Winterstein et al. (1993).

        Parameters
        ----------
        mul_var_distribution : MultivariateDistribution
            The distribution to be used to calculate the contour.
        return_period : float, optional
            The years to consider for calculation. Defaults to 50.
        state_duration : float, optional
            Time period for which an environmental state is measured,
            expressed in hours. Defaults to 3.
        n_points : int, optional
            Number of points on the contour. Defaults to 180.
        timeout : int, optional
            The maximum time in seconds there the contour has to be computed.
            This parameter also controls multiprocessing. If timeout is None
            serial processing is performed, if it is not None multiprocessing
            is used. Defaults to None.
        Raises
        ------
        TimeoutError,
            If the calculation takes too long and the given value for timeout is exceeded.

        example
        -------

        >>> from viroconcom.distributions import (WeibullDistribution,\
                                               LognormalDistribution,\
                                               MultivariateDistribution)
        >>> from viroconcom.params import ConstantParam, FunctionParam
        >>> #Define dependency tuple
        >>> dep1 = (None, None, None)
        >>> dep2 = (0, None, 0)
        >>> #Define parameters
        >>> shape = ConstantParam(1.471)
        >>> loc = ConstantParam(0.8888)
        >>> scale = ConstantParam(2.776)
        >>> par1 = (shape, loc, scale)
        >>> mu = FunctionParam('power3', 0.1000, 1.489, 0.1901)
        >>> sigma = FunctionParam('exp3', 0.0400, 0.1748, -0.2243)
        >>> #Create distributions
        >>> dist1 = WeibullDistribution(*par1)
        >>> dist2 = LognormalDistribution(mu=mu, sigma=sigma)
        >>> distributions = [dist1, dist2]
        >>> dependencies = [dep1, dep2]
        >>> mul_dist = MultivariateDistribution(distributions, dependencies)
        >>> test_contour_iform = IFormContour(mul_dist, 50, 3, 400)

        """
        # Calls _setup
        super().__init__(mul_var_distribution, return_period, state_duration, timeout, n_points)

    def _setup(self, n_points):
        """
        Calculates coordinates using IFORM.

        Parameters
        ----------
        n_points : int
            Number of points the shape contains.
        return_period : float
            The years to consider for calculation. Defaults to 50.
        Returns
        -------
        tuple of objects
            The computed results.
        """

        # Creates list with size that equals grade of dimensions used
        data = [None] * self.distribution.n_dim

        distributions = self.distribution.distributions

        beta = sts.norm.ppf(1 - self.alpha)

        # Create sphere
        if self.distribution.n_dim == 2:
            _phi = np.linspace(0, 2 * np.pi , num=n_points, endpoint=False)
            _x = np.cos(_phi)
            _y = np.sin(_phi)
            _circle = np.stack((_x,_y)).T
            sphere_points = beta * _circle

        else:
            sphere = NSphere(dim=self.distribution.n_dim, n_samples=n_points)
            sphere_points = beta * sphere.unit_sphere_points

        # Get probabilities for coordinates of shape
        norm_cdf_per_dimension = [sts.norm.cdf(sphere_points[:, dim])
                               for dim in range(self.distribution.n_dim)]

        # Inverse procedure. Get coordinates from probabilities.
        for index, distribution in enumerate(distributions):
            data[index] = distribution.i_cdf(norm_cdf_per_dimension[index], rv_values=data,
                                             dependencies=self.distribution.dependencies[index])

        coordinates = data

        return (beta, sphere_points, coordinates)

    def _save(self, computed):
        """
        Save the computed parameters.

        Parameters
        ----------
        computed : tuple of objects
            The computed results to be saved.
        """
        self.beta = computed[0]
        self.sphere_points = computed[1]
        self.coordinates = computed[2]


class ISormContour(Contour):
    def __init__(self, mul_var_distribution, return_period=50, state_duration=3,
                 n_points=180, timeout=None):
        """
        Contour based on the inverse second-order reliability method.

        This method was proposed by Chai and Leira (2018). The paper's DOI
        is 10.1016/j.marstruc.2018.03.007 .

        Parameters
        ----------
        mul_var_distribution : MultivariateDistribution
            The distribution to be used to calculate the contour.
        return_period : float, optional
            The years to consider for calculation. Defaults to 50.
        state_duration : float, optional
            Time period for which an environmental state is measured,
            expressed in hours. Defaults to 3.
        n_points : int, optional
            Number of points on the contour. Defaults to 180.
        timeout : int, optional
            The maximum time in seconds there the contour has to be computed.
            This parameter also controls multiprocessing. If timeout is None
            serial processing is performed, if it is not None multiprocessing
            is used. Defaults to None.
        Raises
        ------
        TimeoutError,
            If the calculation takes too long and the given value for timeout is exceeded.

        example
        -------

        >>> from viroconcom.distributions import (WeibullDistribution,\
                                               LognormalDistribution,\
                                               MultivariateDistribution)
        >>> from viroconcom.params import ConstantParam, FunctionParam
        >>> #Define dependency tuple
        >>> dep1 = (None, None, None)
        >>> dep2 = (0, None, 0)
        >>> #Define parameters
        >>> shape = ConstantParam(1.471)
        >>> loc = ConstantParam(0.8888)
        >>> scale = ConstantParam(2.776)
        >>> par1 = (shape, loc, scale)
        >>> mu = FunctionParam('power3', 0.1000, 1.489, 0.1901)
        >>> sigma = FunctionParam('exp3', 0.0400, 0.1748, -0.2243)
        >>> #Create distributions
        >>> dist1 = WeibullDistribution(*par1)
        >>> dist2 = LognormalDistribution(mu=mu, sigma=sigma)
        >>> distributions = [dist1, dist2]
        >>> dependencies = [dep1, dep2]
        >>> mul_dist = MultivariateDistribution(distributions, dependencies)
        >>> test_contour_isorm = ISormContour(mul_dist, 50, 3, 400)

        """
        # Calls _setup
        super().__init__(mul_var_distribution, return_period, state_duration, timeout, n_points)

    def _setup(self, n_points):
        """
        Calculates coordinates using ISORM.

        Parameters
        ----------
        n_points : int
            Number of points the shape contains.
        return_period : float
            The years to consider for calculation. Defaults to 50.
        Returns
        -------
        tuple of objects
            The computed results.
        """

        # Creates list with size that equals grade of dimensions used.
        data = [None] * self.distribution.n_dim

        distributions = self.distribution.distributions

        # Use the ICDF of a chi-squared distribution with n dimensions. For
        # reference see equation 20 in Chai and Leira (2018).
        beta = math.sqrt(sts.chi2.ppf(1 - self.alpha, self.distribution.n_dim))

        # Create sphere.
        if self.distribution.n_dim == 2:
            _phi = np.linspace(0, 2 * np.pi , num=n_points, endpoint=False)
            _x = np.cos(_phi)
            _y = np.sin(_phi)
            _circle = np.stack((_x,_y)).T
            sphere_points = beta * _circle

        else:
            sphere = NSphere(dim=self.distribution.n_dim, n_samples=n_points)
            sphere_points = beta * sphere.unit_sphere_points

        # Get probabilities for coordinates of shape.
        norm_cdf_per_dimension = [sts.norm.cdf(sphere_points[:, dim])
                               for dim in range(self.distribution.n_dim)]

        # Inverse procedure. Get coordinates from probabilities.
        for index, distribution in enumerate(distributions):
            data[index] = distribution.i_cdf(norm_cdf_per_dimension[index], rv_values=data,
                                             dependencies=self.distribution.dependencies[index])

        coordinates = data

        return (beta, sphere_points, coordinates)

    def _save(self, computed):
        """
        Save the computed parameters.

        Parameters
        ----------
        computed : tuple of objects
            The computed results to be saved.
        """
        self.beta = computed[0]
        self.sphere_points = computed[1]
        self.coordinates = computed[2]


class DirectSamplingContour(Contour):
    def __init__(self, mul_var_dist, return_period=50, state_duration=3,
                 n=100000, deg_step=5, sample=None, timeout=None):
        """
        Drect sampling contour as introduced by Huseby et al. (2013), see
        doi.org/10.1016/j.oceaneng.2012.12.034 .

        This implementation only works for two-dimensional distributions.

        Parameters
        ----------
        mul_var_dist : MultivariateDistribution
            Must be 2-dimensional.
        return_period : int, optional
            Return period given in years. Defaults to 1.
        state_duration : int, optional
            Time period for which an environmental state is measured,
            expressed in hours. Defaults to 3.
        n : int, optional
            Number of data points that shall be Monte Carlo simulated.
        deg_step : float, optional
            Directional step in degrees. Defaults to 5.
        sample : 2-dimensional ndarray, optional
            Monte Carlo simulated environmental states. Array is of shape (d, n)
            with d being the number of variables and n being the number of
            observations.
        timeout : int, optional
            The maximum time in seconds there the contour has to be computed.
            This parameter also controls multiprocessing. If timeout is None
            serial processing is performed, if it is not None multiprocessing
            is used. Defaults to None.
        Raises
        ------
        TimeoutError,
            If the calculation takes too long and the given value for timeout is exceeded.
        """
        # Call _setup .
        super().__init__(mul_var_dist, return_period, state_duration, timeout,
                         n, deg_step, sample)

    def _setup(self, n, deg_step, sample):
        """
        Calculates the coordinates of the DS contour.

        Parameters
        ----------
        n : int
            Number of data points that shall be Monte Carlo simulated.
        deg_step : float
            Directional step in degrees.
        sample : 2-dimensional ndarray, optional
            Array is of shape (d, n) with d being the number of variables and
            n being the number of observations.

        Returns
        -------
        tuple of objects
            The computed results (sample, contour coordinates).
        """
        if self.distribution.n_dim != 2:
            raise NotImplementedError("DirectSamplingContour is currently only "
                                      "implemented for two dimensions.")

        if sample is None:
            sample = self.distribution.draw_sample(n)
        x, y = sample

        # Calculate non-exceedance probability.
        alpha = 1 - (1 / (self.return_period * 365.25 * 24 / self.state_duration))

        # Define the angles such the coordinates[0] and coordinates[1] will
        # be based on the exceedance plane with angle 0 deg, with 0 deg being
        # along the x-axis. Angles will increase counterclockwise in a xy-plot.
        # Not enirely sure why the + 2*rad_step is required, but tests show it.
        rad_step = deg_step * np.pi / 180
        angles = np.arange(0.5 * np.pi + 2 * rad_step, -1.5 * np.pi + rad_step,
                           -1 * rad_step)

        length_t = len(angles)
        r = np.zeros(length_t)

        # Find radius for each angle.
        i = 0
        while i < length_t:
            z = x * np.cos(angles[i]) + y * np.sin(angles[i])
            r[i] = np.quantile(z, alpha)
            i = i + 1

        # Find intersection of lines.
        a = np.array(np.concatenate((angles, [angles[0]]), axis=0))
        r = np.array(np.concatenate((r, [r[0]]), axis=0))

        denominator = np.sin(a[2:]) * np.cos(a[1:len(a)-1]) - \
                      np.sin(a[1:len(a)-1]) * np.cos(a[2:])

        x_cont = (np.sin(a[2:]) * r[1:len(r)-1]
                  - np.sin(a[1:len(a)-1]) * r[2:]) / denominator
        y_cont = (-np.cos(a[2:]) * r[1:len(r)-1]
                  + np.cos(a[1:len(a)-1]) * r[2:]) / denominator

        coordinates = [x_cont, y_cont]


        return (sample, coordinates)

    def _save(self, computed):
        """
        Save the computed parameters.

        Parameters
        ----------
        computed : tuple of objects
            The computed results to be saved (sample, contour coordinates).
        """
        self.sample = computed[0]
        self.coordinates = computed[1]


class HighestDensityContour(Contour):
    def __init__(self, mul_var_distribution, return_period=50, state_duration=3,
                 limits=None, deltas=None, timeout=None):
        """
        Contour based on highest density contour method.

        This method was proposed by Haselsteiner et al. (2017). The paper's
        DOI is 10.1016/j.coastaleng.2017.03.002 .

        Parameters
        ----------
        mul_var_distribution : MultivariateDistribution
            The distribution to be used to calculate the contour.
        return_period : float, optional
            The years to consider for calculation. Defaults to 50.
        state_duration : float, optional
            Time period for which a (environmental) state is measured, expressed in hours.
            Defaults to 3.
        limits : list of tuples, optional
            One 2-Element tuple per dimension in mul_var_distribution,
            containing min and max limits for calculation. ((min, max)).
            Smaller value is always assumed minimum. Defaults to list of (0, 10)
        deltas : float or list of float, optional
            The grid stepsize used for calculation.
            If a single float is supplied it is used for all dimensions.
            If a list of float is supplied it has to be of the same length
            as there are dimensions in mul_var_dist.
            Defaults to 0.5.
        timeout : int, optional
            The maximum time in seconds there the contour has to be computed.
            This parameter also controls multiprocessing. If timeout is None
            serial processing is performed, if it is not None multiprocessing
            is used. Defaults to None.
        Raises
        ------
        TimeoutError,
            If the calculation takes too long and the given value for timeout is exceeded.

        example
        -------

        Creating contour example for 2-d HDC with Weibull and Lognormal
        distribution

        >>> from viroconcom.distributions import (WeibullDistribution,\
                                               LognormalDistribution,\
                                               MultivariateDistribution)
        >>> from viroconcom.params import ConstantParam, FunctionParam
        >>> #Define dependency tuple
        >>> dep1 = (None, None, None)
        >>> dep2 = (0, None, 0)
        >>> #Define parameters
        >>> shape = ConstantParam(1.471)
        >>> loc = ConstantParam(0.8888)
        >>> scale = ConstantParam(2.776)
        >>> par1 = (shape, loc, scale)
        >>> mu = FunctionParam('power3', 0.1000, 1.489, 0.1901)
        >>> sigma = FunctionParam('exp3', 0.0400, 0.1748, -0.2243)
        >>> #Create distributions
        >>> dist1 = WeibullDistribution(*par1)
        >>> dist2 = LognormalDistribution(mu=mu, sigma=sigma)
        >>> distributions = [dist1, dist2]
        >>> dependencies = [dep1, dep2]
        >>> mul_dist = MultivariateDistribution(distributions, dependencies)
        >>> #Calculate contour
        >>> n_years = 50
        >>> limits = [(0, 20), (0, 18)]
        >>> deltas = [0.1, 0.1]
        >>> test_contour_HDC = HighestDensityContour(mul_dist, n_years, 3,\
                                                     limits, deltas)

        """
        # calls _setup
        super().__init__(mul_var_distribution, return_period, state_duration,
                         timeout, limits, deltas)

    def _setup(self, limits, deltas):
        """
        Calculate coordinates using highest density method.

        Parameters
        ----------
        limits : list of tuples
            One 2-Element tuple per dimension in mul_var_distribution,
            containing min and max limits for calculation. ((min, max)).
            Smaller value is always assumed minimum.
        deltas : scalar or list of scalar
            The grid stepsize used for calculation.
            If a single float is supplied it is used for all dimensions.
            If a list of float is supplied it has to be of the same length
            as there are dimensions in mul_var_dist.
        Returns
        -------
        tuple of objects,
            The computed results.
        """

        n_dim = self.distribution.n_dim
        if limits is None:
            limits = [(0, 10)] * n_dim
            for i in range(n_dim):
                # This calculation is based on the relationship for an ISORM
                # contour, see Mackay and Haselsteiner (2020), Expression 12.
                alpha_t = 1.0 / (self.return_period * 365.25 * 24 / self.state_duration)
                beta_Sn = math.sqrt(sts.distributions.chi2.ppf(1 - alpha_t, df=n_dim))
                alpha_m = 1.0 - sts.distributions.norm.cdf(beta_Sn)
                dist = self.distribution.distributions[i]
                non_exeedance_p = 1 - alpha_m * 0.1
                if i == 0:
                    # When implemented this should become self.distribution.marginal_icdf(non_exceedance_p, i)
                    limits[i] = (0, dist.i_cdf(non_exeedance_p))
                else:
                    # When implemented this should become self.distribution.marginal_icdf(non_exceedance_p, i)
                    limits[i] = (0, limits[i-1][1])
        else:
            # Check limits length.
            if len(limits) != self.distribution.n_dim:
                raise ValueError("limits has to be of length equal to number of dimensions, "
                                 "but len(limits)={}, n_dim={}."
                                 "".format(len(limits), self.distribution.n_dim))

        if deltas is None:
            deltas = np.empty(shape=n_dim)
            # Set default cell size to 0.25 percent of the variable space.
            # This is losely based on the results from Fig. 7 in 10.1016/j.coastaleng.2017.03.002
            # In the considered variable space length of 20 a cell length of
            # 0.05 was sufficient --> 20 / 0.05 = 400. 1/400 = 0.0025
            relative_cell_size = 0.0025

            for i in range(n_dim):
                deltas[i] = (limits[i][1] - limits[i][0]) * relative_cell_size
        else:
            # Check if deltas is a scalar.
            try:
                iter(deltas)
                if len(deltas) != self.distribution.n_dim:
                        raise ValueError("deltas has do be either scalar, "
                                     "or list of length equal to number of dimensions, "
                                     "but was list of length {}".format(len(deltas)))
                deltas = list(deltas)
            except TypeError:
                deltas = [deltas] * self.distribution.n_di

        # Create sampling coordinate arrays.
        sample_coords = []
        for i, lim_tuple in enumerate(limits):
            try:
                iter(lim_tuple)
                if len(lim_tuple) != 2:
                    raise ValueError("tuples in limits have to be of length 2 ( = (min, max)), "
                                "but tuple with index = {}, has length = {}."
                                 "".format(i, len(lim_tuple)))
            except TypeError:
                raise ValueError("tuples in limits have to be of length 2 ( = (min, max)), "
                                "but tuple with index = {}, has length = 1."
                                 "".format(i))

            min_ = min(lim_tuple)
            max_ = max(lim_tuple)
            delta = deltas[i]
            samples = np.arange(min_, max_+ delta, delta)
            sample_coords.append(samples)


        f = self.distribution.cell_averaged_joint_pdf(sample_coords)

        if np.isnan(f).any():
            raise ValueError("Encountered nan in cell averaged probabilty joint pdf. "
                             "Possibly invalid distribution parameters?")

        # Calculate probability per cell.
        cell_prob = f
        for delta in deltas:
            cell_prob *= delta

        # Calculate highest density region.
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                HDR, prob_m = self.cumsum_biggest_until(cell_prob, 1 - self.alpha)
        except RuntimeWarning:
            HDR = np.ones_like(cell_prob)
            prob_m = 0
            warnings.warn("A probability of 1-alpha could not be reached. "
                          "Consider enlarging the area defined by limits or "
                          "setting n_years to a smaller value.",
                          RuntimeWarning, stacklevel=4)

        # Calculate fm from probability per cell.
        fm = prob_m
        for delta in deltas:
            fm /= delta

        structure = np.ones(tuple([3] * self.distribution.n_dim), dtype=bool)
        HDC = HDR - ndi.binary_erosion(HDR, structure=structure)

        labeled_array, n_modes = ndi.label(HDC, structure=structure)

        coordinates = []
        # Iterate over all partial contours and start at 1.
        for i in range(1, n_modes+1):
            # Array of arrays with same length, one per dimension
            # containing the indice of the contour.
            partial_contour_indice = np.nonzero(labeled_array == i)

            # Calculate the values corresponding to the indice
            partial_coordinates = []
            for dimension, indice in enumerate(partial_contour_indice):
                partial_coordinates.append(sample_coords[dimension][indice])

            coordinates.append(partial_coordinates)

        if len(coordinates) == 1:
            coordinates = coordinates[0]

        return (deltas, limits, sample_coords, fm, coordinates)
        
    def _save(self, computed):
        """
        Save the computed parameters.

        Parameters
        ----------
        computed : tuple of objects,
            The computed results to be saved.
        """
        self.deltas = computed[0]
        self.limits = computed[1]
        self.sample_coords = computed[2]
        self.fm = computed[3]
        self.coordinates = computed[4]

    def cumsum_biggest_until(self, array, limit):
        """
        Find biggest elements to sum to reach limit.

        Sorts array, and calculates the cumulative sum.
        Returns a boolean array with the same shape as array indicating the
        fields summed to reach limit, as well as the last value added.

        Parameters
        ----------
        array : ndarray
            Array of arbitrary shape with all values >= 0.
        limit : float
            limit to sum up to.

        Returns
        -------
        summed_fields : ndarray, dtype=Bool
            Boolean array of shape like array with True if element was used in summation.
        last_summed : float
            Element that was added last to the sum.

        Raises
        ------
        ValueError
            If `array` contains nan.
        Notes
        ------
        A ``RuntimeWarning`` is raised if the limit cannot be reached by summing all values.
        """

        flat_array = np.ravel(array)
        if np.isnan(flat_array).any():
            raise ValueError("array contains nan.")

        sort_inds = np.argsort(flat_array, kind="mergesort")[::-1]
        sort_vals = flat_array[sort_inds]

        cum_sum = np.cumsum(sort_vals)

        if cum_sum[-1] < limit:
            warnings.warn("The limit could not be reached.", RuntimeWarning, stacklevel=1)

        summed_flat_inds = sort_inds[cum_sum <= limit]

        summed_fields = np.zeros(array.shape)

        summed_fields[np.unravel_index(summed_flat_inds, shape=array.shape)] = 1

        last_summed = array[np.unravel_index(summed_flat_inds[-1], shape=array.shape)]


        return summed_fields, last_summed


def sort_points_to_form_continous_line(x, y, do_search_for_optimal_start=False):
    """
    Sorts contour points to form a a continous line / contour.

    Thanks to https://stackoverflow.com/questions/37742358/sorting-points-to-
    form-a-continuous-line/37744549#37744549

    Parameters
    ----------
    x : array_like
    y : array_like
    do_search_for_optimal_start : boolean, optional
     If true, the algorithm also searches for the ideal starting node, see the
     stackoverflow link for more info.

    Returns
    -------
    sorted_points : tuple of array_like floats
        The sorted points.
    """
    points = np.c_[x, y]
    clf = NearestNeighbors(n_neighbors=2).fit(points)
    G = clf.kneighbors_graph()
    T = nx.from_scipy_sparse_matrix(G)
    order = list(nx.dfs_preorder_nodes(T, 0))

    xx = x[order]
    yy = y[order]

    if do_search_for_optimal_start:
        paths = [list(nx.dfs_preorder_nodes(T, i)) for i in range(len(points))]
        mindist = np.inf
        minidx = 0

        for i in range(len(points)):
            p = paths[i]  # Order of nodes.
            ordered = points[p]  # Ordered nodes.
            # Find cost of that order by the sum of euclidean distances
            # between points (i) and (i + 1).
            cost = (((ordered[:-1] - ordered[1:]) ** 2).sum(1)).sum()
            if cost < mindist:
                mindist = cost
                minidx = i

        opt_order = paths[minidx]

        xx = x[opt_order]
        yy = y[opt_order]

    return (xx, yy)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

