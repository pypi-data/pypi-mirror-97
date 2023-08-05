from direct.directbase.DirectStart import base
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectDialog import DirectDialog
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import *
from NightWind3DLib3.Actor import LoadActor


class Window:
    def __init__(self):
        self.base = base
        self.window = WindowProperties()
        self.window.setSize(1400, 1000)
        self.base.win.requestProperties(self.window)
        self.StartDialog = self.CreateDialog(FrameSize=(-1.4 + 0.01, 1.4 + 0.01,
                                                        -1 + 0.01, 1 + 0.01),
                                             pos=(0, 0, 0), color=(1, 1, 1, 1),
                                             picture="start.png")
        self.font = loader.loadFont("font.ttc")
        self.CreateButton(pos=(0, 0, -0.8), text="开始游戏", scale=0.15, parent=self.StartDialog,
                          command=self.Start, fg=(255 / 255, 220 / 255, 99 / 255, 1),
                          frameColor=(147 / 255, 88 / 255, 51 / 255, 1))

        # 创建玩家角色
        self.player = LoadActor(ModelName="aduan",
                                AnimsName={"walk": "aduan_walk", "stand": "aduan_stand"},
                                pos=(-600, -60, 0), ColliderName="player",
                                MaxSpeed=30, MaxHealth=100)
        self.player.actor.setScale(4.5)
        self.player.acceleration = 100

        # 创建营救对象
        self.friend = LoadActor(ModelName="codemao",
                                AnimsName={"walk": "codemao_walk", "stand": "codemao_stand"},
                                pos=(450, 20, 0), ColliderName="friend",
                                MaxSpeed=40, MaxHealth=100)
        self.friend.actor.setScale(0.6)

        # 创建木头人敌人
        self.woodmen = LoadActor(ModelName="woodmen",
                                 AnimsName={"walk": "woodmen_walk", "stand": "woodmen_stand",
                                            "die": "woodmen_die", "attack": "woodmen_attack"},
                                 pos=(0, -100, 0), ColliderName="woodmen",
                                 MaxSpeed=10, MaxHealth=100)
        self.woodmen.actor.setScale(1.2)
        self.woodmen.acceleration = 100
        self.woodmen.default_orientation = Vec2(0, -1)
        self.woodmen.change_orientation = Vec2(0, -1)
        self.woodmen.detection_distance = 450
        self.woodmen.acceleration_chase = 400

        # 创建地刺敌人
        self.needle = LoadActor(ModelName="GroundNeedle",
                                AnimsName={"motion": "GroundNeedle_motion",
                                           "stop": "GroundNeedle_stop"},
                                pos=(270, 0, -2), ColliderName="needle",
                                MaxSpeed=5, MaxHealth=100)
        self.needle.actor.setScale(0.6)

        self.KeyState = {"up": False, "left": False, "right": False}
        self.KeyEvent()
        taskMgr.add(self.update)

        # 创建碰撞体
        self.base.pusher = CollisionHandlerPusher()
        self.base.cTrav = CollisionTraverser()
        self.base.pusher.setHorizontal(True)
        self.base.pusher.add_in_pattern("%fn-into-%in")
        self.base.pusher.addCollider(self.player.collider, self.player.actor)
        self.base.cTrav.addCollider(self.player.collider, self.base.pusher)
        self.base.pusher.addCollider(self.woodmen.collider, self.woodmen.actor)
        self.base.cTrav.addCollider(self.woodmen.collider, self.base.pusher)
        self.base.run()

    def CreateDialog(self, FrameSize, pos, color, picture):
        return DirectDialog(frameSize=FrameSize,
                            pos=pos, frameColor=color,
                            frameTexture=picture)

    def CreateButton(self, text, parent, command, scale, pos, fg, frameColor):
        DirectButton(text=text, parent=parent, command=command, scale=scale,
                     pos=pos, text_font=self.font, text_fg=fg, frameColor=frameColor)

    # 按下按钮触发此事件
    def Start(self):
        self.StartDialog.hide()
        self.load_model("FieldForest")
        self.base.cam.setHpr(-90, -4, 0)
        self.base.cam.setPos(-1000, -100, 100)
        self.CreateFence(580, 350, 0, 580, -350, 0, 5)
        self.CreateFence(-580, -350, 0, 580, -350, 0, 5)
        self.CreateFence(-580, -350, 0, -580, -150, 0, 5)
        self.CreateFence(-580, -40, 0, -580, 350, 0, 5)
        self.CreateFence(-580, 350, 0, 580, 350, 0, 5)
        self.base.disableMouse()

    def ChangeKeyState(self, direction, key_state):
        self.KeyState[direction] = key_state

    def KeyEvent(self):
        self.base.accept('w', self.ChangeKeyState, ['up', True])
        self.base.accept('w-up', self.ChangeKeyState, ['up', False])
        self.base.accept('a', self.ChangeKeyState, ['left', True])
        self.base.accept('a-up', self.ChangeKeyState, ['left', False])
        self.base.accept('s', self.ChangeKeyState, ['right', True])
        self.base.accept('s-up', self.ChangeKeyState, ['right', False])
        self.base.accept('woodmen-into-fence', self.ChangeWoodmenState)

    def load_model(self, model):
        self.model = loader.loadModel(model)
        self.model.reparentTo(render)

    def CreateFence(self, ax, ay, az, bx, by, bz, r):
        solid = CollisionCapsule(ax, ay, az, bx, by, bz, r)
        node = CollisionNode("fence")
        node.addSolid(solid)
        render.attachNewNode(node)

    def PlayerMove(self, keys: dict, dt):
        self.player.move(dt)
        self.player.walking = False
        if keys["up"]:
            self.player.velocity.addY(self.player.acceleration * dt)
            self.player.walking = True
        if keys["left"]:
            self.player.actor.setH(self.player.actor.getH() + 1)
            self.player.walking = True
        if keys["right"]:
            self.player.actor.setH(self.player.actor.getH() - 1)
            self.player.walking = True

        if self.player.walking:
            player_walk = self.player.actor.getAnimControl("walk")
            if not player_walk.isPlaying():
                self.player.actor.loop("walk")
        else:
            self.player.actor.loop("stand")

    def WoodmenMove(self, dt):
        self.woodmen.move(dt)
        positionVec3 = self.player.actor.getPos() - self.woodmen.actor.getPos()
        positionVec2 = positionVec3.getXy()
        distanceToPlayer = positionVec2.length()

        if distanceToPlayer > self.woodmen.detection_distance:
            self.woodmen.walking = True
            self.woodmen.heading = self.woodmen.default_orientation.signedAngleDeg(
                self.woodmen.change_orientation)
            self.woodmen.actor.setH(self.woodmen.heading)
            self.woodmen.velocity.addY(self.woodmen.acceleration * dt)
        elif 30 < distanceToPlayer < self.woodmen.detection_distance:
            self.woodmen.walking = True
            self.woodmen.heading = self.woodmen.default_orientation.signedAngleDeg(positionVec2)
            self.woodmen.actor.setH(self.woodmen.heading)
            self.woodmen.velocity.addY(self.woodmen.acceleration_chase * dt)
        else:
            self.woodmen.walking = False
            self.woodmen.heading = self.woodmen.default_orientation.signedAngleDeg(positionVec2)
            self.woodmen.actor.setH(self.woodmen.heading)

        if self.woodmen.walking:
            woodmen_walk = self.woodmen.actor.getAnimControl("walk")
            if not woodmen_walk.isPlaying():
                self.woodmen.actor.loop("walk")
        else:
            self.woodmen.actor.loop("stand")

    def update(self, task):
        dt = globalClock.getDt()
        self.PlayerMove(self.KeyState, dt)
        self.WoodmenMove(dt)
        return task.cont

    def ChangeWoodmenState(self, content):
        self.woodmen.acceleration = -self.woodmen.acceleration
        self.woodmen.change_orientation = -self.woodmen.change_orientation


if __name__ == "__main__":
    Window()
