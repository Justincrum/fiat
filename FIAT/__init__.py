"""FInite element Automatic Tabulator -- supports constructing and
evaluating arbitrary order Lagrange and many other elements.
Simplices in one, two, and three dimensions are supported."""

from __future__ import absolute_import, print_function, division

# Import finite element classes
from FIAT.finite_element import FiniteElement, CiarletElement  # noqa
from FIAT.argyris import Argyris
from FIAT.argyris import QuinticArgyris
from FIAT.brezzi_douglas_marini import BrezziDouglasMarini
from FIAT.brezzi_douglas_fortin_marini import BrezziDouglasFortinMarini
from FIAT.discontinuous_lagrange import DiscontinuousLagrange
from FIAT.discontinuous_taylor import DiscontinuousTaylor
from FIAT.discontinuous_raviart_thomas import DiscontinuousRaviartThomas
from FIAT.hermite import CubicHermite
from FIAT.lagrange import Lagrange
from FIAT.gauss_lobatto_legendre import GaussLobattoLegendre
from FIAT.gauss_legendre import GaussLegendre
from FIAT.morley import Morley
from FIAT.nedelec import Nedelec
from FIAT.nedelec_second_kind import NedelecSecondKind
from FIAT.P0 import P0
from FIAT.raviart_thomas import RaviartThomas
from FIAT.crouzeix_raviart import CrouzeixRaviart
from FIAT.regge import Regge
from FIAT.bubble import Bubble
from FIAT.tensor_product import TensorProductElement
from FIAT.enriched import EnrichedElement
from FIAT.discontinuous import DiscontinuousElement
from FIAT.hdiv_trace import TraceHDiv
from FIAT.restricted import RestrictedElement  # noqa
from FIAT.hellan_herrmann_johnson import HellanHerrmannJohnson

# Important functionality
from FIAT.quadrature import make_quadrature  # noqa
from FIAT.quadrature_schemes import create_quadrature  # noqa
from FIAT.reference_element import ufc_cell, ufc_simplex  # noqa
from FIAT.hdivcurl import Hdiv, Hcurl  # noqa

__version__ = "2016.2.0.dev0"

# List of supported elements and mapping to element classes
supported_elements = {"Argyris": Argyris,
                      "Brezzi-Douglas-Marini": BrezziDouglasMarini,
                      "Brezzi-Douglas-Fortin-Marini": BrezziDouglasFortinMarini,
                      "Bubble": Bubble,
                      "Crouzeix-Raviart": CrouzeixRaviart,
                      "Discontinuous Lagrange": DiscontinuousLagrange,
                      "Discontinuous Taylor": DiscontinuousTaylor,
                      "Discontinuous Raviart-Thomas": DiscontinuousRaviartThomas,
                      "Hermite": CubicHermite,
                      "Lagrange": Lagrange,
                      "Gauss-Lobatto-Legendre": GaussLobattoLegendre,
                      "Gauss-Legendre": GaussLegendre,
                      "Morley": Morley,
                      "Nedelec 1st kind H(curl)": Nedelec,
                      "Nedelec 2nd kind H(curl)": NedelecSecondKind,
                      "Raviart-Thomas": RaviartThomas,
                      "Regge": Regge,
                      "EnrichedElement": EnrichedElement,
                      "TensorProductElement": TensorProductElement,
                      "BrokenElement": DiscontinuousElement,
                      "TraceElement": TraceHDiv,
                      "Hellan-Herrmann-Johnson": HellanHerrmannJohnson}

# List of extra elements
extra_elements = {"P0": P0,
                  "Quintic Argyris": QuinticArgyris}
