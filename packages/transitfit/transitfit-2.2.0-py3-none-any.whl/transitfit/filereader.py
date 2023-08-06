'''
file_reader

Module to help make using csv files super easy as inputs
'''

import numpy as np
import pandas as pd
from .priorinfo import PriorInfo, _prior_info_defaults

def _read_data_csv(path):
    '''
    Given a path to a csv with columns [time, depths, errors], will get
    all the data in a way which can be used by the Retriever

    '''
    # Read in with pandas
    data = pd.read_csv(path)

    # Extract the arrays
    times, depths, errors = data.values.T

    return times, depths, errors

def _read_data_txt(path, skiprows=0):
    '''
    Reads a txt data file with columns
    '''
    times, depth, errors = np.loadtxt(path, skiprows=skiprows).T

    return times, depths, errors


def read_data_file(path, skiprows=0, delimiter=None):
    '''
    Reads a file in, assuming that it is either a:
        .csv
        .txt
    with columns in the order time, depth, errors

    Parameters
    ----------
    path : str
        Full path to the file to be loaded
    skiprows : int, optional
        Number of rows to skip in reading txt file (to avoid headers)
    delimiter : str, optional
        The string used to separate values. The default is whitespace.

    Returns
    -------
    times : np.array
        The times of the data series
    flux : np.array
        The flux
    error : np.array
        The uncertainty on the flux
    '''
    if path[-4:] == '.csv':
        return _read_data_csv(path)
    if path[-4:] == '.txt':
        return _read_data_txt(path, skiprows)


def read_data_file_array(data_paths, skiprows=0):
    '''
    If passed an array of paths, will read in to produce times, flux and
    uncertainty arrays
    '''
    data_paths = np.array(data_paths)

    num_wavelengths = data_paths.shape[0]
    num_times = data_paths.shape[1]

    data = np.array([[None for i in range(num_times)] for j in range(num_wavelengths)], object)

    for i in range(num_wavelengths):
        for j in range(num_times):
            if data_paths[i,j] is not None:
                data[i,j] = read_data_file(data_paths[i,j])


    times = np.array([[None for i in range(num_times)] for j in range(num_wavelengths)], object)
    depths = np.array([[None for i in range(num_times)] for j in range(num_wavelengths)], object)
    errors = np.array([[None for i in range(num_times)] for j in range(num_wavelengths)], object)

    for i in range(num_wavelengths):
        for j in range(num_times):
            if data[i,j] is not None:
                times[i,j] = data[i,j][0]
                depths[i,j] = data[i,j][1]
                errors[i,j] = data[i,j][2]

    return times, depths, errors


def read_priors_file(path, limb_dark='quadratic'):
    '''
    If given a csv file containing priors, will produce a PriorInfo object
    based off the given values

    Columns should me in the order
    ------------------------------------------------------------------
    |  key  |   best  |  low_lim  |   high_lim  |  epoch  |  filter  |
    ------------------------------------------------------------------

    If the parameter is invariant across the an epoch or filter, leave the
    entry blank.

    If you want to fix a parameter at a given value, leave low_lim and high_lim
    blank. Just provide best, along with epoch and filter if required

    limb_dark is the model of limb darkening you want to use

    Notes
    -----
    Detrending currently cannot be initialised in the prior file. It will be
    available as a kwarg in the pipeline function
    '''
    table = pd.read_csv(path).values

    # Work out how mnay light curves are being used.
    num_times = sum(table[:, 0] == 't0')
    num_wavelengths = sum(table[:, 0] == 'rp')

    # check the limb darkening coefficients and if they are fitting
    # First, A small dict to check if each LD param is being fitted.
    # This basically checks which parameters are required for the different models
    limb_dark_params = {}
    limb_dark_params['u1'] = False
    limb_dark_params['u2'] = False
    limb_dark_params['u3'] = False
    limb_dark_params['u4'] = False

    if not limb_dark == 'uniform':
        limb_dark_params['u1'] = np.any(table[0] == 'u1')
        if not limb_dark == 'linear':
            limb_dark_params['u2'] = np.any(table[0] == 'u2')
            if limb_dark == 'nonlinear':
                limb_dark_params['u3'] = np.any(table[0] == 'u3')
                limb_dark_params['u4'] = np.any(table[0] == 'u4')

    #######################################################
    # Set up the default dict to initialise the PriorInfo #
    #######################################################
    default_prior_dict = {}

    default_prior_dict['num_times'] = num_times
    default_prior_dict['num_wavelengths'] = num_wavelengths

    # Initialse any variables which vary with epoch or wavelength
    default_prior_dict['rp'] = np.full(num_wavelengths, np.nan)
    default_prior_dict['t0'] = np.full(num_times, np.nan)

    for key in limb_dark_params:
        if limb_dark_params[key]:
            default_prior_dict[key] = np.full(num_wavelengths, np.nan)

    # Now make the default values for the fitting parameters
    for row in table:
        key, best, low, high, epoch, filt = row
        if key == 'rp':
            default_prior_dict[key][int(filt)] = best
        elif key == 't0':
            default_prior_dict[key][int(epoch)] = best
        elif key in ['u1','u2','u3','u4']:
            if limb_dark_params[key]:
                default_prior_dict[key][int(filt)] = best
        else:
            default_prior_dict[key] = best

    # Now we set the fixed values from defaults
    for key in _prior_info_defaults:
        if key not in default_prior_dict:
            default_prior_dict[key] = _prior_info_defaults[key]

    # Check to see if there are any light curves which have not had 'rp' or 't0 defined'
    if np.isnan(default_prior_dict['rp']).any():
        bad_indices = np.where(np.isnan(default_prior_dict['rp']))[0]
        bad_string = str(bad_indices)[1:-1]
        raise ValueError('Light curve(s) {} are missing rp values'.format(bad_string))
    if np.isnan(default_prior_dict['t0']).any():
        bad_indices = np.where(np.isnan(default_prior_dict['t0']))[0]
        bad_string = str(bad_indices)[1:-1]
        raise ValueError('Light curve(s) {} are missing t0 values'.format(bad_string))
    for key in limb_dark_params:
        if limb_dark_params[key]:
            if np.isnan(default_prior_dict[key]).any():
                bad_indices = np.where(np.isnan(default_prior_dict[key]))[0]
                bad_string = str(bad_indices)[1:-1]
                raise ValueError('Light curve(s) {} are missing {}} values'.format(bad_string, key))

    # MAKE DEFAULT PriorInfo #
    prior_info = PriorInfo(default_prior_dict, warn=False)

    #################################
    # Now add in the actual priors! #
    #################################
    for row in table:
        key, best, low, high, epoch, filt = row

        # This is a check to make sure we want to vary the parameter
        if np.isfinite(low) and np.isfinite(high):
            if key in ['rp']:
                prior_info.add_uniform_fit_param(key, best, low, high, filter_idx=int(filt))

            elif key in ['t0']:
                prior_info.add_uniform_fit_param(key, best, low, high, epoch_idx=int(epoch))

            elif key in ['u1','u2','u3','u4']:
                prior_info.add_uniform_fit_param(key, best, low, high, filter_idx=int(filt))

            else:
                prior_info.add_uniform_fit_param(key, best, low, high)

    return prior_info
