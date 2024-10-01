class MagicalCreature:
    def __init__(self, id: int, name: str, lives: int, magic_power: int):
        self.id = id
        self.name = name
        self.lives = lives
        self.magic_power = magic_power

    def __str__(self):
        return f'MagicalCreature(id={self.id}, name="{self.name}", type="{self.lives}", magic_power={self.magic_power})'
