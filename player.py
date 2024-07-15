from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class CastawayPlayer(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(speed=10, **kwargs)
        self.original_speed = self.speed
        self.level = load_blender_scene(name='castaway_items',
            # reload=True
            )

        self.level.enabled = False
        self.bow = duplicate(self.level.bow, parent=camera, position=(.5,0,1), )
# level.bow.enabled = False
# level.bow.shader = colored_lights_shader
        self.arrow_prefab = self.level.arrow
        # self.bow = Entity(parent=camera, model='bow', position=(.5,0,1), scale=Vec3(0.24958, 0.31452, 0.31452), ignore=True, enabled=True)
        self.arrow = None


    def input(self, key):
        if key == 'shift':
            self.speed = self.original_speed * 10
        elif key == 'shift up':
            self.speed = self.original_speed

        if self.bow.enabled and key == 'left mouse down':
            player.arrow = duplicate(self.arrow_prefab, world_parent=self.bow, position=Vec3(-.2,0,0), rotation=Vec3(0,0,0))
            self.arrow.animate('position', self.arrow.position+Vec3(0,0,-2), duration=.2, curve=curve.linear)
            # self.arrow.shader = colored_lights_shader

        if self.bow.enabled and key == 'left mouse up':
            hit_info = raycast(camera.world_position, camera.forward, ignore=scene.triggers)

            triggers_hit_info = raycast(camera.world_position, camera.forward, traverse_target=scene.trigger_parent)
            # print('-----------------', triggers_hit_info.hit)
            # triggers_hit_info.entity.color = color.red
            for e in triggers_hit_info.entities:
                # e.visible_self = True
                e.animate_color(color.red, delay=distance(camera, camera)*50)
                # e.animate_color(color.blue, delay=10)
                # e.color=color.red

            if hit_info.hit and hit_info.world_point:
                # print('hit something', mouse.hovered_entity)
                self.arrow.world_parent = scene
                self.arrow.animate('position', Vec3(*hit_info.world_point), hit_info.distance/100, curve=curve.linear, interrupt='kill')
                # self.arrow.world_parent = scene
                # self.arrow.animate('z', mouse.collision.distance, mouse.collision.distance/500, curve=curve.linear, interrupt='finish')

                # if mouse.hovered_entity == level.eye_trigger:
                #     invoke(open_gate, delay=.3)
                #     destroy(self.arrow, delay=.1)
                #     return

                destroy(self.arrow, delay=10)

            else:
                # player.draw_arrow_animation.kill()
                self.arrow.world_parent = scene
                self.arrow.animate('position', self.arrow.world_position+(self.arrow.forward*500), 1, curve=curve.linear, interrupt='kill')
                # player.arrow.animate('z', 100, .5, curve=curve.linear, interrupt='finish')
                destroy(self.arrow, delay=1)

        # cheat buttons
        if key == 'f1':
            self.bow.enabled = True

if __name__ == '__main__':
    app = Ursina()
    scene.triggers = []
    player = CastawayPlayer()

    torch_collider = Entity(parent=player.level.torch, model='cube', color=color.red, origin_y=-.5, scale=(.45,2.05,.45), collider='box', visible_self=False)
    fire_trigger = Entity(name='fire_trigger', parent=player.level.torch, model='sphere', color=color.blue, y=2.1, scale=.6, collider='sphere', visible_self=True)

    torch = duplicate(player.level.torch, parent=scene, position=(1,0,4))
    ground = Entity(model='plane', scale=100, collider='box', texture='white_cube', texture_scale=(100,100))

    scene.triggers.extend([e for e in scene.entities if e.name == 'fire_trigger' and e.enabled])
    scene.trigger_parent = Entity()
    for e in scene.triggers:
        e.world_parent = scene.trigger_parent

    print(scene.trigger_parent.children)

    app.run()
