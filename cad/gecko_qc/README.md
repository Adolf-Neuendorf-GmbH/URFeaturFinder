# Gecko Quick Changer plate (base for the button-pressing hand)

Taken from OnRobot's Gecko SP3 CAD model
(`https://onrobot.com/storage/309_gecko_sp3_tool.step`, linked on the Gecko product page).
Only the integrated **Quick Changer – tool side** was kept. The Gecko body, column and
pad were removed.

| File | Content |
|---|---|
| `qc_tool_side.step` | The 19 quick-changer parts, kept as separate, named bodies |
| `qc_tool_side.stl` | The same parts as one binary mesh, for viewing |
| `extract_qc.py` | Re-creates both files (downloads the source STEP if it is missing) |
| `preview_qc.png` / `preview_full_gecko.png` | Renders of the isolated part and the full Gecko |

Main parts (OnRobot part numbers):

- `101143`: quick-changer body (robot side, top)
- `100055`: release handle
- `101164`: Ø71 × 4 mm interface plate. Its flat underside (Y = −2.7 mm) is where the hand goes.
- `101014` ×4: screws that held the Gecko body. They stick out 5.6 mm below the plate.
- the rest: locking pins, springs and small hardware

Frame: millimetres, Y = tool axis, robot side is +Y.
