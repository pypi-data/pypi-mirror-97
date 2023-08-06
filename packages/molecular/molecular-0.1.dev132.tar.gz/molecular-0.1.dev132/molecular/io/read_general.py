
from fileinput import input as input_
from glob import glob as glob_
import logging
import numpy as np
import pandas as pd
import time

# Get the molecular.io logger
logger = logging.getLogger('molecular.io')


# Globular loadtxt
def loadtxt(fname, glob=False, verbose=False, **kwargs):
    """
    A refactoring of :ref:`numpy.loadtxt` that allows for globbing files.

    Parameters
    ----------
    fname : file, str, or pathlib.Path
        Name of file.
    glob : bool
        Does `fname` need to be globbed?
    verbose : bool
        Should information about the read-in be displayed?
    **kwargs
        Optional keyword parameters to pass to :ref:`numpy.loadtxt`.

    Returns
    -------
    pandas.Series
        Read file
    """

    # If glob, change fname to include all globbed files
    if glob:
        # Glob first; if glob is empty, throw an error
        fname_glob = glob_(fname)
        if not fname_glob:
            raise FileNotFoundError(fname)

        # Sort glob
        fname_glob = sorted(fname_glob)

        # Output if verbose
        if verbose:
            print(f'glob: {list(fname_glob)}')

        # Update fname to include all globbed files
        fname = input_(fname_glob)

    # Utilize numpy to read-in the file(s)
    data = np.loadtxt(fname, **kwargs)

    # If verbose, note the shape of the data
    if verbose:
        print(f'file loaded with shape {data.shape}')

    # Return
    return data


# TODO enable fname to be stored in the DataFrame? Is this a bad idea?
def read_table(fname, glob=False, sep='\s+', header=None, reindex=False, **kwargs):
    """
    Read table into :class:`pandas.DataFrame`.

    Parameters
    ----------
    fname : str
        Name of file.
    glob : true
        Should `fname` be treated as a globbed path? (Default: False)
    sep : str
        Character used to separate columns? (Default: white space)
    header : bool
        (Default: None)
    reindex : bool
        (Default: False)

    Returns
    -------
    pandas.DataFrame
        Data read in.
    """

    # If glob, change fname to include all globbed files
    if glob:
        # Glob first; if glob is empty, throw an error
        fname_glob = glob_(fname)
        if not fname_glob:
            raise FileNotFoundError(fname)

        # Sort glob
        fnames = sorted(fname_glob)

    # Otherwise, turn fname into a list
    # TODO evaluate if creating this list is right, or if we should short-circuit the read-in
    else:
        fnames = [fname]

    # Log files and start timer
    logger.info(f'processing file(s): {fnames}')
    start_time = time.time()

    # Cycle over fnames and read in
    kwargs['sep'] = sep
    kwargs['header'] = header
    data = [pd.read_table(fname, **kwargs).assign(_source=fname) for fname in fnames]

    # Concatenate
    data = data[0] if len(data) == 1 else pd.concat(data)

    # Log the shape of the data and the runtime
    end_time = time.time()
    logger.info(f'files loaded with shape {data.shape} in {int(end_time - start_time)} seconds')

    # If header is None and index_col is defined, reset columns
    if header is None and kwargs.get('index_col', None) is not None:
        data.columns = np.arange(len(data.columns))

    # Reindex?
    if reindex:
        data = data.reset_index(drop=True)

    # Return
    return data
