# Required packages: NetCDF4, xarray, dask[complete], pydap, lxml, requests
import xarray as xr
from pydap.cas.get_cookies import setup_session as cas_setup
from pydap.cas.urs import setup_session as urs_setup
from pydap.cas.esgf import setup_session as esfg_setup
import datetime


class ReturnCode():
    none = 0
    success = 1
    request_error = 2
    no_dataset = 3
    no_metadata = 4
    invalid_var = 5
    no_data = 6
    save_fail = 7


class AuthType():
    none = 0
    urs = 1
    cas = 2
    esgf = 3


# Textual versions of AuthType properties
AuthTypes = ['none', 'URS', 'CAS', 'ESGF']


# Metadata structure:
# {
#     'vars': {
#         'sst': {
#             'dims': ['time', 'lat', 'lon'],
#             'shape': [1857, 89, 180],
#             'size': 8
#         }
#         'pr': {
#             'dims': ['time', 'lat', 'lon'],
#             'shape': [1857, 89, 180],
#             'size': 8
#         }
#     },
#     'dims': {'time': [list of values], 'lat': [list of values], 'lon': [list of values]}
# }


class OpeNDAPRequest:
    def __init__(self):
        xr.set_options(keep_attrs=True)
        self._dataset = xr.Dataset()
        self._metadata = {}


    def _reset_dataset(self):
        #self._dataset.close()
        self._dataset = xr.Dataset()
        self._metadata = {}


    def _has_dataset(self):
        return len(self._dataset) > 0


    def _has_metadata(self):
        return len(self._metadata) > 0


    def close(self):
        '''
        Closes/resets internal xarray Dataset
        '''
        self._reset_dataset()


    def make_request(self, auth_type=AuthType.none, base_url='', userid=None,
            password=None, auth_url=None):
        '''
        Makes initial request for OpeNDAP request
        Params:
            auth_type (AuthType property)   One of available authorization types
            base_url (str)                  Base url for request
            userid (str)                    Optional userid
            password (str)                  Optional password
            auth_url (str)                  Optional authorization url such as
                                                an OpenID url
        Returns:
            dict    Form: {'return_code': ReturnCode property, 'error': content of Exception str}
        '''
        self._reset_dataset()
        try:
            # https://www.pydap.org/en/latest/client.html#authentication
            # https://github.com/pydata/xarray/issues/1068
            if auth_type == AuthType.urs:
                session = urs_setup(username=userid, password=password, check_url=base_url)
                store = xr.backends.PydapDataStore.open(base_url, session=session)
                self._dataset = xr.open_dataset(store)
            elif auth_type == AuthType.cas:
                session = cas_setup(uri=auth_url, username=userid, password=password)
                store = xr.backends.PydapDataStore.open(base_url, session=session)
                self._dataset = xr.open_dataset(store)
            elif auth_type == AuthType.esgf:
                if userid:
                    session = esfg_setup(openid=auth_url, password=password, username=userid, check_url=base_url)
                else:
                    session = esfg_setup(openid=auth_url, password=password, check_url=base_url)
                store = xr.backends.PydapDataStore.open(base_url, session=session)
                self._dataset = xr.open_dataset(store)
            else: # None
                self._dataset = xr.open_dataset(base_url)
            if not self._has_dataset():
                return {'return_code': ReturnCode.no_dataset, 'error': 'No dataset retrieved'}
        except Exception as err:
            return {'return_code': ReturnCode.request_error, 'error': str(err)}

        vars = {}
        dims = {}
        for dv_name in self._dataset.data_vars:
            dim_names = list(self._dataset.data_vars[dv_name].dims)
            n = len(dim_names)
            if n < 3 or n > 4:
                continue
            shape = list(self._dataset.data_vars[dv_name].shape)
            size = self._dataset.data_vars[dv_name].dtype.itemsize
            vars[dv_name] = {'dims': dim_names, 'shape': shape, 'size': size}
            for dim_name in dim_names:
                if not dim_name in dims.keys():
                    data_list = self._dataset[dim_name].astype(str).data.tolist()
                    dims[dim_name] = data_list
        if not len(vars) or not len(dims):
            return {'return_code': ReturnCode.no_metadata, 'error': 'No metadata retrieved'}
        self._metadata = {'vars': vars, 'dims': dims}
        return {'return_code': ReturnCode.success, 'error': ''}


    def get_vars(self):
        '''
        Returns a list of data variable names
        Params:
            None

        Returns:
            list   Form: ['sst', 'pr']
        '''
        if not 'vars' in self._metadata.keys():
            return []
        return list(self._metadata['vars'].keys())


    def get_info_for_var(self, var):
        '''
        Returns a dict of properties for specified data variable
        Params:
            None

        Returns:
            dict    Form: {'dims': ['time', 'lat', 'lon'], 'shape': [1857, 89, 180], 'size': 8}
        '''
        if not 'vars' in self._metadata.keys():
            return {}
        if not var in self._metadata['vars'].keys():
            return {}
        return self._metadata['vars'][var]


    def get_dims_for_var(self, var):
        if not 'vars' in self._metadata.keys():
            return {}
        if not var in self._metadata['vars'].keys():
            return {}
        dims = {}
        for dim_name in self._metadata['vars'][var]['dims']:
            dims[dim_name] = self._metadata['dims'][dim_name]
        return dims


    def save_var(self, var, constraints={}, file=''):
        '''
        Saves selected data variable for OpeNDAP request to file
        Params:
            constraints (dict)  Dimensional constraints for the data variable. See below
            file (str)          Full path and file name to save selected data variable to
        Returns:
            dict    Form: {'return_code': ReturnCode property, 'error': content of Exception str}

        About the `constraints` parameter:
            It is a dict where each key is the name of a dimension associated with the
            data variable. For each key, there is a 2-item list of `from` and `to` values.
            For example:
                {'time': ['2019-01-01", '2019-01-01'], 'lat': [30, 45], 'lon': [15, 90]}
        '''
        da = xr.DataArray()
        if not self._has_dataset():
            return (ReturnCode.no_dataset, da)
        if not var in self._dataset.data_vars:
            return (ReturnCode.invalid_var, da)
        slices = {}
        for key in constraints:
            try:
                slices[key] = slice(float(constraints[key][0]), float(constraints[key][1]))
            except:
                slices[key] = slice(constraints[key][0], constraints[key][1])
        da = self._dataset[var].sel(slices)
        if len(da):
            ds = xr.Dataset(attrs=self._dataset.attrs)
            ds[da.name] = da
            add_to_history(ds, 'Downloaded via OpeNDAP')
            encodings = get_to_netcdf_encodings(ds, comp_level=4)
            try:
                ds.to_netcdf(path=file, engine='netcdf4', encoding=encodings)
                return {'return_code': ReturnCode.success, 'error': ''}
            except Exception as err:
                return {'return_code': ReturnCode.save_fail, 'error': str(err)}
        else:
            return {'return_code': ReturnCode.no_data, 'error': ''}


