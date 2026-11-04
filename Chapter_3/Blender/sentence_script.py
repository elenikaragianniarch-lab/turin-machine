import bpy
import math
import random

# --------------------------------------------------------
# CONFIG
# --------------------------------------------------------

BASE_COLLECTION_NAME = "3dobjects"   # your base collection

SENTENCE = [
    "monumental",
    "industry",
    "hum",
    "tired",
    "brick",
    "stones",
    "unforgiving",
    "sun",
    "ascent",
]

# Stronger categories so early words already have impact
CATEGORY_INTENSITY = {
    "soft":   1.0,
    "medium": 1.3,
    "chaotic": 1.6,
}

# Per-word behaviour + gentle Z-stretch
WORDS_CONFIG = {
    "monumental": {
        "category": "chaotic",
        "scale_factor": 1.06,
        "dup": 10,
        "scatter_xy": 1.0,
        "scatter_z": 0.6,
        "jitter_rot": 10.0,
        "lift_base": 0.0,
        "ground_lumps": False,
        "harsh_delete": 0.0,
        "z_stretch": 1.05,
    },
    "industry": {
        "category": "medium",
        "scale_factor": 1.04,
        "dup": 9,
        "scatter_xy": 1.3,
        "scatter_z": 0.5,
        "jitter_rot": 8.0,
        "lift_base": 0.0,
        "ground_lumps": False,
        "harsh_delete": 0.0,
        "z_stretch": 1.02,
    },
    "hum": {
        "category": "soft",
        "scale_factor": 1.03,
        "dup": 7,
        "scatter_xy": 1.0,
        "scatter_z": 0.4,
        "jitter_rot": 10.0,
        "lift_base": 0.0,
        "ground_lumps": False,
        "harsh_delete": 0.0,
        "z_stretch": 1.02,
    },
    "tired": {
        "category": "soft",
        "scale_factor": 1.02,
        "dup": 6,
        "scatter_xy": 0.8,
        "scatter_z": 0.35,
        "jitter_rot": 8.0,
        "lift_base": 0.0,
        "ground_lumps": True,
        "harsh_delete": 0.0,
        "z_stretch": 1.0,
    },
    "brick": {
        "category": "medium",
        "scale_factor": 1.03,
        "dup": 8,
        "scatter_xy": 1.0,
        "scatter_z": 0.35,
        "jitter_rot": 6.0,
        "lift_base": 0.0,
        "ground_lumps": True,
        "harsh_delete": 0.0,
        "z_stretch": 1.02,
    },
    "stones": {
        "category": "medium",
        "scale_factor": 1.03,
        "dup": 8,
        "scatter_xy": 1.2,
        "scatter_z": 0.35,
        "jitter_rot": 10.0,
        "lift_base": 0.0,
        "ground_lumps": True,
        "harsh_delete": 0.0,
        "z_stretch": 1.03,
    },
    "unforgiving": {
        "category": "chaotic",
        "scale_factor": 1.06,
        "dup": 10,
        "scatter_xy": 1.5,
        "scatter_z": 0.7,
        "jitter_rot": 16.0,
        "lift_base": 0.1,
        "ground_lumps": False,
        "harsh_delete": 0.10,
        "z_stretch": 1.07,
    },
    "sun": {
        "category": "chaotic",
        "scale_factor": 1.05,
        "dup": 8,
        "scatter_xy": 1.3,
        "scatter_z": 1.1,
        "jitter_rot": 14.0,
        "lift_base": 0.3,
        "ground_lumps": False,
        "harsh_delete": 0.0,
        "z_stretch": 1.20,
    },
    "ascent": {
        "category": "chaotic",
        "scale_factor": 1.04,
        "dup": 6,
        "scatter_xy": 1.0,
        "scatter_z": 1.3,
        "jitter_rot": 12.0,
        "lift_base": 0.4,
        "ground_lumps": False,
        "harsh_delete": 0.0,
        "z_stretch": 1.25,
    },
}

# --------------------------------------------------------
# HELPERS
# --------------------------------------------------------

def get_collection(name: str):
    return bpy.data.collections.get(name)


def duplicate_collection(src_coll, new_name: str):
    new_coll = bpy.data.collections.new(new_name)
    bpy.context.scene.collection.children.link(new_coll)

    for obj in src_coll.objects:
        new_obj = obj.copy()
        if obj.data:
            new_obj.data = obj.data.copy()
        new_coll.objects.link(new_obj)

    return new_coll


def apply_axis_snapped_rotation(obj, jr, factor):
    """
    Rotate object around X, Y, Z by multiples of 90 degrees.
    jr (jitter_rot) + factor control the probability of rotation.
    """
    if jr <= 0:
        return

    prob = min(1.0, (jr * factor) / 60.0)

    for axis in range(3):  # 0:X, 1:Y, 2:Z
        if random.random() < prob:
            steps = random.choice([-2, -1, 1, 2])  # -180, -90, 90, 180
            angle_rad = steps * (math.pi / 2.0)
            obj.rotation_euler[axis] += angle_rad


