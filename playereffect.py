from effect import Effect


class PlayerEffect:
    def __init__(self, player, effect, source, source_type, duration_turns, start_turn):
        if not isinstance(effect, Effect):
            raise TypeError("effect must be an Effect instance.")

        if source_type not in ['potion', 'activity']:
            raise ValueError("source_type must be 'potion' or 'activity'")

        self.player = player
        self.effect = effect
        self.source = source
        self.source_type = source_type
        self.start_turn = start_turn
        self.duration_turns = duration_turns


    def is_expired(self, current_turn):
        if self.duration_turns == 0:
            return True
        return current_turn >= self.start_turn + self.duration_turns


    def turns_remaining(self, current_turn):
        if self.duration_turns == 0:
            return 0
        remaining = (self.start_turn + self.duration_turns) - current_turn
        return max(0, remaining)
