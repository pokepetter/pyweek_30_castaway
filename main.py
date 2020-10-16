from ursina import *
from ursina.shaders import colored_lights_shader

# window.vsync = False
if not application.development_mode:
    window.show_ursina_splash = True
app = Ursina()


# t = time.time()
level = load_blender_scene('castaway_island',
    # reload=True
    )
# print('reload_total:', time.time() - t)
t = time.time()
level.mesh_collider.collider = 'mesh'
level.mesh_collider.visible = False

level.water.color = color.color(160,1,.8,.5)
level.water.enabled = False
Entity(model='plane', position=level.water.position, scale=9999, color=color.color(160,1,.8,.5), double_sided=True)
scene.fog_color = color.color(6, .1, .85)


level.chest.collider = 'box'
level.chest_lid.collider = 'box'
level.chest_lid.double_sided = True

level.bow.parent = camera
level.bow.position = (.5,0,1)
level.bow.enabled = False
level.bow.shader = colored_lights_shader

level.gate.collider = 'box'
level.gate_001.collider = 'box'
level.gate_pattern.world_parent = level.gate
level.gate_pattern_001.world_parent = level.gate_001

level.eye_trigger.collider = 'box'
level.goat.collider = 'mesh'



from ursina.prefabs.first_person_controller import FirstPersonController
player = FirstPersonController(position=level.start_point.position, speed=10)
level.start_point.enabled = False


for e in level.children:
    if not 'terrain' in e.name:
        e.shader = colored_lights_shader

    if 'box_collider' in e.name:
        e.visible = False
        e.collider = 'box'

    if 'pebble' in e.name:
        e.position = raycast(e.position, Vec3(0,-1,0)).world_point

    elif 'rock' in e.name:
        e.collider='box'
        e.flip_faces()

    elif e.name == 'ship':
        e.collider = 'mesh'

    elif 'tree' in e.name:
        e.collider = 'mesh'

def open_chest():
    if distance_xz(player.position, level.chest.position) < 6:
        level.chest_lid.animate('rotation_x', level.chest_lid.rotation_x + 120, duration=.2)
        invoke(setattr, level.bow, 'enabled', True, delay=.25)
        # make sure we can only open it once
        level.chest.on_click = None
        level.chest_lid.on_click = None

level.chest.on_click = open_chest
level.chest_lid.on_click = open_chest


player.original_speed = player.speed
def input(key):
    if key == 'shift':
        player.speed = player.original_speed * 10
    elif key == 'shift up':
        player.speed = player.original_speed

    if level.bow.enabled and key == 'left mouse down':
        player.arrow = duplicate(level.arrow, world_parent=level.bow, position=Vec3(-.2,0,0), rotation=Vec3(0,0,0))
        player.arrow.animate('z', -2, duration=.2, curve=curve.linear)

    if level.bow.enabled and key == 'left mouse up':
        if mouse.hovered_entity:
            # print('hit something', mouse.hovered_entity)
            player.arrow.world_parent = scene
            player.arrow.animate('world_position', Vec3(*mouse.world_point), mouse.collision.distance/500, curve=curve.linear, interrupt='finish')

            if mouse.hovered_entity == level.eye_trigger:
                invoke(open_gate, delay=.3)
                destroy(player.arrow, delay=.1)
                return

            destroy(player.arrow, delay=10)

        else:
            player.arrow.animate('world_position', player.arrow.world_position+(player.arrow.forward*100), .5, curve=curve.linear, interrupt='finish')
            destroy(player.arrow, delay=1)

    # cheat buttons
    if key == 'f1':
        level.bow.enabled = True

    if key == 'f2':
        open_gate()

    if held_keys['control'] and key == 'r':
        player.position = level.start_point.position



orginal_chest_color = level.chest.color
def update():
    if not level.bow.enabled and mouse.hovered_entity in (level.chest, level.chest_lid) and distance_xz(player.position, level.chest.position) < 6:
        level.chest.color = color.color(90, .4, .8)
        level.chest_lid.color = color.color(90, .4, .8)
    else:
        level.chest.color = orginal_chest_color
        level.chest_lid.color = orginal_chest_color



def open_gate():
    destroy(level.eye)
    destroy(level.eye_trigger)
    level.gate.animate_position(level.gate.position+(level.gate.left)*10, duration=5, curve=curve.linear)
    level.gate_001.animate_position(level.gate_001.position+(level.gate_001.right)*10, duration=5, curve=curve.linear)


Sky(texture='castaway_sky')
# EditorCamera()

app.run()
