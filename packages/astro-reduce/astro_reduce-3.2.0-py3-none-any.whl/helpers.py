'''helpers module for astro_reduce -- UI constants and handy functions.'''

from hashlib import md5
from json import dump
from os.path import basename
from re import sub

import click
import matplotlib.colors as colors
import numpy as np
from astropy.io import fits
from astropy.visualization import ImageNormalize, ZScaleInterval


# List of all options.
OPT_LIST = ['setup', 'clear', 'interpolate', 'verbose', 'tmppng', 'redpng',
            'sex', 'psfex', 'sexagain']

# Comment for header keywords.
HC = 'Exposure time in seconds'

# Paths and extensions.
# User image directories.
UDARK = 'DARK'
UFLAT = 'FLAT'
UOBJ = 'ORIGINAL'

# Astro-reduce working directories.
OBJ = 'ar_objects'
DARK = 'ar_darks'
FLAT = 'ar_flats'
TMP = 'tmp'

# File names and extensions.
DI = 'dark'
FI = 'flat'
RED = 'reduced'
AUX = 'aux'

# Astromatic result directories.
SEX_RES = 'SEXRES'
PSFEX_RES = 'PSFRES'
SCAMP_RES = 'SCAMPRES'

# Astromatic configuration files.
AR = 'astro_reduce'
DATA = 'data'
T120_SEX = 't120.sex'
T120_PARAM = 't120.param'
T120_PSFEX = 't120.psfex'
T120_PARAMPSFEX = 't120.parampsfex'
DEFAULT_CONV = 'default.conv'

# Astromatic command templates.
SEX_TMP = 'sex {} -c {} -PARAMETERS_NAME {} -FILTER_NAME {} '\
        + '-CATALOG_NAME {}/{} '\
        + '-CHECKIMAGE_TYPE BACKGROUND,OBJECTS '\
        + '-CHECKIMAGE_NAME {}/{},{}/{} -XML_NAME {}/{} '
PSFEX_TMP = 'psfex -c {} SEXRES/*-c.ldac -XML_NAME PSFRES/{} '\
    + '-CHECKIMAGE_TYPE CHI,PROTOTYPES,SAMPLES,RESIDUALS,SNAPSHOTS '\
    + '-CHECKIMAGE_NAME PSFRES/chi,PSFRES/proto,PSFRES/samp,PSFRES/resi,PSFRES/snap '\
    + '-CHECKPLOT_TYPE FWHM,ELLIPTICITY,COUNTS,COUNT_FRACTION,CHI2,RESIDUALS '\
    + '-CHECKPLOT_NAME PSFRES/fwhm,PSFRES/ellipticity,PSFRES/counts,PSFRES/countfrac,PSFRES/chi,PSFRES/resi '
SEXAGAIN_OPT_TMP = '-PSF_NAME PSFRES/{} '

# Simple hashing function for file names.
hsh = lambda x: md5(x.encode('utf-8')).hexdigest()

def dark_read_header(fname):
    '''Return exposure and standard file name for a dark field image.'''
    head = fits.getheader(fname)
    if 'EXPTIME' in head.keys():
        exp = int(1000 * head['EXPTIME'])
    elif 'EXPOSURE' in head.keys():
        exp = int(1000 * head['EXPOSURE'])
    elif 'EXP (MS)' in head.keys():
        exp = int(head['EXP (MS)'])
    else:
        raise IOError('No exposure keyword in header of `{}`.'.format(fname))
    return exp, '{}_{}_{}.fits'.format(DI, exp, hsh(fname))


def flat_read_header(fname):
    '''Return filter, exposure, standard file name for a flat field image.'''
    head = fits.getheader(fname)
    # Filter.
    if 'FILTER' in head.keys():
        fil = sub('[- _]', '', head['FILTER'])
    else:
        raise IOError('No filter keyword in header of `{}`.'.format(fname))

    # Exposure.
    if 'EXPTIME' in head.keys():
        exp = int(1000 * head['EXPTIME'])
    elif 'EXPOSURE' in head.keys():
        exp = int(1000 * head['EXPOSURE'])
    elif 'EXP (MS)' in head.keys():
        exp = int(head['EXP (MS)'])
    else:
        raise IOError('No exposure keyword in header of `{}`.'.format(fname))

    return fil, exp, '{}_{}_{}_{}.fits'.format(FI, fil, exp, hsh(fname))


def obj_read_header(fname):
    '''Return object, filter, exposure and standard file name for object image.
    '''
    # Add flag to only warn once for empty object names.
    if 'warn_flag' not in obj_read_header.__dict__:
        obj_read_header.warn_flag = True

    # Retrieve object image header.
    head = fits.getheader(fname)

    # Object.
    if 'OBJECT' in head.keys():
        obj = sub('[ _]', '-', head['OBJECT'])
    else:
        raise IOError('No object keyword in header of `{}`.'.format(fname))

    # Warn for empty object name.
    if obj == '' and obj_read_header.warn_flag:
        click.secho('\nW: The object keyword in file `{}` and similar is empty.'
                    '\nW: Undefined behavior.'.format(fname), fg='magenta')
        obj_read_header.warn_flag = False

    # Filter.
    if 'FILTER' in head.keys():
        fil = sub('[- _]', '', head['FILTER'])
    else:
        raise IOError('No filter keyword in header of `{}`.'.format(fname))

    # Exposure.
    if 'EXPTIME' in head.keys():
        exp = int(1000 * head['EXPTIME'])
    elif 'EXPOSURE' in head.keys():
        exp = int(1000 * head['EXPOSURE'])
    elif 'EXP (MS)' in head.keys():
        exp = int(head['EXP (MS)'])
    else:
        raise IOError('No exposure keyword in header of `{}`.'.format(fname))

    return obj, fil, exp, '{}_{}_{}_{}.fits'.format(obj, fil, exp, hsh(fname))


def write_conf_file(objects, exposures, filters, conf_file_name):
    '''Write configuration file from list of objects, exposures, filters.'''
    conf_dic = {'objects': objects,
                'exposures': exposures,
                'filters': filters}
    with open(conf_file_name, 'w') as cdfile:
        dump(conf_dic, cdfile, indent=2)


def fname_bits(fname):
    '''Return the filter and exposure from standard file name of an object.

    'NGC1000_V_1000_0.fits' gives ('V', '1000').
    '''
    pieces = fname.split('.fit')[0].split('_')
    return (pieces[-3], pieces[-2])


def write_png(fname, plt):
    '''Generate PNG version of image read in a fits file.

    Try to use a zscale normalization, and fall back to a classical
    linear scale between the min and max of 1000 randomly picked pixels of the
    image. Save the PNG image in same directory as the fits file.
    '''
    image = fits.getdata(fname)
    norm = ImageNormalize(image, ZScaleInterval())
    plt.figure(42)
    plt.imshow(image, norm=norm, cmap='jet')
    try:
        # If the zscale algorithm doesn't converge, an UnboundLocalError is
        # raised by astropy.visualization ...
        plt.colorbar()
    except UnboundLocalError:
        # ... in this case, just pick 1000 random pixels and linearly scale
        # between them.
        plt.clf()
        sample = np.random.choice(image.ravel(), 1000)
        norm = colors.Normalize(np.min(sample), np.max(sample), clip=True)
        plt.imshow(image, norm=norm, cmap='jet')
        plt.colorbar()
    plt.title(basename(fname).split('.fit')[0])
    plt.savefig('{}.png'.format(fname.split('.fit')[0]), bbox_inches='tight')
    plt.close(42)
