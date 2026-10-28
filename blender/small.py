exec(open(HELPERS).read())
exec(open(EXPORT).read())
R90 = (math.pi / 2, 0, 0)

def palette():
    return dict(INK=mat("Ink", "#10302a"), CARD=mat("Card", "#fffdf7"), ACC=mat("Accent", "#f2b134"),
                CORAL=mat("Coral", "#e0573b"), LEAF=mat("Leaf", "#2f7d5d"), BLUE=mat("Blue", "#cfe3ff"))

def keys(obj, path, idx, pts):
    for f, v in pts:
        getattr(obj, path)[idx] = v; obj.keyframe_insert(path, index=idx, frame=f)

def spin(obj, idx=2, turns=1):
    for f in range(1, 98, 4):
        obj.rotation_euler[idx] = 2 * math.pi * turns * (f - 1) / 96
        obj.keyframe_insert("rotation_euler", index=idx, frame=f)
    act = obj.animation_data.action
    for fc in getattr(act, "fcurves", []):
        for k in fc.keyframe_points: k.interpolation = 'LINEAR'

def build_badge():
    P = palette(); root = empty("Badge", (0, 0, 0))
    rbox("Tile", (0, 0, 0), (1.0, 0.26, 1.0), P["ACC"], bevel=0.22, outline=0.03, parent=root)
    text("LetterFront", "A", (0, -0.13, -0.02), 0.82, P["INK"], extrude=0.03, parent=root)
    text("LetterBack", "A", (0, 0.13, -0.02), 0.82, P["INK"], extrude=0.03, parent=root, rot=(math.pi / 2, 0, math.pi))
    sp = star("Spark", (0.52, -0.05, 0.52), 0.24, P["CORAL"], depth=0.08, outline=0.02, parent=root)
    spin(root, 2)
    wave_keys(root, "location", 2, 0, 0.08, 48)
    wave_keys(sp, "rotation_euler", 1, 0, 0.6, 96)

def build_saas():
    P = palette(); root = empty("Icon", (0, 0, 0))
    rbox("Back", (-0.12, 0.15, -0.1), (1.0, 0.1, 0.75), P["BLUE"], bevel=0.08, outline=0.025, parent=root)
    front = empty("Front", (0.1, -0.05, 0.08), root)
    rbox("Win", (0, 0, 0), (1.0, 0.1, 0.75), P["CARD"], bevel=0.08, outline=0.025, parent=front)
    rbox("Bar", (0, -0.06, 0.22), (1.0, 0.02, 0.05), P["INK"], bevel=0, outline=0, parent=front)
    rbox("Block", (-0.22, -0.06, -0.05), (0.3, 0.03, 0.24), P["ACC"], bevel=0.03, outline=0, parent=front)
    for i, w in enumerate((0.36, 0.26)):
        rbox(f"Line{i}", (0.06 + w / 2, -0.06, 0.0 - i * 0.12), (w, 0.03, 0.06), P["INK"], bevel=0.02, outline=0, parent=front)
    wave_keys(front, "location", 2, 0.08, 0.06, 96)
    wave_keys(front, "location", 1, -0.05, 0.05, 96, phase=0.25)
    wave_keys(root, "rotation_euler", 2, 0, 0.35, 96)

def build_dash():
    P = palette(); root = empty("Icon", (0, 0, 0))
    rbox("Base", (0, 0, -0.42), (1.1, 0.5, 0.08), P["CARD"], bevel=0.03, outline=0.025, parent=root)
    for i, (x, m, ph) in enumerate([(-0.33, P["LEAF"], 0), (0, P["ACC"], 0.33), (0.33, P["CORAL"], 0.66)]):
        pv = empty(f"Pivot{i}", (x, 0, -0.38), root)
        rbox(f"Bar{i}", (0, 0, 0.5), (0.22, 0.22, 1.0), m, bevel=0.04, outline=0.022, parent=pv)
        pv.scale = (1, 1, 0.5)
        for f in range(1, 98, 4):
            pv.scale[2] = 0.55 + 0.3 * (0.5 + 0.5 * math.sin(2 * math.pi * ((f - 1) / 96 + ph))) + 0.1 * i
            pv.keyframe_insert("scale", index=2, frame=f)
    wave_keys(root, "rotation_euler", 2, 0, 0.4, 96)

