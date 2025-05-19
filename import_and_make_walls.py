#!/usr/bin/env python3
# import_and_make_walls.py
# Blender headless script to import an SVG and create wall cubes for each path with file logging.

import bpy
import os
import math
from mathutils import Vector

# ——— USER CONFIG ———
SVG_FILE    = "0001-0040-clean.svg"
WALL_HEIGHT  = 2.0
SCALE_FACTOR = 750
BLEND_OUT    = os.path.join(os.path.dirname(__file__), "walls.blend")

# ——— CLEAR DEFAULT SCENE ———
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.context.view_layer.update()

# ——— ENABLE SVG IMPORTER ———
if not bpy.ops.import_curve.svg.poll():
    bpy.ops.wm.addon_enable(module="io_curve_svg")

# ——— IMPORT SVG ———
bpy.ops.import_curve.svg(filepath=SVG_FILE)
bpy.context.view_layer.update()

# ——— COLLECT CURVES ———
curves = [obj for obj in bpy.data.objects if obj.type == 'CURVE']

# ——— SCALE CURVES ———
for curve in curves:
    curve.scale = (SCALE_FACTOR, SCALE_FACTOR, 1)

bpy.context.view_layer.update()

# ——— PREPARE COLLECTION ———
walls_coll = bpy.data.collections.get("Walls") or bpy.data.collections.new("Walls")
if walls_coll.name not in bpy.context.scene.collection.children.keys():
    bpy.context.scene.collection.children.link(walls_coll)

# ——— BUILD WALL GEOMETRY ———
for idx, curve in enumerate(curves):
    # Convert curve to mesh
    bpy.ops.object.select_all(action='DESELECT')
    curve.select_set(True)
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.convert(target='MESH')
    mesh = bpy.context.active_object

    # Create new object from edge
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value": (0, 0, WALL_HEIGHT)}
    )
    bpy.ops.object.editmode_toggle()

    # Rename and organize
    mesh.name = f"Wall_{idx:04d}"
    for col in list(mesh.users_collection):
        col.objects.unlink(mesh)
    walls_coll.objects.link(mesh)

# ——— SAVE ———
bpy.ops.wm.save_mainfile(filepath=BLEND_OUT)
