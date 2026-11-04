import bpy

print("\n=== HARD ANIMATION CLEAN ===")

# 1. Clear animation data from all objects
for obj in bpy.data.objects:
    if obj.animation_data:
        obj.animation_data_clear()
        print(f"Cleared animation_data for {obj.name}")

# 2. Remove ALL NLA tracks
for obj in bpy.data.objects:
    if obj.animation_data and obj.animation_data.nla_tracks:
        for track in obj.animation_data.nla_tracks:
            obj.animation_data.nla_tracks.remove(track)
        print(f"Removed NLA tracks for {obj.name}")

# 3. Remove ALL actions
for act in list(bpy.data.actions):
    print("Removing action:", act.name)
    bpy.data.actions.remove(act)

# 4. Remove ALL fcurves from meshes too
for mesh in bpy.data.meshes:
    if mesh.animation_data:
        mesh.animation_data_clear()
        print(f"Cleared mesh animation {mesh.name}")

print("\n=== CLEAN COMPLETE ===")
import bpy
import random
from mathutils import Vector

# ==========================
# SETTINGS
# ==========================

COLLECTION_NAME = "3dobjects"

WORD_SEQUENCE = [
    "children", "whispers", "coffee", "imagine", "spirit",
    "laughter", "lost", "echoing", "silence", "sacred",
    "breath", "invite", "ascent", "unforgiving", "joy",
    "monumental", "memory", "tired", "feels", "stones",
    "brick", "warm", "the past", "fountain", "industry",
    "weary", "hum", "sun", "gentle", "perfection",
    "tones", "beauty", "fragrant", "nature", "heart",
    "concrete", "distant", "rhythm", "simple", "hear",
    "mingling", "ideas", "softly"
]

FRAMES_PER_MORPH = 30   # morph duration
FRAMES_PAUSE = 1       # short pause

MAX_DUPLICATES = 5
BASE_SCATTER_RADIUS = 0.7
DUP_SCATTER_RADIUS = 0.6
SCALE_STRENGTH = 0.15   # ±15%


# ==========================
# UTILITIES
# ==========================

def get_original_objects():
    col = bpy.data.collections.get(COLLECTION_NAME)
    if not col:
        raise ValueError(f"Collection '{COLLECTION_NAME}' not found.")
    return [obj for obj in col.objects if obj.type == 'MESH' and "_dup_" not in obj.name]

def random_vector(r):
    return Vector((
        (random.random() - 0.5) * 2 * r,
        (random.random() - 0.5) * 2 * r,
        (random.random() - 0.5) * 2 * r,
    ))

def ensure_anim(obj):
    if not obj.animation_data:
        obj.animation_data_create()
    if not obj.animation_data.action:
        obj.animation_data.action = bpy.data.actions.new(name=obj.name + "_ACT")

def kf(obj, frame):
    obj.keyframe_insert("location", frame=frame)
    obj.keyframe_insert("scale", frame=frame)

def linearize(obj):
    if not obj.animation_data:
        return
    for fc in obj.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = 'LINEAR'


# ==========================
# DUPLICATE SLOTS
# ==========================

def setup_dups(originals):
    dup_map = {}
    scene = bpy.context.scene

    for o in originals:
        dups = []
        for i in range(MAX_DUPLICATES):
            name = f"{o.name}_dup_{i}"
            dup = bpy.data.objects.get(name)
            if dup is None:
                dup = bpy.data.objects.new(name, o.data)
                scene.collection.objects.link(dup)
            dups.append(dup)
        dup_map[o] = dups

    return dup_map


# ==========================
# MAIN SEQUENCE
# ==========================

def run_sequence():
    originals = get_original_objects()

    # Clear any existing animation for these objects to avoid ghosts
    for obj in originals:
        if obj.animation_data:
            obj.animation_data_clear()

    # Record base transforms
    base = {
        o.name: {
            "loc": o.location.copy(),
            "scale": o.scale.copy()
        }
        for o in originals
    }

    # Setup duplicates
    dup_map = setup_dups(originals)

    # Clear duplicate animation as well
    for dups in dup_map.values():
        for d in dups:
            if d.animation_data:
                d.animation_data_clear()

    # Start frame
    frame = 1
    bpy.context.scene.frame_set(frame)

    # Init originals at base
    for o in originals:
        ensure_anim(o)
        o.location = base[o.name]["loc"].copy()
        o.scale = base[o.name]["scale"].copy()
        kf(o, frame)
        linearize(o)

    # Init duplicates at scale 0
    for o, dups in dup_map.items():
        for d in dups:
            ensure_anim(d)
            d.location = base[o.name]["loc"].copy()
            d.scale = Vector((0.0, 0.0, 0.0))
            kf(d, frame)
            linearize(d)

    # Animate per word
    for word in WORD_SEQUENCE:
        print(f"\n=== WORD: {word} ===")

        start = frame
        end = start + FRAMES_PER_MORPH
        hold = end + FRAMES_PAUSE

        # ORIGINAL OBJECTS
        for o in originals:
            info = base[o.name]
            base_loc = info["loc"]
            base_scale = info["scale"]

            # Keyframe current at start
            bpy.context.scene.frame_set(start)
            kf(o, start)

            # Target near base
            offset = random_vector(BASE_SCATTER_RADIUS)
            new_loc = base_loc + offset

            s = 1 + random.uniform(-SCALE_STRENGTH, SCALE_STRENGTH)
            new_scale = Vector((
                base_scale.x * s,
                base_scale.y * s,
                base_scale.z * s
            ))

            # Morph to new state
            bpy.context.scene.frame_set(end)
            o.location = new_loc
            o.scale = new_scale
            kf(o, end)

            # Freeze during pause
            bpy.context.scene.frame_set(hold)
            kf(o, hold)

            linearize(o)

        # DUPLICATES
        for o in originals:
            base_loc = base[o.name]["loc"]
            base_scale = base[o.name]["scale"]
            dups = dup_map[o]

            # Decide how many duplicates this word (0,1,2)
            roll = random.random()
            if roll < 0.7:
                dup_num = 0
            elif roll < 0.9:
                dup_num = 1
            else:
                dup_num = 2

            for i, d in enumerate(dups):
                ensure_anim(d)

                # At start: ALL duplicates are OFF (pop off instantly)
                bpy.context.scene.frame_set(start)
                d.scale = Vector((0.0, 0.0, 0.0))
                d.location = base_loc.copy()
                kf(d, start)

                if i < dup_num:
                    # This duplicate will APPEAR during morph
                    bpy.context.scene.frame_set(end)
                    d.location = base_loc + random_vector(DUP_SCATTER_RADIUS)
                    s_dup = 1 + random.uniform(-SCALE_STRENGTH, SCALE_STRENGTH)
                    d.scale = Vector((
                        base_scale.x * s_dup,
                        base_scale.y * s_dup,
                        base_scale.z * s_dup
                    ))
                    kf(d, end)

                else:
                    # This duplicate stays OFF (scale 0) even at end
                    bpy.context.scene.frame_set(end)
                    d.scale = Vector((0.0, 0.0, 0.0))
                    d.location = base_loc.copy()
                    kf(d, end)

                # IMPORTANT: no keyframes at hold → they stay frozen
                linearize(d)

        # Next word starts after the pause
        frame = hold

    bpy.context.scene.frame_end = frame
    print("\n=== DONE ===")


run_sequence()
