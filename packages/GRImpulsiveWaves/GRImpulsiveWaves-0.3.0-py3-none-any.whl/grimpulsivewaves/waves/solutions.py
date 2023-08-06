import numpy as np

from grimpulsivewaves.integrators import integrate_geodesic


class Solution:

    def generate_geodesic(self, x0, v0, range, dim=4, christoffelParams=None, coordinateParams=None, max_step=np.inf):
        if x0.type != v0.type:
            raise ValueError("x0 and v0 has to be in same coordinate representation")

        sol = integrate_geodesic(x0, v0, (min(range), max(range)), christoffelParams, max_step)

        return ([x0.coordinate_type(x[dim:]) for x in sol.y.T], sol.t)


class RefractionSolution(Solution):

    def generate_geodesic(self, x0, v0, range, dim=4, splitted=True, christoffelParams=None, christoffelParamsPlus=None, coordinateParams=None, max_step=np.inf, identifyPoints=False, rtol=1e-2, atol=1e-4, verbose=False):
        """

        :param x0: Initial particle 4-position
        :param v0: Initial particle 4-velocity
        :return: List of trajectories (each trajectory is list of respective coordinates)
        """
        if christoffelParamsPlus is None:
            christoffelParamsPlus = christoffelParams

        if x0.type != v0.type:
            raise ValueError("x0 and v0 has to be in same coordinate representation")

        #def metric(u):

        #    return -2 * u[0] * u[1] + 2 * u[2] * u[3]

        #def metricp(u, x):
        #    return -2 * u[0] * u[1] + 2 * u[2] * u[3] + 2 * christoffelParams[0] / (2 * 1j * x[2]) * u[0] * u[2] + 2 * np.conj(christoffelParams[0] / (2 * 1j * x[2])) * u[0] * u[3]

        xp, vp = self._refract(x0, v0)
        if verbose:
            print("At:")
            print("U: {} -> {}".format(x0.x[0], xp.x[0]))
            print("V: {} -> {}".format(x0.x[1], xp.x[1]))
            print("x+iy: {} -> {}".format(x0.x[2], xp.x[2]))
            print("x-iy: {} -> {}".format(x0.x[3], xp.x[3]))
            print("")
            print("dU: {} -> {}".format(v0.x[0], vp.x[0]))
            print("dV: {} -> {}".format(v0.x[1], vp.x[1]))
            print("d(x+iy): {} -> {}".format(v0.x[2], vp.x[2]))
            print("d(x-iy): {} -> {}".format(v0.x[3], vp.x[3]))
            print("")
            #print("ds(u, u):")
            #print("Before: {}".format(metric(v0)))
            #if (christoffelParams is not None):
            #    print("After(gyra metric): {}".format(metricp(vp, xp)))
            #else:
            #    print("After: {}".format(metric(vp)))
            print("----------------------------------------------")

        solminus = integrate_geodesic(x0, -v0, (0, -min(range)), christoffelParams, max_step, rtol=rtol, atol=atol)
        if verbose:
            print("Integrating minus part of spacetime")
            print("Status(-): {}\n{}".format(solminus.status, solminus.message))
            print("Max t: {}".format(-np.max(solminus.t)))
        solplus = integrate_geodesic(xp, vp, (0, max(range)), christoffelParamsPlus, max_step, rtol=rtol,  atol=atol)
        if verbose:
            print("Integrating plus part of spacetime")
            print("Status(+): {}\n{}".format(solminus.status, solminus.message))
            print("Max t: {}".format(np.max(solplus.t)))
            print("\n\n")


        #TODO: Return afinne parameter as list aswell (as propper time of each particle if massive)

        if splitted:
            trajectories = []
            times = []
            trajectories.append([x0.coordinate_type(x[dim:]) for x in solminus.y.T[:-1]])
            times.append(-solminus.t[:-1])
            trajectories.append([x0.coordinate_type(x[dim:]) for x in solplus.y.T])
            times.append(solplus.t)
            return (trajectories, times)
        else:
            return ([x0.coordinate_type(x[dim:]) for x in np.append(solminus.y.T[:-1], solplus.y.T)], np.append(-solminus.t[:-1], solplus.t))


