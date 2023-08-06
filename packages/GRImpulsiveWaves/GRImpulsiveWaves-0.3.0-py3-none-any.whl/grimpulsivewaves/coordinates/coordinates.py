import numpy as np

class CoordinatePoint:
    def __init__(self, x, dif):
        self.x = x
        self.dif = dif

    def __getitem__(self, item):
        return self.x[item]

    def __setitem__(self, key, value):
        self.x[key] = value

    def __neg__(self):
        return self.coordinate_type(-self.x, self.dif)

    def __add__(self, other):
        return self.coordinate_type(self.x, other.x, self.dif)

    def __truediv__(self, float):
        return self.coordinate_type(self.x / float, self.dif)

    @property
    def coordinate_type(self):
        return CoordinatePoint


class Cartesian(CoordinatePoint):
    def __init__(self, x, dif=False):
        """
        Cartesian coordinates on Minkowski metric ds^2 = -dt^2 + dz^2 + dx^2 + dy^2
        :param x: Numpy array of numbers
        :param dif: True if this is velocities, default false if coordinates
        """
        super().__init__(x, dif)
        self.type = "cartesian"

    @staticmethod
    def christoffel(x, params):
        return np.zeros((4, 4, 4))

    def to_nulltetrad(self):
        if self.dif:
            return NullTetrad(np.array([1./np.sqrt(2) * (self.x[0] - self.x[1]),
                                        1./np.sqrt(2) * (self.x[0] + self.x[1]),
                                        1./np.sqrt(2) * (self.x[2] - 1j * self.x[3]),
                                        1./np.sqrt(2) * (self.x[2] + 1j * self.x[3])]),
                              True)
        else:
            return NullTetrad(np.array([1./np.sqrt(2) * (self.x[0] - self.x[1]),
                                        1./np.sqrt(2) * (self.x[0] + self.x[1]),
                                        1./np.sqrt(2) * (self.x[2] + 1j * self.x[3]),
                                        1./np.sqrt(2) * (self.x[2] - 1j * self.x[3])]))

    def to_spherical(self):
        raise NotImplementedError()

    def to_null_polar(self):
        raise NotImplementedError()

    @staticmethod
    def convert(x):
        return x.to_cartesian()

    @property
    def coordinate_type(self):
        return Cartesian


class GyratonicCartesian(CoordinatePoint):
    #TODO: Finish this class
    def __init__(self, x, dif=False):
        """
        Cartesian coordinates on Minkowski metric with additional 2 Theta(z-t)J(x, y, z-t) dx dy term
        (Theta is Heaviside function)
        :param x: Numpy array of numbers
        :param dif: True if this is velocities, default false if coordinates
        """
        super().__init__(x, dif)
        self.type = "gyratonic_cartesian"
    @staticmethod
    def christoffel(x, params):
        if(x[0] - x[1] <= 0):
            raise NotImplementedError()
            return np.zeros((4, 4, 4))
        else:
            raise NotImplementedError()


class NullTetrad(CoordinatePoint):
    def __init__(self, x, dif=False):
        """

        :param x: Numpy array of numbers
        :param dif: True if this is velocities, default false if coordinates
        """
        super().__init__(x, dif)
        self.type = "null_tetrad"

    def to_cartesian(self):
        if self.dif:
            return Cartesian(np.array([1. / np.sqrt(2) * np.real(self.x[0] + self.x[1]),
                                       -1. / np.sqrt(2) * np.real(self.x[0] - self.x[1]),
                                       1. / np.sqrt(2) * np.real(self.x[2] + self.x[3]),
                                       1. / np.sqrt(2) * np.imag(self.x[3] - self.x[2])]),
                             True)
        else:
            return Cartesian(np.array([1. / np.sqrt(2) * np.real(self.x[0] + self.x[1]),
                                       -1. / np.sqrt(2) * np.real(self.x[0] - self.x[1]),
                                       1. / np.sqrt(2) * np.real(self.x[2] + self.x[3]),
                                       1. / np.sqrt(2) * np.imag(self.x[2] - self.x[3])]))

    def to_nullcartesian(self):
        if self.dif:
            return NullCartesian(np.array([self.x[0], self.x[1],
                                           1. / np.sqrt(2) * np.real(self.x[2] + self.x[3]),
                                           1. / np.sqrt(2) * np.imag(self.x[3] - self.x[2])]),
                                 True)
        else:
            return NullCartesian(np.array([self.x[0], self.x[1],
                                           1. / np.sqrt(2) * np.real(self.x[2] + self.x[3]),
                                           1. / np.sqrt(2) * np.imag(self.x[2] - self.x[3])]))

    @staticmethod
    def convert(x):
        return x.to_nulltetrad()

    @property
    def coordinate_type(self):
        return NullTetrad

    @staticmethod
    def christoffel(x, params):
        return np.zeros((4, 4, 4))


