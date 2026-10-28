"""Hero scene: Akhiljith at a three-monitor desk by the window, seen from behind.
Works for a while, swivels round to say hello and wave, then turns back. 8 s loop."""
exec(open(HELPERS).read())
OUTLINES = False
clear_scene()
FRAMES = 192
bpy.context.scene.frame_end = FRAMES

# ── materials (portfolio palette, softer/realistic) ──
SKIN = mat("Skin", "#c4876a", 0.6)
HAIR = mat("Hair", "#1a120e", 0.75)
SHIRT = mat("Shirt", "#f3ead6", 0.9)
JEANS = mat("Jeans", "#2b3b4f", 0.9)
SHOE = mat("Shoe", "#f4f1ea", 0.6)
LIP = mat("Lip", "#9c5a52", 0.5)
MOUTH = mat("Mouth", "#3a1f1a", 0.8)
WHITE = mat("EyeWhite", "#fbf7ee", 0.4)
INK = mat("Ink", "#10302a", 0.7)
CHAIR = mat("ChairFabric", "#1d3a34", 0.95)
METAL = mat("Metal", "#2a2f2e", 0.35)
WOOD = mat("Wood", "#c99764", 0.6)
FLOOR = mat("Floor", "#b8875b", 0.7)
WALL = mat("Wall", "#d3e8dc", 0.95)
WALL2 = mat("WallSide", "#c4ddd0", 0.95)
TRIM = mat("Trim", "#fffdf7", 0.6)
CARD = mat("Card", "#fffdf7", 0.6)
ACC = mat("Accent", "#f2b134", 0.6)
CORAL = mat("Coral", "#e0573b", 0.7)
LEAF = mat("Leaf", "#2f7d5d", 0.7)
BEZEL = mat("Bezel", "#1a1f1e", 0.4)
SKY = mat("Sky", "#bfe3f5", 1.0, emit=0.35)       # recoloured per theme in the page
ORB = mat("Orb", "#f2b134", 1.0, emit=0.6)        # sun by day, moon by night
BULB = mat("Bulb", "#e8e2d0", 0.4)                # lit at night by the page
# screen contents glow a little
S_DARK = mat("ScrDark", "#0e1916", 0.5, emit=0.25)
S_LIGHT = mat("ScrLight", "#fffdf7", 0.5, emit=0.35)
S_MINT = mat("ScrMint", "#e6f2ec", 0.5, emit=0.35)
E_CORAL = mat("ScrCoral", "#ff7a5c", 0.5, emit=0.6)
E_LEAF = mat("ScrLeaf", "#4fbf8b", 0.5, emit=0.6)
E_ACC = mat("ScrAcc", "#f2b134", 0.5, emit=0.6)
E_CREAM = mat("ScrCream", "#e6f2ec", 0.5, emit=0.5)
E_LIME = mat("ScrLime", "#c6ff3d", 0.5, emit=0.6)
E_INK = mat("ScrInk", "#10302a", 0.5)
E_GREY = mat("ScrGrey", "#3d5c55", 0.5, emit=0.2)

root = empty("Hero", (0, 0, 0))

# ── room: floor, back wall with window, side wall ──
WY = 1.3                                  # inner face of the back wall
rbox("Floor", (0, 0.2, -0.03), (3.2, 2.5, 0.06), FLOOR, bevel=0.01)
for i in range(1, 8):                     # plank seams
    rbox(f"Seam{i}", (-1.6 + i * 0.4, 0.2, 0.0005), (0.006, 2.5, 0.002), mat("Seam", "#9c7048"), bevel=0)
cyl("RugEdge", (0, 0.05, 0.004), 0.82, 0.008, LEAF, seg=64)
cyl("Rug", (0, 0.05, 0.009), 0.74, 0.008, CARD, seg=64)
WX0, WX1, WZ0, WZ1 = -0.85, 0.85, 1.05, 2.15  # window opening
for name, x0, x1, z0, z1 in [("WallL", -1.6, WX0, 0, 2.5), ("WallR", WX1, 1.6, 0, 2.5),
                             ("WallB", WX0, WX1, 0, WZ0), ("WallT", WX0, WX1, WZ1, 2.5)]:
    rbox(name, ((x0 + x1) / 2, WY + 0.06, (z0 + z1) / 2), (x1 - x0, 0.12, z1 - z0), WALL, bevel=0)
rbox("Skirting", (0, WY - 0.01, 0.05), (3.2, 0.02, 0.1), TRIM, bevel=0)
rbox("SideWall", (-1.66, 0.2, 1.25), (0.12, 2.5, 2.5), WALL2, bevel=0)
rbox("SideSkirting", (-1.59, 0.2, 0.05), (0.02, 2.5, 0.1), TRIM, bevel=0)
# window frame, mullions, sill
fw = 0.05
for name, loc, size in [("FrameL", (WX0 + fw / 2, WY + 0.03, 1.6), (fw, 0.08, WZ1 - WZ0)),
                        ("FrameR", (WX1 - fw / 2, WY + 0.03, 1.6), (fw, 0.08, WZ1 - WZ0)),
                        ("FrameT", (0, WY + 0.03, WZ1 - fw / 2), (WX1 - WX0, 0.08, fw)),
                        ("FrameB", (0, WY + 0.03, WZ0 + fw / 2), (WX1 - WX0, 0.08, fw)),
                        ("Mullion", (0, WY + 0.05, 1.6), (0.035, 0.05, WZ1 - WZ0)),
                        ("Transom", (0, WY + 0.05, 1.82), (WX1 - WX0, 0.05, 0.035))]:
    rbox(name, loc, size, TRIM, bevel=0.008)