class AichelburgSexlSolution(RefractionSolution):
    def __init__(self, mu):
        """
        Aichelburg - Sexl solution is a solution to Einstein equations describing
        massless blackhole moving at the speed of light. This solution effectively
        represents planar wave on Minkowski background.

        :param mu: Mu parameter of wave
        """

        self.mu = mu

    def _refract(self, x, u, keepCoordinates=True):
        """
        Internal method for geodesic plotting
        :param x: Position in internal coordinates
        :param u: Velocity in internal coordinates
        :param keepCoordinates: If false returns x and u in internal coordinates (for example when there is no inverse)
        :return: Position and velocity after refraction
        """
        #Several coordinate representations of refraction equations are presented
        if x.dif:
            raise Exception("Coordinate argument x cannot be differential")
        if not u.dif:
            raise Exception("4-velocity argument u has to be differential")
        defined = ["null_tetrad"]
        if x.type not in defined:
            _x = x.to_nulltetrad()
            _u = u.to_nulltetrad()
        else:
            _x = x
            _u = u
        #Checking in case more represenations are implemented
        if _x.type == "null_tetrad":
            _nx = np.array([_x[0],
                            _x[1] + self._h(_x),
                            _x[2], _x[3]])
            _dhz = self._hz(_x)
            _nu = np.array([_u[0],
                            _u[1] + _dhz * _u[2] + np.conj(_dhz) * _u[3] + _dhz * np.conj(_dhz) * _u[0],
                            _u[2] + np.conj(_dhz) * _u[0],
                            _u[3] + _dhz * _u[0]])
        else:
            raise Exception("Something went wrong while converting to internal coordinate representation")


        #TODO: Do this more pythonic
        if keepCoordinates and _x.type != x.type:
            _x.x = _nx
            _u.x = _nu
            return x.coordinate_type.convert(_x), u.coordinate_type.convert(_u)
        else:
            return _x.coordinate_type(_nx), _x.coordinate_type(_nu, True)

    def _h(self, x):
        if x.dif:
            raise Exception("Coordinate argument x cannot be differential")
        if x.type == "null_tetrad":
            #Branch cut [-inf , 0]
            return -self.mu * np.log(2 * x[2] * x[3])
        if x.type == "null_cartesian":
            return -self.mu * np.log(x[2]**2 + x[3]**2)

    def _hz(self, x):
        if x.dif:
            raise Exception("Coordinate argument x cannot be differential")
        if x.type == "null_tetrad":
            # Branch cut [-inf , 0]
            return -self.mu * 1./x[2]
        else:
            raise Exception("Tried to call wrong derivative of H")

    def _hx(self, x):
        if x.dif:
            raise Exception("Coordinate argument x cannot be differential")
        if x.type == "null_cartesian":
            # Branch cut [-inf , 0]
            return -self.mu * 2. * x[2] / (x[2]**2 + x[3]**2)

    def _hy(self, x):
        if x.dif:
            raise Exception("Coordinate argument x cannot be differential")
        if x.type == "null_cartesian":
            # Branch cut [-inf , 0]
            return -self.mu * 2. * x[3] / (x[2]**2 + x[3]**2)


class GeneralMinkowskiRefractionSolution(RefractionSolution):
    def __init__(self, _h, _hz, *args):
        """
        Aichelburg - Sexl solution is a solution to Einstein equations describing
        massless blackhole moving at the speed of light. This solution effectively
        represents planar wave on Minkowski background.

        :param mu: Mu parameter of wave
        """

        self._h = _h
        self._hz = _hz
        self.args = args

    def _refract(self, x, u, keepCoordinates=True):
        """
        Internal method for geodesic plotting
        :param x: Position in internal coordinates
        :param u: Velocity in internal coordinates
        :param keepCoordinates: If false returns x and u in internal coordinates (for example when there is no inverse)
        :return: Position and velocity after refraction
        """
        #Several coordinate representations of refraction equations are presented
        if x.dif:
            raise Exception("Coordinate argument x cannot be differential")
        if not u.dif:
            raise Exception("4-velocity argument u has to be differential")
        defined = ["null_tetrad"]
        if x.type not in defined:
            _x = x.to_nulltetrad()
            _u = u.to_nulltetrad()
        else:
            _x = x
            _u = u
        #Checking in case more represenations are implemented
        if _x.type == "null_tetrad":
            _nx = np.array([_x[0],
                            _x[1] + self._h(_x, self.args),
                            _x[2], _x[3]])
            _dhz = self._hz(_x, self.args)
            _nu = np.array([_u[0],
                            _u[1] + _dhz * _u[2] + np.conj(_dhz) * _u[3] + _dhz * np.conj(_dhz) * _u[0],
                            _u[2] + np.conj(_dhz) * _u[0],
                            _u[3] + _dhz * _u[0]])
        else:
            raise Exception("Something went wrong while converting to internal coordinate representation")


        #TODO: Do this more pythonic
        if keepCoordinates and _x.type != x.type:
            _x.x = _nx
            _u.x = _nu
            return x.coordinate_type.convert(_x), u.coordinate_type.convert(_u)
        else:
            return _x.coordinate_type(_nx), _x.coordinate_type(_nu, True)