class NullCartesian(CoordinatePoint):
    def __init__(self, x, dif=False):
        """

        :param x: Numpy array of numbers
        :param dif: True if this is velocities, default false if coordinates
        """
        super().__init__(x, dif)
        self.type = "null_cartesian"

    def to_cartesian(self):
        return Cartesian(np.array([1. / np.sqrt(2) * (self.x[0] + self.x[1]),
                                   1. / np.sqrt(2) * (self.x[0] - self.x[1]),
                                   self.x[2], self.x[3]]), self.dif)

    def to_nulltetrad(self):
        if self.dif:
            return NullTetrad(np.array([self.x[0], self.x[1],
                                        1. / np.sqrt(2) * (self.x[2] - 1j * self.x[3]),
                                        1. / np.sqrt(2) * (self.x[2] + 1j * self.x[3])]), True)
        else:
            return NullTetrad(np.array([self.x[0], self.x[1],
                                        1. / np.sqrt(2) * (self.x[2] + 1j * self.x[3]),
                                        1. / np.sqrt(2) * (self.x[2] - 1j * self.x[3])]))

    @staticmethod
    def convert(x):
        return x.to_nullcartesian()

    @property
    def coordinate_type(self):
        return NullCartesian

    @staticmethod
    def christoffel(x, params):
        return np.zeros((4, 4, 4))


class NullTetradConstantHeavisideGyraton(CoordinatePoint):
    def __init__(self, x, dif=False):
        """
        Gyratonic null tetrad coordinates for spacetime with gyratonic Aichelburg Sexl impulsive wave
        :param x: Numpy array of numbers
        :param dif: True if this is velocities, default false if coordinates
        """
        super().__init__(x, dif)
        self.type = "null_tetrad_constant_heaviside_gyraton"

    @staticmethod
    def christoffel(x, params):
        if not params[1]:
            return np.zeros((4, 4, 4), dtype=np.complex128)
        else:
            ch = np.zeros((4, 4, 4), dtype=np.complex128)
            ch[1, 2, 2] = - 1j * (params[0]) / (2 * x[2] * x[2])
            ch[1, 3, 3] = 1j * (params[0]) / (2 * x[3] * x[3])
            return ch

    @staticmethod
    def convert(x):
        return x.to_aichelburg_sexl_gyraton_null_tetrad()

    @property
    def coordinate_type(self):
        return NullTetradConstantHeavisideGyraton


class Spherical(CoordinatePoint):
    def __init__(self, x, dif=False):
        """
        -dt^2 + dr^2 +r^2 d\theta^2 + r^2 sin^2 \theta d\phi^2
        :param x: Numpy array of numbers
        :param dif: True if this is velocities, default false if coordinates
        """
        super().__init__(x, dif)
        self.type = "spherical"

    @staticmethod
    def christoffel(x, params):
        cf = np.zeros((4, 4, 4))
        cf[1, 2, 2] = - x[1]  # r theta theta
        cf[1, 3, 3] = - x[1] * np.sin(x[2])**2  # r phi phi
        cf[2, 1, 2] = 1. / x[1]
        cf[2, 2, 1] = 1. / x[1]
        cf[2, 3, 3] = - np.sin(x[2]) * np.cos(x[2])
        cf[3, 1, 3] = 1. / x[1]
        cf[3, 3, 1] = 1. / x[1]
        cf[3, 2, 3] = np.cos(x[2]) / np.sin(x[2])
        cf[3, 3, 2] = np.cos(x[2]) / np.sin(x[2])
        return cf


    def to_cartesian(self):
        pass

    def to_null(self):
        pass

    def to_nullpolar(self):
        if self.dif:
            return NullPolar(np.array([1./np.sqrt(2) * (self.x[0] - self.x[1]),
                                        1./np.sqrt(2) * (self.x[0] + self.x[1]),
                                        self.x[2],
                                        self.x[3]]))
        else:
            return NullPolar(np.array([]))

    @staticmethod
    def convert(x):
        return x.to_spherical()

    @property
    def coordinate_type(self):
        return Spherical


