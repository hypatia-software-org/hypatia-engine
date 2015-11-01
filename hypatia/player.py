"""Interactive map entities/players!

Note:
  Could even be something like a sign! Or the human player.

"""

import pygame

from hypatia import constants
from hypatia import actor


class HumanPlayer(actor.Actor):

    def __init__(self, *args, **kwargs):
        actor.Actor.__init__(self, *args, **kwargs)

    # NOTE: outdated/needs to be updated for velocity
    def move(self, game, direction):
        """Modify human player's positional data legally (check
        for collisions).
        Note:
          Will round down to nearest probable step
          if full step is impassable.
          Needs to use velocity instead...
        Args:
          direction (constants.Direction):

        """

        self.walkabout.direction = direction

        # hack for incorporating new velocity system, will update later
        if direction in (constants.Direction.north, constants.Direction.south):
            planned_movement_in_pixels = self.velocity.y
        else:
            planned_movement_in_pixels = self.velocity.x

        adj_speed = game.screen.time_elapsed_milliseconds / 1000.0
        iter_pixels = max([1, int(planned_movement_in_pixels)])

        # test a series of positions
        for pixels in range(iter_pixels, 0, -1):
            # create a rectangle at the new position
            new_topleft_x, new_topleft_y = self.walkabout.topleft_float

            # what's going on here
            if pixels == 2:
                adj_speed = 1

            if direction == constants.Direction.north:
                new_topleft_y -= pixels * adj_speed
            elif direction == constants.Direction.east:
                new_topleft_x += pixels * adj_speed
            elif direction == constants.Direction.south:
                new_topleft_y += pixels * adj_speed
            elif direction == constants.Direction.west:
                new_topleft_x -= pixels * adj_speed

            destination_rect = pygame.Rect((new_topleft_x, new_topleft_y),
                                           self.walkabout.size)
            collision_rect = self.walkabout.rect.union(destination_rect)

            if not game.scene.collide_check(collision_rect):
                # we're done, we can move!
                new_topleft = (new_topleft_x, new_topleft_y)
                self.walkabout.action = constants.Action.walk
                animation = self.walkabout.current_animation()
                self.walkabout.size = animation.largest_frame_size()
                self.walkabout.rect = destination_rect
                self.walkabout.topleft_float = new_topleft

                return True

        # never found an applicable destination
        self.walkabout.action = constants.Action.stand

        return False


class Npc(actor.Actor):

    def __init__(self, *args, **kwargs):
        actor.Actor.__init__(self, *args, **kwargs)
