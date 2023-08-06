# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 20:02:36 2019

@author: Reuben
"""

import numpy as np
import matplotlib.pyplot as plt
from . import utils
import warnings

def plot(box, x_var, y_var, fig_num=None, legend=False, xlim=None, 
                ylim=None, y_ind=None, **kwargs):
    pass

def vector_plot(box, x_var, y_var, dct=None, fig_num=None, legend=False, xlim=None, 
                ylim=None, y_ind=None, **kwargs):
    ''' Plot results for two vectors 
    
    Args:
        box (Box): A Box instance
        x_var (Variable): The x variable
        y_var (Variable): The y variable
        dct (dict): A dictionary of key-value pairs that must be 
            present in all rows.
        fig_num (int): Optional figure number. 
        legend (bool): Display the legend
        xlim ((float, float)): Optional tuple of x limits
        ylim ((float, float)): Optional tuple of y limits
        y_ind (int): If the y-variable data is a 2D array, provide the index
        for the desired component.
        kwargs: Optional keyword arguments passed to pyplot.plot.
        
    '''
    keys = [x_var, y_var]
    x_list, y_list, labels = box.vectors(keys, dct=dct)
    if len(labels) == 0:
        warnings.warn('No data for plot of: ' + str(keys))
    fig = plt.figure(fig_num)
    for x, y, label in zip(x_list, y_list, labels):
        if np.ndim(y) == 3:
            if y_ind is None:
                raise ValueError('y_ind must be supplied for 2D arrays' )
            # It's a list of 2D vectors, so try to select the right ones
            y = [vector[y_ind] for vector in utils.orient(y, len(x))]
        plt.plot(x, y, label=label, **kwargs)
    plt.xlabel(x_var)
    plt.ylabel(y_var)
    if legend:
        plt.legend()
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    return fig

