import bpy, os
def export_glb(name):
    out = os.path.normpath(os.path.join(S, "..", "assets", "3d"))   # S = this blender/ folder, set by the runner
    os.makedirs(out, exist_ok=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in bpy.context.scene.objects:
        if o.type in ('MESH', 'EMPTY'): o.select_set(True)
    path = os.path.join(out, name + ".glb")
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_apply=True,
                              export_animations=True, export_animation_mode='SCENE',
                              export_anim_scene_split_object=False, export_bake_animation=True,
                              export_optimize_animation_size=True, export_cameras=False, export_lights=False,
                              export_vertex_color='NAME', export_vertex_color_name='Glow',
                              export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=7)
    print(name, os.path.getsize(path) // 1024, "KB")
