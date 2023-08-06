from typing import Optional

import pp
from pp.cell import cell
from pp.component import Component
from pp.components.coupler_ring import coupler_ring
from pp.components.waveguide import waveguide as waveguide_function
from pp.config import call_if_func
from pp.snap import assert_on_2nm_grid
from pp.tech import TECH_SILICON_C, Tech
from pp.types import ComponentFactory


@cell
def ring_double(
    gap: float = 0.2,
    length_x: float = 0.01,
    radius: Optional[float] = None,
    length_y: float = 0.01,
    coupler: ComponentFactory = coupler_ring,
    waveguide: ComponentFactory = waveguide_function,
    pins: bool = False,
    tech: Tech = TECH_SILICON_C,
) -> Component:
    """Double bus ring made of two couplers (ct: top, cb: bottom)
    connected with two vertical waveguides (wyl: left, wyr: right)

    .. code::

         --==ct==--
          |      |
          wl     wr length_y
          |      |
         --==cb==-- gap

          length_x

    .. plot::
      :include-source:

      import pp

      c = pp.c.ring_double(gap=0.2, length_x=4, length_y=0.1, radius=5)
      c.plot()
    """
    radius = radius or tech.bend_radius
    assert_on_2nm_grid(gap)

    coupler = call_if_func(
        coupler, gap=gap, radius=radius, length_x=length_x, tech=tech
    )
    waveguide = call_if_func(waveguide, length=length_y, tech=tech)

    c = Component()
    cb = c << coupler
    ct = c << coupler
    wl = c << waveguide
    wr = c << waveguide

    wl.connect(port="E0", destination=cb.ports["N0"])
    ct.connect(port="N1", destination=wl.ports["W0"])
    wr.connect(port="W0", destination=ct.ports["N0"])
    cb.connect(port="N1", destination=wr.ports["E0"])
    c.add_port("E0", port=cb.ports["E0"])
    c.add_port("W0", port=cb.ports["W0"])
    c.add_port("E1", port=ct.ports["W0"])
    c.add_port("W1", port=ct.ports["E0"])
    if pins:
        pp.add_pins_to_references(c)
    return c


if __name__ == "__main__":

    c = ring_double()
    c.show()
