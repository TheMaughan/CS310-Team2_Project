from arcade import texture
from Player_Obj import DEAD_ZONE
import arcade, random, math

MOVEMENT_SPEED = 1
SLOW_SPEED = 0.5

RIGHT_FACING = 0
LEFT_FACING = 1

SCALING = 0.2
DEAD_ZONE = 0.1

# How many pixels to move before we change the texture in the walking animation
DISTANCE_TO_CHANGE_TEXTURE = 3

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
        self.textures = []

        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        image = f"Sprites/flipped"
        texture = arcade.load_texture(f"{image}_creeper.png")
        self.textures.append(texture)
        texture = arcade.load_texture(f"{image}_creeper.png", 
                                                flipped_horizontally=True)
        self.textures.append(texture)
        
        # By default, face right.
        self.texture = texture
        #self.points = [[-16, -40], [16, -40], [16, 28], [-16, 28]]
        #self.set_hit_box(self.texture.hit_box_points)
        #self.hit_box = self.creep_pair.hit_box_points        

    # Reset position for when the enemy falls off the edge.
    def reset_pos(self):
        self.center_x = 250
        self.center_y = 125

    def reset(self): # reset the enemy
        self.reset_pos()


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
            self.texture = self.textures[LEFT_FACING] # Change Sprite to face player

        elif self.center_x > player_sprite.center_x: # Needs to move left
            self.center_x -= min(MOVEMENT_SPEED, self.center_x - player_sprite.center_x)
            self.texture = self.textures[RIGHT_FACING] # Change Sprite to face player



class Enemy_1(arcade.Sprite):

    def __init__(self):

        super().__init__()
        # Create a variable to hold our speed. 'angle' is created by the parent

        self.speed = 0
        self.scale = SCALING * 0.2
        self.textures = []

        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        
        image = f"Sprites/enemies/1_bit/enemy_4"
        self.fly_textres = []
        for i in range(2):
            texture = arcade.load_texture_pair(f"{image}_fly_{i}.png")
            self.textures.append(texture)
        
        self.textures.append(texture)
        
        # By default, face right.
        self.texture = texture
        #self.points = [[-16, -40], [16, -40], [16, 28], [-16, 28]]
        #self.set_hit_box(self.texture.hit_box_points)
        #self.hit_box = self.creep_pair.hit_box_points        

    # Reset position for when the enemy falls off the edge.
    def reset_pos(self):
        self.center_x = 250
        self.center_y = 125

    def reset(self): # reset the enemy
        self.reset_pos()


    """This function will move the enemy sprite towards the player sprite."""
    def follow_sprite(self, player_sprite):

        # Makes adjustments vertically.
        if self.center_y < player_sprite.center_y: # Needs to move up
            self.texture = self.textures[LEFT_FACING] # Change Sprite to face player

        elif self.center_y > player_sprite.center_y: # Needs to move down
            self.texture = self.textures[RIGHT_FACING] # Change Sprite to face player

        # Makes adjustments horizontally.
        if self.center_x < player_sprite.center_x: # Needs to move right
            self.texture = self.textures[LEFT_FACING] # Change Sprite to face player

        elif self.center_x > player_sprite.center_x: # Needs to move left
            self.texture = self.textures[RIGHT_FACING] # Change Sprite to face player

        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of SPRITE_SPEED.
        """

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Random 1 in 100 chance that we'll change from our old direction and
        # then re-aim toward the player
        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the player
            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y

            # Do math to calculate how to get the enemy to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the enemy will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the enemy travels.
            self.change_x = math.cos(angle) * SLOW_SPEED
            self.change_y = math.sin(angle) * SLOW_SPEED