# Middle-finger button-pressing tool (OnRobot Quick Changer)

A 3D-printed tool that clicks into the OnRobot Quick Changer (robot side) like any OnRobot
tool. It carries a hand with an extended middle finger so the robot can press buttons.

The hand comes in 4 versions, turned 0°, 90°, 180° and 270° around the tool axis
(`preview_orientations.png`, upright: `preview_orientations_upright.png`). Print **one** of the `plate_hand_rot*.stl` files, plus the body and
the slider.

Hand model: ["Middle finger hand"](https://sketchfab.com/models/efa2d616f50d488c8ce64daf38b5a65f)
by **D.p**, licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: forearm
cut off, scaled to 60 %, simplified to about 100k faces, and fused onto the plate.

## Parts

| Part | File | Notes |
|---|---|---|
| Body | `base_body.stl` | The quick-changer part that hooks onto the robot side. Original OnRobot geometry; unused holes filled. |
| Slider | `base_slider.stl` | Spring-loaded latch with the release handle. Original geometry. |
| Plate + hand | `plate_hand_rot{0,90,180,270}.stl` | Original interface plate on an 8 mm solid boss, with the hand fused underneath. Has a printed stop pin and 4 M6 tap holes. The fingertip is 151 mm below the quick-changer interface and lies on the tool axis. |
| Plate only | `base_plate.stl` | The same plate without the hand. |

The STEP files hold the same parts as exact CAD.

## Hardware

- 2 compression springs, about 4.5 mm OD and about 25 mm long (ballpoint-pen springs work).
  They sit in the two slots of the slider and push it outward. Travel is 4.3 mm.
- 4 M6 cylinder-head screws (DIN 912), M6 × 10 (a 12 mm screw just pokes out the bottom). They go through the body into the plate. The plate
  holes are Ø5.0, the M6 tap-drill size: drill them out to 5.0 mm after printing, then tap
  M6. Works best in nylon.

## Assembly

1. Put the springs into the slider slots.
2. Put the slider into the body from below. Its spring ends rest against the body wall.
3. Put the plate on, so the stop pin goes into the slider's slot, and screw it together.
4. Check that pressing the handle moves the slider inward and that it snaps back.

## Printing

- Print the plate + hand standing on the plate (finger up). The hand needs only a little
  support under the curled fingers and thumb.
- Nylon (PA), PETG or PLA, 0.2 mm layers or finer. Dry nylon before printing; it shrinks a
  little, so check the slider fit and sand if needed. Use 100 % infill for the finger and 4+ perimeters
  for the body.
- The slider cavity has 0.15 mm clearance per side. If your printer prints tight, sand the
  slider sides.

## Rebuild

1. `python build_base.py` (needs `cadquery`) downloads the Gecko SP3 STEP from onrobot.com if
   it is missing and regenerates the body, slider and plate.
2. `python build_tool.py main_fuck.stl [scale]` (needs `trimesh manifold3d fast-simplification`)
   fuses the hand onto the plate in the 4 orientations. The hand STL comes from the Sketchfab
   download.
