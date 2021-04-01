from Player_Obj import DEAD_ZONE
import arcade

MOVEMENT_SPEED = 1

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

SCALING = 0.2
DEAD_ZONE = 0.1

def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

""" Enemy Class """
class Enemy(arcade.Sprite):

    def __init__(self):

        super().__init__()
        # Create a variable to hold our speed. 'angle' is created by the parent

        self.speed = 0
        self.scale = SCALING * 0.2
        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        image = f"Sprites\\flipped"
        self.creep_pair = arcade.load_texture_pair(f"{image}_creeper.png", hit_box_algorithm="Detailed")
        #self.textures.append(self.texture)

        # By default, face right.
        self.character_face_direction = TEXTURE_RIGHT
        self.texture = self.creep_pair[0]

        self.hit_box = self.texture.hit_box_points

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        # Figure out if we need to flip face left or right
        if dx < -DEAD_ZONE and self.character_face_direction == TEXTURE_RIGHT:
            self.character_face_direction = TEXTURE_LEFT
        elif dx > DEAD_ZONE and self.character_face_direction == TEXTURE_LEFT:
            self.character_face_direction = TEXTURE_RIGHT
        

    # Reset position for when the enemy falls off the edge.
    def reset_pos(self):
        self.center_x = 250
        self.center_y = 125

    def reset(self): # reset the enemy
        self.reset_pos()

    def update(self):
        # Changes the spirite to face left or right respectively. For some reason not currently working.
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]

    """This function will move the enemy sprite towards the player sprite."""
    def follow_sprite(self, player_sprite):
        # Makes adjustments vertically.
        if self.center_y < player_sprite.center_y: # Needs to move up
            self.center_y += min(MOVEMENT_SPEED * 3, player_sprite.center_y - self.center_y) # Purposefully multiplied MOVEMENT_SPEED so that the creeper would hop. We liked the hoppy creeper.
        elif self.center_y > player_sprite.center_y: # Needs to move down
            self.center_y -= min(MOVEMENT_SPEED, self.center_y - player_sprite.center_y)

        # Makes adjustments horizontally.
        if self.center_x < player_sprite.center_x: # Needs to move right
            self.center_x += min(MOVEMENT_SPEED, player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x: # Needs to move left
            self.center_x -= min(MOVEMENT_SPEED, self.center_x - player_sprite.center_x)