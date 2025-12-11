import pickle
import os


class Activity:
    _extent = []

    def __init__(self, name, description, effect=None, effect_duration=3):
        self.__class__._extent.append(self)

        if not isinstance(name, str):
            raise TypeError("Activity name must be a string.")
        if not name.strip():
            raise ValueError("Name cannot be empty or just spaces.")
        self.name = name

        if not isinstance(description, str):
            raise TypeError("Activity description must be a string.")
        if not description.strip():
            raise ValueError("Activity description cannot be empty or just spaces.")
        self.description = description

        if not isinstance(effect_duration, int):
            raise TypeError("Effect duration must be an integer.")
        if effect_duration < 0:
            raise ValueError("Effect duration cannot be negative.")
        self.effect_duration = effect_duration

        self._tools = []

        self._effect = None
        if effect is not None:
            from effect import Effect
            if not isinstance(effect, Effect):
                raise TypeError("effect must be an Effect instance or None.")
        self.effect = effect

    @property
    def tools(self):
        return self._tools.copy()

    def add_tool(self, tool):
        if tool not in self._tools:
            self._tools.append(tool)

    def remove_tool(self, tool):
        if tool in self._tools:
            self._tools.remove(tool)


    @property
    def effect(self):
        return self._effect


    @effect.setter
    def effect(self, new_effect):
        from effect import Effect

        if self._effect is not None:
            self._effect.remove_activity(self)

        if new_effect is not None:
            if not isinstance(new_effect, Effect):
                raise TypeError("effect must be an Effect instance or None.")
            new_effect.add_activity(self)

        self._effect = new_effect


    def perform(self, player, current_turn, tool=None):
        from entities.player import Player
        if not isinstance(player, Player):
            raise TypeError("player must be a Player instance.")

        result_message = f"Performed {self.name}."

        if self.effect is not None:
            player.apply_effect_from_activity(
                self.effect,
                self,
                current_turn,
                duration_turns=self.effect_duration
            )
            result_message += f" {self.effect.name} effect applied!"

        if tool is not None:
            from items.tool import Tool
            if not isinstance(tool, Tool):
                raise TypeError("tool must be a Tool instance.")
            if tool.activity != self:
                raise ValueError(f"Tool {tool.name} cannot perform {self.name}")

            tool_result = tool.use()
            result_message += f" {tool_result}"

        return result_message

    def delete(self):
        for tool in self._tools.copy():
            tool.activity = None

        if self._effect is not None:
            self._effect.remove_activity(self)

        if self in self.__class__._extent:
            self.__class__._extent.remove(self)

    @classmethod
    def get_extent(cls):
        return cls._extent.copy()

    @classmethod
    def save_extent(cls, filename="activities.dat"):
        with open(filename, "wb") as file:
            pickle.dump(cls._extent, file)

    @classmethod
    def load_extent(cls, filename="activities.dat"):
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                cls._extent = pickle.load(file)
        else:
            cls._extent = []

    @classmethod
    def clear_extent(cls):
        cls._extent = []