#==========
# Utility functions
#==========

def get_to_netcdf_encodings(ds, comp_level=None):
    '''
    Returns default encodings for an xarray Dataset for
    use with Dataset::to_netcdf() method
    Parameters:
        ds          xarray Dataset
        comp_level  Level of compression: 0-9. If 0 no compression.
                    Compression starts with 1.
                    If None, then leave it up to xarray to decide.
    '''
    # A bit convoluted byt allows for adding new encodings in future
    # Merges two dicts of dicts based on keys in dict1
    def merge(dict1, dict2):
        for key in dict1:
            if key in dict2:
                dict1[key].update(dict2[key])
        return dict1

    # Map from Python datatype to default NetCDF _FillValue
    # See netCDF4.default_fillvals
    fillvalue_map = {
        'int8': -127, # i1
        'uint8': 255, # u1
        'int16': -32767, # i2
        'uint16': 65535, # u2
        'int32': -2147483647, # i4
        'uint32': 4294967295, # u4
        'int64': -9223372036854775806, # i8
        'uint64': 18446744073709551614, # u8
        'float32': 9.969209968386869e+36, # f4
        'float64': 9.969209968386869e+36, # f8
        'str': '\x00' # S1
    }
    # Real compression levels used for NetCDF
    real_comp_levels = [1,2,3,4,5,6,7,8,9]

    # Set up a base dict with key for all variables in ds set to empty dicts
    enc_base = {var_name:  {} for var_name in ds.variables}
    enc_fv = {} # Encodings for _FillValue
    enc_cl = {} # Encodings for compression level

    # Iterate each variable > 2 dimensions
    for var_name in ds.data_vars:
        # _FillValue encodings
        # Meant to fix when xarray makes them Python nan which
        # we don't want
        if len(ds[var_name].dims) > 2:
            # Test if _FillValue already exists. If not, add to encoding
            # using default value for data type
            if not '_FillValue' in ds[var_name].attrs:
                def_fv = fillvalue_map[ds[var_name].dtype.name]
                enc_fv[var_name] = dict(_FillValue=def_fv)
            else:
                pass
        else:
            enc_fv[var_name] = dict(_FillValue=None)

        # Compression encodings
        if len(ds[var_name].dims) > 2:
            if comp_level in real_comp_levels:
                enc_cl[var_name] = dict(zlib=True, complevel=comp_level)
            elif comp_level == 0:
                enc_cl[var_name] = dict(zlib=False)
            else:
                pass
        else:
            pass
    # Merge the dictionaries and return the merged one
    merged = merge(enc_base, enc_fv)
    merged = merge(merged, enc_cl)
    return merged


def add_to_history(ds, txt='', prepend=True):
    '''
    Adds text to `history` attribute for xarray Dataset
    '''
    hist = ''
    dt = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
    if 'history' in ds.attrs:
        hist = ds.attrs['history']
        hist = hist.strip('\n')
    if prepend is True:
        hist = dt + ' ' + txt + '\n' + hist
    else:
        hist = hist + '\n' + dt + ' ' + txt
    ds.attrs['history'] = hist