def apply_z_stretch(obj, z_stretch_base, factor):
    """
    Gentle extra Z-scale on SOME fragments.
    Linear, clamped, and with a probability so it's not everywhere.
    """
    if z_stretch_base == 1.0:
        return

    prob = min(0.2 + 0.1 * factor, 0.8)
    if random.random() > prob:
        return

    # respond more to factor (up to 3x for later words)
    z_sf = 1.0 + (z_stretch_base - 1.0) * min(factor, 3.0)
    obj.scale.z *= z_sf


def apply_word_to_collection(coll, cfg, factor: float):
    """
    - uniform scale (linear, clamped)
    - local vertical jitter + slight global lift
    - AXIS-SNAPPED 90° rotations (X/Y/Z)
    - gentle extra Z-stretch for some fragments
    - duplicates with XY + Z scatter
    - optional ground clumping + deletion
    """
    base_sf = cfg["scale_factor"]
    jr = cfg["jitter_rot"]
    dup_count = int(cfg["dup"] * factor)
    scatter_xy = cfg["scatter_xy"] * factor
    scatter_z = cfg["scatter_z"] * factor
    lift_base = cfg["lift_base"] * factor
    ground_lumps = cfg["ground_lumps"]
    delete_ratio = cfg["harsh_delete"]
    z_stretch_base = cfg["z_stretch"]

    objs = list(coll.objects)

    # 1. SCALE, Z-JITTER, LIFT, ROTATION, Z-STRETCH on existing objects
    for obj in objs:
        if not hasattr(obj.data, "vertices"):
            continue

        # uniform scale (linear, more responsive, capped at factor 3)
        if base_sf != 1.0:
            sf = 1.0 + (base_sf - 1.0) * min(factor, 3.0)
            obj.scale.x *= sf
            obj.scale.y *= sf
            obj.scale.z *= sf

        # local vertical jitter
        if scatter_z > 0.0:
            obj.location.z += random.uniform(-0.3 * scatter_z, 0.6 * scatter_z)

        # slight overall lift
        if lift_base != 0.0:
            obj.location.z += lift_base

        # rotations snapped to 90° on all axes
        apply_axis_snapped_rotation(obj, jr, factor)

        # gentle extra Z stretch for some pieces
        apply_z_stretch(obj, z_stretch_base, factor)

    # 2. DUPLICATION + 3D SCATTER
    for i in range(dup_count):
        if not objs:
            break
        src = random.choice(objs)
        new_obj = src.copy()
        if src.data:
            new_obj.data = src.data.copy()
        coll.objects.link(new_obj)

        # scatter in XY and Z
        new_obj.location.x += random.uniform(-scatter_xy, scatter_xy)
        new_obj.location.y += random.uniform(-scatter_xy, scatter_xy)

        if scatter_z > 0.0:
            z_min = -0.2 * scatter_z
            z_max = scatter_z
            new_obj.location.z += random.uniform(z_min, z_max)

        # rotations for duplicates
        apply_axis_snapped_rotation(new_obj, jr, factor)

        # z-stretch for some duplicates as well
        apply_z_stretch(new_obj, z_stretch_base, factor)

        # optionally pull some pieces towards ground
        if ground_lumps:
            new_obj.location.z = min(new_obj.location.z, random.uniform(0.0, 0.3))

        objs.append(new_obj)

    # 3. HARSH DELETE (for unforgiving)
    if delete_ratio > 0.0:
        to_delete = []
        for obj in coll.objects:
            if not hasattr(obj.data, "vertices"):
                continue
            if random.random() < delete_ratio:
                to_delete.append(obj)
        for obj in to_delete:
            coll.objects.unlink(obj)
            bpy.data.objects.remove(obj, do_unlink=True)


# --------------------------------------------------------
# BUILD SENTENCE SEQUENCE
# --------------------------------------------------------

def build_sentence_sequence():
    base_coll = get_collection(BASE_COLLECTION_NAME)
    if base_coll is None:
        print(f"Base collection '{BASE_COLLECTION_NAME}' not found.")
        return

    prev_coll = base_coll
    created_colls = []

    for step_index, word in enumerate(SENTENCE, start=1):
        cfg = WORDS_CONFIG.get(word)
        if cfg is None:
            print(f"Word '{word}' not in WORDS_CONFIG, skipping.")
            continue

        cat = cfg["category"]
        cat_factor = CATEGORY_INTENSITY.get(cat, 1.0)

        # FASTER growth: 1, 2, 3, 4... instead of 0.5 + 0.5 * step
        position_factor = step_index
        factor = cat_factor * position_factor

        coll_name = f"sent_{step_index:02d}_{word}"
        new_coll = duplicate_collection(prev_coll, coll_name)

        # layout steps in a row along X
        offset_x = step_index * 5.0
        for obj in new_coll.objects:
            obj.location.x += offset_x

        apply_word_to_collection(new_coll, cfg, factor)

        created_colls.append(new_coll)
        prev_coll = new_coll

    print("Created sentence collections:")
    for c in created_colls:
        print("  -", c.name)


# --------------------------------------------------------
# RUN
# --------------------------------------------------------

build_sentence_sequence()
