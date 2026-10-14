"""Isolate the integrated Quick Changer (tool side) from OnRobot's Gecko SP3 STEP model.

Downloads the Gecko SP3 assembly from onrobot.com (no login needed), keeps only the
quick-changer sub-assembly (component NAUO7) and writes it as STEP (all parts, with
names) and binary STL (for viewing / slicing).

Coordinate frame is OnRobot's: Y is the tool axis, robot side is +Y. The flat
underside of the interface plate (part 101164) sits at Y = -2.7 mm, which is the
face the hand model will be built on.

Usage:  pip install cadquery trimesh && python extract_qc.py
"""
import os
import sys
import urllib.request

import cadquery as cq
import trimesh
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDataStd import TDataStd_Name
from OCP.TDF import TDF_Label, TDF_LabelSequence
from OCP.TDocStd import TDocStd_Document
from OCP.TopLoc import TopLoc_Location
from OCP.XCAFDoc import XCAFDoc_DocumentTool

SOURCE_URL = "https://onrobot.com/storage/309_gecko_sp3_tool.step"
QC_COMPONENT = "NAUO7"
HERE = os.path.dirname(os.path.abspath(__file__))


def label_name(label):
    attr = TDataStd_Name()
    if label.FindAttribute(TDataStd_Name.GetID_s(), attr):
        return attr.Get().ToExtString()
    return "?"


def read_parts(step_path):
    """Return [(component path, part number, located shape)] for every leaf part."""
    doc = TDocStd_Document(TCollection_ExtendedString("doc"))
    reader = STEPCAFControl_Reader()
    reader.SetNameMode(True)
    reader.ReadFile(step_path)
    reader.Transfer(doc)
    tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())

    parts = []

    def walk(label, loc, path):
        if tool.IsAssembly_s(label):
            comps = TDF_LabelSequence()
            tool.GetComponents_s(label, comps)
            for i in range(1, comps.Length() + 1):
                comp = comps.Value(i)
                ref = TDF_Label()
                tool.GetReferredShape_s(comp, ref)
                walk(ref, loc.Multiplied(tool.GetLocation_s(comp)), path + [label_name(comp)])
        else:
            shape = cq.Shape.cast(tool.GetShape_s(label).Moved(loc))
            parts.append(("/".join(path), label_name(label), shape))

    roots = TDF_LabelSequence()
    tool.GetFreeShapes(roots)
    walk(roots.Value(1), TopLoc_Location(), [])
    return parts


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "gecko_sp3.step")
    if not os.path.exists(src):
        print(f"Downloading {SOURCE_URL}")
        urllib.request.urlretrieve(SOURCE_URL, src)

    qc = [p for p in read_parts(src) if p[0].split("/")[0] == QC_COMPONENT]

    asm = cq.Assembly(name="Gecko_QC_tool_side")
    for path, part_no, shape in qc:
        asm.add(shape, name=f"{part_no}_{path.split('/')[-1]}")
    asm.export(os.path.join(HERE, "qc_tool_side.step"))

    compound = cq.Compound.makeCompound([s for *_, s in qc])
    tmp = os.path.join(HERE, "_tmp_ascii.stl")
    cq.exporters.export(compound, tmp, tolerance=0.05, angularTolerance=0.2)
    trimesh.load(tmp, force="mesh").export(os.path.join(HERE, "qc_tool_side.stl"))
    os.remove(tmp)

    bb = compound.BoundingBox()
    print(f"{len(qc)} parts, bbox X[{bb.xmin:.1f},{bb.xmax:.1f}] "
          f"Y[{bb.ymin:.1f},{bb.ymax:.1f}] Z[{bb.zmin:.1f},{bb.zmax:.1f}] mm")


if __name__ == "__main__":
    main()
