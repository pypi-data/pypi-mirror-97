#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Weight(ABC):

    @abstractmethod
    def __call__(self, X, Y=None, eval_gradient=False):
        '''Computes the weight matrix and optionally its gradient with respect
        to hyperparameters.

        Parameters
        ----------
        X: list of graphs
            The first dataset to be compared.
        Y: list of graphs or None
            The second dataset to be compared. If None, X will be compared with
            itself.
        eval_gradient: bool
            If True, returns the gradient of the weight matrix alongside the
            matrix itself.

        Returns
        -------
        weight_matrix: 2D ndarray
            A weight matrix between the datasets.
        weight_matrix_gradients: 3D ndarray
            A tensor where the i-th frontal slide [:, :, i] contain the partial
            derivative of the weight matrix with respect to the i-th
            hyperparameter.
        '''
        pass

    @property
    @abstractmethod
    def theta(self):
        '''An ndarray of all the hyperparameters in log scale.'''
        pass

    @theta.setter
    @abstractmethod
    def theta(self, values):
        '''Set the hyperparameters from an array of log-scale values.'''
        pass

    @property
    @abstractmethod
    def bounds(self):
        '''The log-scale bounds of the hyperparameters as a 2D array.'''
        pass


class RBFOverHausdorff(Weight):
    '''Compute weights by applying an RBF onto the Hausdorff distance as
    derived from the graph kernel.

    Parameters
    ----------
    kernel: object
        A graph kernel
    ADDITIONAL_ARGUMENTS: @Thomas this is at your discretion.
    '''

    def __init__(self, kernel, *ADDITIONAL_ARGUMENTS):
        pass

    def __call__(self, X, Y=None, eval_gradient=False, **kernel_options):
        '''A concrete implementation of the abstract method from the base
        class.

        Parameters
        ----------
        X, Y, eval_gradient: as previously defined.
            As defined in the base class.
        kernel_options: keyword arguments
            Additional arguments to be passed into the graph kernel.
        '''

    @property
    def theta(self):
        '''A concatenation of the hyperparameters of the RBF and the graph
        kernel.'''
        pass
