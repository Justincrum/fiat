from sympy import *
import numpy as np
from FIAT.finite_element import FiniteElement
from FIAT import dual_set, reference_element
from FIAT.lagrange import Lagrange
from FIAT.dual_set import make_entity_closure_ids
from FIAT.polynomial_set import mis

x, y, z = symbols('x y z')
vars = (x, y, z)

dx = (1-x, x)
dy = (1-y, y)
dz = (1-z, z)


class Serendipity(FiniteElement):

    def __new__(cls, ref_el, degree):
        dim = ref_el.get_spatial_dimension()
        if dim == 1:
            return Lagrange(ref_el, degree)
        elif dim == 0:
            raise IndexError("reference element cannot be dimension 0")
        else:
            self = super().__new__(cls)
            return self

    def __init__(self, ref_el, degree):

        dim = ref_el.get_spatial_dimension()
        topology = ref_el.get_topology()

        VL = list(v_lambda_0(dim))
        EL = []
        FL = []
        IL = []
        s_list = []
        entity_ids = {}
        cur = 0

        for top_dim, entities in topology.items():
            entity_ids[top_dim] = {}
            for entity in entities:
                entity_ids[top_dim][entity] = []

        for j in sorted(topology[0]):
            entity_ids[0][j] = [cur]
            cur = cur + 1

        for i in range(degree - 1):
            EL += e_lambda_0(i, dim)

        for j in sorted(topology[1]):
            entity_ids[1][j] = list(range(cur, cur + degree - 1))
            cur = cur + degree - 1

        for i in range(4, degree + 1):
            FL += f_lambda_0(i, dim)

        for j in sorted(topology[2]):
            entity_ids[2][j] = list(range(cur, cur + int((degree - 3)*(degree - 2)/2)))
            cur = cur + int((degree - 3)*(degree - 2)/2)

        if dim == 3:
            for i in range(6, degree + 1):
                IL += i_lambda_0(i)

            entity_ids[3] = {}
            entity_ids[3][0] = list(range(cur, cur + len(IL)))

        s_list = VL + EL + FL + IL
        formdegree = 0
        derivs = (0,)*dim

        super(Serendipity, self).__init__(ref_el=ref_el, dual=None, order=degree, formdegree=formdegree)

        self.basis = {derivs:Array(s_list)}
        self.entity_ids = entity_ids
        self.entity_closure_ids = make_entity_closure_ids(ref_el, entity_ids)
        self.degree = degree


    def degree(self):
        return self.degree

    def get_nodal_basis(self):
        raise NotImplementedError("get_nodal_basis not implemented for serendipity")

    def get_dual_set(self):
        raise NotImplementedError("")

    def get_coeffs(self):
        raise NotImplementedError("get_coeffs not implemented for serendipity")

    def tabulate(self, order, points, entity):

        phivals = {}
        T = []
        dim = self.ref_el.get_spatial_dimension()
        if dim <= 1:
            raise NotImplementedError('no tabulate method for serendipity elements of dimension 1 or less.')
        if dim >= 4:
            raise NotImplementedError('tabulate does not support higher dimensions than 3.')
        derivs = np.zeros(dim)
        for j in range(order + 1):
            alphas = mis(dim, j)
            for alpha in alphas:
                try:
                    poly = self.basis[alpha]
                except KeyError:
                    max_alpha = max(alpha)
                    index = alpha.index(max_alpha)
                    alpha = list(alpha)
                    alpha[index] += -1
                    alpha = tuple(alpha)
                    poly = diff(self.basis[alpha], vars[index])
                for i in range(len(points)):
                    if dim == 3:
                        T += [f.evalf(subs={x: points[i][0], y: points[i][1], z: points[i][2]}) for f in poly]
                    elif dim == 2:
                        T += [f.evalf(subs={x: points[i][0], y: points[i][1]}) for f in poly]
                T = np.transpose(np.reshape(np.array(T), (len(points), -1)))
                phivals[alpha] = T
                self.basis[alpha] = Array(poly)

        return phivals

    def entity_dofs(self):
        """Return the map of topological entities to degrees of
        freedom for the finite element."""
        return self.entity_ids

    def entity_closure_dofs(self):
        """Return the map of topological entities to degrees of
        freedom on the closure of those entities for the finite element."""
        return self.entity_closure_ids

    def value_shape(self):
        raise NotImplementedError("")

    def dmats(self):
        raise NotImplementedError("")

    def get_num_members(self, arg):
        raise NotImplementedError("")

    def space_dimension(self):
        raise NotImplementedError("")


def v_lambda_0(dim):

    if dim == 2:
        VL = tuple([a*b for a in dx for b in dy])
    else:
        VL = tuple([a*b*c for a in dx for b in dy for c in dz])

    return VL

def e_lambda_0(i, dim):

    assert i >= 0, 'invalid value of i'

    if dim == 2:
        EL = tuple([dx[0]*dx[1]*b*x**i for b in dy]
                   + [dy[0]*dy[1]*a*y**i for a in dx])
    else:
        EL = tuple([dx[0]*dx[1]*b*c*x**i for b in dy for c in dz]
                   + [dy[0]*dy[1]*a*c*y**i for c in dz for a in dx]
                   + [dz[0]*dz[1]*a*b*z**i for a in dx for b in dy])

    return EL

def f_lambda_0(i, dim):

    assert i >= 4, 'invalid value for i'

    if dim == 2:
        FL = tuple([dx[0]*dx[1]*dy[0]*dy[1]*(x**(i-4-j))*(y**j)
                    for j in range(i-3)])
    else:
        FL = tuple([dx[0]*dx[1]*dy[0]*dy[1]*(x**(i-4-j))*(y**j)*c
                    for j in range(i-3) for c in dz]
                   + [dx[0]*dx[1]*dz[0]*dz[1]*(x**(i-4-j))*(z**j)*b
                    for j in range(i-3) for b in dy]
                   + [dy[0]*dy[1]*dz[0]*dz[1]*(y**(i-4-j))*(z**j)*a
                    for j in range(i-3) for a in dx])

    return FL

def i_lambda_0(i):

    assert i >= 6, 'invalid value for i'
    assert dim == 3, 'reference element must be dimension 3'

    IL = tuple([dx[0]*dx[1]*dy[0]*dy[1]*dz[0]*dz[1]*(x**(i-6-j))*(y**(j-k))*(z**k)
                for j in range(i-5) for k in range(j+1)])

    return IL


def S(ref_el, degree):
    return Serendipity(ref_el, degree)