class Polar(CoordinatePoint):
    def __init__(self, x, dif=False):
        """

        :param x: Numpy array of numbers
        :param dif: True if this is velocities, default false if coordinates
        """
        super().__init__(x, dif)


class NullPolar(CoordinatePoint):
    def __init__(self, x, dif=False):
        """

        :param x: Numpy array of numbers
        :param dif: True if this is velocities, default false if coordinates
        """
        super().__init__(x, dif)
        self.type = "nullpolar"

    def to_cartesian(self):
        pass

    def to_null(self):
        pass

    def to_spherical(self):
        pass

    @staticmethod
    def Convert(x):
        return x.to_nullpolar()

    @property
    def coordinate_type(self):
        return NullPolar


class FiveDimensional(CoordinatePoint):
    def __init__(self, x, l, dif=False):
        super().__init__(x, dif)
        self.lmb = l
        self.a = np.sqrt(3/np.abs(l))


class DeSitterNullTetrad(CoordinatePoint):
    def __init__(self, x, dif=False):
        """
        Complex null coordinates coordinates with non-zero arbitrary lambda
        Christoffel symbol parameters are [\Lambda]
        :param x: Numpy array of numbers
        :param dif: True if this is velocities, default false if coordinates
        """
        super().__init__(x, dif)
        self.type = "desitternull"

    @property
    def coordinate_type(self):
        return DeSitterNullTetrad

    @staticmethod
    def christoffel(x, params):
        cf = np.zeros((4, 4, 4), dtype=np.complex128)
        cf[0, 0, 0] = - 2 * x[1] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # u u u
        cf[0, 0, 2] = x[3] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # u u eta
        cf[0, 2, 0] = cf[0, 0, 2]  # u eta u
        cf[0, 0, 3] = x[2] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0]) # u u etabar
        cf[0, 3, 0] = cf[0, 0, 3]  # u etabar u
        cf[0, 2, 3] = - x[0] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # u eta etabar
        cf[0, 3, 2] = cf[0, 2, 3]  # u etabar eta
        cf[1, 1, 1] = - 2 * x[0] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # v v v
        cf[1, 1, 2] = x[3] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # v v eta
        cf[1, 2, 1] = cf[1, 1, 2]  # v eta v
        cf[1, 1, 3] = x[2] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # v v etabar
        cf[1, 3, 1] = cf[1, 1, 3]  # v etabar v
        cf[1, 2, 3] = - x[1] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # v eta etabar
        cf[1, 3, 2] = cf[1, 2, 3]  # v etabar eta
        cf[2, 0, 1] = x[2] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # eta u v
        cf[2, 1, 0] = cf[2, 0, 1]  # eta v u
        cf[2, 0, 2] = - x[1] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  #eta u eta
        cf[2, 2, 0] = cf[2, 0, 2]  # eta eta u
        cf[2, 1, 2] = - x[0] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0]) #eta v eta
        cf[2, 2, 1] = cf[2, 1, 2]  # eta eta v
        cf[2, 2, 2] = 2 * x[3] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0]) #eta eta eta
        cf[3, 0, 1] = x[3] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0]) #etabar u v
        cf[3, 1, 0] = cf[3, 0, 1] #etabar v u
        cf[3, 0, 3] = - x[1] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0]) #etabar u etabar
        cf[3, 3, 0] = cf[3, 0, 3] #etabar etabar u
        cf[3, 1, 3] = - x[0] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0]) #etabar v etabar
        cf[3, 3, 1] = cf[3, 1, 3] #etabar etabar v
        cf[3, 3, 3] = 2 * x[2] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0]) #etabar etabar etabar
        return cf

