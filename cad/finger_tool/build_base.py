"""Printable Quick Changer base for the middle-finger button-pressing tool.

Turns the quick-changer tool side of OnRobot's Gecko SP3 model into three printable parts:

  base_body    the quick-changer body that hooks onto the robot side (holes of the
               dropped electrical contacts/magnets/dowel are filled)
  base_slider  the spring-loaded latch, unchanged geometry; the body/plate cavity
               is widened by CLEAR instead so it slides after printing
  base_plate   the interface plate on top of a solid boss; the hand gets fused
               onto its underside later. Has M6 tap holes and is made symmetric, so the
               body can be screwed on in two positions 180 deg apart.

Hardware: 2 compression springs (about 4.5 mm OD, about 25 mm long, e.g. ballpoint-pen
springs) in the slider slots, and 4x M6 cylinder-head screws (DIN 912) through the
body into the plate.

Frame is OnRobot's: mm, Y = tool axis, robot side +Y, plate underside at Y = -2.7.

Usage:  python build_base.py [gecko_sp3.step]
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gecko_qc"))
from extract_qc import SOURCE_URL, read_parts  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

Y_SPLIT = 1.3        # plate top face = body/plate split
Y_PLATE_BOT = -2.7   # plate underside
BOSS_TOP = -0.75     # just below the lowest point of the body (-0.7)
BOSS = 8.0           # boss thickness below the original plate
SCREW_TAP = 5.0      # M6 thread cut directly into plastic
SCREW_DEPTH = 14.0
CLEAR = 0.15         # slider clearance per side

# components of the quick-changer sub-assembly (NAUO7)
BODY, PLATE, SLIDER = "NAUO9", "NAUO15", "NAUO10"
SCREWS = ["NAUO11", "NAUO12", "NAUO13", "NAUO14"]
# contacts, magnets and the dowel whose holes get filled in the body
BODY_FILLS = ["NAUO18", "NAUO19", "NAUO22", "NAUO23", "NAUO24", "NAUO25", "NAUO26", "NAUO27", "NAUO20"]


def build(parts):
    big = 200
    above = cq.Solid.makeBox(big, big, big, cq.Vector(-big / 2, Y_SPLIT, -big / 2))

    fills = parts[BODY_FILLS[0]]
    for k in BODY_FILLS[1:]:
        fills = fills.fuse(parts[k])
    body = parts[BODY].fuse(fills.intersect(above)).clean()

    boss = cq.Solid.makeCylinder(35.5, BOSS_TOP - (Y_PLATE_BOT - BOSS), cq.Vector(0, BOSS_TOP, 0), cq.Vector(0, -1, 0))
    boss = cq.Workplane().add(boss).faces("<Y").edges().chamfer(1.0).val()
    # The steel stop pin 100364 is left out: the body alone limits the slider travel.
    plate = parts[PLATE].fuse(boss)
    for k in SCREWS:
        c = parts[k].Center()
        plate = plate.cut(cq.Solid.makeCylinder(SCREW_TAP / 2, SCREW_DEPTH, cq.Vector(c.x, Y_SPLIT + 0.1, c.z), cq.Vector(0, -1, 0)))

    # Widen the slider cavity in Y and Z (X is the sliding direction). Cut one shifted
    # copy at a time: fusing the copies first makes OpenCascade run out of memory.
    slider = parts[SLIDER]
    for dy, dz in [(CLEAR, 0), (-CLEAR, 0), (0, CLEAR), (0, -CLEAR),
                   (CLEAR, CLEAR), (CLEAR, -CLEAR), (-CLEAR, CLEAR), (-CLEAR, -CLEAR)]:
        moved = slider.translate(cq.Vector(0, dy, dz))
        body = body.cut(moved)
        plate = plate.cut(moved)
    # Keep only material that fits the body in both positions, so one plate gives 0 and 180 deg.
    plate = plate.intersect(plate.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 180))
    return {"base_body": body, "base_plate": plate, "base_slider": slider}


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "gecko_qc", "gecko_sp3.step")
    if not os.path.exists(src):
        import urllib.request
        urllib.request.urlretrieve(SOURCE_URL, src)
    parts = {path.split("/")[-1]: shape for path, _, shape in read_parts(src) if path.startswith("NAUO7/")}
    for name, shape in build(parts).items():
        assert shape.isValid() and len(shape.Solids()) == 1, name
        cq.exporters.export(shape, os.path.join(HERE, name + ".step"))
        cq.exporters.export(shape, os.path.join(HERE, name + ".stl"), tolerance=0.02, angularTolerance=0.15)
        print(f"{name}: {shape.Volume():.0f} mm3")


if __name__ == "__main__":
    main()