class GeneralGyratonicRefractionSolution(RefractionSolution):
    def __init__(self, h, hz, chi, *args):
        """
        Frolov-Fursaev Gyraton is an explicit family of waves with twisting source. This solution implements Aichelburg-Sexl
        solution with additional off-diagonal terms in spacetime in front of the wavefront.
        :param mu: Mu parameter of wave
        :param chi: Twisting parameter of spacetime u > 0
        """
        if chi == 0:
            raise Exception("For xi=0 please use AichelburgSexlSolution class")
        self.chi = chi
        self._h = h
        self._hz = hz
        self.args = args


    def _refract(self, x, u, keepCoordinates=True):
        """
        Internal method for geodesic plotting
        :param x: Position in internal coordinates
        :param u: Velocity in internal coordinates
        :param keepCoordinates: If false returns x and u in internal coordinates (for example when there is no inverse)
        :return: Position and velocity after refraction
        """

        # Several coordinate representations of refraction equations are presented
        if x.dif:
            raise Exception("Coordinate argument x cannot be differential")
        if not u.dif:
            raise Exception("4-velocity argument u has to be differential")
        defined = ["null_tetrad_constant_heaviside_gyraton"]
        _x = x
        _u = u
        if x.type not in defined:
            raise Exception("Wrong coordinates for this wave solution")
        _nx = np.array([_x[0],
                        _x[1] + self._h(_x, self.args),
                        _x[2], _x[3]])
        _dhz = self._hz(_x, self.args)
        _nu = np.array([_u[0],
                        _u[1] + _dhz * _u[2] + np.conj(_dhz) * _u[3] + (_dhz * np.conj(_dhz) - self.chi**2 / (4. * _x[2] * _x[3])) * _u[0],
                        _u[2] + (np.conj(_dhz) - 1j * self.chi / (2. * _x[3])) * _u[0],
                        np.conj(_u[2] + (np.conj(_dhz) - 1j * self.chi / (2. * _x[3])) * _u[0])])

        # TODO: Do this more pythonic
        if keepCoordinates and _x.type != x.type:
            _x.x = _nx
            _u.x = _nu
            return x.coordinate_type.convert(_x), u.coordinate_type.convert(_u)
        else:
            return _x.coordinate_type(_nx), _x.coordinate_type(_nu, True)


class LambdaGeneralSolution(RefractionSolution):
    def __init__(self, l, h, h_z, *args):
        """
        Hotta - Tanaka solution is generalized Aichelburg-Sexl solution for non-zero cosmological
        constant.
        :param l: Cosmological constant
        :param mu: Mu parameter of wave
        """
        if l==0:
            raise Exception("For l=0 please use AichelburgSexlSolution class")
        self.l = l
        self.h = h
        self.h_z = h_z
        self.args = args

    def _refract(self, x, u, keepCoordinates=True):
        """
        Internal method for geodesic plotting
        :param x: Position in internal coordinates
        :param u: Velocity in internal coordinates
        :param keepCoordinates: If false returns x and u in internal coordinates (for example when there is no inverse)
        :return: Position and velocity after refraction
        """
        # Several coordinate representations of refraction equations are presented
        if x.dif:
            raise Exception("Coordinate argument x cannot be differential")
        if not u.dif:
            raise Exception("4-velocity argument u has to be differential")
        defined = ["desitternull"]
        if x.type not in defined:
            raise Exception("Using undefined coordinates for Hotta-Tanaka solution refraction")
        else:
            _x = x
            _u = u
        # Checking in case more represenations are implemented
        if _x.type == "desitternull":
            _nx = np.array([_x[0],
                            _x[1] + self.h(_x, self.l, self.args),
                            _x[2], _x[3]])
            _dhz = self.h_z(_x, self.l, self.args)
            _nu = np.array([_u[0],
                            _u[1] + _dhz * _u[2] + np.conj(_dhz) * _u[3] + _dhz * np.conj(_dhz) * _u[0],
                            _u[2] + np.conj(_dhz) * _u[0],
                            _u[3] + _dhz * _u[0]])
        else:
            raise Exception("Something went wrong while converting to internal coordinate representation")

        if keepCoordinates and _x.type != x.type:
            _x.x = _nx
            _u.x = _nu
            return x.coordinate_type.convert(_x), u.coordinate_type.convert(_u)
        else:
            return _x.coordinate_type(_nx), _x.coordinate_type(_nu, True)


