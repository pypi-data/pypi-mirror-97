
"""
This module is the geometrical part of the ToFu general package
It includes all functions and object classes necessary for tomography on Tokamaks
"""

# Built-in
import sys
import os
import warnings
import copy


# Common
import numpy as np
import scipy.interpolate as scpinterp
import datetime as dtm
import matplotlib.pyplot as plt
import matplotlib as mpl

# ToFu-specific
from tofu import __version__ as __version__
import tofu.pathfile as tfpf
import tofu.utils as utils
try:
    import tofu.geom._def as _def
    import tofu.geom._GG as _GG
    import tofu.geom._comp_optics as _comp_optics
    import tofu.geom._plot_optics as _plot_optics
except Exception:
    from . import _def as _def
    from . import _GG as _GG
    from . import _comp_optics as _comp_optics
    from . import _plot_optics as _plot_optics



__all__ = ['CrystalBragg']



_Type = 'Tor'
_NTHREADS = 16

# rotate / translate instance
_RETURN_COPY = False

"""
###############################################################################
###############################################################################
                        Ves class and functions
###############################################################################
"""



class CrystalBragg(utils.ToFuObject):
    """ A class defining crystals for Bragg diffraction

    A crystal can be of Type flat, cylindrical or spherical
    It is characterized by its:
        - geometry (Type, dimensions, curvature radii and position/orientation)
        - Material and lattice
        - Bragg parameters (angle vs lambda)


    Parameters
    ----------
    Id :            str / tfpf.ID
        A name string or a pre-built tfpf.ID class to be used to identify this
        particular instance, if a string is provided, it is fed to tfpf.ID()
    dgeom :         dict
        An array (2,N) or (N,2) defining the contour of the vacuum vessel in a
        cross-section, if not closed, will be closed automatically
     dspectral:     str
        Flag indicating whether the vessel will be a torus ('Tor') or a linear
        device ('Lin')
    SavePath :      None / str
        If provided, forces the default saving path of the object to the
        provided value

    """

    # Fixed (class-wise) dictionary of default properties
    _ddef = {'Id':{'shot': 0, 'Exp': 'dummy', 'Diag': 'dummy',
                   'include':['Mod', 'Cls', 'Exp', 'Diag',
                              'Name', 'shot', 'version']},
             'dgeom':{'Type': 'sph', 'Typeoutline': 'rect'},
             'dmat':{},
             'dbragg':{},
             'dmisc':{'color':'k'}}
    _dplot = {'cross':{'Elt':'P',
                       'dP':{'color':'k','lw':2},
                       'dI':{'color':'k','ls':'--','marker':'x','ms':8,'mew':2},
                       'dBs':{'color':'b','ls':'--','marker':'x','ms':8,'mew':2},
                       'dBv':{'color':'g','ls':'--','marker':'x','ms':8,'mew':2},
                       'dVect':{'color':'r','scale':10}},
              'hor':{'Elt':'P',
                     'dP':{'color':'k','lw':2},
                     'dI':{'color':'k','ls':'--'},
                     'dBs':{'color':'b','ls':'--'},
                     'dBv':{'color':'g','ls':'--'},
                     'Nstep':50},
              '3d':{}}
    _DEFLAMB = 3.971561e-10
    _DEFNPEAKS = 12
    # _DREFLECT_DTYPES = {'specular':0, 'diffusive':1, 'ccube':2}


    # Does not exist beofre Python 3.6 !!!
    def __init_subclass__(cls, color='k', **kwdargs):
        # Python 2
        super(CrystalBragg,cls).__init_subclass__(**kwdargs)
        # Python 3
        #super().__init_subclass__(**kwdargs)
        cls._ddef = copy.deepcopy(CrystalBragg._ddef)
        cls._dplot = copy.deepcopy(CrystalBragg._dplot)
        cls._set_color_ddef(cls._color)

    @classmethod
    def _set_color_ddef(cls, color):
        cls._ddef['dmisc']['color'] = mpl.colors.to_rgba(color)

    def __init__(self, dgeom=None, dmat=None, dbragg=None,
                 Id=None, Name=None, Exp=None, Diag=None, shot=None,
                 fromdict=None, sep=None,
                 SavePath=os.path.abspath('./'),
                 SavePath_Include=tfpf.defInclude, color=None):

        # To replace __init_subclass__ for Python 2
        if sys.version[0]=='2':
            self._dstrip = utils.ToFuObjectBase._dstrip.copy()
            self.__class__._strip_init()

        # Create a dplot at instance level
        self._dplot = copy.deepcopy(self.__class__._dplot)

        kwdargs = locals()
        del kwdargs['self']
        # super()
        super(CrystalBragg,self).__init__(**kwdargs)

    def _reset(self):
        # super()
        super(CrystalBragg,self)._reset()
        self._dgeom = dict.fromkeys(self._get_keys_dgeom())
        self._dmat = dict.fromkeys(self._get_keys_dmat())
        self._dbragg = dict.fromkeys(self._get_keys_dbragg())
        self._dmisc = dict.fromkeys(self._get_keys_dmisc())
        #self._dplot = copy.deepcopy(self.__class__._ddef['dplot'])

    @classmethod
    def _checkformat_inputs_Id(cls, Id=None, Name=None,
                               Exp=None, Diag=None, shot=None, Type=None,
                               include=None,
                               **kwdargs):
        if Id is not None:
            assert isinstance(Id,utils.ID)
            Name, Exp, Type = Id.Name, Id.Exp, Id.Type
        if Type is None:
            Type = cls._ddef['dgeom']['Type']
        if Exp is None:
            Exp = cls._ddef['Id']['Exp']
        if Diag is None:
            Diag = cls._ddef['Id']['Diag']
        if shot is None:
            shot = cls._ddef['Id']['shot']
        if include is None:
            include = cls._ddef['Id']['include']

        dins = {'Name':{'var':Name, 'cls':str},
                'Exp': {'var':Exp, 'cls':str},
                'Diag': {'var':Diag, 'cls':str},
                'shot': {'var':shot, 'cls':int},
                'Type': {'var':Type, 'in':['sph']},
                'include':{'var':include, 'listof':str}}
        dins, err, msg = cls._check_InputsGeneric(dins)
        if err:
            raise Exception(msg)

        kwdargs.update({'Name':Name, 'shot':shot,
                        'Exp':Exp, 'Diag':Diag, 'Type':Type,
                        'include':include})
        return kwdargs

    ###########
    # Get largs
    ###########

    @staticmethod
    def _get_largs_dgeom(sino=True):
        largs = ['dgeom']
        return largs

    @staticmethod
    def _get_largs_dmat():
        largs = ['dmat']
        return largs

    @staticmethod
    def _get_largs_dbragg():
        largs = ['dbragg']
        return largs

    @staticmethod
    def _get_largs_dmisc():
        largs = ['color']
        return largs

    ###########
    # Get check and format inputs
    ###########

    @classmethod
    def _checkformat_dgeom(cls, dgeom=None):
        if dgeom is None:
            return
        assert isinstance(dgeom, dict)
        lkok = cls._get_keys_dgeom()
        assert all([isinstance(ss, str) and ss in lkok for ss in dgeom.keys()])
        for kk in cls._ddef['dgeom'].keys():
            dgeom[kk] = dgeom.get(kk, cls._ddef['dgeom'][kk])
        for kk in lkok:
            dgeom[kk] = dgeom.get(kk, None)
        if dgeom['center'] is not None:
            dgeom['center'] = np.atleast_1d(dgeom['center']).ravel()
            assert dgeom['center'].size == 3
        else:
            assert dgeom['summit'] is not None
            assert dgeom['rcurve'] is not None
        if dgeom['summit'] is not None:
            dgeom['summit'] = np.atleast_1d(dgeom['summit']).ravel()
            assert dgeom['summit'].size == 3
        else:
            assert dgeom['center'] is not None
            assert dgeom['rcurve'] is not None
        if dgeom['extenthalf'] is not None:
            dgeom['extenthalf'] = np.atleast_1d(dgeom['extenthalf'])
            assert dgeom['extenthalf'].size == 2
        if dgeom['rcurve'] is not None:
            dgeom['rcurve'] = float(dgeom['rcurve'])
        if dgeom['nout'] is not None:
            dgeom['nout'] = np.atleast_1d(dgeom['nout'])
            dgeom['nout'] = dgeom['nout'] / np.linalg.norm(dgeom['nout'])
            assert dgeom['nout'].size == 3
        if dgeom['nin'] is not None:
            dgeom['nin'] = np.atleast_1d(dgeom['nin'])
            dgeom['nin'] = dgeom['nin'] / np.linalg.norm(dgeom['nin'])
            assert dgeom['nin'].size == 3
        if dgeom['e1'] is not None:
            dgeom['e1'] = np.atleast_1d(dgeom['e1'])
            dgeom['e1'] = dgeom['e1'] / np.linalg.norm(dgeom['e1'])
            assert dgeom['e1'].size == 3
            assert dgeom['e2'] is not None
        if dgeom['e2'] is not None:
            dgeom['e2'] = np.atleast_1d(dgeom['e2'])
            dgeom['e2'] = dgeom['e2'] / np.linalg.norm(dgeom['e2'])
            assert dgeom['e2'].size == 3
        if dgeom['e1'] is not None:
            assert np.abs(np.sum(dgeom['e1']*dgeom['e2'])) < 1.e-12
            if dgeom['nout'] is not None:
                assert np.abs(np.sum(dgeom['e1']*dgeom['nout'])) < 1.e-12
                assert np.abs(np.sum(dgeom['e2']*dgeom['nout'])) < 1.e-12
                assert np.linalg.norm(np.cross(dgeom['e1'], dgeom['e2'])
                                      - dgeom['nout']) < 1.e-12
            if dgeom['nin'] is not None:
                assert np.abs(np.sum(dgeom['e1']*dgeom['nin'])) < 1.e-12
                assert np.abs(np.sum(dgeom['e2']*dgeom['nin'])) < 1.e-12
                assert np.linalg.norm(np.cross(dgeom['e1'], dgeom['e2'])
                                      + dgeom['nin']) < 1.e-12
        return dgeom

    @classmethod
    def _checkformat_dmat(cls, dmat=None):
        if dmat is None:
            return
        assert isinstance(dmat, dict)
        lkok = cls._get_keys_dmat()
        assert all([isinstance(ss, str) for ss in dmat.keys()])
        assert all([ss in lkok for ss in dmat.keys()])
        for kk in cls._ddef['dmat'].keys():
            dmat[kk] = dmat.get(kk, cls._ddef['dmat'][kk])
        if dmat.get('d') is not None:
            dmat['d'] = float(dmat['d'])
        if dmat.get('formula') is not None:
            assert isinstance(dmat['formula'], str)
        if dmat.get('density') is not None:
            dmat['density'] = float(dmat['density'])
        if dmat.get('lengths') is not None:
            dmat['lengths'] = np.atleast_1d(dmat['lengths']).ravel()
        if dmat.get('angles') is not None:
            dmat['angles'] = np.atleast_1d(dmat['angles']).ravel()
        if dmat.get('cut') is not None:
            dmat['cut'] = np.atleast_1d(dmat['cut']).ravel().astype(int)
            assert dmat['cut'].size <= 4
        return dmat

    @classmethod
    def _checkformat_dbragg(cls, dbragg=None):
        if dbragg is None:
            return
        assert isinstance(dbragg, dict)
        lkok = cls._get_keys_dbragg()
        assert all([isinstance(ss, str) for ss in dbragg.keys()])
        assert all([ss in lkok for ss in dbragg.keys()])

        for kk in cls._ddef['dbragg'].keys():
            dbragg[kk] = dbragg.get(kk, cls._ddef['dbragg'][kk])
        if dbragg.get('rockingcurve') is not None:
            assert isinstance(dbragg['rockingcurve'], dict)
            drock = dbragg['rockingcurve']
            lkeyok = ['sigam', 'deltad', 'Rmax', 'dangle', 'lamb', 'value',
                      'type', 'source']
            lkout = [kk for kk in drock.keys() if kk not in lkeyok]
            if len(lkout) > 0:
                msg = ("Unauthorized keys in dbrag['rockingcurve']:\n"
                       + "\t-" + "\n\t-".join(lkout))
                raise Exception(msg)
            try:
                if drock.get('sigma') is not None:
                    dbragg['rockingcurve']['sigma'] = float(drock['sigma'])
                    dbragg['rockingcurve']['deltad'] = float(
                        drock.get('deltad', 0.))
                    dbragg['rockingcurve']['Rmax'] = float(
                        drock.get('Rmax', 1.))
                    dbragg['rockingcurve']['type'] = 'lorentz-log'
                elif drock.get('dangle') is not None:
                    c2d = (drock.get('lamb') is not None
                           and drock.get('value').ndim == 2)
                    if c2d:
                        if drock['value'].shape != (drock['dangle'].size,
                                                    drock['lamb'].size):
                            msg = ("Tabulated 2d rocking curve should be:\n"
                                   + "\tshape = (dangle.size, lamb.size)")
                            raise Exception(msg)
                        dbragg['rockingcurve']['dangle'] = np.r_[
                            drock['dangle']]
                        dbragg['rockingcurve']['lamb'] = np.r_[drock['lamb']]
                        dbragg['rockingcurve']['value'] = drock['value']
                        dbragg['rockingcurve']['type'] = 'tabulated-2d'
                    else:
                        if drock.get('lamb') is None:
                            msg = ("Please also specify the lamb for which "
                                   + "the rocking curve was tabulated!")
                            raise Exception(msg)
                        dbragg['rockingcurve']['lamb'] = float(drock['lamb'])
                        dbragg['rockingcurve']['dangle'] = np.r_[
                            drock['dangle']]
                        dbragg['rockingcurve']['value'] = np.r_[drock['value']]
                        dbragg['rockingcurve']['type'] = 'tabulated-1d'
                    if drock.get('source') is None:
                        msg = "Unknonw source for the tabulated rocking curve!"
                        warnings.warn(msg)
                    dbragg['rockingcurve']['source'] = drock.get('source')
            except Exception as err:
                msg = ("Provide the rocking curve as a dict with either:\n"
                       + "\t- parameters of a lorentzian in log10:\n"
                       + "\t\t{'sigma': float,\n"
                       + "\t\t 'deltad': float,\n"
                       + "\t\t 'Rmax': float}\n"
                       + "\t- tabulated (dangle, value), with source (url...)"
                       + "\t\t{'dangle': np.ndarray,\n"
                       + "\t\t 'value': np.ndarray,\n"
                       + "\t\t 'source': str}")
                raise Exception(msg)
        return dbragg

    @classmethod
    def _checkformat_inputs_dmisc(cls, color=None):
        if color is None:
            color = mpl.colors.to_rgba(cls._ddef['dmisc']['color'])
        assert mpl.colors.is_color_like(color)
        return tuple(mpl.colors.to_rgba(color))

    ###########
    # Get keys of dictionnaries
    ###########

    @staticmethod
    def _get_keys_dgeom():
        lk = ['Type', 'Typeoutline',
              'summit', 'center', 'extenthalf', 'surface',
              'nin', 'nout', 'e1', 'e2', 'rcurve',
              'move', 'move_param', 'move_kwdargs']
        return lk

    @staticmethod
    def _get_keys_dmat():
        lk = ['formula', 'density', 'symmetry',
              'lengths', 'angles', 'cut', 'd']
        return lk

    @staticmethod
    def _get_keys_dbragg():
        lk = ['rockingcurve']
        return lk

    @staticmethod
    def _get_keys_dmisc():
        lk = ['color']
        return lk

    ###########
    # _init
    ###########

    def _init(self, dgeom=None, dmat=None, dbragg=None,
              color=None, **kwdargs):
        allkwds = dict(locals(), **kwdargs)
        largs = self._get_largs_dgeom()
        kwds = self._extract_kwdargs(allkwds, largs)
        self.set_dgeom(**kwds)
        largs = self._get_largs_dmat()
        kwds = self._extract_kwdargs(allkwds, largs)
        self.set_dmat(**kwds)
        largs = self._get_largs_dbragg()
        kwds = self._extract_kwdargs(allkwds, largs)
        self._set_dbragg(**kwds)
        largs = self._get_largs_dmisc()
        kwds = self._extract_kwdargs(allkwds, largs)
        self._set_dmisc(**kwds)
        self._dstrip['strip'] = 0

    ###########
    # set dictionaries
    ###########

    def set_dgeom(self, dgeom=None):
        dgeom = self._checkformat_dgeom(dgeom)
        if dgeom['e1'] is not None:
            if dgeom['nout'] is None:
                dgeom['nout'] = np.cross(dgeom['e1'], dgeom['e2'])
            if dgeom['nin'] is None:
                dgeom['nin'] = -dgeom['nout']
            if dgeom['center'] is None:
                dgeom['center'] = (dgeom['summit']
                                   + dgeom['nin']*dgeom['rcurve'])
            if dgeom['summit'] is None:
                dgeom['summit'] = (dgeom['center']
                                   + dgeom['nout']*dgeom['rcurve'])
        elif dgeom['center'] is not None and dgeom['summit'] is not None:
            if dgeom['nout'] is None:
                nout = (dgeom['summit'] - dgeom['center'])
                dgeom['nout'] = nout / np.linalg.norm(nout)

        if dgeom['extenthalf'] is not None:
            if dgeom['Type'] == 'sph' and dgeom['Typeoutline'] == 'rect':
                ind = np.argmax(dgeom['extenthalf'])
                dphi = dgeom['extenthalf'][ind]
                sindtheta = np.sin(dgeom['extenthalf'][ind-1])
                dgeom['surface'] = 4.*dgeom['rcurve']**2*dphi*sindtheta
        self._dgeom = dgeom
        if dgeom['move'] is not None:
            self.set_move(move=dgeom['move'], param=dgeom['move_param'],
                          **dgeom['move_kwdargs'])

    def set_dmat(self, dmat=None):
        dmat = self._checkformat_dmat(dmat)
        self._dmat = dmat

    def set_dbragg(self, dbragg=None):
        dbragg = self._checkformat_dbragg(dbragg)
        self._dbragg = dbragg

    def _set_color(self, color=None):
        color = self._checkformat_inputs_dmisc(color=color)
        self._dmisc['color'] = color
        self._dplot['cross']['dP']['color'] = color
        self._dplot['hor']['dP']['color'] = color
        # self._dplot['3d']['dP']['color'] = color

    def _set_dmisc(self, color=None):
        self._set_color(color)

    ###########
    # strip dictionaries
    ###########

    def _strip_dgeom(self, lkeep=None):
        lkeep = self._get_keys_dgeom()
        utils.ToFuObject._strip_dict(self._dgeom, lkeep=lkeep)

    def _strip_dmat(self, lkeep=None):
        lkeep = self._get_keys_dmat()
        utils.ToFuObject._strip_dict(self._dmat, lkeep=lkeep)

    def _strip_dbragg(self, lkeep=None):
        lkeep = self._get_keys_dbragg()
        utils.ToFuObject._strip_dict(self._dbragg, lkeep=lkeep)

    def _strip_dmisc(self, lkeep=['color']):
        utils.ToFuObject._strip_dict(self._dmisc, lkeep=lkeep)

    ###########
    # rebuild dictionaries
    ###########

    def _rebuild_dgeom(self, lkeep=None):
        lkeep = self._get_keys_dgeom()
        reset = utils.ToFuObject._test_Rebuild(self._dgeom, lkeep=lkeep)
        if reset:
            utils.ToFuObject._check_Fields4Rebuild(self._dgeom,
                                                   lkeep=lkeep, dname='dgeom')
            self._set_dgeom(dgeom=self._dgeom)

    def _rebuild_dmat(self, lkeep=None):
        lkeep = self._get_keys_dmat()
        reset = utils.ToFuObject._test_Rebuild(self._dmat, lkeep=lkeep)
        if reset:
            utils.ToFuObject._check_Fields4Rebuild(self._dmat,
                                                   lkeep=lkeep, dname='dmat')
            self.set_dmat(self._dmat)

    def _rebuild_dbragg(self, lkeep=None):
        lkeep = self._get_keys_dbragg()
        reset = utils.ToFuObject._test_Rebuild(self._dbragg, lkeep=lkeep)
        if reset:
            utils.ToFuObject._check_Fields4Rebuild(self._dbragg,
                                                   lkeep=lkeep, dname='dbragg')
            self.set_dbragg(self._dbragg)

    def _rebuild_dmisc(self, lkeep=['color']):
        reset = utils.ToFuObject._test_Rebuild(self._dmisc, lkeep=lkeep)
        if reset:
            utils.ToFuObject._check_Fields4Rebuild(self._dmisc,
                                                   lkeep=lkeep, dname='dmisc')
            self._set_dmisc(color=self.dmisc['color'])

    ###########
    # _strip and get/from dict
    ###########

    @classmethod
    def _strip_init(cls):
        cls._dstrip['allowed'] = [0,1]
        nMax = max(cls._dstrip['allowed'])
        doc = """
                 1: Remove nothing"""
        doc = utils.ToFuObjectBase.strip.__doc__.format(doc,nMax)
        if sys.version[0]=='2':
            cls.strip.__func__.__doc__ = doc
        else:
            cls.strip.__doc__ = doc

    def strip(self, strip=0):
        # super()
        super(CrystalBragg, self).strip(strip=strip)

    def _strip(self, strip=0):
        if strip==0:
            self._rebuild_dgeom()
            self._rebuild_dmat()
            self._rebuild_dbragg()
            self._rebuild_dmisc()
        else:
            self._strip_dgeom()
            self._strip_dmat()
            self._strip_dbragg()
            self._strip_dmisc()

    def _to_dict(self):
        dout = {'dgeom':{'dict':self._dgeom, 'lexcept':None},
                'dmat':{'dict':self._dmat, 'lexcept':None},
                'dbragg':{'dict':self._dbragg, 'lexcept':None},
                'dmisc':{'dict':self._dmisc, 'lexcept':None},
                'dplot':{'dict':self._dplot, 'lexcept':None}}
        return dout

    def _from_dict(self, fd):
        self._dgeom.update(**fd.get('dgeom', {}))
        self._dmat.update(**fd.get('dmat', {}))
        self._dbragg.update(**fd.get('dbragg', {}))
        self._dmisc.update(**fd.get('dmisc', {}))
        self._dplot.update(**fd.get('dplot', {}))

    # -----------
    # Properties
    # -----------

    @property
    def Type(self):
        """Return the type of structure """
        return self._Id.Type

    @property
    def dgeom(self):
        return self._dgeom

    @property
    def dmat(self):
        """Return the polygon defining the structure cross-section"""
        return self._dmat

    @property
    def dbragg(self):
        """Return the polygon defining the structure cross-section"""
        return self._dbragg

    @property
    def dmisc(self):
        return self._dmisc

    @property
    def nin(self):
        return self._dgeom['nin']

    @property
    def nout(self):
        return self._dgeom['nout']

    @property
    def e1(self):
        return self._dgeom['e1']

    @property
    def e2(self):
        return self._dgeom['e2']

    @property
    def summit(self):
        return self._dgeom['summit']

    @property
    def center(self):
        return self._dgeom['center']

    @property
    def rockingcurve(self):
        if self._dbragg.get('rockingcurve') is not None:
            if self._dbragg['rockingcurve'].get('type') is not None:
                return self._dbragg['rockingcurve']
        raise Exception("rockingcurve was not set!")

    # -----------------
    # methods for color
    # -----------------

    def set_color(self, col):
        self._set_color(col)

    def get_color(self):
        return self._dmisc['color']

    # -----------------
    # methods for printing
    # -----------------

    def get_summary(self, sep='  ', line='-', just='l',
                    table_sep=None, verb=True, return_=False):
        """ Summary description of the object content """

        # -----------------------
        # Build material
        col0 = ['formula', 'symmetry', 'cut', 'density',
                'd (A)', 'bragg({:7.4} A) (deg)'.format(self._DEFLAMB*1e10),
                'rocking curve']
        ar0 = [self._dmat['formula'], self._dmat['symmetry'],
               str(self._dmat['cut']), str(self._dmat['density']),
               '{0:5.3f}'.format(self._dmat['d']*1.e10),
               str(self.get_bragg_from_lamb(self._DEFLAMB)[0]*180./np.pi)]
        try:
            ar0.append(self.rockingcurve['type'])
        except Exception as err:
            ar0.append('None')


        # -----------------------
        # Build geometry
        col1 = ['Type', 'outline', 'surface (cm^2)', 'rcurve',
                'half-extent', 'summit', 'center', 'nin', 'e1']
        ar1 = [self._dgeom['Type'], self._dgeom['Typeoutline'],
               '{0:5.1f}'.format(self._dgeom['surface']*1.e4),
               '{0:5.2f}'.format(self._dgeom['rcurve']),
               str(np.round(self._dgeom['extenthalf'], decimals=3)),
               str(np.round(self._dgeom['summit'], decimals=2)),
               str(np.round(self._dgeom['center'], decimals=2)),
               str(np.round(self._dgeom['nin'], decimals=2)),
               str(np.round(self._dgeom['e1'], decimals=2))]
        if self._dgeom.get('move') not in [None, False]:
            col1 += ['move', 'param']
            ar1 += [self._dgeom['move'],
                    str(np.round(self._dgeom['move_param'], decimals=5))]

        if self._dmisc.get('color') is not None:
            col1.append('color')
            ar1.append(str(self._dmisc['color']))

        lcol = [col0, col1]
        lar = [ar0, ar1]
        return self._get_summary(lar, lcol,
                                  sep=sep, line=line, table_sep=table_sep,
                                  verb=verb, return_=return_)
    # -----------------
    # methods for moving
    # -----------------

    def _update_or_copy(self, dgeom, pinhole=None,
                        return_copy=None,
                        name=None, diag=None, shot=None):
        if return_copy is None:
            return_copy = _RETURN_COPY
        for kk, vv in self._dgeom.items():
            if kk not in dgeom.keys():
                dgeom[kk] = vv
        if return_copy is True:
            if name is None:
                name = self.Id.Name + 'copy'
            if diag is None:
                diag = self.Id.Diag
            if shot is None:
                diag = self.Id.shot
            return self.__class__(dgeom=dgeom,
                                  dbragg=self._dbragg,
                                  dmat=self._dmat,
                                  color=self._dmisc['color'],
                                  Exp=self.Id.Exp,
                                  Diag=diag,
                                  Name=name,
                                  shot=shot,
                                  SavePath=self.Id.SavePath)
        else:
            dgeom0 = self.dgeom
            try:
                self.set_dgeom(dgeom=dgeom)
            except Exception as err:
                # Make sure instance does not move
                self.set_dgeom(dgeom=dgeom0)
                msg = (str(err)
                       + "\nAn exception occured during updating\n"
                       + "  => instance unmoved")
                raise Exception(msg)

    def _rotate_or_translate(self, func, **kwdargs):
        pts = np.array([self._dgeom['summit'], self._dgeom['center']]).T
        if 'rotate' in func.__name__:
            vect = np.array([self._dgeom['nout'],
                             self._dgeom['e1'], self._dgeom['e2']]).T
            pts, vect = func(pts=pts, vect=vect, **kwdargs)
            return {'summit': pts[:, 0], 'center': pts[:, 1],
                    'nout': vect[:, 0], 'nin': -vect[:, 0],
                    'e1': vect[:, 1], 'e2': vect[:, 2]}
        else:
            pts = func(pts=pts, **kwdargs)
            return {'summit': pts[:, 0], 'center': pts[:, 1]}

    def translate_in_cross_section(self, distance=None, direction_rz=None,
                                   phi=None,
                                   return_copy=None,
                                   diag=None, name=None, shot=None):
        """ Translate the instance in the cross-section """
        if phi is None:
            phi = np.arctan2(*self.summit[1::-1])
            msg = ("Poloidal plane was not explicitely specified\n"
                   + "  => phi set to self.summit's phi ({})".format(phi))
            warnings.warn(msg)
        dgeom = self._rotate_or_translate(
            self._translate_pts_poloidal_plane,
            phi=phi, direction_rz=direction_rz, distance=distance)
        return self._update_or_copy(dgeom,
                                    return_copy=return_copy,
                                    diag=diag, name=name, shot=shot)

    def translate_3d(self, distance=None, direction=None,
                     return_copy=None,
                     diag=None, name=None, shot=None):
        """ Translate the instance in provided direction """
        dgeom = self._rotate_or_translate(
            self._translate_pts_3d,
            direction=direction, distance=distance)
        return self._update_or_copy(dgeom,
                                    return_copy=return_copy,
                                    diag=diag, name=name, shot=shot)

    def rotate_in_cross_section(self, angle=None, axis_rz=None,
                                phi=None,
                                return_copy=None,
                                diag=None, name=None, shot=None):
        """ Rotate the instance in the cross-section """
        if phi is None:
            phi = np.arctan2(*self.summit[1::-1])
            msg = ("Poloidal plane was not explicitely specified\n"
                   + "  => phi set to self.summit's phi ({})".format(phi))
            warnings.warn(msg)
        dgeom = self._rotate_or_translate(
            self._rotate_pts_vectors_in_poloidal_plane,
            axis_rz=axis_rz, angle=angle, phi=phi)
        return self._update_or_copy(dgeom,
                                    return_copy=return_copy,
                                    diag=diag, name=name, shot=shot)

    def rotate_around_torusaxis(self, angle=None,
                                return_copy=None,
                                diag=None, name=None, shot=None):
        """ Rotate the instance around the torus axis """
        dgeom = self._rotate_or_translate(
            self._rotate_pts_vectors_around_torusaxis,
            angle=angle)
        return self._update_or_copy(dgeom,
                                    return_copy=return_copy,
                                    diag=diag, name=name, shot=shot)

    def rotate_around_3daxis(self, angle=None, axis=None,
                             return_copy=None,
                             diag=None, name=None, shot=None):
        """ Rotate the instance around the provided 3d axis """
        dgeom = self._rotate_or_translate(
            self._rotate_pts_vectors_around_3daxis,
            axis=axis, angle=angle)
        return self._update_or_copy(dgeom,
                                    return_copy=return_copy,
                                    diag=diag, name=name, shot=shot)

    def set_move(self, move=None, param=None, **kwdargs):
        """ Set the default movement parameters

        A default movement can be set for the instance, it can be any of the
        pre-implemented movement (rotations or translations)
        This default movement is the one that will be called when using
        self.move()

        Specify the type of movement via the name of the method (passed as a
        str to move)

        Specify, for the geometry of the instance at the time of defining this
        default movement, the current value of the associated movement
        parameter (angle / distance). This is used to set an arbitrary
        difference for user who want to use absolute position values
        The desired incremental movement to be performed when calling self.move
        will be deduced by substracting the stored param value to the provided
        param value. Just set the current param value to 0 if you don't care
        about a custom absolute reference.

        kwdargs must be a parameters relevant to the chosen method (axis,
        direction...)

        e.g.:
            self.set_move(move='rotate_around_3daxis',
                          param=0.,
                          axis=([0.,0.,0.], [1.,0.,0.]))
            self.set_move(move='translate_3d',
                          param=0.,
                          direction=[0.,1.,0.])
        """
        move, param, kwdargs = self._checkformat_set_move(move, param, kwdargs)
        self._dgeom['move'] = move
        self._dgeom['move_param'] = param
        if isinstance(kwdargs, dict) and len(kwdargs) == 0:
            kwdargs = None
        self._dgeom['move_kwdargs'] = kwdargs

    def move(self, param):
        """ Set new position to desired param according to default movement

        Can only be used if default movement was set before
        See self.set_move()
        """
        param = self._move(param, dictname='_dgeom')
        self._dgeom['move_param'] = param


    # -----------------
    # methods for rocking curve
    # -----------------

    def get_rockingcurve_func(self, lamb=None, n=None):
        drock = self.rockingcurve
        if drock['type'] == 'tabulated-1d':
            if lamb is not None and lamb != drock['lamb']:
                msg = ("rocking curve was tabulated only for:\n"
                       + "\tlamb = {} m\n".format(lamb)
                       + "  => Please let lamb=None")
                raise Exception(msg)
            bragg = self._checkformat_bragglamb(lamb=drock['lamb'], n=n)
            func = scpinterp.interp1d(drock['dangle']+bragg, drock['value'],
                                      kind='linear', bounds_error=False,
                                      fill_value=0, assume_sorted=True)

        elif drock['type'] == 'tabulated-2d':
            lmin, lmax = drock['lamb'].min(), drock['lamb'].max()
            if lamb is None or lamb < lmin or lamb > lmax:
                msg = ("rocking curve was tabulated only in interval:\n"
                       + "\tlamb in [{}; {}] m\n".format(lmin, lmax)
                       + "  => Please set lamb accordingly")
                raise Exception(msg)
            bragg = self._checkformat_bragglamb(lamb=lamb, n=n)

            def func(angle, lamb=lamb, bragg=bragg, drock=drock):
                return scpinterp.interp2d(drock['dangle']+bragg, drock['lamb'],
                                          drock['value'], kind='linear',
                                          bounds_error=False, fill_value=0,
                                          assume_sorted=True)(angle, lamb)

        else:
            def func(angle, d=d, delta_bragg=delta_bragg,
                     Rmax=drock['Rmax'], sigma=drock['sigma']):
                core = sigma**2/((angle - (bragg+delta_bragg))**2 + sigma**2)
                if Rmax is None:
                    return core/(sigma*np.pi)
                else:
                    return Rmax*core
        return func

    def plot_rockingcurve(self, lamb=None,
                          fs=None, ax=None):
        drock = self.rockingcurve
        func = self.get_rockingcurve_func(bragg=bragg, n=n)
        return _plot_optics.CrystalBragg_plot_rockingcurve(func, fs=fs, ax=ax)

    # -----------------
    # methods for surface and contour sampling
    # -----------------

    def sample_outline_plot(self, res=None):
        if self._dgeom['Type'] == 'sph':
            if self._dgeom['Typeoutline'] == 'rect':
                func = _comp_optics.CrystBragg_sample_outline_plot_sphrect
                outline = func(self._dgeom['center'], self.dgeom['nout'],
                               self._dgeom['e1'], self._dgeom['e2'],
                               self._dgeom['rcurve'], self._dgeom['extenthalf'],
                               res)
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
        return outline

    def sample_outline_Rays(self, res=None):
        if self._dgeom['Type'] == 'sph':
            if self._dgeom['Typeoutline'] == 'rect':
                func = _comp_optics.CrystBragg_sample_outline_Rays
                pts, phi, theta = func()
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
        return outline



    # -----------------
    # methods for surface and contour sampling
    # -----------------

    def _checkformat_bragglamb(self, bragg=None, lamb=None, n=None):
        lc = [lamb is not None, bragg is not None]
        if not any(lc):
            lamb = self._DEFLAMB
            lc[0] = True
        assert np.sum(lc) == 1, "Provide lamb xor bragg!"
        if lc[0]:
            bragg = self.get_bragg_from_lamb(np.atleast_1d(lamb),
                                             n=n)
        else:
            bragg = np.atleast_1d(bragg)
        return bragg

    def _checkformat_get_Rays_from(self, phi=None, bragg=None):
        assert phi is not None
        assert bragg is not None
        bragg = np.atleast_1d(bragg)
        phi = np.atleast_1d(phi)
        nrays = max(phi.size, bragg.size)
        if not phi.shape == bragg.shape:
            if phi.size == 1:
                phi = np.full(bragg.shape, phi[0])
            elif bragg.size == 1:
                bragg = np.full(phi.shape, bragg[0])
            else:
                msg = "phi and bragg/lamb must have the same shape!\n"
                msg += "   phi.shape:        %s\n"%str(phi.shape)
                msg += "   bragg/lamb.shape: %s\n"%str(bragg.shape)
                raise Exception(msg)
        return phi, bragg

    def get_Rays_from_summit(self, phi=None, bragg=None,
                             lamb=None, n=None,
                             returnas=object, config=None, name=None):

        # Check inputs
        bragg = self._checkformat_bragglamb(bragg=bragg, lamb=lamb)
        phi, bragg = self._checkformat_get_Rays_from(phi=phi, bragg=bragg)
        # assert phi.ndim == 1
        phi = phi[None, ...]
        bragg = bragg[None, ...]

        # Prepare
        shape = tuple([3] + [1 for ii in range(phi.ndim)])
        nin = self._dgeom['nin'].reshape(shape)
        e1 = self._dgeom['e1'].reshape(shape)
        e2 = self._dgeom['e2'].reshape(shape)

        # Compute start point (D) and unit vectors (us)
        D = self._dgeom['summit']
        us = (np.sin(bragg)*nin
              + np.cos(bragg)*(np.cos(phi)*e1 + np.sin(phi)*e2))

        # Format output
        if returnas == tuple:
            return (D, us)
        elif returnas == object:
            from ._core import CamLOS1D
            if name is None:
                name = self.Id.Name + 'ExtractCam'
                if us.ndim > 2:
                    us = us.reshape((3, phi.size))
            return CamLOS1D(dgeom=(D, us), Name=name, Diag=self.Id.Diag,
                            Exp=self.Id.Exp, shot=self.Id.shot, config=config)

    def get_Rays_envelop(self,
                         phi=None, bragg=None, lamb=None, n=None,
                         returnas=object, config=None, name=None):
        # Check inputs
        phi, bragg = self._checkformat_get_Rays_from(phi=phi, bragg=bragg,
                                                     lamb=lamb, n=n)
        assert phi.ndim == 1

        # Compute
        func = _comp_optics.CrystBragg_sample_outline_Rays
        D, us = func(self._dgeom['center'], self._dgeom['nout'],
                     self._dgeom['e1'], self._dgeom['e2'],
                     self._dgeom['rcurve'], self._dgeom['extenthalf'],
                     bragg, phi)

        # Format output
        if returnas == tuple:
            return (D, us)
        elif returnas == object:
            from ._core import CamLOS1D
            if name is None:
                name = self.Id.Name + 'ExtractCam'
            return CamLOS1D(dgeom=(D, us), Name=name, Diag=self.Id.Diag,
                            Exp=self.Id.Exp, shot=self.Id.shot, config=config)



    # -----------------
    # methods for general plotting
    # -----------------

    def plot(self, lax=None, proj=None, res=None, element=None,
             color=None, det_cent=None,
             det_nout=None, det_ei=None, det_ej=None,
             dP=None, dI=None, dBs=None, dBv=None,
             dVect=None, dIHor=None, dBsHor=None,
             dBvHor=None, dleg=None,
             draw=True, fs=None, wintit=None, Test=True):
        kwdargs = locals()
        lout = ['self']
        for k in lout:
            del kwdargs[k]
        return _plot_optics.CrystalBragg_plot(self, **kwdargs)

    # -----------------
    # methods for generic first-approx
    # -----------------

    def get_phi_from_magaxis_summit(self, r, z, lamb=None, bragg=None, n=None):
        # Check / format input
        r = np.atleast_1d(r)
        z = np.atleast_1d(z)
        assert r.shape == z.shape
        bragg = self._checkformat_bragglamb(bragg=bragg, lamb=lamb, n=n)

        # Compute phi

        return phi



    def get_bragg_from_lamb(self, lamb, n=None):
        """ Braggs' law: n*lamb = 2dsin(bragg) """
        if self._dmat['d'] is None:
            msg = "Interplane distance d no set !\n"
            msg += "  => self.set_dmat({'d':...})"
            raise Exception(msg)
        return _comp_optics.get_bragg_from_lamb(np.atleast_1d(lamb),
                                                self._dmat['d'], n=n)

    def get_lamb_from_bragg(self, bragg, n=None):
        """ Braggs' law: n*lamb = 2dsin(bragg) """
        if self._dmat['d'] is None:
            msg = "Interplane distance d no set !\n"
            msg += "  => self.set_dmat({'d':...})"
            raise Exception(msg)
        return _comp_optics.get_lamb_from_bragg(np.atleast_1d(bragg),
                                                self._dmat['d'], n=n)

    def get_detector_approx(self, bragg=None, lamb=None,
                            rcurve=None, n=None,
                            ddist=None, di=None, dj=None,
                            dtheta=None, dpsi=None, tilt=None,
                            tangent_to_rowland=None, plot=False):
        """ Return approximate ideal detector geometry

        Assumes infinitesimal and ideal crystal
        Assumes detector center tangential to Rowland circle
        Assumes detector center matching lamb (m) / bragg (rad)

        Detector described by center position, and (nout, ei, ej) unit vectors
        By convention, nout = np.cross(ei, ej)
        Vectors (ei, ej) define an orthogonal frame in the detector's plane

        Return:
        -------
        det_cent:   np.ndarray
            (3,) array of (x, y, z) coordinates of detector center
        det_nout:   np.ndarray
            (3,) array of (x, y, z) coordinates of unit vector
                perpendicular to detector' surface
                oriented towards crystal
        det_ei:     np.ndarray
            (3,) array of (x, y, z) coordinates of unit vector
                defining first coordinate in detector's plane
        det_ej:     np.ndarray
            (3,) array of (x, y, z) coordinates of unit vector
                defining second coordinate in detector's plane
        """

        # Check / format inputs
        if rcurve is None:
            rcurve = self._dgeom['rcurve']
        bragg = self._checkformat_bragglamb(bragg=bragg, lamb=lamb, n=n)
        if np.all(np.isnan(bragg)):
            msg = ("There is no available bragg angle!\n"
                   + "  => Check the vlue of self.dmat['d'] vs lamb")
            raise Exception(msg)

        lf = ['summit', 'nout', 'e1', 'e2']
        lc = [rcurve is None] + [self._dgeom[kk] is None for kk in lf]
        if any(lc):
            msg = ("Some missing fields in dgeom for computation:"
                   + "\n\t-" + "\n\t-".join(['rcurve'] + lf))
            raise Exception(msg)

        # Compute crystal-centered parameters in (nout, e1, e2)
        func = _comp_optics.get_approx_detector_rel
        (det_dist, n_crystdet_rel,
         det_nout_rel, det_ei_rel) = _comp_optics.get_approx_detector_rel(
            rcurve, bragg, tangent_to_rowland=tangent_to_rowland)

        # Deduce absolute position in (x, y, z)
        det_cent, det_nout, det_ei, det_ej = _comp_optics.get_det_abs_from_rel(
            det_dist, n_crystdet_rel, det_nout_rel, det_ei_rel,
            self._dgeom['summit'],
            self._dgeom['nout'], self._dgeom['e1'], self._dgeom['e2'],
            ddist=ddist, di=di, dj=dj,
            dtheta=dtheta, dpsi=dpsi, tilt=tilt)

        if plot:
            dax = self.plot()
            p0 = np.repeat(det_cent[:,None], 3, axis=1)
            vv = np.vstack((det_nout, det_ei, det_ej)).T
            dax['cross'].plot(np.hypot(det_cent[0], det_cent[1]),
                              det_cent[2], 'xb')
            dax['hor'].plot(det_cent[0], det_cent[1], 'xb')
            dax['cross'].quiver(np.hypot(p0[0, :], p0[1, :]), p0[2, :],
                                np.hypot(vv[0, :], vv[1, :]), vv[2, :],
                                units='xy', color='b')
            dax['hor'].quiver(p0[0, :], p0[1, :], vv[0, :], vv[1, :],
                              units='xy', color='b')
        return det_cent, det_nout, det_ei, det_ej

    def get_local_noute1e2(self, theta, psi):
        """ Return (nout, e1, e2) associated to pts on the crystal's surface

        All points on the spherical crystal's surface are identified
            by (theta, psi) coordinates, where:
                - theta  = np.pi/2 for the center
                - psi = 0 for the center
            They are the spherical coordinates from a sphere centered on the
            crystal's center of curvature.

        Return the pts themselves and the 3 perpendicular unti vectors
            (nout, e1, e2), where nout is towards the outside of the sphere and
            nout = np.cross(e1, e2)

        Return:
        -------
        summit:     np.ndarray
            (3,) array of (x, y, z) coordinates of the points on the surface
        nout:       np.ndarray
            (3,) array of (x, y, z) coordinates of outward unit vector
        e1:         np.ndarray
            (3,) array of (x, y, z) coordinates of first unit vector
        e2:         np.ndarray
            (3,) array of (x, y, z) coordinates of second unit vector

        """
        if np.allclose([theta, psi], [np.pi/2., 0.]):
            summit = self._dgeom['summit']
            nout = self._dgeom['nout']
            e1, e2 = self._dgeom['e1'], self._dgeom['e2']
        else:
            func = _comp_optics.CrystBragg_get_noute1e2_from_psitheta
            nout, e1, e2 = func(self._dgeom['nout'],
                                self._dgeom['e1'], self._dgeom['e2'],
                                [psi], [theta])
            nout, e1, e2 = nout[:, 0], e1[:, 0], e2[:, 0]
            summit = self._dgeom['center'] + self._dgeom['rcurve']*nout
        return summit, nout, e1, e2


    def calc_xixj_from_phibragg(self, phi=None,
                                bragg=None, lamb=None, n=None,
                                theta=None, psi=None,
                                det_cent=None, det_nout=None,
                                det_ei=None, det_ej=None,
                                data=None, plot=True, ax=None):
        """ Assuming crystal's summit as frame origin

        According to [1], this assumes a local frame centered on the crystal

        These calculations are independent from the tokamak's frame:
            The origin of the local frame is the crystal's summit
            The (O, ez) axis is the crystal's normal
            The crystal is tangent to (O, ex, ey)

        [1] tofu/Notes_Upgrades/SpectroX2D/SpectroX2D_EllipsesOnPlane.pdf

        Parameters:
        -----------
        Z:      float
            Detector's plane intersection with (O, ez) axis
        n:      np.ndarray
            (3,) array containing local (x,y,z) coordinates of the plane's
            normal vector
        """
        # Check / format inputs
        bragg = self._checkformat_bragglamb(bragg=bragg, lamb=lamb, n=n)
        phi = np.atleast_1d(phi)
        assert bragg.ndim == phi.ndim == 1
        nphi, nbragg = phi.size, bragg.size
        npts = max(nphi, nbragg)
        assert nbragg in [1, npts] and nphi in [1, npts], (nbragg, nphi)
        if nbragg < npts:
            bragg = np.full((npts,), bragg[0])
        elif nphi < npts:
            phi = np.full((npts,), phi[0])

        lc = [det_cent is None, det_nout is None,
              det_ei is None, det_ej is None]
        assert all(lc) or not any(lc)
        if all(lc):
            func = self.get_detector_approx
            det_cent, det_nout, det_ei, det_ej = func(lamb=self._DEFLAMB)

        # Get local summit nout, e1, e2 if non-centered
        if theta is None:
            theta = np.pi/2.
        if psi is None:
            psi = 0.
        summit, nout, e1, e2 = self.get_local_noute1e2(theta, psi)

        # Compute
        xi, xj = _comp_optics.calc_xixj_from_braggphi(summit,
                                                      det_cent, det_nout,
                                                      det_ei, det_ej,
                                                      nout, e1, e2,
                                                      bragg, phi)
        if plot:
            func = _plot_optics.CrystalBragg_plot_approx_detector_params
            ax = func(bragg, xi, xj, data, ax)
        return xi, xj

    @staticmethod
    def _checkformat_pts(pts):
        pts = np.atleast_1d(pts)
        if pts.ndim == 1:
            pts = pts.reshape((3, 1))
        if 3 not in pts.shape or pts.ndim != 2:
            msg = "pts must be a (3, npts) array of (X, Y, Z) coordinates!"
            raise Exception(msg)
        if pts.shape[0] != 3:
            pts = pts.T
        return pts

    @staticmethod
    def _checkformat_xixj(xi, xj):
        xi = np.atleast_1d(xi)
        xj = np.atleast_1d(xj)

        if xi.shape == xj.shape:
            return xi, xj, (xi, xj)
        else:
            return xi, xj, np.meshgrid(xi, xj)

    @staticmethod
    def _checkformat_psidtheta(psi=None, dtheta=None,
                               psi_def=0., dtheta_def=0.):
        if psi is None:
            psi = psi_def
        if dtheta is None:
            dtheta = dtheta_def
        psi = np.r_[psi]
        dtheta = np.r_[dtheta]
        if psi.size != dtheta.size:
            msg = "psi and dtheta must be 1d arrays fo same size!"
            raise Exception(msg)


    def calc_phibragg_from_xixj(self, xi, xj, n=None,
                                det_cent=None, det_ei=None, det_ej=None,
                                dtheta=None, psi=None,
                                plot=True, ax=None, **kwdargs):

        # Check / format inputs
        xi, xj, (xii, xjj) = self._checkformat_xixj(xi, xj)

        lc = [det_cent is None, det_ei is None, det_ej is None]
        assert all(lc) or not any(lc)
        if all(lc):
            det_cent, _, det_ei, det_ej = self.get_detector_approx(
                lamb=self._DEFLAMB)

        # Get local summit nout, e1, e2 if non-centered
        bragg, phi = self.calc_phibragg_from_pts(pts)

        if plot != False:
            lax = _plot_optics.CrystalBragg_plot_braggangle_from_xixj(
                xi=xii, xj=xjj,
                ax=ax, plot=plot,
                bragg=bragg * 180./np.pi,
                angle=phi * 180./np.pi,
                braggunits='deg', angunits='deg', **kwdargs)
        return bragg, phi

    # DEPRECATED ???
    def calc_phibragg_from_pts_on_summit(self, pts, n=None):
        """ Return the bragg angle and phi of pts from crystal summit

        The pts are provided as a (x, y, z) coordinates array
        The bragg angle and phi are computed from the crystal's summit

        """
        # Check / format inputs
        pts = self._checkformat_pts(pts)

        # Compute
        vect = pts - self._dgeom['summit'][:, None]
        vect = vect / np.sqrt(np.sum(vect**2, axis=0))
        bragg = np.pi/2 - np.arccos(np.sum(vect*self._dgeom['nin'][:, None],
                                           axis=0))
        v1 = np.sum(vect*self._dgeom['e1'][:, None], axis=0)
        v2 = np.sum(vect*self._dgeom['e2'][:, None], axis=0)
        phi = np.arctan2(v2, v1)
        return bragg, phi

    def plot_line_tracing_on_det(self, lamb=None, n=None,
                                 xi_bounds=None, xj_bounds=None, nphi=None,
                                 det_cent=None, det_nout=None,
                                 det_ei=None, det_ej=None,
                                 johann=False, lpsi=None, ltheta=None,
                                 rocking=False, fs=None, dmargin=None,
                                 wintit=None, tit=None):
        """ Visualize the de-focusing by ray-tracing of chosen lamb
        """
        # Check / format inputs
        if lamb is None:
            lamb = self._DEFLAMB
        lamb = np.atleast_1d(lamb).ravel()
        nlamb = lamb.size

        det = np.array([[xi_bounds[0], xi_bounds[1], xi_bounds[1],
                         xi_bounds[0], xi_bounds[0]],
                        [xj_bounds[0], xj_bounds[0], xj_bounds[1],
                         xj_bounds[1], xj_bounds[0]]])

        # Compute lamb / phi
        _, phi = self.calc_phibragg_from_xixj(
            det[0, :], det[1, :], n=n,
            det_cent=det_cent, det_ei=det_ei, det_ej=det_ej,
            theta=None, psi=None, plot=False)
        phimin, phimax = np.nanmin(phi), np.nanmax(phi)
        phimin, phimax = phimin-(phimax-phimin)/10, phimax+(phimax-phimin)/10
        del phi

        # Get reference ray-tracing
        if nphi is None:
            nphi = 300
        phi = np.linspace(phimin, phimax, nphi)
        bragg = self._checkformat_bragglamb(lamb=lamb, n=n)

        xi = np.full((nlamb, nphi), np.nan)
        xj = np.full((nlamb, nphi), np.nan)
        for ll in range(nlamb):
            xi[ll, :], xj[ll, :] = self.calc_xixj_from_phibragg(
                bragg=bragg[ll], phi=phi, n=n,
                det_cent=det_cent, det_nout=det_nout,
                det_ei=det_ei, det_ej=det_ej, plot=False)

        # Get johann-error raytracing (multiple positions on crystal)
        xi_er, xj_er = None, None
        if johann and not rocking:
            if lpsi is None or ltheta is None:
                lpsi = np.linspace(-1., 1., 15)
                ltheta = np.linspace(-1., 1., 15)
                lpsi, ltheta = np.meshgrid(lpsi, ltheta)
                lpsi = lpsi.ravel()
                ltheta = ltheta.ravel()
            lpsi = self._dgeom['extenthalf'][0]*np.r_[lpsi]
            ltheta = np.pi/2 + self._dgeom['extenthalf'][1]*np.r_[ltheta]
            npsi = lpsi.size
            assert npsi == ltheta.size

            xi_er = np.full((nlamb, npsi*nphi), np.nan)
            xj_er = np.full((nlamb, npsi*nphi), np.nan)
            for l in range(nlamb):
                for ii in range(npsi):
                    i0 = np.arange(ii*nphi, (ii+1)*nphi)
                    xi_er[l, i0], xj_er[l, i0] = self.calc_xixj_from_phibragg(
                        phi=phi, bragg=bragg[l], lamb=None, n=n,
                        theta=ltheta[ii], psi=lpsi[ii],
                        det_cent=det_cent, det_nout=det_nout,
                        det_ei=det_ei, det_ej=det_ej, plot=False)

        # Get rocking curve error
        if rocking:
            pass

        # Plot
        ax = _plot_optics.CrystalBragg_plot_line_tracing_on_det(
            lamb, xi, xj, xi_er, xj_er, det=det,
            johann=johann, rocking=rocking,
            fs=fs, dmargin=dmargin, wintit=wintit, tit=tit)

    def calc_johannerror(self, xi=None, xj=None, err=None,
                         det_cent=None, det_ei=None, det_ej=None, n=None,
                         lpsi=None, ltheta=None,
                         plot=True, fs=None, cmap=None,
                         vmin=None, vmax=None, tit=None, wintit=None):
        """ Plot the johann error

        The johann error is the error (scattering) induced by defocalization
            due to finite crystal dimensions
        There is a johann error on wavelength (lamb => loss of spectral
            resolution) and on directionality (phi)
        If provided, lpsi and ltheta are taken as normalized variations with
            respect to the crystal summit and to its extenthalf.
            Typical values are:
                - lpsi   = [-1, 1, 1, -1]
                - ltheta = [-1, -1, 1, 1]
            They must have the same len()

        """

        # Check / format inputs
        xi, xj, (xii, xjj) = self._checkformat_xixj(xi, xj)
        nxi = xi.size if xi is not None else np.unique(xii).size
        nxj = xj.size if xj is not None else np.unique(xjj).size

        # Compute lamb / phi
        bragg, phi = self.calc_phibragg_from_xixj(
            xii, xjj, n=n,
            det_cent=det_cent, det_ei=det_ei, det_ej=det_ej,
            theta=None, psi=None, plot=False)
        assert bragg.shape == phi.shape
        lamb = self.get_lamb_from_bragg(bragg, n=n)

        if lpsi is None:
            lpsi = np.r_[-1., 0., 1., 1., 1., 0., -1, -1]
        lpsi = self._dgeom['extenthalf'][0]*np.r_[lpsi]
        if ltheta is None:
            ltheta = np.r_[-1., -1., -1., 0., 1., 1., 1., 0.]
        ltheta = np.pi/2 + self._dgeom['extenthalf'][1]*np.r_[ltheta]
        npsi = lpsi.size
        assert npsi == ltheta.size
        lamberr = np.full(tuple(np.r_[npsi, lamb.shape]), np.nan)
        phierr = np.full(lamberr.shape, np.nan)
        for ii in range(npsi):
            bragg, phierr[ii, ...] = self.calc_phibragg_from_xixj(
                xii, xjj, n=n,
                det_cent=det_cent, det_ei=det_ei, det_ej=det_ej,
                theta=ltheta[ii], psi=lpsi[ii], plot=False)
            lamberr[ii, ...] = self.get_lamb_from_bragg(bragg, n=n)
        err_lamb = np.nanmax(np.abs(lamb[None, ...] - lamberr), axis=0)
        err_phi = np.nanmax(np.abs(phi[None, ...] - phierr), axis=0)
        if plot is True:
            ax = _plot_optics.CrystalBragg_plot_johannerror(
                xi, xj, lamb, phi, err_lamb, err_phi, err=err,
                cmap=cmap, vmin=vmin, vmax=vmax, fs=fs, tit=tit, wintit=wintit)
        return err_lamb, err_phi

    def calc_phibragg_from_pts(self, pts, dtheta=None, dpsi=None):

        # Check / format pts
        pts = self._checkformat_pts(pts)

        # Get local summit nout, e1, e2 if non-centered
        psi, dtheta = self._checkformat_psidtheta(psi=psi, dtheta=dtheta)
        summit, nout, e1, e2 = self.get_local_noute1e2(dtheta, psi)

        # Compute
        bragg, phi = _comp_optics.calc_braggphi_from_xixjpts(
            det_cent, det_ei, det_ej,
            summit, -nout, e1, e2, pts=pts)
        return phi, bragg

    def get_lamb_avail_from_pts(self, pts):
        pass

    def calc_thetapsi_from_lambpts(self, pts=None, lamb=None, n=None,
                                   ntheta=None):

        # Check / Format inputs
        pts = self._checkformat_pts(pts)
        npts = pts.shape[1]

        if lamb is None:
            lamb = self._DEFLAMB
        lamb = np.r_[lamb]
        nlamb = lamb.size
        bragg = self.get_bragg_from_lamb(lamb, n=n)

        dtheta, psi, indnan = _comp_optics.calc_psidthetaphi_from_pts_lamb(
            pts, self._dgeom['center'], self._dgeom['rcurve'],
            bragg, nlamb, npts,
            self._dgeom['nout'], self._dgeom['e1'], self._dgeom['e2'],
            self._dgeom['extenthalf'], ntheta=ntheta)

        # import ipdb;    ipdb.set_trace()    # DB
        bragg = np.repeat(np.repeat(bragg[:, None], npts, axis=-1)[..., None],
                          ntheta, axis=-1)
        bragg[indnan] = np.nan
        phi[ind] = self.calc_braggphi_from_pts(pts,
                                               dtheta=dtheta[ind],
                                               dpsi=dpsi[ind])

        return dtheta, psi, phi, bragg

    def plot_line_from_pts_on_det(self, lamb=None, pts=None,
                                  xi_bounds=None, xj_bounds=None, nphi=None,
                                  det_cent=None, det_nout=None,
                                  det_ei=None, det_ej=None,
                                  johann=False, lpsi=None, ltheta=None,
                                  rocking=False, fs=None, dmargin=None,
                                  wintit=None, tit=None):
        """ Visualize the de-focusing by ray-tracing of chosen lamb
        """
        # Check / format inputs
        if lamb is None:
            lamb = self._DEFLAMB
        lamb = np.atleast_1d(lamb).ravel()
        nlamb = lamb.size

        det = np.array([[xi_bounds[0], xi_bounds[1], xi_bounds[1],
                         xi_bounds[0], xi_bounds[0]],
                        [xj_bounds[0], xj_bounds[0], xj_bounds[1],
                         xj_bounds[1], xj_bounds[0]]])

        # Compute lamb / phi
        _, phi = self.calc_phibragg_from_xixj(
            det[0, :], det[1, :], n=n,
            det_cent=det_cent, det_ei=det_ei, det_ej=det_ej,
            theta=None, psi=None, plot=False)
        phimin, phimax = np.nanmin(phi), np.nanmax(phi)
        phimin, phimax = phimin-(phimax-phimin)/10, phimax+(phimax-phimin)/10
        del phi

        # Get reference ray-tracing
        if nphi is None:
            nphi = 300
        phi = np.linspace(phimin, phimax, nphi)
        bragg = self._checkformat_bragglamb(lamb=lamb, n=n)

        xi = np.full((nlamb, nphi), np.nan)
        xj = np.full((nlamb, nphi), np.nan)
        for ll in range(nlamb):
            xi[ll, :], xj[ll, :] = self.calc_xixj_from_phibragg(
                bragg=bragg[ll], phi=phi, n=n,
                det_cent=det_cent, det_nout=det_nout,
                det_ei=det_ei, det_ej=det_ej, plot=False)

        # Get johann-error raytracing (multiple positions on crystal)
        xi_er, xj_er = None, None
        if johann and not rocking:
            if lpsi is None or ltheta is None:
                lpsi = np.linspace(-1., 1., 15)
                ltheta = np.linspace(-1., 1., 15)
                lpsi, ltheta = np.meshgrid(lpsi, ltheta)
                lpsi = lpsi.ravel()
                ltheta = ltheta.ravel()
            lpsi = self._dgeom['extenthalf'][0]*np.r_[lpsi]
            ltheta = np.pi/2 + self._dgeom['extenthalf'][1]*np.r_[ltheta]
            npsi = lpsi.size
            assert npsi == ltheta.size

            xi_er = np.full((nlamb, npsi*nphi), np.nan)
            xj_er = np.full((nlamb, npsi*nphi), np.nan)
            for l in range(nlamb):
                for ii in range(npsi):
                    i0 = np.arange(ii*nphi, (ii+1)*nphi)
                    xi_er[l, i0], xj_er[l, i0] = self.calc_xixj_from_phibragg(
                        phi=phi, bragg=bragg[l], lamb=None, n=n,
                        theta=ltheta[ii], psi=lpsi[ii],
                        det_cent=det_cent, det_nout=det_nout,
                        det_ei=det_ei, det_ej=det_ej, plot=False)

        # Get rocking curve error
        if rocking:
            pass

        # Plot
        ax = _plot_optics.CrystalBragg_plot_line_tracing_on_det(
            lamb, xi, xj, xi_er, xj_er, det=det,
            johann=johann, rocking=rocking,
            fs=fs, dmargin=dmargin, wintit=wintit, tit=tit)

    def plot_data_vs_lambphi(self, xi=None, xj=None, data=None, mask=None,
                             det_cent=None, det_ei=None, det_ej=None,
                             theta=None, psi=None, n=None,
                             nlambfit=None, nphifit=None,
                             magaxis=None, npaxis=None,
                             plot=True, fs=None,
                             cmap=None, vmin=None, vmax=None):
        # Check / format inputs
        assert data is not None
        xi, xj, (xii, xjj) = self._checkformat_xixj(xi, xj)
        nxi = xi.size if xi is not None else np.unique(xii).size
        nxj = xj.size if xj is not None else np.unique(xjj).size

        # Compute lamb / phi
        bragg, phi = self.calc_phibragg_from_xixj(
            xii, xjj, n=n,
            det_cent=det_cent, det_ei=det_ei, det_ej=det_ej,
            theta=theta, psi=psi, plot=False)
        assert bragg.shape == phi.shape == data.shape
        lamb = self.get_lamb_from_bragg(bragg, n=n)

        # Compute lambfit / phifit and spectrum1d
        if mask is not None:
            data[~mask] = np.nan
        if nlambfit is None:
            nlambfit = nxi
        if nphifit is None:
            nphifit = nxj
        lambfit, phifit = _comp_optics.get_lambphifit(lamb, phi,
                                                      nlambfit, nphifit)
        lambfitbins = 0.5*(lambfit[1:] + lambfit[:-1])
        ind = np.digitize(lamb, lambfitbins)
        spect1d = np.array([np.nanmean(data[ind == ii])
                            for ii in np.unique(ind)])
        phifitbins = 0.5*(phifit[1:] + phifit[:-1])
        ind = np.digitize(phi, phifitbins)
        vertsum1d = np.array([np.nanmean(data[ind == ii])
                              for ii in np.unique(ind)])

        # Get phiref from mag axis
        lambax, phiax = None, None
        if magaxis is not None:
            if npaxis is None:
                npaxis = 1000
            thetacryst = np.arctan2(self._dgeom['summit'][1],
                                    self._dgeom['summit'][0])
            thetaax = thetacryst + np.pi/2*np.linspace(-1, 1, npaxis)
            pts = np.array([magaxis[0]*np.cos(thetaax),
                            magaxis[0]*np.sin(thetaax),
                            np.full((npaxis,), magaxis[1])])
            braggax, phiax = self.calc_phibragg_from_pts(pts)
            lambax = self.get_lamb_from_bragg(braggax)
            phiax = np.arctan2(np.sin(phiax-np.pi), np.cos(phiax-np.pi))
            ind = ((lambax >= lambfit[0]) & (lambax <= lambfit[-1])
                   & (phiax >= phifit[0]) & (phiax <= phifit[-1]))
            lambax, phiax = lambax[ind], phiax[ind]
            ind = np.argsort(lambax)
            lambax, phiax = lambax[ind], phiax[ind]

        # plot
        if plot:
            ax = _plot_optics.CrystalBragg_plot_data_vs_lambphi(
                xi, xj, bragg, lamb, phi, data,
                lambfit=lambfit, phifit=phifit, spect1d=spect1d,
                vertsum1d=vertsum1d, lambax=lambax, phiax=phiax,
                cmap=cmap, vmin=vmin, vmax=vmax, fs=fs)
        return ax

    def plot_data_fit2d(self, xi=None, xj=None, data=None, mask=None,
                        det_cent=None, det_ei=None, det_ej=None,
                        theta=None, psi=None, n=None,
                        nlamb=None, lamb0=None, forcelamb=False,
                        deg=None, knots=None, nbsplines=None,
                        method=None, max_nfev=None,
                        xtol=None, ftol=None, gtol=None,
                        loss=None, verbose=0, debug=None,
                        plot=True, fs=None, dlines=None, dmoments=None,
                        cmap=None, vmin=None, vmax=None):
        # Check / format inputs
        assert data is not None
        xi, xj, (xii, xjj) = self._checkformat_xixj(xi, xj)
        nxi = xi.size if xi is not None else np.unique(xii).size
        nxj = xj.size if xj is not None else np.unique(xjj).size

        # Compute lamb / phi
        func = self.calc_phibragg_from_xixj
        bragg, phi = func(xii, xjj, n=n,
                          det_cent=det_cent, det_ei=det_ei, det_ej=det_ej,
                          theta=theta, psi=psi, plot=False)
        assert bragg.shape == phi.shape == data.shape
        lamb = self.get_lamb_from_bragg(bragg, n=n)

        # Compute lambfit / phifit and spectrum1d
        lambfit, phifit = _comp_optics.get_lambphifit(lamb, phi, nxi, nxj)
        lambfitbins = 0.5*(lambfit[1:] + lambfit[:-1])
        ind = np.digitize(lamb, lambfitbins)
        spect1d = np.array([np.nanmean(data[ind==ii]) for ii in np.unique(ind)])

        # Compute fit for spect1d to get lamb0 if not provided
        import tofu.data._spectrafit2d as _spectrafit2d

        func = _spectrafit2d.multiplegaussianfit1d
        dfit1d = func(lambfit, spect1d,
                      nmax=nlamb, lamb0=lamb0, forcelamb=forcelamb,
                      p0=None, bounds=None,
                      max_nfev=None, xtol=xtol, verbose=0,
                      percent=20, plot_debug=False)

        # Reorder wrt lamb0
        ind = np.argsort(dfit1d['lamb0'])
        for kk in ['lamb0', 'amp', 'ampstd',
                   'sigma', 'sigmastd', 'dlamb', 'dlambstd']:
            if dfit1d[kk].ndim == 1:
                dfit1d[kk] = dfit1d[kk][ind]
            else:
                dfit1d[kk] = dfit1d[kk][0,ind]


        # Compute dfit2d
        if mask is None:
            mask = np.ones(data.shape, dtype=bool)
        func = _spectrafit2d.multigaussianfit2d
        dfit2d = func(lamb[mask].ravel(), phi[mask].ravel(), data[mask].ravel(),
                      std=dfit1d['std'],
                      lamb0=dfit1d['lamb0'], forcelamb=forcelamb,
                      deg=deg, nbsplines=nbsplines,
                      method=method, max_nfev=max_nfev,
                      xtol=xtol, ftol=ftol, gtol=gtol,
                      loss=loss, verbose=verbose, debug=debug)


        # plot
        func = _plot_optics.CrystalBragg_plot_data_vs_fit
        ax = func(xi, xj, bragg, lamb, phi, data, mask=mask,
                  lambfit=lambfit, phifit=phifit, spect1d=spect1d,
                  dfit1d=dfit1d, dfit2d=dfit2d, lambfitbins=lambfitbins,
                  cmap=cmap, vmin=vmin, vmax=vmax,
                  fs=fs, dmoments=dmoments)
        return ax, dfit1d, None
