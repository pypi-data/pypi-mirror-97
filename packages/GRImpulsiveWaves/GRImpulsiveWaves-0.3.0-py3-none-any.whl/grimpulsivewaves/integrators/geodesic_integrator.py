import numpy as np
from scipy.integrate import solve_ivp

def integrate_geodesic(x0, v0, range, christoffelParams, max_step, dim=4, rtol=1e-2, atol=1e-4):
    z0 = np.append(v0.x, x0.x)
    def geodeseq(t, z):

        if(np.iscomplexobj(v0.x) or np.iscomplexobj(x0.x)):
            a = np.zeros(2*dim, dtype=np.complex128)
        else:
            a = np.zeros(2*dim)
        a[:dim] = -np.einsum('abc,bc->a', v0.coordinate_type.christoffel(z[dim:], christoffelParams), np.outer(z[:dim], z[:dim])).reshape(dim)
        a[dim:] = z[:dim].reshape(dim)
        #TODO: Add corrections/checks to 4-velocity norm?
        return a

    return solve_ivp(geodeseq, range, z0, vectorized=True, max_step=max_step, rtol=rtol, atol=atol, method="RK45")