class HottaTanakaSolution(RefractionSolution):
    def __init__(self, l, mu):
        """
        Hotta - Tanaka solution is generalized Aichelburg-Sexl solution for non-zero cosmological
        constant.
        :param l: Cosmological constant
        :param mu: Mu parameter of wave
        """
        if l==0:
            raise Exception("For l=0 please use AichelburgSexlSolution class")
        self.l = l
        self.mu = mu

    def _refract(self, x, u, keepCoordinates=True):
        """
        Internal method for geodesic plotting
        :param x: Position in internal coordinates
        :param u: Velocity in internal coordinates
        :param keepCoordinates: If false returns x and u in internal coordinates (for example when there is no inverse)
        :return: Position and velocity after refraction
        """
        # Several coordinate representations of refraction equations are presented
        if x.dif:
            raise Exception("Coordinate argument x cannot be differential")
        if not u.dif:
            raise Exception("4-velocity argument u has to be differential")
        defined = ["desitternull"]
        if x.type not in defined:
            raise Exception("Using undefined coordinates for Hotta-Tanaka solution refraction")
        else:
            _x = x
            _u = u
        # Checking in case more represenations are implemented
        if _x.type == "desitternull":
            _nx = np.array([_x[0],
                            _x[1] + self._h(_x),
                            _x[2], _x[3]], dtype=np.complex128)
            _dhz = self._hz(_x)
            _nu = np.array([_u[0],
                            _u[1] + _dhz * _u[2] + np.conj(_dhz) * _u[3] + _dhz * np.conj(_dhz) * _u[0],
                            _u[2] + np.conj(_dhz) * _u[0],
                            _u[3] + _dhz * _u[0]], dtype=np.complex128)
        else:
            raise Exception("Something went wrong while converting to internal coordinate representation")

        #TODO: Do this more pythonic
        if keepCoordinates and _x.type != x.type:
            _x.x = _nx
            _u.x = _nu
            return x.coordinate_type.convert(_x), u.coordinate_type.convert(_u)
        else:
            return _x.coordinate_type(_nx), _x.coordinate_type(_nu, True)

    #def _h(self, x):
    #    return -self.mu * (1. - 1. / 6. * self.l * x[2] * x[3]) * np.log(1. / 6. * np.abs(self.l) * x[2] * x[3])\
    #           + 2. * self.mu * (1. + 1. / 6. * self.l * x[2] * x[3])
    
    #def _h(self, x):
    #    return self.mu * np.abs(self.l) * 2. / 3. * (- 2. - (-6. + self.l * x[2] * x[3]) * np.log(6./(self.l * x[2] * x[3])) / (6. + self.l * x[2] * x[3]))

    def _h(self, x):
        return 1./24. * self.mu * (2 * (-5 + x[2] * x[3] * self.l) + (6 + x[2] * x[3] * self.l) * np.log(6 * np.abs(x[2] * x[3] * self.l) ) )

    #def _hz(self, x):
    #    return self.mu * 2. * self.l * (-36. + x[2]**2 * x[3]**2 * self.l**2 - 12 * x[2] * x[3] * self.l *
    #                                    np.log(6/(x[2] * x[3] * self.l)))/ (3. * x[2] *
    #                                                                       (6. + x[2] * x[3] * self.l)**2)

    def _hz(self, x):
        return self.mu/(24 * x[2]) * (-6 + x[2] * x[3] * self.l * (1 + np.log( (6 * np.abs(self.l))/(self.l * self.l * np.abs(x[2] * x[3])) )))


