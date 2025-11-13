from entities.entity import Entity


class NPC(Entity):
    def __init__(self, drop, name, current_health):
        super().__init__(name, current_health)
        # TODO idk
        self.drop = drop