# Copyright 2008 by Robert C. Kirby (Texas Tech University)
# License: LGPL

import finite_element, polynomial_set, dual_set , functional

class MorleyDualSet( dual_set.DualSet ):
    """The dual basis for Lagrange elements.  This class works for
    simplices of any dimension.  Nodes are point evaluation at
    equispaced points."""
    def __init__( self , ref_el ):
        entity_ids = {}
        nodes = []
        cur = 0

        # make nodes by getting points
        # need to do this dimension-by-dimension, facet-by-facet
        top = ref_el.get_topology()
        verts = ref_el.get_vertices()
        sd = ref_el.get_spatial_dimension()
        if sd != 2:
            raise Exception, "Illegal spatial dimension"

        pd = functional.PointDerivative

        # vertex point evaluations

        entity_ids[0] = {}
        for v in sorted( top[0] ):
            nodes.append( functional.PointEvaluation( ref_el , verts[v] ) )

            entity_ids[0][v] = [cur]
            cur += 1
                          
        # edge dof -- normal at each edge midpoint
        entity_ids[1] = {}
        for e in sorted( top[1] ):
            pt = ref_el.make_points( 1 , e , 2 )[0]
            n = functional.PointNormalDerivative( ref_el , e , pt )
            nodes.append( n )
            entity_ids[1][e] = [cur]
            cur += 1

        dual_set.DualSet.__init__( self , nodes , ref_el , entity_ids )

class Morley( finite_element.FiniteElement ):
    """The Morley finite element."""
    def __init__( self , ref_el ):
        poly_set = polynomial_set.ONPolynomialSet( ref_el , 2 )
        dual = MorleyDualSet( ref_el  )
        finite_element.FiniteElement.__init__( self , poly_set , dual , 2 )

if __name__=="__main__":
    import reference_element
    T = reference_element.DefaultTriangle()
    U = Morley( T )

    Ufs = U.get_nodal_basis()
    pts = T.make_lattice( 1 )
    print pts
    print Ufs.tabulate(pts).values()[0]
