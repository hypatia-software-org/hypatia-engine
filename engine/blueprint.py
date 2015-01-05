class GameBlueprint(object):

    def __init__(self, tilemap, viewport, human_player, items):
        self.human_player = human_player
        self.tilemap = tilemap
        self.viewport = viewport
        self.items = items

