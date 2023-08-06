"""

"""
import pp
from pp.add_pins import _add_pins_triangle
from pp.component import Component


def test_pins_custom() -> Component:
    """We can even define the `pins_function` that we use to add markers to each port"""
    c = pp.c.waveguide()
    cc = pp.add_pins(component=c, function=_add_pins_triangle)
    return cc


if __name__ == "__main__":
    c = test_pins_custom()
    c.show()
