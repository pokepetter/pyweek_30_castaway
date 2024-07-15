if __name__ == '__main__':
    from ursina import *
    app = Ursina()
    from ursina.shaders import colored_lights_shader
    Entity.default_shader = colored_lights_shader
    level = load_blender_scene(name='castaway_island', reload=True)
    if hasattr(level, 'mesh_collider'):
        level.mesh_collider.enabled = False
    for e in level.children:
        if 'collider' in e.name:
            e.enabled = False

    EditorCamera()
    app.run()