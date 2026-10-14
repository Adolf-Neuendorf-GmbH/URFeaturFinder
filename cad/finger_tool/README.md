# Middle-finger button-pressing tool (OnRobot Quick Changer)

A 3D-printed tool that clicks into the OnRobot Quick Changer (robot side) like any OnRobot
tool. It carries a hand with an extended middle finger so the robot can press buttons.

Status: **base done, hand not yet chosen.** Once the hand is added there will be 4 versions,
with the hand turned 0°, 90°, 180° and 270° around the tool axis.

## Parts

| Part | File | Notes |
|---|---|---|
| Body | `base_body.stl` | The quick-changer part that hooks onto the robot side. Original OnRobot geometry; unused holes filled. |
| Slider | `base_slider.stl` | Spring-loaded latch with the release handle. Original geometry. |
| Plate (+ hand) | `base_plate.stl` | Original interface plate on an 8 mm solid boss. The hand is fused onto the underside. Has a printed stop pin and 4 M6 tap holes. |

The STEP files hold the same parts as exact CAD.

## Hardware

- 2 compression springs, about 4.5 mm OD and about 25 mm long (ballpoint-pen springs work).
  They sit in the two slots of the slider and push it outward. Travel is 4.3 mm.
- 4 M6 cylinder-head screws (DIN 912), M6 × 10 (a 12 mm screw just pokes out the bottom). They go through the body into the plate and
  cut their own thread in the plastic (Ø5.0 holes).

## Assembly

1. Put the springs into the slider slots.
2. Put the slider into the body from below. Its spring ends rest against the body wall.
3. Put the plate on, so the stop pin goes into the slider's slot, and screw it together.
4. Check that pressing the handle moves the slider inward and that it snaps back.

## Printing

- PETG or PLA, 0.2 mm layers or finer. Use 100 % infill for the finger and 4+ perimeters
  for the body.
- The slider cavity has 0.15 mm clearance per side. If your printer prints tight, sand the
  slider sides.

## Rebuild

`python build_base.py` (needs `cadquery`) downloads the Gecko SP3 STEP from onrobot.com if it
is missing and regenerates the three parts.
