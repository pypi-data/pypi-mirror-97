"""
replica_exchange.py

author: C. Lockhart <chris@lockhartlab.org>
language: Python3
"""

from molecular.io import loadtxt

import numpy as np
import pandas as pd


# TODO this name vs CoupledMarkovChain??
class ReplicaWalk:
    def __init__(self, data):
        n_replicas = data['replica'].nunique()
        for replica in range(n_replicas):
            tmp = data.query(f'replica == {replica}')['config'].diff().fillna(0)
            assert tmp.min() == -1
            assert tmp.max() == 1
        self.data = data

    # Read NAMD history file (from RE multiwalker)
    @classmethod
    def from_namd(cls, fname, n_replicas, glob=False):
        data = pd.DataFrame()
        for replica in range(n_replicas):
            tmp = loadtxt(fname.format(replica=replica), glob=glob)
            data = data.append(pd.DataFrame({
                'step': tmp[:, 0],
                'replica': np.repeat(replica, len(tmp)),
                'config': tmp[:, 1].astype(int),
                'temperature': tmp[:, 2]
            }), ignore_index=True)
        return cls(data.sort_values(['replica', 'step']))

    def exchange_rate(self):
        pass

    def mosaic_plot(self, interval=100, cmap='jet'):
        import matplotlib.pyplot as plt
        from matplotlib.ticker import MultipleLocator, MaxNLocator
        import uplot as u

        u.core.set_mpl_theme()

        data = self.trajectory(by='config', reset_index=True)
        steps = data.index.to_numpy(dtype='int')[::interval]
        replicas = data.columns.to_numpy(dtype='int')
        if replicas[0] == 0:
            replicas = replicas + 1
            data = data + 1
        mosaic = data.to_numpy(dtype='int')[::interval, :]
        x = np.arange(mosaic.shape[0] + 1)
        y = np.arange(mosaic.shape[1] + 1)

        # Start figure and axis
        fig = plt.figure()
        ax = fig.add_subplot()
        # im = ax.pcolormesh(mosaic, cmap=cmap, edgecolors='k', linewidth=0.5)  # bwr
        im = ax.pcolormesh(x - 0.5, y - 0.5, mosaic.T, cmap=cmap, edgecolors='k', linewidth=0.5)

        # Format x axis
        # TODO change this so only units of X are display
        ax.set_xticks(np.arange(len(steps)))
        ax.set_xticklabels(steps)
        ax.set_xlabel(r'$step$')

        # Format y axis
        ax.set_yticks(np.arange(len(replicas)))
        ax.set_yticklabels(replicas)
        ax.set_ylabel(r'$temperature\ index$')

        # Format tick lines
        # ax.spines['top'].set_visible(False)
        # ax.spines['right'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='both', which='both', direction='out')

        ax.xaxis.set_major_locator(MultipleLocator(10))
        ax.xaxis.set_minor_locator(MultipleLocator(10))

        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_minor_locator(MultipleLocator(1))

        # fig.colorbar()
        ax.set_aspect('auto')
        # ax.grid(which='minor', color='w', linestyle='-', linewidth=5)

        ax.grid(linestyle='')

        # plt.axis('equal')
        # Add color bar
        cbar = plt.colorbar(im, ax=ax, shrink=0.5, drawedges=False)
        cbar.outline.set_linewidth(0.5)
        # cbar.ax.spines['right'].set_visible(True)
        cbar.ax.tick_params(direction='out', length=5.)
        cbar.ax.tick_params(which='minor', length=0)
        #        cbar.ax.yaxis.set_major_locator(MultipleLocator(1))
        cbar.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        cbar.ax.set_ylabel(r'$replica\ index$')

        # Save the image
        # fig.show()
        fig.savefig('mosaic_plot.png')

    def trajectory(self, by='config', reset_index=True):
        columns = 'config'
        values = 'replica'
        if by == 'replica':
            columns, values = values, columns
        elif by != 'config':
            raise AttributeError('unexpected `by`')
        data = self.data.pivot_table(index='step', columns=columns, values=values)
        if reset_index:
            data.reset_index(drop=True, inplace=True)
            data.index.name = 'step'
        return data


