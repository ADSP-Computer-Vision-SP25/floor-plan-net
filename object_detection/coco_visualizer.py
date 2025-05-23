"""
Simple COCO annotation visualizer
"""
import json
import os
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def visualize_coco_annotations(annotation_file, image_file, image_dir, ax=None, show=True):
    """
    Visualize COCO annotations for a specific image
    
    Args:
        annotation_file: Path to COCO annotation JSON file
        image_file: Name of the image file
        image_dir: Directory containing the image
        output_file: Path to save the visualization (if None, just displays)
    """
    # Load COCO annotations
    with open(annotation_file, 'r') as f:
        coco = json.load(f)

    cat_map = {cat['id']: cat['name'] for cat in coco['categories']}

    # Lookup image ID in the 'images' list
    image_info = next((img for img in coco['images'] 
                       if img['file_name'] == image_file), None)
    if image_info is None:
        raise ValueError(f"Image {image_file} not found in annotations.json")
    image_id = image_info['id']
    
    # Filter annotations for this image
    anns = [ann for ann in coco['annotations'] 
            if ann['image_id'] == image_id]

    # load image
    img = Image.open(os.path.join(image_dir, image_file)).convert("RGBA")

    # prepare figure/axes
    created_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
        created_fig = True
    else:
        fig = ax.figure

    # draw image and boxes
    ax.imshow(img)
    for ann in anns:
        x, y, w_box, h_box = ann['bbox']
        label = cat_map[ann['category_id']]

        rect = patches.Rectangle(
            (x, y),
            w_box, h_box,
            linewidth=2,
            edgecolor='red',
            facecolor='none'
        )
        ax.add_patch(rect)
        ax.text(
            x, y - 5, label,
            fontsize=8,
            color='white',
            weight='bold',
            backgroundcolor='red',
            va='bottom'
        )
    
    ax.axis('off')
    if created_fig:
        plt.tight_layout()

    # show or return
    if show:
        plt.show()
    else:
        return fig, ax
