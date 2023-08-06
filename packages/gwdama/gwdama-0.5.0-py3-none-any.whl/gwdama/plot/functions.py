"""
This submodule contains some function to produce nice plots 'out of the box'
"""

import matplotlib.pyplot as plt

def make_hist(data, xlabel='Value', title=None, **kwargs):
    """
    Function to prepare plots.
    """
    
    default_kwgs = {
        'color':'#78909c',
        'bins':'auto',
        'alpha': .6,
        'rwidth': 0.9,
        'density': True
        }
        
    for k, v in default_kwgs.items():
        kwargs[k] = kwargs.get(k, v)
    
    fig, ax = plt.subplots(figsize=(10,6))
    # An "interface" to matplotlib.axes.Axes.hist() method
    n, bins, patches = ax.hist(x=data, **kwargs)
    ax.grid(alpha=0.4)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    if kwargs['density']:
        ax.set_ylabel('Density')
    else:
        ax.set_ylabel('Occurrence')

    return fig
