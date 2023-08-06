#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parameter for distributions.
"""

from abc import ABC, abstractmethod

import numpy as np

import warnings # TODO remove warnings as soon as changes are done

__all__ = ["Param", "ConstantParam", "FunctionParam", "Wrapper"]


class Param(ABC):
    """
    Abstract base class for callable parameters.

    Replaces a constant or a function, so no distinction has to be made.
    """

    def __call__(self, x):
        """
        Parameters
        ----------
        x : float or array_like
            Point(s) at which to evaluate Param.

        Returns
        -------
        self._value(x) : float or list
            If x is an iterable a list of the same length will be returned,
            else if x is a scalar a float will be returned.

        """
        try:
            return [self._value(y) for y in x]
        except TypeError:  # not iterable
            return self._value(x)

    @abstractmethod
    def _value(self, x):
        """
        The value at x. Will be returned on call.
        """
        pass


class ConstantParam(Param):
    """A constant, but callable parameter."""

    def __init__(self, constant):
        """
        Parameters
        ----------
        constant : scalar
            The constant value to return.
        """

        if constant is None:
            self._constant = constant
        else:
            self._constant = float(constant)

    def _value(self, _):
        return self._constant

    def __str__(self):
        return str(self._constant)



class FunctionParam(Param):
    """A callable parameter, which depends on the value supplied."""

    def __init__(self, func_name, a, b, c, d=None,
                 C1=None, C2=None, C3=None, C4=None, wrapper=None):
        r"""
        Parameters
        ----------
        func_name : str
            Defines which kind of dependence function to use:
                :power3: :math:`a + b * x^c`
                :exp3: :math:`a + b * e^{x * c}`
                :lnsquare2: :math:`\ln[a + b * \sqrt(x / 9.81)]`
                :powerdecrease3: :math:`a + 1 / (x + b)^c`
                :asymdecrease3: :math:`a + b / (1 + c * x)`
                :logistics4: :math:`a + b / [1 + e^{-1 * |c| * (x - d)}]`
        a,b,c : float
            The function parameters.
        d : float, defaults to None
            An optional function parameter (only some function have more than
            3 parameters.
        C1, C2, C3, C4 : float, default to None
            Parameters that are used for the alpha3 dependence function.
        wrapper : function or Wrapper
            A function or a Wrapper object to wrap around the function.
            The function has to be pickleable. (i.e. lambdas, clojures, etc. are not supported.)
            Using this wrapper, one can e.g. create :math:`exp(a + b * x^c)`
            with func_type=polynomial and wrapper=math.exp.
        """

        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.C1 = C1
        self.C2 = C2
        self.C3 = C3
        self.C4 = C4

        if func_name == "power3":
            self._func = self._power3
            self.func_name = func_name
        elif func_name == "exp3":
            self._func = self._exp3
            self.func_name = func_name
        elif func_name == "lnsquare2":
            self._func = self._lnsquare2
            self.func_name = func_name
        elif func_name == "powerdecrease3":
            self._func = self._powerdecrease3
            self.func_name = func_name
        elif func_name == "asymdecrease3":
            self._func = self._asymdecrease3
            self.func_name = func_name
        elif func_name == "logistics4":
            self._func = self._logistics4
            self.func_name = func_name
        elif func_name == "alpha3":
            self._func = self._alpha3
            self.func_name = func_name
        elif func_name == "poly2":
            self._func = self._poly2
            self.func_name = func_name
        elif func_name == "poly1":
            self._func = self._poly1
            self.func_name = func_name
        else:
            raise ValueError("{} is not a known kind of function.".format(func_name))

        if wrapper is None:
            self._wrapper = Wrapper(self._identity)
        elif isinstance(wrapper, Wrapper):
            self._wrapper = wrapper
        elif callable(wrapper):
            self._wrapper = Wrapper(wrapper)
        else:
            raise ValueError("Wrapper has to be a callable.")
        # TODO test wrapper with Wrapper and with function object

    def _identity(self, x):
        return x

    # The 3-parameter power function (a dependence function).
    def _power3(self, x):
        return self.a + self.b * x ** self.c

    # The 3-parameter exponential function (a dependence function).
    def _exp3(self, x):
        return self.a + self.b * np.exp(self.c * x)

    # The 2-parameter logarithmic square function (a dependence function).
    def _lnsquare2(self, x):
        return np.log(self.a + self.b * np.sqrt(np.divide(x, 9.81)))

    # The 3-parameter decreasing power function (a dependence function).
    def _powerdecrease3(self, x):
        return self.a + 1.0 / (x + self.b) ** self.c

    # A 3-parameter function that asymptotically decreases (a dependence function).
    def _asymdecrease3(self, x):
        return self.a + self.b / (1 + self.c * x)

    # A 4-parameter logististics function (a dependence function).
    def _logistics4(self, x, a=None, b=None, c=None, d=None):
        if a == None:
            return self.a + self.b / (1 + np.exp(-1 * np.abs(self.c) * (x - self.d)))
        else:
            return a + b / (1 + np.exp(-1 * np.abs(c) * (x - d)))

    # A 3-parameter function designed for the scale parameter (alpha) of an
    # exponentiated Weibull distribution with shape2=5 (see 'Global hierarchical
    # models for wind and wave contours').
    def _alpha3(self, x):
        return (self.a + self.b * x ** self.c) \
               / 2.0445 ** (1 / self._logistics4(x, self.C1, self.C2, self.C3, self.C4))

    # A 3-parameter 2nd order polynomial  (a dependence function).
    def _poly2(self, x):
        return self.a * x**2 + self.b * x + self.c
    
    # A 2-parameter 1st order polynomial  (a dependence function).
    def _poly1(self, x):
        return self.a * x + self.b

    def _value(self, x):
        return self._wrapper(self._func(x))

    def __str__(self):
        if self.func_name == "power3":
            function_string = "" + str(self.a) + " + " + str(self.b) + \
                              "x" + "^(" + str(self.c) + ")"
        elif self.func_name == "exp3":
            function_string = "" + str(self.a) + " + " + str(self.b) + \
                              "e^{" + str(self.c) + "x}"
        elif self.func_name == "lnsquare2":
            function_string = "ln[" + str(self.a) + " + " + str(self.b) + \
                              "sqrt(x / 9.81)]"
        elif self.func_name == "powerdecrease3":
            function_string = "" + str(self.a) + " + 1 / (x + " + str(self.b) + \
                               ")^" + str(self.c)
        elif self.func_name == "asymdecrease3":
            function_string = "" + str(self.a) + " + " + str(self.b) + \
                               "/ (1 + " + str(self.c) + " * x)"
        elif self.func_name == "logistics4":
            function_string = "" + str(self.a) + " + " + str(self.b) + \
                              " / {1 + e^[-1 * |" + str(self.c) + \
                              "| * (x - " + str(self.d) + ")]}"
        elif self.func_name == "alpha3":
            function_string =  "(" + str(self.a) + " + " + str(self.b) + \
                "x^" + str(self.c) + ") / 2.0445^(1 / logistics4(" + \
                str(self.C1) + ", " + str(self.C2) + ", |" + str(self.C3) + \
                "|, " + str(self.C4) + ")"
        elif self.func_name == "poly2":
            function_string = f"{self.a} * x^2 + {self.b} * x + {self.c}"
        elif self.func_name == "poly1":
            function_string = f"{self.a} * x + {self.b}"
        if isinstance(self._wrapper.func, np.ufunc):
            function_string += " with _wrapper: " + str(self._wrapper)
        return function_string


class Wrapper():

    def __init__(self, func, inner_wrapper=None):
        self.func = func
        self.inner_wrapper = inner_wrapper

    def __call__(self, x):
        if self.inner_wrapper is None:
            return self.func(x)
        else:
            return self.func(self.inner_wrapper(x))

    def __str__(self):
        return "Wrapper with function '" + str(self.func) + "' and inner_wrapper '" + str(self.inner_wrapper) + '"'