class DeSitterConstantHeavisideGyratonNullTetrad(CoordinatePoint):
    def __init__(self, x, dif=False):
        """
        Complex null coordinates coordinates with non-zero arbitrary lambda
        Christoffel symbol parameters are [\Lambda]
        :param x: Numpy array of numbers
        :param dif: True if this is velocities, default false if coordinates
        """
        super().__init__(x, dif)
        self.type = "desitter_constant_heaviside_gyraton_null"

    @property
    def coordinate_type(self):
        return DeSitterConstantHeavisideGyratonNullTetrad

    @staticmethod
    def christoffel(x, params):
        cf = np.zeros((4, 4, 4), dtype=np.complex128)
        cf[0, 0, 0] = - 2 * x[1] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # u u u
        cf[0, 2, 3] = - x[0] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # u eta etabar
        cf[0, 3, 2] = cf[0, 2, 3]  # u etabar eta
        cf[1, 1, 1] = - 2 * x[0] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # v v v
        cf[1, 1, 2] = x[3] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # v v eta
        cf[1, 2, 1] = cf[1, 1, 2]  # v eta v
        cf[1, 1, 3] = x[2] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # v v etabar
        cf[1, 3, 1] = cf[1, 1, 3]  # v etabar v
        cf[2, 1, 2] = - x[0] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # eta v eta
        cf[2, 2, 1] = cf[2, 1, 2]  # eta eta v
        cf[2, 2, 2] = 2 * x[3] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # eta eta eta
        cf[3, 1, 3] = - x[0] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # etabar v etabar
        cf[3, 3, 1] = cf[3, 1, 3]  # etabar etabar v
        cf[3, 3, 3] = 2 * x[2] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # etabar etabar etabar

        if not params[2]:
            cf[0, 0, 2] = x[3] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # u u eta
            cf[0, 0, 3] = x[2] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # u u etabar
            cf[1, 2, 3] = - x[1] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # v eta etabar
            cf[2, 0, 1] = x[2] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # eta u v
            cf[2, 0, 2] = - x[1] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # eta u eta
            cf[3, 0, 1] = x[3] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # etabar u v
            cf[3, 0, 3] = - x[1] * params[0] / (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])  # etabar u etabar
        else:
            cf[0, 0, 2] = 0.5 * params[0] * (2. * x[3] * x[2] + 1j * x[0] * params[1]) / (x[2] * (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])) # u u eta
            cf[0, 0, 3] = 0.5 * params[0] * (2. * x[2] * x[3] - 1j * x[0] * params[1]) / (x[3] * (6. + (x[0] * x[1] - x[2] * x[3]) * params[0]))  # u u etabar
            cf[1, 1, 0] = 0.5 * x[1] * params[0] * params[1]**2 / (- x[2] * x[3] * (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])) # v v u
            cf[1, 0, 1] = cf[1, 1, 0] # v u v
            cf[1, 2, 0] = 0.25j * params[0] * params[1] * (2. * x[1] * x[2] * x[3] - x[0] * params[1]**2) / (x[2] * x[2] * x[3] * (6. + (x[0]*x[1] - x[2]*x[3]) * params[0])) # v eta u
            cf[1, 0, 2] = cf[1, 2, 0] # v u eta
            cf[1, 2, 2] = - 0.5j * params[1] / (x[2] * x[2]) # v eta eta
            cf[1, 3, 0] = 0.25j * params[0] * params[1] * (2. * x[1] * x[2] * x[3] - x[0] * params[1]**2) / (- x[2] * x[3] * x[3] * (6. + (x[0]*x[1] - x[2]*x[3]) * params[0])) # v etabar u
            cf[1, 0, 3] = cf[1, 3, 0] # v etabar u
            cf[1, 2, 3] = 0.5 * params[0] * (2. * x[1] * x[2] * x[3] - x[0] * params[1]**2) / (- x[2] * x[3] * (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])) # v eta etabar
            cf[1, 3, 3] = 0.5j * (params[1]) / (x[3] * x[3]) # v etabar etabar
            cf[2, 0, 1] = cf[0, 0, 3] # eta u v
            cf[2, 0, 2] = 0.25 * params[0] * (4. * x[1] * x[2] * x[3] - params[1] * (2j * x[2] * x[3] + x[0] * params[1])) / (- x[2] * x[3] * (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])) #eta u eta
            cf[2, 3, 0] = 0.25 * params[0] * params[1] * (2j * x[2] * x[3] + x[0] * params[1]) / (- x[3] * x[3] * (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])) #eta etabar u
            cf[2, 0, 3] = cf[2, 3, 0] # eta u etabar
            cf[2, 2, 3] = 0.5j * x[0] * params[0] * params[1] / (x[3] * (6. + (x[0] * x[1] - x[2] * x[3]) * params[0]))  # eta eta etabar
            cf[2, 3, 2] = cf[2, 2, 3]  # eta etabar eta
            cf[3, 0, 1] = cf[0, 0, 2] # etabar u v
            cf[3, 2, 0] = 0.25 * params[0] * params[1] * (2j * x[2] * x[3] + x[0] * params[1]) / (x[2] * x[2] * (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])) # etabar eta u
            cf[3, 0, 2] = cf[3, 2, 0]
            cf[3, 0, 3] = 0.25 * params[0] * (4. * x[1] * x[2] * x[3] + params[1] * (2j + x[2] * x[3] - x[0] * params[1])) / (- x[2] * x[3] * (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])) # etabar u etabar
            cf[3, 2, 3] = 0.5j * x[0] * params[0] * params[1] / (- x[2] * (6. + (x[0] * x[1] - x[2] * x[3]) * params[0])) # etabar eta etabar
            cf[3, 3, 2] = cf[3, 2, 3] # etabar etabar eta

        cf[0, 2, 0] = cf[0, 0, 2]  # u eta u
        cf[0, 3, 0] = cf[0, 0, 3]  # u etabar u
        cf[1, 3, 2] = cf[1, 2, 3]  # v etabar eta
        cf[2, 1, 0] = cf[2, 0, 1]  # eta v u
        cf[2, 2, 0] = cf[2, 0, 2]  # eta eta u
        cf[3, 1, 0] = cf[3, 0, 1]  # etabar v u
        cf[3, 3, 0] = cf[3, 0, 3]  # etabar etabar u

        return cf
