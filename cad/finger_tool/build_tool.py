"""Fuse the hand onto the printable plate in four orientations.

Input:  base_plate.stl (from build_base.py) and the hand mesh
        ("Middle finger hand" by D.p on Sketchfab, CC-BY 4.0, file main_fuck.stl).
Output: plate_hand.stl, the plate with the hand fused on. The plate is symmetric, so
        screwing the body on in its second position turns the hand by 180 deg. Turned
        around the tool axis. 0 deg = palm facing +X (the side away from the release handle).

The hand is cut 20 mm behind the wrist, scaled, simplified and placed so that the
wrist-to-fingertip line is the tool axis.

Usage:  python build_tool.py path/to/main_fuck.stl [scale]
"""
import os
import sys

import fast_simplification
import manifold3d as mf
import numpy as np
import trimesh

HERE = os.path.dirname(os.path.abspath(__file__))
FOREARM_KEEP = 20.0      # mm of forearm left behind the wrist (model scale)
SCALE = 0.6              # hand size relative to the model (life size)
FACES = 100_000
PLATE_BOTTOM_Y = -10.7   # underside of the boss in base_plate
SINK = 1.0               # how far the wrist goes into the boss
DEGREES = (0,)           # 180 deg comes from mounting the body the other way round


def to_manifold(m):
    return mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices, np.float32),
                               tri_verts=np.asarray(m.faces, np.uint32)))


def to_trimesh(man):
    out = man.to_mesh()
    return trimesh.Trimesh(out.vert_properties[:, :3], out.tri_verts, process=True)


def prepare_hand(path, scale):
    m = trimesh.load(path)
    m = max(m.split(only_watertight=False), key=lambda b: len(b.faces))  # drop stray specks
    m.apply_scale(1000.0)                                                # model is in metres
    m.apply_translation([-m.bounds[0][0], 0, 0])                         # wrist cut at x = 0
    v, f = fast_simplification.simplify(m.vertices, m.faces, 1 - FACES / len(m.faces))
    hand = to_manifold(trimesh.Trimesh(v, f))
    hand = hand.trim_by_plane([1.0, 0.0, 0.0], FOREARM_KEEP)              # keep x >= FOREARM_KEEP
    # centre the wrist cut on the tool axis
    cut = to_trimesh(hand)
    ring = cut.vertices[cut.vertices[:, 0] < FOREARM_KEEP + 0.5]
    centre = (ring.min(0) + ring.max(0)) / 2
    hand = hand.translate([-FOREARM_KEEP, -centre[1], -centre[2]]).scale([scale] * 3)
    # hand +X -> tool -Y (away from the robot), hand Y -> tool X, hand Z -> tool Z
    rot = np.array([[0, 1, 0, 0], [-1, 0, 0, PLATE_BOTTOM_Y + SINK], [0, 0, 1, 0]], dtype=float)
    return hand.transform(rot)


def main():
    hand_path = sys.argv[1]
    scale = float(sys.argv[2]) if len(sys.argv) > 2 else SCALE
    plate = to_manifold(trimesh.load(os.path.join(HERE, "base_plate.stl")))
    hand = prepare_hand(hand_path, scale)
    for deg in DEGREES:
        tool = plate + hand.rotate([0.0, float(deg), 0.0])
        out = to_trimesh(tool)
        assert out.is_watertight and len(out.split()) == 1, deg
        out.export(os.path.join(HERE, "plate_hand.stl" if deg == 0 else f"plate_hand_rot{deg}.stl"))
        tip = out.vertices[:, 1].min()
        print(f"rot {deg:3d}: {len(out.faces)} faces, fingertip at Y={tip:.1f} mm, volume {out.volume / 1000:.1f} cm3")


if __name__ == "__main__":
    main()
