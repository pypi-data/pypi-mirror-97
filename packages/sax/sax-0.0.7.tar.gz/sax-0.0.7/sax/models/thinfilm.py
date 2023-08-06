""" SAX thin-film models """

import jax.numpy as jnp
from ..typing import Dict, Float, Model, ComplexFloat
from ..constants import pi


#######################
## Fresnel interface ##
#######################


def r_fresnel_ij(params: Dict[str, Float]) -> ComplexFloat:
    """
    Normal incidence amplitude reflection from Fresnel's equations
    ni : refractive index of the initial medium
    nj : refractive index of the final medium
    """
    return (params["ni"] - params["nj"]) / (params["ni"] + params["nj"])


def r_fresnel_ji(params: Dict[str, Float]) -> ComplexFloat:
    """
    Normal incidence amplitude reflection from Fresnel's equations
    ni : refractive index of the initial medium
    nj : refractive index of the final medium
    """
    return -1 * r_fresnel_ij(params)


def t_fresnel_ij(params: Dict[str, Float]) -> ComplexFloat:
    """
    Normal incidence amplitude transmission from Fresnel's equations
    ni : refractive index of the initial medium
    nj : refractive index of the final medium
    """
    return 2 * params["ni"] / (params["ni"] + params["nj"])


def t_fresnel_ji(params: Dict[str, Float]) -> ComplexFloat:
    """
    Normal incidence amplitude transmission from Fresnel's equations
    ni : refractive index of the initial medium
    nj : refractive index of the final medium
    """
    return (1 - r_fresnel_ij(params) ** 2) / t_fresnel_ij(params)


fresnel_mirror_ij: Model = Model(
    funcs={
        ("in", "in"): r_fresnel_ij,
        ("in", "out"): t_fresnel_ij,
        ("out", "in"): t_fresnel_ji,
        ("out", "out"): r_fresnel_ji,
    },
    params={
        "ni": 1.0,
        "nj": 1.0,
    },
)
""" fresnel interface """

#################
## Propagation ##
#################


def prop_i(params: Dict[str, Float]) -> ComplexFloat:
    """
    Phase shift acquired as a wave propagates through medium i
    wl : wavelength (arb. units)
    ni : refractive index of medium (at wavelength wl)
    di : thickness of layer (same arb. unit as wl)
    """
    return jnp.exp(1j * 2 * pi * params["ni"] / params["wl"] * params["di"])


propagation_i: Model = Model(
    funcs={
        ("in", "out"): prop_i,
        ("out", "in"): prop_i,
    },
    params={
        "ni": 1.0,
        "di": 500.0,
        "wl": 532.0,
    },
)
""" propagation phase """

#################################
## Lossless reciprocal element ##
#################################


def t_complex(params: Dict[str, Float]) -> ComplexFloat:
    """
    Transmission coefficient (design parameter)
    """
    return params["t_amp"] * jnp.exp(-1j * params["t_ang"])


def r_complex(params: Dict[str, Float]) -> ComplexFloat:
    """
    Reflection coefficient, derived from transmission coefficient
    Magnitude from |t|^2 + |r|^2 = 1
    Phase from phase(t) - phase(r) = pi/2
    """
    r_amp = jnp.sqrt((1.0 - params["t_amp"] ** 2))
    r_ang = params["t_ang"] - pi / 2
    return r_amp * jnp.exp(-1j * r_ang)


mirror: Model = Model(
    funcs={
        ("in", "in"): r_complex,
        ("in", "out"): t_complex,
        ("out", "in"): t_complex,
        ("out", "out"): r_complex,
    },
    params={
        "t_amp": jnp.sqrt(0.5),
        "t_ang": 0.0,
    },
)
""" fresnel mirror """
