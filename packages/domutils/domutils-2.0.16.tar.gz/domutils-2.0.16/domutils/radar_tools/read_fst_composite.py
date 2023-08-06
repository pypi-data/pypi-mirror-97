from typing import Callable, Iterator, Union, Optional, List, Iterable, MutableMapping

def read_fst_composite(fst_file:   str=None,
                       latlon:     Optional[bool] = False,
                       no_data:    Optional[float]= -9999.,
                       undetect:   Optional[float]= -3333.,
                       verbose:    Optional[int]  = 0) :

    """ Read reflectivity or precip_rate from CMC *standard* files
        

    Validity date is obtained via the *datev* attribute of the entry in the standard file being 
    read.
    Quality index is set to 1 wherever data is not missing



    Args:
        fst_file:        /path/to/fst/composite.std .stnd .fst or no 'extention'
        latlon:          When true, will output latitudes and longitudes
        no_data:         Value that will be assigned to missing values
        undetect:        Value that will be assigned to valid measurement of no precipitation

    Returns:
        None:            If no or invalid file present

        or 

        { 
            'reflectivity':       (ndarray) 2D reflectivity

            'total_quality_index':  (ndarray) 2D quality index

            'valid_date':          (python datetime object) date of validity

            'latitudes':          (ndarray) 2d latitudes  of data (conditional on latlon = True)

            'longitudes':         (ndarray) 2d longitudes of data (conditional on latlon = True)
        }

    Example:

           >>> #read fst file
           >>> import os, inspect
           >>> import domutils.radar_tools as radar_tools
           >>> currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
           >>> parentdir = os.path.dirname(currentdir) #directory where this package lives
           >>> out_dict = radar_tools.read_fst_composite(parentdir + '/test_data/std_radar_mosaics/2019103116_30ref_4.0km.stnd')
           >>> reflectivity        = out_dict['reflectivity']
           >>> total_quality_index = out_dict['total_quality_index']
           >>> valid_date          = out_dict['valid_date']
           >>> print(reflectivity.shape)
           (1650, 1500)
           >>> print(valid_date)
           2019-10-31 16:30:00+00:00


    """
    import os
    import datetime
    import logging
    import time
    import numpy as np
    from rpnpy.rpndate import RPNDate
    import os,sys,inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir) 
    import domcmc.fst_tools as fst_tools

    #logging
    logger = logging.getLogger(__name__)

    if verbose > 0:
        logger.warning('verbose keyword is deprecated, please set logging level in calling handler')

    #checks that filename was provided and is valid
    if fst_file is None :
        raise ValueError('fst_file must be provided')
    else :
        if not os.path.isfile(fst_file) :
            #no file present print warning and return None
            logger.warning('fst_file: ' + fst_file + ' does not exist. Returning None')
            return None

    qty_list = ['pr',   'ref',  'ref',  'ref']
    var_list = ['RDPR', 'RDBZ', 'RDBR', 'L1' ]
    #attempt to read to following variables stop when one is found
    for this_var in var_list:
        fst_dict = fst_tools.get_data(file_name=fst_file,
                                      var_name=this_var,
                                      latlon=latlon)
        if fst_dict is not None:
            break
    #nothing was found
    if fst_dict is None:
        logger.warning('Did not find reflectivity or precipitation rates in file:')
        logger.warning(fst_file)
        logger.warning('searched for: '+ str(var_list))
        logger.warning('returning None')
        return None
    values = fst_dict['values']

    #make datestamp for output
    datev = fst_dict['meta']['datev']
    date_obj = RPNDate(datev)
    valid_date = date_obj.toDateTime()

    #missing and undetect depend on how data was encoded in fst file, this is very annoying...
    if this_var == 'RDPR':
        #precipitation rate with quality index available

        #get quality index
        qi_dict = fst_tools.get_data(file_name=fst_file,
                                     var_name='RDQI')
        if qi_dict is not None:
            total_quality_index = qi_dict['values']
        else:
            logger.warning('RDQI not found, filling everything with ones')
            total_quality_index = np.ones_like(values)

        #constructuct output dictionary
        out_dict = {'precip_rate':          values,
                    'total_quality_index':  total_quality_index,
                    'valid_date':           valid_date}

    else:
        #reflectivity; quality ndex not available
        if this_var == 'RDBZ':
            missing_fst  = -999.
            undetect_fst = -99.
        if this_var == 'RDBR':
            missing_fst  = -999.
            undetect_fst = -99.
        if this_var == 'L1':
            missing_fst  = -10.
            undetect_fst = 0.

        #mark missing data to user defined no_data value
        missing_pts = np.isclose(values, missing_fst ).nonzero()
        if missing_pts[0].size > 0:
            values[missing_pts] = no_data

        #construct a fake quality index = 1 wherever we have data or undetect
        total_quality_index = np.ones_like(values)
        if missing_pts[0].size > 0:
            total_quality_index[missing_pts] = 0.

        #mark undetect to user defined undetect
        undetect_pts = np.isclose(values, undetect_fst ).nonzero()
        if undetect_pts[0].size > 0:
            values[undetect_pts] = undetect

        #constructuct output dictionary
        out_dict = {'reflectivity':         values,
                    'total_quality_index':  total_quality_index,
                    'valid_date':           valid_date}

    if latlon : 
        out_dict['latitudes']  = fst_dict['lat']
        out_dict['longitudes'] = fst_dict['lon']

    return out_dict
           
