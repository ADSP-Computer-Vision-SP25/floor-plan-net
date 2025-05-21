#!/usr/bin/env python3
# import_and_make_walls.py
# Blender script to load preprocessed segments JSON, create extruded walls per category, and merge them.

import bpy
import os
import json

# ——— USER CONFIG ———
SEGMENTS_JSON = os.path.join(os.path.dirname(__file__), "segments.json")
WALL_HEIGHT   = 2.0
SCALE_FACTOR  = 0.15
BLEND_OUT     = os.path.join(os.path.dirname(__file__), "walls.blend")

# ——— CLEAR SCENE ———
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.context.view_layer.update()

# ——— LOAD SEGMENTS DATA ———
if not os.path.isfile(SEGMENTS_JSON):
    raise FileNotFoundError(f"Segments JSON not found: {SEGMENTS_JSON}")
with open(SEGMENTS_JSON, 'r') as f:
    data = json.load(f)

# ——— PROCESS EACH CATEGORY ———
for category, segments in data.items():
    # Create or get collection for this category
    coll = bpy.data.collections.get(category) or bpy.data.collections.new(category)
    if category not in bpy.context.scene.collection.children.keys():
        bpy.context.scene.collection.children.link(coll)

    created_objs = []
    for idx, seg in enumerate(segments, start=1):
        # Compute 3D coordinates
        x1 = seg['x1'] * SCALE_FACTOR
        y1 = seg['y1'] * SCALE_FACTOR
        x2 = seg['x2'] * SCALE_FACTOR
        y2 = seg['y2'] * SCALE_FACTOR

        # Create mesh with two vertices and one edge
        mesh = bpy.data.meshes.new(f"{category}_{idx:03d}")
        mesh.from_pydata([(x1, y1, 0), (x2, y2, 0)], [(0, 1)], [])
        mesh.update()

        # Create object
        obj = bpy.data.objects.new(mesh.name, mesh)
        coll.objects.link(obj)
        created_objs.append(obj)

        # Extrude edge upward
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value": (0, 0, WALL_HEIGHT)}
        )
        bpy.ops.object.editmode_toggle()
        obj.select_set(False)

    # Merge all objects in this category
    if created_objs:
        for o in created_objs:
            o.select_set(True)
        bpy.context.view_layer.objects.active = created_objs[0]
        bpy.ops.object.join()
        merged = bpy.context.active_object
        merged.name = category.replace(' ', '_')
        merged.select_set(False)

# ——— SAVE BLEND FILE ———
bpy.ops.wm.save_mainfile(filepath=BLEND_OUT)
