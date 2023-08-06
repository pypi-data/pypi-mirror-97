"""
This submodule contains some function to produce nice plots 'out of the box'
"""

import matplotlib.pyplot as plt

def make_hist(data, xlabel='Value', figsize=(10,6), title=None, **kwargs):
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
    
    fig, ax = plt.subplots(figsize=figsize)
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

def reshow(fig):
    """This function creates a dummy figure and uses its manager to
    display ``fig``. This is useful whaen you want to show again a
    pyplot Figure object that has been closed.
    """
    plt.close(fig)
    dummy = plt.figure()
    new_manager = dummy.canvas.manager
    new_manager.canvas.figure = fig
    fig.set_canvas(new_manager.canvas)


def plot_itf_meta(meta, t0=None, sample_rate=None, mode='bar'):
    """
    WORK in Progress
    Function to plot 'V1:DQ_META_ITF_Mode'
    For rference:
    ITF_mode: 	V1:DQ_META_ITF_Mode:
             1: Science
             0: Unknown
            -1: Adjusting
            -3: Commissioning
            -4: Maintenance
            -5: Calibration
            -7: Locked
            -8: Not locked
            -9: Locking
            -11:Upgrading
            -12:Troubleshooting
    """
    
    
    labels = ['Science', 'Unknown', 'Adjusting', 'Commissioning',
              'Maintenance','Calibration','Locked','Not locked',
              'Locking','Upgrading','Troubleshooting']

    colors = ['green','red','fuchsia', 'darkorange',
              'firebrick', 'darkviolet','blue', 'gold',
              'lightskyblue', 'lightcoral','crimson']

    #metadict = {'Science': }
    
    ax1.set_title("S200311ba - "+channel)
    ax2.axvspan(ti[0],tl, color='g', label='Science {:.2f}%'.format(100 * sum(meta.data==1)/meta.size))
    ax2.axvspan(tl,tr, color='magenta', label='Adjusting {:.2f}%'.format(100 * sum(meta.data==-1)/meta.size))
    ax2.axvspan(tr,ti[-1], color='g')
    ax2.set_xlabel(f'Time [sec] around {from_gps(e_gps)} UTC ({e_gps})')
    ax2.set_xlim(ti[0],ti[-1])
    ax2.set_yticks([])
    leg = ax2.legend(title='V1:DQ_META_ITF_Mode', bbox_to_anchor=(1.02, 1.5), loc='upper left',)
    leg._legend_box.align = "left"
    
    
    return fig