rbox("Sill", (0, WY - 0.07, WZ0 - 0.02), (1.9, 0.2, 0.04), TRIM, bevel=0.01)
# outside: sky, sun/moon, city, trees, drifting clouds
rbox("SkyPanel", (0, WY + 0.75, 1.6), (2.6, 0.02, 1.6), SKY, bevel=0)
orb = sphere("SunMoon", (0.45, WY + 0.72, 1.98), (0.11, 0.01, 0.11), ORB)
city = [(-1.0, 0.5), (-0.78, 0.75), (-0.55, 0.42), (-0.36, 0.9), (-0.12, 0.55), (0.1, 0.68), (0.3, 0.4), (0.5, 0.82), (0.72, 0.5), (0.95, 0.66)]
boxes("City", [((x, WY + 0.62, 0.8 + h / 2), (0.2, 0.04, h)) for x, h in city], mat("City", "#8fbfa8", 0.9))
boxes("CityWindows", [((x - 0.04 + (k % 2) * 0.08, WY + 0.6, 0.95 + (k // 2) * 0.12), (0.03, 0.01, 0.05))
                      for x, h in city for k in range(int(h / 0.12) * 2) if 0.95 + (k // 2) * 0.12 < 0.8 + h - 0.05],
      mat("CityLights", "#fffdf7", 0.5, emit=0.4))
for i, (x, r) in enumerate([(-0.7, 0.16), (-0.45, 0.12), (0.2, 0.14), (0.65, 0.17)]):
    sphere(f"Tree{i}", (x, WY + 0.45, 1.0 + r * 0.3), (r, r * 0.6, r), LEAF)
clouds = []
for i, (z, s0) in enumerate([(1.95, 0.0), (1.72, 0.5)]):
    c = empty(f"Cloud{i}", (0, WY + 0.68, z), root)
    for j, (dx, dz, r) in enumerate([(-0.08, 0, 0.06), (0, 0.025, 0.08), (0.09, 0, 0.06)]):
        sphere(f"Cloud{i}_{j}", (dx, 0, dz), (r, 0.02, r * 0.75), mat("Cloud", "#ffffff", 1.0, emit=0.4), parent=c)
    clouds.append((c, s0))
# curtains on a rod, gently moving in the breeze
# Each curtain is built in CURTAIN_STEPS positions from open to closed (material Curtain{k}); the page shows
# one at a time and steps through them so the curtains draw shut at night.
CURTAIN_STEPS = 8
CY = 1.105                                # in front of the sill, just behind the desk
rbox("Rod", (0, CY, 2.3), (2.7, 0.025, 0.025), METAL, bevel=0.01)
def curtain_mat(k):
    m = mat(f"Curtain{k}", "#f2b134", 1.0)
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Alpha"].default_value = 1.0 if k == 0 else 0.0   # open by default
    for attr, val in (("surface_render_method", "BLENDED"), ("blend_method", "BLEND")):
        try: setattr(m, attr, val)
        except (AttributeError, TypeError): pass
    return m
curtains = []
for s in (-1, 1):
    pv = empty(f"CurtainPivot{s}", (1.27 * s, CY, 2.3), root)   # hangs from the outer end of the rod
    for k in range(CURTAIN_STEPS):
        w = 0.42 + (1.29 - 0.42) * k / (CURTAIN_STEPS - 1)          # inner edge slides to the middle
        amp = 0.022 * (0.42 / w) ** 0.5                              # folds flatten as the fabric stretches
        bm = bmesh.new()
        nx, nz, h = 32, 6, 1.45
        vs = [[bm.verts.new((-s * i / nx * w, amp * math.sin(i / nx * math.pi * 6), -j / nz * h)) for i in range(nx + 1)]
              for j in range(nz + 1)]
        for j in range(nz):
            for i in range(nx):
                bm.faces.new((vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i]))
        o = mesh_from_bm(f"Curtain{s}_{k}", bm); o.parent = pv
        sol = o.modifiers.new("thick", "SOLIDIFY"); sol.thickness = 0.012
        finish(o, curtain_mat(k), 0)
    curtains.append(pv)
# window sill plants
cyl("SillPot", (-0.55, WY - 0.08, WZ0 + 0.05), 0.05, 0.1, CORAL, r2=0.06)
for k in range(3):
    sphere(f"Cactus{k}", (-0.55 + (k - 1) * 0.03, WY - 0.08, WZ0 + 0.13 + 0.04 * (k == 1)), (0.025, 0.025, 0.06 + 0.03 * (k == 1)), LEAF)
cyl("SillPot2", (0.6, WY - 0.08, WZ0 + 0.045), 0.045, 0.09, CARD)
sphere("SillPlant", (0.6, WY - 0.08, WZ0 + 0.13), (0.07, 0.07, 0.06), LEAF)
# wall clock (back wall, right of window)
clk = empty("Clock", (1.22, WY - 0.02, 1.85), root)
cyl("ClockFace", (0, 0, 0), 0.15, 0.03, CARD, parent=clk, rot=(math.pi / 2, 0, 0))
bpy.ops.mesh.primitive_torus_add(major_radius=0.15, minor_radius=0.014, major_segments=40, minor_segments=8)
t = bpy.context.active_object; t.name = "ClockRim"; t.parent = clk; t.rotation_euler = (math.pi / 2, 0, 0); finish(t, INK, 0)
for k in range(12):
    a = k * math.pi / 6
    rbox(f"Tick{k}", (0.12 * math.sin(a), -0.017, 0.12 * math.cos(a)), (0.008, 0.004, 0.022 if k % 3 else 0.034), INK, bevel=0, parent=clk,
         rot=(0, a, 0))
mh = empty("MinuteHand", (0, -0.02, 0), clk); rbox("MinuteMesh", (0, 0, 0.05), (0.01, 0.004, 0.11), INK, bevel=0, parent=mh)
hh = empty("HourHand", (0, -0.024, 0), clk); rbox("HourMesh", (0, 0, 0.035), (0.016, 0.004, 0.075), CORAL, bevel=0, parent=hh)
hh.rotation_euler = (0, 1.2, 0)
# side wall: shelf with books + framed poster
rbox("Shelf", (-1.5, 0.55, 1.45), (0.2, 0.7, 0.03), WOOD, bevel=0.005)
for k, (h, m) in enumerate([(0.22, CORAL), (0.18, ACC), (0.24, LEAF), (0.2, CARD), (0.16, INK)]):
    rbox(f"ShelfBook{k}", (-1.5, 0.3 + k * 0.055, 1.465 + h / 2), (0.15, 0.045, h), m, bevel=0.004)
sphere("ShelfPlant", (-1.5, 0.78, 1.53), (0.07, 0.07, 0.07), LEAF)
cyl("ShelfPot", (-1.5, 0.78, 1.49), 0.05, 0.08, CARD)
rbox("PosterFrame", (-1.59, -0.15, 1.6), (0.02, 0.55, 0.42), INK, bevel=0.005)
rbox("Poster", (-1.578, -0.15, 1.6), (0.01, 0.49, 0.36), ACC, bevel=0)
text("PosterText", "</>", (-1.57, -0.15, 1.6), 0.18, INK, extrude=0.006, rot=(math.pi / 2, 0, math.pi / 2))
# floor plant in the corner
cyl("BigPot", (1.3, 0.95, 0.18), 0.17, 0.36, CARD, r2=0.2)
for k, (ang, tilt, ln) in enumerate([(0, 0.1, 0.9), (1.1, 0.45, 0.8), (2.3, 0.5, 0.75), (3.4, 0.45, 0.85), (4.6, 0.5, 0.7), (5.6, 0.4, 0.8)]):
    lf = sphere(f"BigLeaf{k}", (1.3, 0.95, 0.36), (0.09, 0.025, ln / 2), LEAF, seg=16, ring=10)
    lf.rotation_euler = (tilt, 0, ang)
    lf.location.z += ln / 2 * math.cos(tilt)
    lf.location.x -= math.sin(tilt) * math.sin(ang) * ln / 2
    lf.location.y += math.sin(tilt) * math.cos(ang) * ln / 2

# ── desk ──
DY = 0.69                                  # desk centre (front edge ~0.31)
rbox("DeskTop", (0, DY, 0.705), (1.9, 0.76, 0.04), WOOD, bevel=0.012)
for s in (-1, 1):
    rbox(f"DeskLeg{s}", (0.88 * s, DY, 0.35), (0.05, 0.62, 0.05), METAL, bevel=0.01)
    rbox(f"DeskPost{s}", (0.88 * s, DY, 0.36), (0.05, 0.05, 0.68), METAL, bevel=0.01)
    rbox(f"DeskFoot{s}", (0.88 * s, DY, 0.02), (0.06, 0.66, 0.04), METAL, bevel=0.01)
rbox("DeskBeam", (0, DY + 0.25, 0.62), (1.76, 0.04, 0.05), METAL, bevel=0.01)
rbox("DeskMat", (0.05, 0.47, 0.728), (0.95, 0.36, 0.006), mat("Felt", "#34443f", 1.0), bevel=0.004)
rbox("KbBase", (0, 0.44, 0.738), (0.44, 0.14, 0.016), CARD, bevel=0.005)
boxes("Keys", [((-0.2 + c * 0.0335 + (r % 2) * 0.01, 0.395 + r * 0.03, 0.75), (0.028, 0.024, 0.01))
               for r in range(4) for c in range(12)], mat("KeyCap", "#e7e1d3", 0.5))
rbox("Spacebar", (0, 0.505, 0.75), (0.17, 0.024, 0.01), mat("KeyCap", "#e7e1d3", 0.5), bevel=0.003)
mouse = rbox("Mouse", (0.36, 0.45, 0.745), (0.06, 0.1, 0.03), CARD, bevel=0.014)
# mug + steam, notebook, phone, lamp
cyl("Mug", (0.6, 0.52, 0.775), 0.045, 0.1, CORAL)
limb("MugHandle", (0.646, 0.52, 0.8), (0.646, 0.52, 0.755), 0.012, CORAL)
cyl("Coffee", (0.6, 0.52, 0.823), 0.04, 0.004, mat("Coffee", "#4a2a1a"))
steam = [sphere(f"Steam{i}", (0.6, 0.52, 0.84), (0.018, 0.018, 0.018), mat("Steam", "#ffffff", 1.0, emit=0.2), seg=12, ring=8)
         for i in range(3)]
rbox("Notebook", (-0.52, 0.5, 0.735), (0.2, 0.26, 0.018), ACC, bevel=0.004, rot=(0, 0, 0.15))
rbox("NotebookPage", (-0.52, 0.5, 0.745), (0.18, 0.24, 0.004), CARD, bevel=0, rot=(0, 0, 0.15))
limb("Pen", (-0.6, 0.42, 0.75), (-0.45, 0.47, 0.75), 0.006, INK)
rbox("Phone", (-0.3, 0.52, 0.731), (0.07, 0.14, 0.008), INK, bevel=0.006, rot=(0, 0, -0.2))
lamp = empty("Lamp", (-0.8, 0.88, 0.725), root)
cyl("LampBase", (0, 0, 0.012), 0.07, 0.024, INK, parent=lamp)
limb("LampArm1", (0, 0, 0.02), (0.05, -0.04, 0.42), 0.012, INK, parent=lamp)
lhead = empty("LampHeadPivot", (0.05, -0.04, 0.42), lamp)
limb("LampArm2", (0, 0, 0), (0.2, -0.12, 0.02), 0.012, INK, parent=lhead)
cyl("LampShade", (0.22, -0.13, -0.02), 0.03, 0.1, ACC, parent=lhead, r2=0.075, rot=(0.3, math.radians(170), 0))
sphere("LampBulb", (0.23, -0.14, -0.07), (0.03, 0.03, 0.03), BULB, parent=lhead)
# night-only lamp light: a soft cone and a pool on the desk (the page fades these in for dark mode)
def glow_mat(name, hexcol, alpha):
    m = mat(name, hexcol, 1.0, emit=1.0)
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Alpha"].default_value = alpha
    for attr, val in (("surface_render_method", "BLENDED"), ("blend_method", "BLEND")):
        try: setattr(m, attr, val)
        except (AttributeError, TypeError): pass
    m.use_backface_culling = False
    return m
def glow_disc(name, loc, rx, ry, m, rot=(0, 0, 0)):
    """Flat disc whose 'Glow' vertex alpha fades from the centre to nothing at the rim (soft light)."""
    bm = bmesh.new(); seg = 48
    rings = [(0.0, 1.0), (0.3, 0.85), (0.6, 0.45), (0.82, 0.15), (1.0, 0.0)]
    centre = bm.verts.new((0, 0, 0))
    vs = [[bm.verts.new((math.cos(2 * math.pi * i / seg) * r * rx, math.sin(2 * math.pi * i / seg) * r * ry, 0))
           for i in range(seg)] for r, _ in rings[1:]]
    for i in range(seg):
        j = (i + 1) % seg
        bm.faces.new((centre, vs[0][i], vs[0][j]))
        for k in range(len(vs) - 1):
            bm.faces.new((vs[k][i], vs[k + 1][i], vs[k + 1][j], vs[k][j]))
    alpha = {centre: 1.0}
    for k, (_, a) in enumerate(rings[1:]):
        for v in vs[k]: alpha[v] = a
    bm.verts.index_update()
    by_index = {v.index: a for v, a in alpha.items()}
    o = mesh_from_bm(name, bm); o.location = loc; o.rotation_euler = rot
    ca = o.data.color_attributes.new("Glow", 'FLOAT_COLOR', 'POINT')
    for i, a in by_index.items(): ca.data[i].color = (1, 1, 1, a)
    return finish(o, m, 0, smooth=False)

bm = bmesh.new()
bmesh.ops.create_cone(bm, cap_ends=False, segments=40, radius1=0.3, radius2=0.035, depth=0.34)
cone = mesh_from_bm("LampCone", bm); cone.location = (-0.49, 0.66, 0.9)
finish(cone, glow_mat("LampGlow", "#ffd27a", 0.14), 0)
glow_disc("LampPool", (-0.47, 0.64, 0.7262), 0.42, 0.42, glow_mat("LampPool", "#ffc65c", 0.22))
glow_disc("LampPoolCore", (-0.48, 0.65, 0.7268), 0.2, 0.2, glow_mat("LampPoolCore", "#ffe1a0", 0.3))
cyl("DeskPot", (0.82, 0.86, 0.78), 0.06, 0.11, CARD, r2=0.07)
for k, (ang, tilt, ln) in enumerate([(0, 0.0, 0.28), (1.3, 0.5, 0.22), (2.6, 0.55, 0.2), (4.0, 0.5, 0.24), (5.2, 0.45, 0.2)]):
    lf = sphere(f"DeskLeaf{k}", (0.82, 0.86, 0.84), (0.03, 0.012, ln / 2), LEAF, seg=12, ring=8)
    lf.rotation_euler = (tilt, 0, ang)
    lf.location.z += ln / 2 * math.cos(tilt)
    lf.location.x -= math.sin(tilt) * math.sin(ang) * ln / 2
    lf.location.y += math.sin(tilt) * math.cos(ang) * ln / 2

# ── three monitors on a shared arm, screens facing the chair (and the viewer) ──
rbox("ArmPole", (0, 0.98, 0.95), (0.04, 0.04, 0.46), METAL, bevel=0.008)
rbox("ArmClamp", (0, 0.98, 0.715), (0.08, 0.08, 0.03), METAL, bevel=0.008)
rbox("ArmBar", (0, 0.95, 1.06), (1.2, 0.03, 0.03), METAL, bevel=0.008)
MW, MH = 0.6, 0.35
monitors = {}
for key, x, y, yaw in [("center", 0, 0.9, 0), ("left", -0.6, 0.75, 0.5), ("right", 0.6, 0.75, -0.5)]:
    m = empty(f"Mon_{key}", (x, y, 1.06), root); m.rotation_euler = (0, 0, yaw)
    rbox(f"Bezel_{key}", (0, 0, 0), (MW + 0.03, 0.03, MH + 0.03), BEZEL, bevel=0.008, parent=m)
    rbox(f"BackHump_{key}", (0, 0.03, 0), (0.24, 0.04, 0.16), BEZEL, bevel=0.02, parent=m)
    monitors[key] = m
# night-only screen light spilling into the room (the page fades these in for dark mode)
glow_disc("SpillDesk", (0, 0.58, 0.7258), 1.05, 0.4, glow_mat("SpillDesk", "#a8dcff", 0.2))
glow_disc("SpillDeskCore", (0, 0.66, 0.7262), 0.65, 0.22, glow_mat("SpillDeskCore", "#d6f0ff", 0.22))
glow_disc("SpillFloor", (0, 0.05, 0.0145), 1.25, 0.95, glow_mat("SpillFloor", "#8fcfff", 0.12))
glow_disc("SpillFloorCore", (0, 0.15, 0.0152), 0.7, 0.5, glow_mat("SpillFloorCore", "#b8e4ff", 0.14))
for k, (rx, rz, a) in enumerate([(1.4, 0.45, 0.12), (1.0, 0.32, 0.16), (0.75, 0.22, 0.2)]):
    glow_disc(f"SpillHalo{k}", (0, 1.075 - k * 0.004, 1.15), rx, rz, glow_mat(f"SpillHalo{k}", "#9fd8ff", a), rot=(math.pi / 2, 0, 0))

SY = -0.017   # screen surface, monitor-local
def scr(name, mon, x, z, w, h, m, dy=0.0, parent=None):
    return rbox(name, (x, SY - dy, z), (w, 0.002, h), m, bevel=0, parent=parent or mon)

# centre: code editor typing itself out
mc = monitors["center"]
scr("CodeBg", mc, 0, 0, MW, MH, S_DARK)
scr("CodeTabs", mc, 0, MH / 2 - 0.015, MW, 0.03, E_GREY, 0.001)
scr("CodeTab", mc, -0.22, MH / 2 - 0.015, 0.12, 0.03, S_DARK, 0.002)
scr("CodeGutter", mc, -0.275, -0.015, 0.035, MH - 0.03, mat("ScrGutter", "#13211d", 0.5, emit=0.2), 0.001)
code_lines = []
spec = [(0.0, 0.2, E_CORAL), (0.03, 0.3, E_CREAM), (0.06, 0.24, E_LEAF), (0.06, 0.32, E_CREAM), (0.03, 0.14, E_ACC),
        (0.06, 0.28, E_LIME), (0.03, 0.22, E_CREAM), (0.0, 0.1, E_CORAL)]
for i, (ind, w, m) in enumerate(spec):
    z = MH / 2 - 0.06 - i * 0.034
    scr(f"LineNo{i}", mc, -0.275, z, 0.012, 0.012, E_GREY, 0.002)
    pv = empty(f"CodeLine{i}", (-0.235 + ind, SY - 0.002, z), mc)
    rbox(f"CodeLineBar{i}", (w / 2, 0, 0), (w, 0.002, 0.013), m, bevel=0, parent=pv)
    code_lines.append(pv)
cursor = scr("Cursor", mc, -0.235 + 0.11, MH / 2 - 0.06 - 7 * 0.034, 0.006, 0.02, E_LIME, 0.003)

# left: dashboard
ml = monitors["left"]
scr("DashBg", ml, 0, 0, MW, MH, S_LIGHT)
scr("DashNav", ml, -0.255, 0, 0.09, MH, mat("ScrNav", "#10302a", 0.5, emit=0.15), 0.001)
for k, m in enumerate((E_ACC, E_LEAF, E_CORAL)):
    scr(f"Kpi{k}", ml, -0.13 + k * 0.13, 0.115, 0.11, 0.07, m, 0.001)
dash_bars = []
for k, m in enumerate((E_LEAF, E_ACC, E_CORAL, E_LEAF, E_ACC, E_CORAL)):
    pv = empty(f"DashBar{k}", (-0.17 + k * 0.045, SY - 0.002, -0.15), ml)
    rbox(f"DashBarMesh{k}", (0, 0, 0.09), (0.028, 0.002, 0.18), m, bevel=0, parent=pv)
    dash_bars.append(pv)
ring = empty("DashRing", (0.18, SY - 0.004, -0.05), ml)
bpy.ops.mesh.primitive_torus_add(major_radius=0.065, minor_radius=0.014, major_segments=40, minor_segments=6)
tor = bpy.context.active_object; tor.name = "DashRingMesh"; tor.parent = ring; tor.rotation_euler = (math.pi / 2, 0, 0)
tor.scale = (1, 1, 0.15); finish(tor, E_ACC, 0)
sphere("DashRingNotch", (0.065, 0, 0), (0.022, 0.004, 0.022), E_CORAL, parent=ring)

# right: AI chat with messages arriving
mr = monitors["right"]
scr("ChatBg", mr, 0, 0, MW, MH, S_MINT)
scr("ChatHead", mr, 0, MH / 2 - 0.02, MW, 0.04, mat("ScrHead", "#10302a", 0.5, emit=0.15), 0.001)
scr("ChatInput", mr, 0, -MH / 2 + 0.03, MW - 0.06, 0.035, S_LIGHT, 0.001)
chat_msgs = []
for k, (side, w, m) in enumerate([(1, 0.22, E_LEAF), (-1, 0.3, S_LIGHT), (1, 0.16, E_LEAF), (-1, 0.34, S_LIGHT)]):
    z = MH / 2 - 0.075 - k * 0.058
    x = side * (MW / 2 - 0.03 - w / 2)
    pv = empty(f"ChatMsg{k}", (x, SY - 0.002, z), mr)
    rbox(f"ChatMsgMesh{k}", (0, 0, 0), (w, 0.002, 0.042), m, bevel=0, parent=pv)
    chat_msgs.append(pv)
chat_dots = [sphere(f"ChatDot{k}", (-0.24 + k * 0.025, SY - 0.004, -MH / 2 + 0.075), (0.008, 0.002, 0.008), E_INK, parent=mr)
             for k in range(3)]

# ── office chair: base rolls back, top swivels ──
chair = empty("ChairRoot", (0, 0, 0), root)
cyl("GasLift", (0, 0, 0.27), 0.022, 0.3, METAL, parent=chair)
cyl("Hub", (0, 0, 0.11), 0.05, 0.05, METAL, parent=chair)
for k in range(5):
    a = k * 2 * math.pi / 5 + 0.3
    limb(f"ChairLeg{k}", (0, 0, 0.1), (0.28 * math.cos(a), 0.28 * math.sin(a), 0.07), 0.018, METAL, parent=chair)
    sphere(f"Caster{k}", (0.28 * math.cos(a), 0.28 * math.sin(a), 0.03), (0.03, 0.022, 0.03), INK, parent=chair)
swivel = empty("Swivel", (0, 0, 0), chair)
top = empty("ChairTop", (0, 0, 0), swivel); top.rotation_euler = (0, 0, math.pi)   # person-local: facing -Y
rbox("Seat", (0, -0.02, 0.45), (0.5, 0.48, 0.08), CHAIR, bevel=0.035, parent=top)
rbox("SeatPan", (0, -0.02, 0.4), (0.36, 0.34, 0.03), METAL, bevel=0.01, parent=top)
rbox("BackSpine", (0, 0.25, 0.6), (0.06, 0.03, 0.3), METAL, bevel=0.01, parent=top, rot=(-0.1, 0, 0))
rbox("Backrest", (0, 0.27, 0.82), (0.46, 0.07, 0.36), CHAIR, bevel=0.035, parent=top, rot=(-0.12, 0, 0))
for s in (-1, 1):
    rbox(f"ArmPost{s}", (0.27 * s, 0.02, 0.56), (0.03, 0.03, 0.2), METAL, bevel=0.008, parent=top)
    rbox(f"ArmPad{s}", (0.27 * s, -0.04, 0.665), (0.06, 0.24, 0.03), CHAIR, bevel=0.012, parent=top)

# ── person (person-local: facing -Y, right side = -X) ──
person = empty("Person", (0, 0, 0), top)
body = empty("Body", (0, 0, 0), person)
sphere("Hips", (0, 0.02, 0.55), (0.18, 0.13, 0.09), JEANS, parent=body)
sphere("Belly", (0, 0.0, 0.67), (0.165, 0.115, 0.13), SHIRT, parent=body)
sphere("Chest", (0, 0.0, 0.86), (0.2, 0.125, 0.21), SHIRT, parent=body)
for s in (-1, 1):
    sphere(f"ShoulderBall{s}", (0.17 * s, 0.0, 0.975), (0.06, 0.06, 0.05), SHIRT, parent=body)
cyl("Collar", (0, 0.0, 1.05), 0.065, 0.04, SHIRT, parent=body)
cyl("Neck", (0, 0.0, 1.08), 0.048, 0.1, SKIN, parent=body)
for s in (-1, 1):
    limb(f"Thigh{s}", (0.1 * s, 0.0, 0.53), (0.11 * s, -0.42, 0.53), 0.072, JEANS, parent=person)
    limb(f"Shin{s}", (0.11 * s, -0.42, 0.53), (0.11 * s, -0.46, 0.1), 0.052, JEANS, parent=person)
    sphere(f"Shoe{s}", (0.11 * s, -0.51, 0.045), (0.05, 0.11, 0.045), SHOE, parent=person)
    rbox(f"Sole{s}", (0.11 * s, -0.51, 0.008), (0.1, 0.21, 0.016), mat("Sole", "#cfc8b8"), bevel=0.006, parent=person)

# head: built at the earlier (chibi) size and scaled to realistic proportions
head = empty("Head", (0, 0, 1.11), body)
head.scale = (0.42, 0.42, 0.42)
HC = Vector((0, 0, 0.3)); HR = Vector((0.28, 0.28, 0.33))
def shell(name, scale, pieces, m, thick=0.02, parent=None):
    out = bmesh.new()
    for cuts in pieces:
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=40, radius=1)
        bmesh.ops.scale(bm, vec=Vector((HR.x * scale[0], HR.y * scale[1], HR.z * scale[2])), verts=bm.verts)
        bmesh.ops.translate(bm, vec=HC, verts=bm.verts)
        for co, no in cuts:
            bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], dist=1e-5,
                                   plane_co=Vector(co), plane_no=Vector(no).normalized(), clear_outer=True)
        tmp = bpy.data.meshes.new("tmp"); bm.to_mesh(tmp); bm.free()
        out.from_mesh(tmp); bpy.data.meshes.remove(tmp)
    bmesh.ops.remove_doubles(out, verts=out.verts, dist=1e-4)
    o = mesh_from_bm(name, out)
    sol = o.modifiers.new("thick", "SOLIDIFY"); sol.thickness = thick; sol.offset = 1
    return finish(o, m, 0, parent=parent)

sphere("Face", HC, HR, SKIN, parent=head)
for s in (-1, 1):
    sphere(f"Ear{s}", (0.275 * s, 0.02, 0.31), (0.045, 0.035, 0.07), SKIN, parent=head)
sphere("Nose", (0, -0.285, 0.27), (0.045, 0.04, 0.05), SKIN, parent=head)
shell("HairCap", (1.04, 1.04, 1.03), [[((0, -0.28, 0.5), (0, -0.35, -0.56))]], HAIR, thick=0.015, parent=head)
import random
random.seed(11)
curls = [(-0.17, -0.2, 0.58), (-0.05, -0.23, 0.6), (0.07, -0.22, 0.6), (0.18, -0.17, 0.57),
         (-0.22, -0.08, 0.6), (-0.1, -0.11, 0.67), (0.03, -0.12, 0.68), (0.15, -0.1, 0.66), (0.24, -0.05, 0.58),
         (-0.18, 0.05, 0.64), (-0.05, 0.0, 0.7), (0.09, 0.02, 0.7), (0.2, 0.07, 0.62),
         (-0.1, 0.14, 0.62), (0.05, 0.15, 0.63), (0.16, 0.18, 0.56), (-0.2, 0.17, 0.54),
         (-0.08, 0.24, 0.52), (0.08, 0.25, 0.52), (0.0, 0.2, 0.6)]
for i, c in enumerate(curls):
    r = 0.07 + random.random() * 0.02
    sphere(f"Curl{i}", c, (r, r, r * 0.9), HAIR, parent=head, seg=16, ring=10)
a = math.radians(24)
shell("Beard", (1.04, 1.08, 1.05),
      [[((0, 0, 0), (-s, 0, 0)), ((0, 0, 0.15), (-s * math.sin(a), 0, math.cos(a))), ((0, 0.06, 0), (0, 1, 0))]
       for s in (1, -1)], HAIR, thick=0.02, parent=head)
for s in (-1, 1):
    limb(f"Moustache{s}", (0, -0.3, 0.215), (0.085 * s, -0.285, 0.19), 0.026, HAIR, parent=head)
mouth = sphere("Mouth", (0, -0.292, 0.168), (0.045, 0.02, 0.03), MOUTH, parent=head, bake=False)
lip = sphere("Lip", (0, -0.298, 0.15), (0.058, 0.022, 0.022), LIP, parent=head, bake=False)
eyes, brows = [], []
for s in (-1, 1):
    ep = empty(f"EyePivot{s}", (0.1 * s, -0.25, 0.36), head)
    sphere(f"EyeWhite{s}", (0, 0, 0), (0.05, 0.02, 0.034), WHITE, parent=ep)
    sphere(f"Iris{s}", (0.004 * s, -0.016, -0.002), (0.026, 0.012, 0.03), HAIR, parent=ep)
    eyes.append(ep)
    bp = empty(f"BrowPivot{s}", (0.1 * s, -0.265, 0.435), head)
    rbox(f"Brow{s}", (0, 0, 0), (0.12, 0.035, 0.034), HAIR, bevel=0.014, parent=bp, rot=(0, 0.14 * s, 0))
    brows.append(bp)

# arms: shoulder -> elbow chain, short sleeves
arms = {}
for s in (-1, 1):
    sh = empty(f"Shoulder{s}", (0.2 * s, 0.0, 0.99), body)
    limb(f"UpperArm{s}", (0, 0, 0), (0, 0, -0.27), 0.047, SHIRT, parent=sh)
    el = empty(f"Elbow{s}", (0, 0, -0.27), sh)
    limb(f"Forearm{s}", (0, 0, 0), (0, 0, -0.23), 0.036, SKIN, parent=el)
    hand = empty(f"Hand{s}", (0, 0, -0.27), el)
    sphere(f"Palm{s}", (0, 0, 0), (0.042, 0.024, 0.06), SKIN, parent=hand)
    sphere(f"Thumb{s}", (-0.035 * s, -0.012, 0.01), (0.014, 0.014, 0.03), SKIN, parent=hand)
    arms[s] = (sh, el, hand)

# "hello!" bubble near the head once turned, facing the default camera
bub = empty("Bubble", (0.5, -0.3, 1.72), root)
bub.rotation_euler = (0, 0, math.radians(22))
rbox("BubbleCard", (0, 0, 0), (0.66, 0.04, 0.16), mat("Bubble", "#fffdf7", 0.6), bevel=0.07, parent=bub)
star("BubbleTail", (-0.23, 0, -0.085), 0.055, mat("Bubble", "#fffdf7", 0.6), depth=0.035, parent=bub)
text("BubbleText", "hi, I'm Akhiljith!", (0, -0.025, 0.0), 0.085, mat("BubbleText", "#e0573b", 0.7), extrude=0.01, parent=bub)

# ── animation ──
def smooth(e0, e1, f):
    t = min(max((f - e0) / (e1 - e0), 0), 1); return t * t * (3 - 2 * t)
def key_fn(obj, path, idx, fn, step=2):
    for f in range(1, FRAMES + 2, step):
        if idx is None: setattr(obj, path, fn(f)); obj.keyframe_insert(path, frame=f)
        else: getattr(obj, path)[idx] = fn(f); obj.keyframe_insert(path, index=idx, frame=f)
def linear(obj):
    act = obj.animation_data.action
    curves = list(getattr(act, "fcurves", []) or [])
    for layer in getattr(act, "layers", []):
        for strip in layer.strips:
            for bag in getattr(strip, "channelbags", []): curves += list(bag.fcurves)
    for fc in curves:
        for k in fc.keyframe_points: k.interpolation = 'LINEAR'
sin = lambda f, period, ph=0: math.sin(2 * math.pi * ((f - 1) / period + ph))
lerp = lambda a, b, t: a + (b - a) * t

turn = lambda f: smooth(86, 108, f) * (1 - smooth(150, 172, f))          # chair swivel
look = lambda f: smooth(80, 100, f) * (1 - smooth(156, 174, f))          # head leads, then lags back
wave = lambda f: smooth(100, 114, f) * (1 - smooth(138, 152, f))         # right arm up
work = lambda f: 1 - smooth(82, 92, f) * (1 - smooth(166, 176, f))       # typing amount

key_fn(chair, "location", 1, lambda f: -0.16 * smooth(84, 104, f) * (1 - smooth(152, 170, f)))
key_fn(swivel, "rotation_euler", 2, lambda f: math.radians(-150) * turn(f))
# head: glances between monitors while working, then looks back over the right shoulder
key_fn(head, "rotation_euler", 2, lambda f: 0.32 * math.sin(2 * math.pi * (f - 1) / 96) * (1 - look(f)) + math.radians(-18) * look(f))
key_fn(head, "rotation_euler", 0, lambda f: 0.04 * sin(f, 32) * work(f) - 0.08 * look(f))
key_fn(head, "rotation_euler", 1, lambda f: -0.1 * wave(f))
key_fn(body, "rotation_euler", 2, lambda f: math.radians(-8) * look(f))   # shoulders follow a little
key_fn(body, "location", 2, lambda f: 0.004 * sin(f, 48))                # breathing
for b in brows:
    key_fn(b, "location", 2, lambda f: 0.435 + 0.03 * wave(f))
# "hel-lo!" mouth shapes, and a smile while waving
def talk(f):
    return max(math.sin(math.pi * min(max((f - 110) / 6, 0), 1)), math.sin(math.pi * min(max((f - 118) / 9, 0), 1)) * 1.2)
key_fn(mouth, "scale", 2, lambda f: 0.03 * (0.15 + 0.85 * talk(f)), step=1)
key_fn(lip, "scale", 0, lambda f: 0.058 * (1 + 0.25 * wave(f)))
for e in eyes:
    def blink(f):
        for c in (40, 128, 182):
            if abs(f - c) <= 3: return 0.15 + 0.85 * abs(f - c) / 3
        return 1.0
    key_fn(e, "scale", 2, blink, step=1)

# arms. Typing pose: upper arm a little forward, forearm level over the keyboard.
for s, ph in ((-1, 0.0), (1, 0.5)):
    sh, el, hand = arms[s]
    key_fn(sh, "rotation_euler", 0, lambda f, ph=ph: -0.38 + 0.035 * sin(f, 8, ph) * work(f))
    key_fn(sh, "rotation_euler", 1, lambda f, s=s: -0.12 * s * work(f) + 0.12 * s * (1 - work(f)))
    key_fn(el, "rotation_euler", 0, lambda f, ph=ph: -1.22 - 0.05 * sin(f, 8, ph + 0.25) * work(f))
    key_fn(hand, "rotation_euler", 0, lambda f: 0.15)
# right arm (-X) raises out to the side and waves from the elbow
sh, el, hand = arms[-1]
key_fn(sh, "rotation_euler", 0, lambda f: lerp(-0.38 + 0.035 * sin(f, 8) * work(f), -0.2, wave(f)))
key_fn(sh, "rotation_euler", 1, lambda f: lerp(0.12 * work(f) - 0.12 * (1 - work(f)), 1.3, wave(f)))
key_fn(el, "rotation_euler", 0, lambda f: lerp(-1.22 - 0.05 * sin(f, 8, 0.25) * work(f), 0.0, wave(f)))
key_fn(el, "rotation_euler", 1, lambda f: wave(f) * (1.75 + 0.32 * sin(f - 112, 12)))
key_fn(hand, "rotation_euler", 0, lambda f: 0.15 * (1 - wave(f)))

def pop(f):
    g = smooth(104, 114, f); out = smooth(146, 154, f)
    return max(0.0, g * (1 + 0.25 * math.sin(math.pi * g)) * (1 - out))
key_fn(bub, "scale", None, lambda f: (1.5 * pop(f),) * 3)

# screens
for i, ln in enumerate(code_lines):
    st0 = 4 + i * 10
    key_fn(ln, "scale", 0, lambda f, s=st0: max(0.001, smooth(s, s + 7, f) * (1 - smooth(178, 188, f))), step=1)
key_fn(cursor, "scale", 2, lambda f: 1.0 if ((f - 1) // 12) % 2 == 0 else 0.0, step=1)
for k, pv in enumerate(dash_bars):
    key_fn(pv, "scale", 2, lambda f, k=k: 0.3 + 0.65 * (0.5 + 0.5 * sin(f, 96, k * 0.17)))
key_fn(ring, "rotation_euler", 1, lambda f: -2 * math.pi * (f - 1) / 96, step=4); linear(ring)
for k, pv in enumerate(chat_msgs):
    st0 = 10 + k * 22
    key_fn(pv, "scale", None, lambda f, s=st0: (max(0.001, smooth(s, s + 6, f) * (1 - smooth(178, 186, f))),) * 3, step=1)
for k, d in enumerate(chat_dots):
    key_fn(d, "location", 2, lambda f, k=k: -MH / 2 + 0.075 + 0.008 * max(0, sin(f, 16, -k * 0.15)), step=1)
# mouse nudges while working
key_fn(mouse, "location", 0, lambda f: 0.36 + 0.01 * sin(f, 48) * work(f))
# room life: steam, clock, clouds, curtains
for i, st in enumerate(steam):
    ph = i / 3
    key_fn(st, "location", 2, lambda f, ph=ph: 0.84 + 0.16 * (((f - 1) / 64 + ph) % 1))
    key_fn(st, "scale", None, lambda f, ph=ph: (1.2 * (1 - (((f - 1) / 64 + ph) % 1)) ** 0.7,) * 3, step=1)
    key_fn(st, "location", 0, lambda f, ph=ph: 0.6 + 0.015 * math.sin(2 * math.pi * (((f - 1) / 64 + ph) % 1) * 1.5))
key_fn(mh, "rotation_euler", 1, lambda f: 2 * math.pi * (f - 1) / FRAMES, step=4); linear(mh)
key_fn(hh, "rotation_euler", 1, lambda f: 1.2 + 2 * math.pi * (f - 1) / FRAMES / 12, step=8); linear(hh)
for c, s0 in clouds:
    key_fn(c, "location", 0, lambda f, s0=s0: -1.2 + 2.4 * (((f - 1) / FRAMES + s0) % 1), step=1)
for k, pv in enumerate(curtains):
    key_fn(pv, "rotation_euler", 0, lambda f, k=k: 0.035 * sin(f, 96, k * 0.3) - 0.02)
    key_fn(pv, "rotation_euler", 1, lambda f, k=k: 0.015 * sin(f, 64, k * 0.5))

cam = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera")); link(cam)
cam.location = (1.6, -3.6, 2.2); cam.data.lens = 32
cam.rotation_euler = (Vector((0.0, 0.5, 1.05)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam
sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", 'SUN')); link(sun)
sun.data.energy = 3.0; sun.rotation_euler = (math.radians(50), 0, math.radians(200))
print("built", len(bpy.data.objects))
