import numpy as np
from scipy import integrate

class RK45(integrate.RK45):
    def __init__(self, fun, t0, x0, v0, t_bound, stepsize, rdelta=None, adelta=None):
        """
        INIT

        PARAMETERS
        ----------
        :param fun: function
            Accepts t, x as parameters, returns same type as x
        :param t0: initial lambda parameter
        :param x0:
        :param t_bound:
        :param stepsize:
        """

        self.t_bound = t_bound
        if rdelta is None:
            rdelta = 0.1 * stepsize

        if adelta is None:
            adelta = rdelta

        self.x = x0
        self.v = v0

        super(RK45, self).__init__(
            fun=fun,
            t0=t0,
            y0=v0.x.append(x0.x),
            t_bound=self.t_bound,
            first_step=0.5 * stepsize,
            max_step=5*stepsize,
            rtol=rdelta,
            atol=adelta,
            vectorized=True
        )

        def step(self):
            super(RK45, self).step()
            self.x.x = self.y[4:]
            self.v.x = self.y[:4]