def build_realtime():
    P = palette(); root = empty("Icon", (0, 0, 0))
    sphere("Core", (0, 0, 0), (0.18, 0.18, 0.18), P["CORAL"], outline=0.02, parent=root)
    for i in range(3):
        rg = empty(f"Ring{i}", (0, 0, 0), root)
        bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.06, major_segments=48, minor_segments=10)
        o = bpy.context.active_object; o.name = f"RingMesh{i}"; o.parent = rg
        o.rotation_euler = R90
        finish(o, P["LEAF"] if i % 2 else P["ACC"], outline=0)
        for f in range(1, 98, 4):
            t = ((f - 1) / 96 + i / 3) % 1.0
            s = 0.25 + 0.5 * t
            rg.scale = (s, s, s); rg.keyframe_insert("scale", frame=f)
        for fc in getattr(rg.animation_data.action, "fcurves", []):
            for k in fc.keyframe_points: k.interpolation = 'LINEAR'
    wave_keys(root, "rotation_euler", 2, 0, 0.5, 96)

def build_ai():
    P = palette(); root = empty("Icon", (0, 0, 0))
    big = star("Big", (-0.08, 0, -0.05), 0.48, P["ACC"], depth=0.14, outline=0.025, parent=root)
    s1 = star("Small1", (0.36, -0.05, 0.36), 0.18, P["CORAL"], depth=0.08, outline=0.02, parent=root)
    s2 = star("Small2", (0.38, -0.05, -0.32), 0.12, P["LEAF"], depth=0.06, outline=0.018, parent=root)
    wave_keys(big, "rotation_euler", 1, 0, 0.3, 96)
    for s, ph in ((s1, 0), (s2, 0.5)):
        for f in range(1, 98, 4):
            k = 0.7 + 0.3 * math.sin(2 * math.pi * ((f - 1) / 48 + ph))
            s.scale = (k, k, k); s.keyframe_insert("scale", frame=f)
    wave_keys(root, "rotation_euler", 2, 0, 0.45, 96)

def build_rebuild():
    P = palette(); root = empty("Icon", (0, 0, 0))
    cols = [P["LEAF"], P["ACC"], P["CORAL"]]
    for i in range(3):
        b = rbox(f"Block{i}", (0, 0, -0.3 + i * 0.3), (0.5 - i * 0.08, 0.5 - i * 0.08, 0.26), cols[i], bevel=0.05, outline=0.022, parent=root)
        if i == 0: continue
        # upper blocks drop in one after another, then lift away so the loop restarts cleanly
        z0 = -0.3 + i * 0.3; up = z0 + 0.45; start = 1 + (i - 1) * 14
        keys(b, "location", 2, [(1, up), (start, up), (start + 14, z0), (start + 18, z0 + 0.06),
                                  (start + 22, z0), (78, z0), (97, up)])
    spin(root, 2)

def build_figma():
    P = palette(); root = empty("Icon", (0, 0, 0))
    rbox("Frame", (0, 0.1, 0), (1.0, 0.08, 0.8), P["CARD"], bevel=0.06, outline=0.025, parent=root)
    blk = rbox("Shape", (-0.15, 0.03, 0.05), (0.42, 0.04, 0.34), P["BLUE"], bevel=0.04, outline=0.015, parent=root)
    cur = empty("Cursor", (0.25, -0.1, -0.15), root)
    bm = bmesh.new()
    pts = [(0, 0, 0), (0, 0, -0.42), (0.1, 0, -0.32), (0.18, 0, -0.48), (0.24, 0, -0.45), (0.16, 0, -0.29), (0.3, 0, -0.29)]
    vs = [bm.verts.new(p) for p in pts]; f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, vec=(0, 0.06, 0), verts=[v for v in ext['geom'] if isinstance(v, bmesh.types.BMVert)])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    co = mesh_from_bm("Arrow", bm); co.location = (0, -0.06, 0.24); co.parent = cur
    finish(co, P["CORAL"], outline=0.015, smooth=False)
    # cursor drags the shape across, then back
    for obj, base in ((cur, (0.25, -0.1, -0.15)), (blk, (-0.15, 0.03, 0.05))):
        keys(obj, "location", 0, [(1, base[0]), (20, base[0]), (50, base[0] + 0.3), (70, base[0] + 0.3), (96, base[0])])
    keys(blk, "scale", 0, [(1, 1), (20, 1), (50, 1.15), (70, 1.15), (96, 1)])
    wave_keys(root, "rotation_euler", 2, 0, 0.35, 96)

for name, fn in [("badge", build_badge), ("icon-saas", build_saas), ("icon-dashboards", build_dash),
                 ("icon-realtime", build_realtime), ("icon-ai", build_ai), ("icon-rebuild", build_rebuild),
                 ("icon-figma", build_figma)]:
    if ONLY and name not in ONLY: continue
    clear_scene(); fn()
    if not NO_EXPORT: export_glb(name)