class AichelburgSexlGyratonSolution(RefractionSolution):
    def __init__(self, mu, chi):
        """
        Frolov-Fursaev Gyraton is an explicit family of waves with twisting source. This solution implements Aichelburg-Sexl
        solution with additional off-diagonal terms in spacetime in front of the wavefront.
        :param mu: Mu parameter of wave
        :param chi: Twisting parameter of spacetime u > 0
        """
        if chi == 0:
            raise Exception("For xi=0 please use AichelburgSexlSolution class")
        self.mu = mu
        self.chi = chi

    def _h(self, x):
        if x.dif:
            raise Exception("Coordinate argument x cannot be differential")
        if x.type == "null_tetrad_constant_heaviside_gyraton":
            # Branch cut [-inf , 0]
            return -self.mu * np.log(2 * x[2] * x[3])
        else:
            raise Exception("Error in inner conversion to Null Tetrad Constant Heaviside Gyraton coordinate system")

    def _hz(self, x):
        if x.dif:
            raise Exception("Coordinate argument x cannot be differential")
        if x.type == "null_tetrad_constant_heaviside_gyraton":
            # Branch cut [-inf , 0]
            return -self.mu * 1. / x[2]
        else:
            raise Exception("Error in inner conversion to Null Tetrad Constant Heaviside Gyraton coordinate system")

    def _refract(self, x, u, keepCoordinates=True):
        """
        Internal method for geodesic plotting
        :param x: Position in internal coordinates
        :param u: Velocity in internal coordinates
        :param keepCoordinates: If false returns x and u in internal coordinates (for example when there is no inverse)
        :return: Position and velocity after refraction
        """

        # Several coordinate representations of refraction equations are presented
        if x.dif:
            raise Exception("Coordinate argument x cannot be differential")
        if not u.dif:
            raise Exception("4-velocity argument u has to be differential")
        defined = ["null_tetrad_constant_heaviside_gyraton"]
        _x = x
        _u = u
        if x.type not in defined:
            raise Exception("Wrong coordinates for this wave solution")
        _nx = np.array([_x[0],
                        _x[1] + self._h(_x),
                        _x[2], _x[3]])
        _dhz = self._hz(_x)
        _nu = np.array([_u[0],
                        _u[1] + _dhz * _u[2] + np.conj(_dhz) * _u[3] + (_dhz * np.conj(_dhz) - self.chi**2 / (4. * _x[2] * _x[3])) * _u[0],
                        _u[2] + (np.conj(_dhz) - 1j * self.chi / (2. * _x[3])) * _u[0],
                        np.conj(_u[2] + (np.conj(_dhz) - 1j * self.chi / (2. * _x[3])) * _u[0])])

        # TODO: Do this more pythonic
        if keepCoordinates and _x.type != x.type:
            _x.x = _nx
            _u.x = _nu
            return x.coordinate_type.convert(_x), u.coordinate_type.convert(_u)
        else:
            return _x.coordinate_type(_nx), _x.coordinate_type(_nu, True)


class GeneralLambdaGyratonSolution(RefractionSolution):
    def __init__(self, l, chi, h, h_z, *args):
        """
        Hotta - Tanaka solution is generalized Aichelburg-Sexl solution for non-zero cosmological
        constant.
        :param l: Cosmological constant
        :param mu: Mu parameter of wave
        """
        if l==0:
            raise Exception("For l=0 please use something else")
        self.l = l
        self.chi = chi
        self._h = h
        self._hz = h_z
        self.args = args

    def _refract(self, x, u, keepCoordinates=True):
        """
        Internal method for geodesic plotting
        :param x: Position in internal coordinates
        :param u: Velocity in internal coordinates
        :param keepCoordinates: If false returns x and u in internal coordinates (for example when there is no inverse)
        :return: Position and velocity after refraction
        """
        # Several coordinate representations of refraction equations are presented
        if x.dif:
            raise Exception("Coordinate argument x cannot be differential")
        if not u.dif:
            raise Exception("4-velocity argument u has to be differential")
        defined = ["desitternull", "desitter_constant_heaviside_gyraton_null"]
        if x.type not in defined:
            raise Exception("Using undefined coordinates for Hotta-Tanaka solution refraction")
        else:
            _x = x
            _u = u
        # Checking in case more represenations are implemented
        if _x.type in ["desitternull", "desitter_constant_heaviside_gyraton_null"]:
            _nx = np.array([_x[0],
                            _x[1] + self._h(_x, self.l, self.args),
                            _x[2], _x[3]])
            _dhz = self._hz(_x, self.l, self.args)
            _nu = np.array([_u[0],
                            _u[1] + _dhz * _u[2] + np.conj(_dhz) * _u[3] + (
                                        _dhz * np.conj(_dhz) - self.chi ** 2 / (4. * _x[2] * _x[3])) * _u[0],
                            _u[2] + (np.conj(_dhz) - 1j * self.chi / (2. * _x[3])) * _u[0],
                            np.conj(_u[2] + (np.conj(_dhz) - 1j * self.chi / (2. * _x[3])) * _u[0])])
        else:
            raise Exception("Something went wrong while converting to internal coordinate representation")

        if keepCoordinates and _x.type != x.type:
            _x.x = _nx
            _u.x = _nu
            return x.coordinate_type.convert(_x), u.coordinate_type.convert(_u)
        else:
            return _x.coordinate_type(_nx), _x.coordinate_type(_nu, True)
