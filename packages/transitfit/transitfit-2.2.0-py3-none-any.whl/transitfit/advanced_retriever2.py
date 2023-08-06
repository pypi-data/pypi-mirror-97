'''
AdvancedRetriever2

I've made this to piece-by-piece try and work out why the AdvancedRetriever
doesn't work.

'''

from .retriever import Retriever
from .io import read_input_file, read_priors_file
from ._pipeline import run_retrieval

class AdvancedRetriever2:
    def __init__(self, data_path, prior_path, filter_path=None):
        '''
        AdvancedRetriever2
        '''
        # Nothing happens here for now except saving some paths
        self.data_path = data_path
        self.prior_path = prior_path
        self.filter_path = filter_path

    def make_priors(self, ld_fit_method='independent', ld_model='quadratic',
                    detrend=True, normalise=True, detrending_list=[['nth order', 2]]):
        '''
        Makes PriorInfo
        '''

        '''
        # load the lightcurves
        lightcurves, detrending_index_array = read_input_file(self.data_path)

        n_telescopes = lightcurves.shape[0]
        n_filters = lightcurves.shape[1]
        n_epochs = lightcurves.shape[2]


        print('Loading priors from ')
        priors = read_priors_file(self.prior_path, n_telescopes, n_filters, n_epochs, ld_model)

        if ld_fit_method == 'independent':
            print('Initialising limb darkening fitting...')
            priors.fit_limb_darkening(ld_fit_method)

        if detrend:
            priors.fit_detrending(lightcurves, detrending_list, detrending_index_array)

        if normalise:
            print('Initialising normalisation...')
            priors.fit_normalisation(lightcurves)
        '''
        lightcurves, detrending_index_array = read_input_file(self.data_path)

        n_telescopes = lightcurves.shape[0]
        n_filters = lightcurves.shape[1]
        n_epochs = lightcurves.shape[2]

        # Read in the priors
        print('Loading priors from {}...'.format(self.prior_path))
        priors = read_priors_file(self.prior_path, n_telescopes, n_filters, n_epochs, 'quadratic')

        # Set up all the optional fitting modes (limb darkening, detrending,
        # normalisation...)
        print('Initialising limb darkening fitting...')
        priors.fit_limb_darkening('independent')

        print('Initialising detrending...')
        priors.fit_detrending(lightcurves, [['nth order', 2]], detrending_index_array)

        print('Initialising normalisation...')
        priors.fit_normalisation(lightcurves)

        print(priors.detrend)

        return priors, lightcurves

    def run_retrieval_Retriever(self, nlive=60, dlogz=0.7, sample='rslice'):
        '''
        Runs retrieval using the old Retriever
        '''

        # Make the priors and get lightcurves
        priors, lightcurves = self.make_priors()

        print(priors.detrend)

        retriever = Retriever()

        return retriever.run_dynesty(lightcurves, priors, nlive=nlive, dlogz=dlogz, sample=sample)

    def run_pipeline_function(self, nlive=60, dlogz=0.7, sample='rslice'):
        '''
        Runs retrieval directly calling the existing pipeline
        '''
        return run_retrieval(self.data_path, self.prior_path, [['nth order', 2]],
            nlive=60, dlogz=0.7, sample='rslice', use_batches=False)

    def run_pipeline_full(self, nlive=60, dlogz=0.7, sample='rslice'):
        print('Loading light curve data...')

        lightcurves, detrending_index_array = read_input_file(self.data_path)

        n_telescopes = lightcurves.shape[0]
        n_filters = lightcurves.shape[1]
        n_epochs = lightcurves.shape[2]

        # Read in the priors
        print('Loading priors from {}...'.format(self.prior_path))
        priors = read_priors_file(self.prior_path, n_telescopes, n_filters, n_epochs, 'quadratic')

        # Set up all the optional fitting modes (limb darkening, detrending,
        # normalisation...)
        print('Initialising limb darkening fitting...')
        priors.fit_limb_darkening('independent')

        print('Initialising detrending...')
        priors.fit_detrending(lightcurves, [['nth order', 2]], detrending_index_array)

        print('Initialising normalisation...')
        priors.fit_normalisation(lightcurves)

        print('The parameters we are retrieving are: {}'.format(priors.fitting_params))
        print('Beginning retrieval of {} parameters...'.format(len(priors.fitting_params)))
        retriever = Retriever()
        return retriever.run_dynesty(lightcurves, priors, nlive=nlive,
                                     dlogz=dlogz, sample=sample)


def test_ar2_old_retriever(nlive=60, dlogz=0.7, sample='rslice'):
    priors_path = 'priors_ROnly.csv'
    filter_path = 'filter_info_ROnly.csv'
    data_path = 'files_input_ROnly.csv'

    ar2 = AdvancedRetriever2(data_path, priors_path, filter_path)

    try:
        return ar2.run_retrieval_Retriever(nlive, dlogz, sample)

    except:
        return -1

def test_ar2_pipeline():
    priors_path = 'priors_ROnly.csv'
    filter_path = 'filter_info_ROnly.csv'
    data_path = 'files_input_ROnly.csv'

    ar2 = AdvancedRetriever2(data_path, priors_path, filter_path)

    return ar2.run_pipeline_function()

def test_ar2_pipeline_full_write():
    priors_path = 'priors_ROnly.csv'
    filter_path = 'filter_info_ROnly.csv'
    data_path = 'files_input_ROnly.csv'

    ar2 = AdvancedRetriever2(data_path, priors_path, filter_path)

    return ar2.run_pipeline_full()