# Create a temperature schedule
def temp_schedule(temp_min=300, temp_max=440, n_temps=40, mode='geometric'):
    r"""
    Create a temperature schedule that could be used, for instance, with replica exchange.

    There are several choices for `mode`. Note that :math:`T` refers to the temperature at :math:`i = 1 ... R`, where
    :math:`T_1` is `temp_min` and :math:`T_R` is `temp_max`. In total, there are :math:`R` temperatures (= `n_temps`).

    * "geometric" [#]_

    .. math :: T_i = T_1 \left( \frac{T_R}{T_1} \right)^{\frac{i-1}{R-1}}

    * "linear"

    .. math :: T_i = T_1 + (i-1) \frac{T_R-T_1}{R-1}

    * "parabolic" (Note if `n_temps` is even, `temp_max` won't directly be sampled).

    .. math :: T_i = T_1 - \frac{T_R-T_1}{\left( \frac{R-1}{2} \right) ^2} (i-1) (i-R)

    Parameters
    ----------
    temp_min : float
        Lowest temperature
    temp_max : float
        Highest temperature
    n_temps : int
        Number of temperatures
    mode : str
        Mode to produce schedule. Valid options include "geometric", "linear", "parabolic". Any substring will match,
        but the preference should be to use the full option label. (Default: "geometric")

    Returns
    -------
    numpy.ndarray
        Temperature schedule

    Examples
    --------
    .. plot::
       :include-source:

       import matplotlib.pyplot as plt
       import molecular as mol

       n_temps = 10
       geometric = mol.temp_schedule(300, 440, n_temps, 'geometric')
       linear = mol.temp_schedule(300, 440, n_temps, 'linear')
       parabolic = mol.temp_schedule(300, 440, n_temps, 'parabolic')

       plt.figure()
       plt.plot(range(n_temps), geometric, label='geometric')
       plt.plot(range(n_temps), linear, label='linear')
       plt.plot(range(n_temps), parabolic, label='parabolic')
       plt.xlabel('index')
       plt.ylabel('temperature')
       plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
       plt.show()

    References
    ----------
    .. [#] Nymeyer, H., Gnanakaran, S., & García, A. E. (2004) Atomistic simulations of protein folding, using the
       replica exchange algorithm. *Methods Enzymol.* **383**: 119-149.
    """

    mode = mode.lower()

    if mode in 'geometric':
        schedule = temp_min * np.power(temp_max / temp_min, np.arange(n_temps) / (n_temps - 1.), dtype=np.float64)

    elif mode in 'linear':
        schedule = np.linspace(start=temp_min, stop=temp_max, num=n_temps)

    elif mode in 'parabolic':
        temp_range = temp_max - temp_min
        temp_ind = np.arange(n_temps)
        schedule = temp_min - (temp_range / np.square((n_temps - 1.) / 2.)) * temp_ind * (temp_ind - n_temps + 1.)

    else:
        raise AttributeError(f'mode {mode} not supported')

    return schedule


class ReplicaWalk:
    def __init__(self, data):
        n_replicas = data['replica'].nunique()
        for replica in range(n_replicas):
            tmp = data.query(f'replica == {replica}')['config'].diff().fillna(0)
            assert tmp.min() == -1
            assert tmp.max() == 1
        self.data = data

    # Read NAMD history file (from RE multiwalker)
    @classmethod
    def from_namd(cls, fname, n_replicas, glob=False):
        data = pd.DataFrame()
        for replica in range(n_replicas):
            tmp = mol.loadtxt(fname.format(replica=replica), glob=glob)
            data = data.append(pd.DataFrame({
                'step': tmp[:, 0],
                'replica': np.repeat(replica, len(tmp)),
                'config': tmp[:, 1].astype(int),
                'temperature': tmp[:, 2]
            }), ignore_index=True)
        return cls(data.sort_values(['replica', 'step']))

    def exchange_rate(self):
        pass

    def mosaic_plot(self, interval=100, cmap='jet'):
        import matplotlib.pyplot as plt
        from matplotlib.ticker import MultipleLocator, MaxNLocator
        import uplot as u

        u.core.set_mpl_theme()

        data = self.trajectory(by='config', reset_index=True)
        steps = data.index.to_numpy(dtype='int')[::interval]
        replicas = data.columns.to_numpy(dtype='int')
        if replicas[0] == 0:
            replicas = replicas + 1
            data = data + 1
        mosaic = data.to_numpy(dtype='int')[::interval, :]
        x = np.arange(mosaic.shape[0] + 1)
        y = np.arange(mosaic.shape[1] + 1)

        # Start figure and axis
        fig = plt.figure()
        ax = fig.add_subplot()
        # im = ax.pcolormesh(mosaic, cmap=cmap, edgecolors='k', linewidth=0.5)  # bwr
        im = ax.pcolormesh(x - 0.5, y - 0.5, mosaic.T, cmap=cmap, edgecolors='k', linewidth=0.5)

        # Format x axis
        # TODO change this so only units of X are display
        ax.set_xticks(np.arange(len(steps)))
        ax.set_xticklabels(steps)
        ax.set_xlabel(r'$step$')

        # Format y axis
        ax.set_yticks(np.arange(len(replicas)))
        ax.set_yticklabels(replicas)
        ax.set_ylabel(r'$temperature\ index$')

        # Format tick lines
        # ax.spines['top'].set_visible(False)
        # ax.spines['right'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='both', which='both', direction='out')

        ax.xaxis.set_major_locator(MultipleLocator(10))
        ax.xaxis.set_minor_locator(MultipleLocator(10))

        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_minor_locator(MultipleLocator(1))

        # fig.colorbar()
        ax.set_aspect('auto')
        # ax.grid(which='minor', color='w', linestyle='-', linewidth=5)

        ax.grid(linestyle='')

        # plt.axis('equal')
        # Add color bar
        cbar = plt.colorbar(im, ax=ax, shrink=0.5, drawedges=False)
        cbar.outline.set_linewidth(0.5)
        # cbar.ax.spines['right'].set_visible(True)
        cbar.ax.tick_params(direction='out', length=5.)
        cbar.ax.tick_params(which='minor', length=0)
        #        cbar.ax.yaxis.set_major_locator(MultipleLocator(1))
        cbar.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        cbar.ax.set_ylabel(r'$replica\ index$')

        # Save the image
        # fig.show()
        fig.savefig('mosaic_plot.png')

    def trajectory(self, by='config', reset_index=True):
        columns = 'config'
        values = 'replica'
        if by == 'replica':
            columns, values = values, columns
        elif by != 'config':
            raise AttributeError('unexpected `by`')
        data = self.data.pivot_table(index='step', columns=columns, values=values)
        if reset_index:
            data.reset_index(drop=True, inplace=True)
            data.index.name = 'step'
        return data


if __name__ == '__main__':
    print(temp_schedule(temp_min=300, temp_max=440, n_temps=5, mode='geometric'))
    # print(temp_schedule(temp_min=310, temp_max=500, n_temps=5, mode='parabolic'))
