'''
OutputWriter.py

Object to deal with writing fitting results to files
'''
import numpy as np
import os
import csv
import pandas as pd
from .retriever import global_params, filter_dependent_params, lightcurve_dependent_params
from ._utils import weighted_avg_and_std, host_radii_to_AU


class OutputWriter:
    def __init__(self, lightcurves, full_prior, host_r=None):
        '''
        Designed to handle writing outputs from retrieval to files

        Parameters
        ----------
        lightcurves : array_like, shape (n_telescopes, n_filters, n_epochs)
            The full lightcurves array to be retrieved.

        '''
        self.all_lightcurves = lightcurves

        self.full_prior = full_prior

        self.ld_coeffs = self.full_prior.limb_dark_coeffs

        self.host_r = host_r

    def save_final_light_curves(self, results, priors, lightcurves,
                                folder='./final_light_curves', folded=False):
        '''

        '''
        pass

    def save_folded_results(self, results, priors, lightcurves, constants_dict,
                            output_folder='./output_parameters',
                            summary_file='summary_output.csv',
                            full_output_file='full_output.csv'):
        '''
        Saves the outputs from folded mode retrieval

        This allows for contant values to be used (eg P and t0 when folded)


        '''
        pass

    def save_results(self, results, priors, lightcurves,
                     output_folder='./output_parameters',
                     summary_file='summary_output.csv',
                     full_output_file='full_output.csv',):
        '''
        Saves results to .csv files

        Parameters
        ----------
        results : array_like, shape (n_batches, )
            The results from each run
        priors : array_like, shape (n_batches, )
            The priors for each run
        lightcurves : array_like, shape (n_batches, )
            The light curves for each run
        fit_ld : bool, optional
            Must be true if LDCs are fitted. Default is True
        output_folder : str, optional
            The folder to save output files to (not plots). Default is
            `'./output_parameters'`
        summary_file : str, optional
            The file name for the final output. This file only gives the
            averaged values, rather than individual values fitted within
            batches if there are any. Default is `'summary_output.csv'`
        full_output_file : str, optional
            The file name for the full output file. This file gives partial
            results from batches, rather than the averaged results. Default is
            `'full_output.csv'`

        Returns
        -------
        best_vals : dict
            Each entry is [best val, error]
        combined_dict : dict
            The combined results dictionary. Each entry is a list of values
            from the results dictionaries -
            [[best value, median, 16th percentile, 84th percentile, stdev],...]
        '''
        fit_ld = priors[0].fit_ld

        results_dicts = []

        for i, ri in enumerate(results):
            results_dicts.append(self.get_results_dict(ri, priors[i], lightcurves[i]))

        best_vals, combined_results = self.get_best_vals(results_dicts, fit_ld)

        # Put each dict into a pandas DataFrame so we can output it nicely
        # Columns:
        # Best vals - param, tidx, fidx, eidx, best, error
        # Combined vals - param, tidx, fidx, eidx, batch, best, error
        best_vals_arr = np.zeros((1, 6), dtype=object)
        batched_vals_arr = np.zeros((1, 7), dtype=object)

        for param in best_vals:
            # Sort out display of the parameters
            if param == 'rp':
                print_param = 'rp/r*'
            elif param == 'a':
                print_param = 'a/r*'
            else:
                print_param = param

            for i in np.ndindex(best_vals[param].shape):
                # Sort out the indices:
                if param in global_params:
                    tidx, fidx, eidx = None, None, None
                elif param in filter_dependent_params:
                    tidx, fidx, eidx = None, i[1], None
                else:
                    tidx, fidx, eidx = i

                # Add the best values in
                best_vals_arr = np.append(best_vals_arr, np.array([[print_param, tidx, fidx, eidx, *best_vals[param][i]]]), axis=0)


                if param == 'a' and self.host_r is not None:
                    # Put a into AU as well
                    a_AU, a_AU_err = host_radii_to_AU(best_vals[param][i][0],
                                                      self.host_r[0],
                                                      best_vals[param][i][1],
                                                      self.host_r[1], True)
                    best_vals_arr = np.append(best_vals_arr, np.array([['a/AU', tidx, fidx, eidx, a_AU, a_AU_err]]), axis=0)

                # Loop over batches
                for bi in range(len(combined_results[param][i])):
                    batched_vals_arr = np.append(batched_vals_arr, np.array([[print_param, tidx, fidx, eidx, bi, combined_results[param][i][bi][0], combined_results[param][i][bi][-1]]]), axis=0)

                    if param == 'a' and self.host_r is not None:
                        # Put a into AU as well
                        a_AU, a_AU_err = host_radii_to_AU(combined_results[param][i][bi][0],
                                                          self.host_r[0],
                                                          combined_results[param][i][bi][-1],
                                                          self.host_r[1], True)
                        batched_vals_arr = np.append(batched_vals_arr, np.array([['a/AU', tidx, fidx, eidx, bi, a_AU, a_AU_err]]), axis=0)

        # Make the DataFrames - cut off the first (all zeros) entries
        best_df = pd.DataFrame(best_vals_arr[1:], columns=['Parameter', 'Telescope', 'Filter', 'Epoch', 'Best', 'Error'])
        batched_df  = pd.DataFrame(batched_vals_arr[1:], columns=['Parameter', 'Telescope', 'Filter', 'Epoch', 'Batch', 'Best', 'Error'])

        # Save outputs
        os.makedirs(output_folder, exist_ok=True)
        best_df.to_csv(os.path.join(output_folder, summary_file), index=False, na_rep='-')
        batched_df.to_csv(os.path.join(output_folder, full_output_file), index=False, na_rep='-')

        return best_vals, combined_results

    def get_results_dict(self, results, priors, lightcurves):
        '''
        Makes dictionaries of results from a single dynesty run.

        Useful for putting results in a form which allows for easy summary etc.

        Parameters
        ----------
        results : dict
            Results from a single dynesty run
        priors : PriorInfo
            The priors for the run
        lightcurves : array_like, shape (n_telescopes, n_filters, n_epochs)
            The lightcurves for the run

        Returns
        -------
        results_dict : dict
            Each entry is [best value, median, 16th percentile, 84th percentile, stdev]
        '''
        results_dict = {}

        # Loop over all fitting parameters and access the results
        for i, param_info in enumerate(priors.fitting_params):
            param_name, batch_tidx, batch_fidx, batch_eidx = param_info

            batch_idx = (batch_tidx, batch_fidx, batch_eidx)
            # GET INDICES
            # The indices here are for a particular batch. We want global
            # values so pull them out of the LightCurves
            full_idx = self._batch_to_full_idx(batch_idx, param_name, lightcurves, priors.fit_ttv)

            result_entry = [results.best[i], results.median[i], results.lower_err[i], results.upper_err[i], results.uncertainties[i]]

            # Check that the parameter has been initialised in the dict
            results_dict = self._initialise_dict_entry(results_dict, param_name)
            if results_dict[param_name][full_idx] is None:
                # Initialise a list
                results_dict[param_name][full_idx] = []

            results_dict[param_name][full_idx].append(result_entry)

        # Go through the PriorInfo and get the constant values out
        # These are ones that were in the priors and NOT in fitting params
        for param_name in priors.priors:
            if param_name not in priors.fitting_params:
                # This is a constant value
                # Check that the parameter has been initialised in the dict
                results_dict = self._initialise_dict_entry(results_dict, param_name)
                for i in np.ndindex(priors.priors[param_name].shape):
                    if priors.priors[param_name] is not None:
                        result_entry = [priors.priors[param_name].default_value, None, None, None, None]

                        if results_dict[param_name][i] is None:
                            # Initialise a list
                            results_dict[param_name][i] = []

                        results_dict[param_name][i].append(result_entry)

        print(results_dict)
        return results_dict

    def get_best_vals(self, results_dicts, fit_ld=True, return_combined=True):
        '''
        Gets the best values for a set of runs from the given results dicts

        Parameters
        ----------
        results_dicts : array_like, shape (n_batches, )
            The results_dicts obtained from get_results_dict
        fit_ld : bool, optional
            Should be True if LDC fitting. Default is True
        return_combined : bool, optional
            If True, will return the results dicts combined into a single dict.
            Default is True.

        Returns
        -------
        best_vals : dict
            Each entry is [best val, error]
        combined_dict : dict
            The combined results dictionary. Returned if return_combined is
            True
        '''
        best_vals = {}

        # Collate the results dicts
        combined_dict = self.combine_results_dicts(results_dicts)

        for param in combined_dict:
            # Loop through each parameter
            best_vals = self._initialise_dict_entry(best_vals, param)

            for i in np.ndindex(combined_dict[param].shape):
                if combined_dict[param][i] is not None:
                    # get the weighted avrage and error
                    if np.any(combined_dict[param][i][:,-1] == None):
                        # This is a constant
                        best_vals[param][i] = [combined_dict[param][i][:,0], None]
                    else:
                        best_vals[param][i] = weighted_avg_and_std(combined_dict[param][i][:, 0], combined_dict[param][i][:, -1], single_val=True)

        # Limb darkening bits
        if fit_ld:
            best_vals, combined_dict = self.add_best_u(best_vals, combined_dict)

        print(best_vals)

        if return_combined:
            return best_vals, combined_dict
        return best_vals

    def combine_results_dicts(self, results_dicts):
        '''
        Combines the given results dicts into one dict

        Parameters
        ----------
        results_dicts : array_like, shape (n_batches, )
            The results_dicts obtained from get_results_dict

        Returns
        -------
        combined_dict : dict
            The combined results dictionary. Each entry is a list of values
            from the results dictionaries -
            [[best value, median, 16th percentile, 84th percentile, stdev],...]
        '''
        combined_dict = {}

        # Loop through each dict and the params
        for rd in results_dicts:
            for param in rd.keys():
                combined_dict = self._initialise_dict_entry(combined_dict, param)

                for i in np.ndindex(combined_dict[param].shape):
                    if rd[param][i] is not None:

                        if combined_dict[param][i] is None:
                            combined_dict[param][i] = rd[param][i]
                        else:
                            combined_dict[param][i].append(rd[param][i])

                # Convert to np.arrays
                for i in np.ndindex(combined_dict[param].shape):
                    combined_dict[param][i] = np.array(combined_dict[param][i])

        return combined_dict

    def add_best_u(self, best_dict, combined_dict):
        '''
        Given results dicts, adds in the u vals

        Parameters
        ----------
        best_dict : dict
            The dictionary of best results
        combined_dict : dict
            The full results

        Returns
        -------
        best_dict : dict
            The same dictionary with the best u vals added.
        combined_dict : dict
            The same dictionary with the u vals added.
        '''
        # Initialise each of the u params
        u_coeffs = []
        for param in self.ld_coeffs:
            ldc_q = 'q{}'.format(param[-1])
            ldc_u = 'u{}'.format(param[-1])
            u_coeffs.append(ldc_u)

            if ldc_u not in best_dict:
                combined_dict[ldc_u] = combined_dict[ldc_q].generate_blank_ParamArray()
                best_dict[ldc_u] = combined_dict[ldc_u].generate_blank_ParamArray()

        # Now get the values!
        for i in np.ndindex(best_dict['q0'].shape):
            if best_dict['q0'][i] is not None:
                # There are q values associated with this filter
                for u in u_coeffs:
                    best_dict[u][i] = []
                    combined_dict[u][i] = []

                # Put all the q values for a given filter into one place so we
                # can access q0, q1 simultaneously for converting to u
                n_batches = len(combined_dict['q0'][i])

                # indexing is filter_q[batch, val/err, qX]
                filter_q = np.zeros((n_batches, 2, len(self.ld_coeffs)))

                for b in range(n_batches):
                    for qi, q in enumerate(self.ld_coeffs):
                        filter_q[b,0,qi] = combined_dict[q][i][b][0]
                        filter_q[b,1,qi] = combined_dict[q][i][b][-1]

                # indexing is best_filter_q[val/err, qX]
                best_filter_q = np.vstack((best_dict[q][i] for q in self.ld_coeffs)).T

                # Convert the q values. First up the combined dict:
                for b in range(n_batches):
                    u, u_err = self.full_prior.ld_handler.convert_qtou_with_errors(*filter_q[b])

                    for k, uk in enumerate(u_coeffs):
                        combined_dict[uk][i].append([u[k], u_err[k]])

                # Now the best dict:
                u, u_err = self.full_prior.ld_handler.convert_qtou_with_errors(*best_filter_q)
                for k, uk in enumerate(u_coeffs):
                    best_dict[uk][i] = np.array([u[k], u_err[k]])

        return best_dict, combined_dict

    def _initialise_dict_entry(self, d, param):
        '''
        Initialises param in results dictionaries using ParamArray
        '''
        if param not in d:
            d[param] = self.full_prior.priors[param].generate_blank_ParamArray()
        return d

    def _batch_to_full_idx(self, i, param_name, lightcurves, fit_ttv):
        '''
        Converts a batch index into a full index

        Parameter
        ---------
        i : tuple
            (batch_tidx, batch_fidx, batch_eidx)

        Returns
        -------
        (tidx, fidx, eidx)
        '''
        batch_tidx, batch_fidx, batch_eidx = i

        if param_name in global_params or (param_name == 't0' and not fit_ttv):
            tidx, fidx, eidx = None, None, None
        elif param_name == 't0' and fit_ttv:
            for k in np.ndindex(lightcurves.shape):
                if k[2] == batch_eidx and lightcurves[k] is not None:
                    tidx = None
                    fidx = None
                    eidx = lightcurves[k].epoch_idx
                    break
        elif param_name in filter_dependent_params:
            for k in np.ndindex(lightcurves.shape):
                if k[1] == batch_fidx and lightcurves[k] is not None:
                    tidx = None
                    fidx = lightcurves[k].filter_idx
                    eidx = None
                    break
        else:
            tidx = lightcurves[batch_tidx, batch_fidx, batch_eidx].telescope_idx
            fidx = lightcurves[batch_tidx, batch_fidx, batch_eidx].filter_idx
            eidx = lightcurves[batch_tidx, batch_fidx, batch_eidx].epoch_idx

        return tidx, fidx, eidx
