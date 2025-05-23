#!/usr/bin/env python3
# place_detected_objects.py
# Blender script to load YOLO detections JSON and create basic cube placeholders per class.

import bpy
import os
import json
from mathutils import Vector

# ——— USER CONFIG ———
DETECTIONS_JSON = os.path.join(os.path.dirname(__file__), "detections.json")
SCALE_FACTOR    = 1 / 16           # scale pixel coords to Blender units
IGNORE_CLASSES  = {1, 2}        # wall classes to ignore

# Map class IDs to human labels
CLASS_LABELS = {
    3:  "single door",
    4:  "double door",
    5:  "sliding door",
    9:  "window",
    11: "sliding window",
    12: "opening symbol",
    13: "sofa",
    14: "bed",
    15: "chair",
    16: "table",
    17: "tv cabinet",
    18: "wardrobe",
    19: "cabinet",
    20: "refrigerator",
    21: "airconditioner",
    22: "gas stove",
    23: "sink",
    24: "bath",
    25: "bath tub",
    26: "washing machine",
    27: "squat toilet",
    28: "urinal",
    29: "toilet",
    30: "stair",
    31: "elevator"
}

# Approximate heights per class (Z dimension)
CLASS_HEIGHTS = {
    3: 2.0, 4: 2.0, 5: 2.0,
    9: 1.5, 11: 1.5,
    13: 1.0, 14: 1.0, 15: 1.0, 16: 1.0,
    17: 0.8, 18: 2.0, 19: 1.2,
    20: 1.8, 21: 0.3,
    22: 0.8, 23: 0.9,
    24: 1.2, 25: 1.2,
    26: 1.0, 27: 0.4, 28: 0.4, 29: 0.4,
    30: 2.0, 31: 2.5
}
DEFAULT_HEIGHT = 1.0

# ——— CLEAR SCENE ———
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.context.view_layer.update()

# ——— LOAD DETECTIONS ———
if not os.path.isfile(DETECTIONS_JSON):
    raise FileNotFoundError(f"Detections JSON not found: {DETECTIONS_JSON}")
with open(DETECTIONS_JSON, 'r') as f:
    detections = json.load(f)

# ——— PROCESS DETECTIONS ———
for det in detections:
    cls = det.get('class_id')
    if cls in IGNORE_CLASSES:
        continue
    label = CLASS_LABELS.get(cls, f"class_{cls}")

    # Prepare collection per label
    coll = bpy.data.collections.get(label) or bpy.data.collections.new(label)
    if label not in bpy.context.scene.collection.children.keys():
        bpy.context.scene.collection.children.link(coll)

    # Compute position and size
    x = det.get('x', 0) * SCALE_FACTOR
    y = det.get('y', 0) * SCALE_FACTOR
    w = det.get('w', 1) * SCALE_FACTOR
    h = det.get('h', 1) * SCALE_FACTOR
    height = CLASS_HEIGHTS.get(cls, DEFAULT_HEIGHT)

    mid = Vector((x, y, height / 2))

    # Add cube primitive
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=mid
    )
    cube = bpy.context.active_object
    cube.name = f"{label.replace(' ', '_')}_{cls}"
    cube.scale = (w / 2, h / 2, height / 2)

    # Move into collection
    for c in list(cube.users_collection):
        c.objects.unlink(cube)
    coll.objects.link(cube)

# ——— SAVE BLEND FILE ———
BLEND_OUT = os.path.join(os.path.dirname(__file__), "placement.blend")
bpy.ops.wm.save_mainfile(filepath=BLEND_OUT)

print(f"Placed {len(detections)} objects into {len(CLASS_LABELS)} categories and saved to {BLEND_OUT}")
