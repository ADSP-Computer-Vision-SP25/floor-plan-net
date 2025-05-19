"""
Annotation processing configuration
"""

# Directory paths
PATHS = {
    "images": "data/cad/images",
    "annotations": "data/cad/annotations",
    "masks": "data/cad/masks"
}

# Dataset splits to process
SPLITS = [
    "train-00",
    "train-01",
    "test-00"
]

# Processing parameters
PARAMETERS = {
    "sample_step": 1,
    "max_verts": 100
}

# Class mapping (ID to name)
CLASS_MAP = {
    1: "wall",
    2: "curtain wall",
    3: "single door",
    4: "double door",
    5: "sliding door",
    9: "window",
    11: "sliding window/blind window",
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

# Category grouping (coarse categories)
CATEGORIES = {
    1: "door",
    2: "window",
    3: "stair",
    4: "home appliance",
    5: "furniture",
    6: "equipment",
}

# Mapping from class IDs to category IDs
CATEGORY_MAPPING = {
    # Doors (category 1)
    3: 1, 4: 1, 5: 1,
    # Windows (category 2)
    9: 2, 11: 2,
    # Stairs (category 3)
    30: 3,
    # Home appliances (category 4)
    20: 4, 21: 4, 22: 4, 26: 4,
    # Furniture (category 5)
    13: 5, 14: 5, 15: 5, 16: 5, 17: 5, 18: 5, 19: 5,
    # Equipment (category 6)
    12: 6, 23: 6, 24: 6, 25: 6, 27: 6, 28: 6, 29: 6, 31: 6
}

def build_categories_hierarchical():
    """
    Build a hierarchical category list for COCO format
    
    Returns:
        List of dictionaries with id, name, and supercategory
    """
    cats = []
    for class_id, class_name in CLASS_MAP.items():
        category_id = CATEGORY_MAPPING.get(class_id)
        supercat = CATEGORIES[category_id] if category_id is not None else ""
        cats.append({
            "id": class_id,
            "name": class_name,
            "supercategory": supercat
        })
    return cats

# Pre-built categories list for convenience
COCO_CATEGORIES = build_categories_hierarchical()
