from astropy import units as u

def which_parameters(*args):
    return NotImplementedError('See use case 23 for desired behavior. Probably needs to be built around a dictionary.')

# JCY: Needs a check so that if parallax is set and t_0_par is not,
# t_0_par is set to t_0.
class ModelParameters(object):
    """
    A class for the basic microlensing model parameters (t_0, u_0,
    t_E, rho, s, q, alpha, pi_E). Can handle point lens or binary
    lens. pi_E assumes NE coordinates (Parallel, Perpendicular
    coordinates are not supported).
    """
    def __init__(self, parameters):
        """
        Set up parameters for a MulensModel.Model object.
        
        Attributes:
            t_0: time of closest approach between source and lens
            u_0: impact parameter between source and lens (in Einstein radii)
            t_E: Einstein crossing time
            rho: source size as a fraction of the Einstein radius
            s: separation between primary and companion(s) (in Einstein radii)
            q: mass ratio between primary and companion(s)
            alpha: angle of source trajectory relative to binary lens axis 
            (CCW???)

            parallax vector may be defined 
            EITHER as:
               pi_E: list, tuple, or numpy.ndarray of 2 values
               pi_E_ref: defines reference system for pi_E (see
                   MulensParallaxVector)
            OR:
               pi_E_N: North component of the parallax
               pi_E_E: East component of the parallax
               
        """

        self._check_valid_combination(parameters.keys())
        self.parameters = parameters

    def __repr__(self):
        """A nice way to represent a ModelParameters object as a string"""        
        #Initialize Header line
        variables = '{0:>11} {1:>9} '.format(
            "t_0 (HJD)", 'u_0')
        try:
            variables = '{0} {1:>9}'.format(
                variables, 't_E ({0})'.format(self._t_E.unit))
        except AttributeError:
            variables = '{0} {1:>9}'.format(variables, 't_E')

        #t_0 value
        try:
            values = '{0:>11.5f}'.format(self.t_0)
        except AttributeError:
            values = '{0:>11}'.format(None)
        #u_0 value
        try:
            values = '{0} {1:>9.6f}'.format(values, self._u_0)
        except AttributeError:
            values = '{0} {1:>9}'.format(values, None)

        #t_E value
        try:
            values = '{0} {1:>10.4f}'.format(values, self.t_E)
        except AttributeError:
            values = '{0} {1:>10}'.format(values,None)

        #rho value and header column
        try:
            values = '{0} {1:>7.5f}'.format(values, self._rho)
        except (AttributeError, TypeError, ValueError):
            pass
        else:
            variables = '{0} {1:>7}'.format(variables, 'rho') 

        #s, q values and header columns
        try:
            variables = '{0} {1:>9} {2:>12} {3:>11}'.format(
                variables, 's', 'q', 'alpha ({0})'.format(self._alpha.unit))
            values = '{0} {1:>9.5f} {2:>12.8f} {3:>11.5f}'.format(
                values, self._s, self._q, self._alpha.value)
        except AttributeError:
            pass

        return '{0}\n{1}\n'.format(variables, values)

    def _check_valid_combination(self, keys):
        return NotImplementedError('Should check that the combination of parameters is reasonable, i.e. sufficient to describe a proper model AND prevents specifying 3 variables for 2 observables (e.g. u0, teff, and tE).')

    @property
    def n_lenses(self):
        """number of objects in the lens system"""
        if ( (not 's' in self.parameters.keys()) 
             and (not 'q' in self.parameters.keys())
             and (not 'alpha' in self.parameters.keys()) ):
            return 1
        else:
            return 2

    @property
    def t_0(self):
        """
        The time of minimum projected separation between the source
        and the lens center of mass.
        """
        return self.parameters['t_0']

    @t_0.setter
    def t_0(self, new_t_0):
        self.parameters['t_0'] = new_t_0

    @property
    def u_0(self):
        """
        The minimum projected separation between the source
        and the lens center of mass.
        """
        if 'u_0' in self.parameters.keys():
            return self.parameters['u_0']
        else:
            try:
                return self.parameters['t_eff'] / self.parameters['t_E']
            except KeyError:
                raise AttributeError(
                    'u_0 is not defined for these parameters: {0}'.format(
                        self.parameters.keys()))
        # Needs option to return u_0 if t_eff is set.

    @u_0.setter
    def u_0(self, new_u_0):
        self.parameters['u_0'] = new_u_0
    # Needs check for 'rho' in parameters.keys(), cf t_eff.setter

    @property
    def t_star(self):
        """
        t_star = rho * tE
        returns value in days.
        """
        if 't_star' in self.parameters.keys():
            self._check_time_quantity('t_star')
            return self.parameters['t_star'].to(u.day).value 
        else:
            try:
                return self.parameters['t_E'].to(u.day).value * self.parameters['rho']
            except KeyError:
                raise AttributeError(
                    't_star is not defined for these parameters: {0}'.format(
                        self.parameters.keys()))

    @t_star.setter
    def t_star(self, new_t_star):
        if 't_star' in self.parameters.keys():
            self._set_time_quantity('t_star', new_t_star)
        else:
            raise KeyError('t_star is not a parameter of this model.')

    @property
    def t_eff(self):
        """
        t_eff = u_0 * t_E
        returns value in days.
        """
        if 't_eff' in self.parameters.keys():
            self._check_time_quantity('t_eff')
            return self.parameters['t_eff'].to(u.day).value 
        else:
            try:
                return self.parameters['t_E'].to(u.day).value  * self.parameters['u_0']
            except KeyError:
                raise AttributeError(
                    't_eff is not defined for these parameters: {0}'.format(
                        self.parameters.keys()))

    @t_eff.setter
    def t_eff(self, new_t_eff):
        if 't_eff' in self.parameters.keys():
            self._set_time_quantity('t_eff', new_t_eff)
        else:
            raise KeyError('t_eff is not a parameter of this model.')

    @property
    def t_E(self):
        """
        The Einstein timescale. An astropy.Quantity. "day" is the
        default unit. Regardless of input value, returns value with
        units of u.day.
        """
        if 't_E' in self.parameters.keys():
            self._check_time_quantity('t_E')
            return self.parameters['t_E'].to(u.day).value 
        elif 't_star' in self.parameters.keys() and 'rho' in self.parameters.keys():
            return self.t_star/self.rho
        elif 't_eff' in self.parameters.keys() and 'u_0' in self.parameters.keys():
            return self.t_eff/self.u_0
    
    @t_E.setter
    def t_E(self, new_t_E):
        if new_t_E is None:
            raise ValueError('Must provide a value')

        if new_t_E < 0.:
            raise ValueError('Einstein timescale cannot be negative:', new_t_E)

        self._set_time_quantity('t_E', new_t_E)
    # Needs check for 't_E' in parameters.keys(), cf t_eff.setter

    def _set_time_quantity(self, key, new_time):
        """
        Save a variable with units of time (e.g. t_E, t_star,
        t_eff). If units are not given, assume days.
        """
        if isinstance(new_time, u.Quantity):
            self.parameters[key] = new_time
        else:
            self.parameters[key] = new_time * u.day

    def _check_time_quantity(self, key):
        if not isinstance(self.parameters[key], u.Quantity):
            self._set_time_quantity(key, self.parameters[key])


    @property
    def rho(self):
        """source size as a fraction of the Einstein radius"""
        return self.parameters['rho']
    # Needs code for if t_star is set instead of rho
    
    @rho.setter
    def rho(self, new_rho):
        if new_rho < 0.:
            raise ValueError('source size (rho) cannot be negative')
        self.parameters['rho'] = new_rho
    # Needs check for 'rho' in parameters.keys(), cf t_eff.setter
    
    @property
    def alpha(self):
        """
        The angle of the source trajectory relative to the binary lens axis
        (or primary-secondary axis). Measured CW/CCW (TBD). An
        astropy.Quantity. "deg" is the default unit.
        TBD - make sure CW/CCW convention is according to Skowron+11 appendix A
        """
        return self.parameters['alpha']

    @alpha.setter
    def alpha(self, new_alpha):
        if isinstance(new_alpha, u.Quantity):
            self.parameters['alpha'] = new_alpha
        else:
            self.parameters['alpha'] = new_alpha * u.deg

    @property
    def q(self):
        """mass ratio of two lens components"""
        return self.parameters['q']
        
    @q.setter
    def q(self, new_q):
        self.parameters['q'] = new_q
    
    @property
    def s(self):
        """separation of two lens components relative to Einstein ring size"""
        return self.parameters['s']

    @s.setter
    def s(self, new_s):
        self.parameters['s'] = new_s

    @property
    def pi_E(self):
        """
        The microlens parallax vector. Must be set
        as a vector/list (i.e. [pi_E_N, pi_E_E]). To get the magnitude of pi_E, use pi_E_mag
        """
        if 'pi_E' in self.parameters.keys():
            return self.parameters['pi_E']
        elif 'pi_E_N' in self.parameters.keys() and 'pi_E_E' in self.parameters.keys():
            return [self.parameters['pi_E_N'], self.parameters['pi_E_E']]
        else:
            #raise KeyError('pi_E not defined for this model')
            return None

    @pi_E.setter
    def pi_E(self, new_pi_E):
        if isinstance(new_pi_E, np.ndarray):
            new_pi_E = new_pi_E.flatten()

        if 'pi_E' in self.parameters.keys():
            if len(new_pi_E) == 2:
                self.parameters['pi_E'] = new_pi_E                    
            else:
                raise TypeError('pi_E is a 2D vector. It must have length 2.')

        elif 'pi_E_N' in self.parameters.keys() and 'pi_E_E' in self.parameters.keys():
            self.parameters['pi_E_N'] = new_pi_E[0]
            self.parameters['pi_E_E'] = new_pi_E[1]
        else:
            raise KeyError('pi_E is not a parameter of this model.')

    @property
    def pi_E_mag(self):
        """
        The magnitude of the microlensing parallax vector.
        """
        if 'pi_E' in self.parameters.keys():
            pi_E_N = self.parameters['pi_E'][0]
            pi_E_E = self.parameters['pi_E'][1]
        elif 'pi_E_N' in self.parameters.keys() and 'pi_E_E' in self.parameters.keys():
            pi_E_N = self.parameters['pi_E_N']
            pi_E_E = self.parameters['pi_E_E']
        else:
            raise KeyError('pi_E not defined for this model')
        return np.sqrt( pi_E_N**2 + pi_E_E**2)

    @property
    def pi_E_N(self):
        """
        The North component of the microlens parallax vector.
        """
        if 'pi_E_N' in self.parameters.keys():
            return self.parameters['pi_E_N']
        elif 'pi_E' in self.parameters.keys():
            return self.parameters['pi_E'][0]
        else:
            raise KeyError('pi_E_N not defined for this model')

    @pi_E_N.setter
    def pi_E_N(self, new_value):
        if 'pi_E_N' in self.parameters.keys():
            self.parameters['pi_E_N'] = new_value
        elif 'pi_E' in self.paramters.keys():
            self.parameters['pi_E'][0] = new_value
        else:
            raise KeyError('pi_E_N is not a parameter of this model.')

    @property
    def pi_E_E(self):
        """
        The East component of the microlens parallax vector.
        """
        if 'pi_E_E' in self.parameters.keys():
            return self.parameters['pi_E_E']
        elif 'pi_E' in self.parameters.keys():
            return self.parameters['pi_E'][1]
        else:
            raise KeyError('pi_E_N not defined for this model')

    @pi_E_E.setter
    def pi_E_N(self, new_value):
        if 'pi_E_E' in self.parameters.keys():
            self.parameters['pi_E_E'] = new_value
        elif 'pi_E' in self.paramters.keys():
            self.parameters['pi_E'][1] = new_value
        else:
            raise KeyError('pi_E_E is not a parameter of this model.')

    
    @property
    def t_0_par(self):
        """
        The reference time for the calculation of parallax. If not set
        explicitly, set t_0_par = t_0.
        """
        if not 't_0_par' in self.parameters.keys():
            self.parameters['t_0_par'] = self.parameters['t_0']
        return self.parameters['t_0_par']
    

    @t_0.setter
    def t_0_par(self, new_t_0_par):
        self.parameters['t_0_par'] = new_t_0_par
