from direct.actor.Actor import Actor
from direct.directbase.DirectStart import base
from panda3d.core import*


class LoadActor(Actor):
    def __init__(self, ModelName, AnimsName, pos, ColliderName, MaxSpeed, MaxHealth):
        super().__init__()
        self.actor = Actor(ModelName, AnimsName)
        self.actor.reparentTo(render)
        self.actor.setPos(pos)
        capsule = CollisionSphere(0, 0, 0, 5)
        ColliderNode = CollisionNode(ColliderName)
        ColliderNode.addSolid(capsule)
        self.collider = self.actor.attachNewNode(ColliderNode)
        self.max_speed = MaxSpeed
        self.velocity = Vec3(0, 0, 0)
        self.NeAcc = 500
        self.walking = False
        self.max_health = self.health = MaxHealth

    def move(self, dt):
        speed = self.velocity.length()
        if speed > self.max_speed:
            self.velocity.normalize()
            self.velocity *= self.max_speed
            speed = self.max_speed

        if not self.walking:
            NeSpeed = self.NeAcc * dt
            if NeSpeed > speed:
                self.velocity = Vec3(0, 0, 0)
            else:
                SlowSpeed = -self.velocity
                SlowSpeed.normalize()
                SlowSpeed *= NeSpeed
                self.velocity += SlowSpeed

        self.actor.setY(self.actor, -(self.velocity * dt).length())

    def CountHealth(self, ChangeHealth):
        self.health += ChangeHealth
        if self.health > self.max_health:
            self.health = self.max_health

    def CleanUp(self):
        if self.collider is not None:
            base.cTrav.removeCollider(self.collider)
            self.collider = None
        if self.actor is not None:
            self.actor.cleanup()
            self.actor.removeNode()
            self.actor = None
