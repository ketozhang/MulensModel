import numpy as np

from MulensModel.lens import Lens
from MulensModel.source import Source

class MulensSystem(object):
    """
    A microlensing system consisting of a lens and a source.
    """
    def __init__(self, lens=None, source=None):
        if lens is not None :
            if source is None:
                raise AttributeError(
                    'If lens is specified, source must also be specified.')
            else:
                self.lens = lens
                self.source = source
        if source is not None and lens is None:
            raise AttributeError(
                'If source is specified, lens must also be specified.')

    @property
    def lens(self):
        """
        Physical properties of the lens. A Lens object. Note: lens
        mass must be in solMasses.
        """
        return self._lens

    @lens.setter
    def lens(self, value):
        if isinstance(value, Lens):
            self._lens = value
        else:
            raise TypeError("lens must be a Lens object")

    @property
    def source(self):
        """
        Physical properties of the source. A Source object.
        """
        return self._source

    @source.setter
    def source(self, value):
        if isinstance(value, Source):
            self._source = value
        else:
            raise TypeError("source must be a Source object")

    @property
    def pi_rel(self):
        """
        The source-lens relative parallax in milliarcseconds.
        """
        return self.lens.pi_L.to(u.mas) - self.source.pi_S.to(u.mas)

    @property
    def theta_E(self):
        """
        The angular Einstein Radius in milliarcseconds.
        """
        kappa = 8.14 * u.mas / u.solMass
        return np.sqrt(
            kappa * self.lens.total_mass.to(u.solMass) 
            * self.pi_rel.to(u.mas))

if __name__ == "__main__":
    import astropy.units as u
    my_lens = Lens(mass=0.5*u.solMass, distance=6.e3*u.pc)
    print(my_lens.mass)
    my_source = Source(distance=8.e3*u.pc)
    print(my_source.distance)
    point_lens = MulensSystem(lens=my_lens, source=my_source)
    print(point_lens.theta_E)