import bpy, bmesh, math
from mathutils import Vector, Euler

def hexc(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple((x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1,)

OUTLINES = True   # set False before building for a softer, outline-free look

def mat(name, hexcol, rough=0.85, emit=0.0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = hexc(hexcol); b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = hexc(hexcol); b.inputs["Emission Strength"].default_value = emit
    m.diffuse_color = hexc(hexcol)
    return m

def outline_mat():
    m = bpy.data.materials.get("Outline")
    if not m:
        m = mat("Outline", "#10302a", 1.0)
    m.use_backface_culling = True
    return m

def link(o, coll=None):
    (coll or bpy.context.scene.collection).objects.link(o)
    return o

def finish(o, m, outline=0.018, smooth=True, parent=None):
    o.data.materials.clear(); o.data.materials.append(m)
    if smooth:
        for p in o.data.polygons: p.use_smooth = True
    if outline and OUTLINES:
        o.data.materials.append(outline_mat())
        s = o.modifiers.new("outline", "SOLIDIFY")
        s.thickness = outline; s.offset = 1; s.use_flip_normals = True
        s.use_rim = False; s.material_offset = 1
    if parent: o.parent = parent
    return o

def mesh_from_bm(name, bm):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    return link(bpy.data.objects.new(name, me))

def sphere(name, loc, scale, m, outline=0.018, parent=None, seg=32, ring=16, bake=True):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=ring, radius=1)
    if bake: bmesh.ops.scale(bm, vec=Vector(scale), verts=bm.verts)
    o = mesh_from_bm(name, bm); o.location = loc
    if not bake: o.scale = scale
    return finish(o, m, outline, parent=parent)

def rbox(name, loc, size, m, bevel=0.04, outline=0.018, parent=None, rot=(0, 0, 0)):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    if bevel:
        bmesh.ops.bevel(bm, geom=bm.edges[:] + bm.verts[:], offset=bevel, segments=4, affect='EDGES', profile=0.5)
    o = mesh_from_bm(name, bm); o.location = loc; o.rotation_euler = rot
    finish(o, m, outline, smooth=bool(bevel), parent=parent)
    return o

def cyl(name, loc, r, depth, m, outline=0.018, parent=None, rot=(0, 0, 0), seg=32, r2=None):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=(r if r2 is None else r2), depth=depth)
    o = mesh_from_bm(name, bm); o.location = loc; o.rotation_euler = rot
    finish(o, m, outline, parent=parent)
    for p in o.data.polygons:
        if abs(p.normal.z) > 0.9: p.use_smooth = False
    return o

def limb(name, a, b, r, m, outline=0.016, parent=None):
    """Capsule from a to b (local to parent)."""
    a, b = Vector(a), Vector(b); d = b - a
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=r)
    for v in bm.verts:
        if v.co.z > 0: v.co.z += d.length
    o = mesh_from_bm(name, bm)
    o.location = a; o.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
    return finish(o, m, outline, parent=parent)

def empty(name, loc, parent=None):
    e = link(bpy.data.objects.new(name, None)); e.location = loc
    if parent: e.parent = parent
    return e

def star(name, loc, size, m, depth=0.04, outline=0.012, parent=None, rot=(math.pi / 2, 0, 0)):
    """4-point sparkle ✦."""
    bm = bmesh.new(); pts = []
    for i in range(8):
        ang = i * math.pi / 4; rr = size if i % 2 == 0 else size * 0.3
        pts.append(bm.verts.new((math.cos(ang) * rr, math.sin(ang) * rr, 0)))
    f = bm.faces.new(pts)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, vec=(0, 0, depth), verts=[v for v in ext['geom'] if isinstance(v, bmesh.types.BMVert)])
    bmesh.ops.translate(bm, vec=(0, 0, -depth / 2), verts=bm.verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = mesh_from_bm(name, bm); o.location = loc; o.rotation_euler = rot
    return finish(o, m, outline, smooth=False, parent=parent)

def text(name, body, loc, size, m, extrude=0.03, parent=None, rot=(math.pi / 2, 0, 0), outline=0.0):
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = body; cu.size = size
    cu.extrude = extrude; cu.align_x = 'CENTER'; cu.align_y = 'CENTER'; cu.bevel_depth = 0.004
    o = link(bpy.data.objects.new(name, cu)); o.location = loc; o.rotation_euler = rot
    if parent: o.parent = parent
    # convert to mesh
    bpy.context.view_layer.update()
    me = bpy.data.meshes.new_from_object(o.evaluated_get(bpy.context.evaluated_depsgraph_get()))
    mo = link(bpy.data.objects.new(name, me)); mo.matrix_world = o.matrix_world.copy()
    if parent: mo.parent = parent; mo.matrix_parent_inverse = parent.matrix_world.inverted()
    bpy.data.objects.remove(o, do_unlink=True); bpy.data.curves.remove(cu)
    mo.name = name
    return finish(mo, m, outline, smooth=False)

def wave_keys(obj, path, index, base, amp, period, frames=96, phase=0.0, step=2):
    for f in range(1, frames + 2, step):
        v = base + amp * math.sin(2 * math.pi * ((f - 1) / period + phase))
        if index is None:
            setattr(obj, path, v)
            obj.keyframe_insert(path, frame=f)
        else:
            getattr(obj, path)[index] = v
            obj.keyframe_insert(path, index=index, frame=f)

def clear_scene():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.curves, bpy.data.actions):
        for d in list(coll): coll.remove(d)
    sc = bpy.context.scene
    sc.render.fps = 24; sc.frame_start = 1; sc.frame_end = 96

def boxes(name, specs, m, bevel=0.0, parent=None):
    """Many boxes as one mesh: specs = [(loc, size)]."""
    bm = bmesh.new()
    for loc, size in specs:
        r = bmesh.ops.create_cube(bm, size=1)
        bmesh.ops.scale(bm, vec=Vector(size), verts=r["verts"])
        bmesh.ops.translate(bm, vec=Vector(loc), verts=r["verts"])
    if bevel:
        bmesh.ops.bevel(bm, geom=bm.edges[:], offset=bevel, segments=2, affect="EDGES", profile=0.5)
    o = mesh_from_bm(name, bm)
    return finish(o, m, 0, smooth=False, parent=parent)
