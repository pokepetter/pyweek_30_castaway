if __name__ == '__main__':
    from ursina import *
    app = Ursina()
    from ursina.shaders import colored_lights_shader
    Entity.default_shader = colored_lights_shader
    load_blender_scene(name='castaway_items', reload=True)
    EditorCamera()
    app.run()