#TODO: Add gyratonic coordinates (probably not for general J, will see)


class SchwarzschildCoordinates(CoordinatePoint):
    def __init__(self, x, dif=False):
        """
        Schwarzschild coordinates t, r, \theta, \phi
        Christoffel symbol parameters are [Schwarzschild_Radius]
        :param x: Numpy array of numbers
        :param dif: True if this is velocities, default false if coordinates
        """
        super().__init__(x, dif)
        self.type = "schwarzschild_coordinates"

    @property
    def coordinate_type(self):
        return SchwarzschildCoordinates

    @staticmethod
    def christoffel(x, params):
        cf = np.zeros((4, 4, 4))
        cf[0, 1, 0] = params[0] / (2 * x[1]*x[1] - 2 * x[1] * params[0])  # t r t
        cf[0, 0, 1] = cf[0, 1, 0]  # t t r
        cf[1, 0, 0] = (x[1] - params[0]) * params[0] / (2 * x[1] * x[1] * x[1])  # r t t
        cf[1, 1, 1] = - params[0] / (2 * x[1] * x[1] - 2 * x[1] * params[0])  # r r r
        cf[1, 2, 2] = - x[1] + params[0]  # r theta theta
        cf[1, 3, 3] = np.sin(x[2])**2 * (params[0] - x[1])  # r phi phi
        cf[2, 2, 1] = 1/x[1]  # theta theta r
        cf[2, 1, 2] = cf[2, 2, 1]  # theta r theta
        cf[2, 3, 3] = - np.cos(x[2]) * np.sin(x[2])  # theta phi phi
        cf[3, 3, 1] = 1/x[1]  # phi phi r
        cf[3, 1, 3] = cf[3, 3, 1]  # phi r phi
        cf[3, 3, 2] = 1/np.tan(x[2])  # phi phi theta
        cf[3, 2, 3] = cf[3, 3, 2]  # phi theta phi

        return cf


