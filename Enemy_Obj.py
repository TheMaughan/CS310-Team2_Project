import arcade


MUSIC_VOLUME = 0.0
SPRITE_SCALING = 0.5
TILE_SCALING = 0.9

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Platformer"


MOVEMENT_SPEED = 3
GRAVITY = .2 #change this to enable jumping
JUMP_SPEED = 11  

VIEWPORT_MARGIN = 250

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1



class Enemy(arcade.Sprite):
    """ Enemy Class """

    def __init__(self, image, scale):

        super().__init__(image, scale)
        # Create a variable to hold our speed. 'angle' is created by the parent
        self.speed = 0
        self.scale = SPRITE_SCALING *.2
        self.textures = []

        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        texture = arcade.load_texture(image)
        self.textures.append(texture)
        texture = arcade.load_texture(image, flipped_horizontally=True)
        self.textures.append(texture)

        # By default, face right.
        self.texture = texture

    def reset_pos(self):
        self.center_x = 250
        self.center_y = 125

    

    def reset(self): # reset the player
        self.reset_pos()

    def update(self):

        # Check for out-of-bounds

        # Changes the spirite to face left or right respectively. For some reason not currently working.
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]

    def follow_sprite(self, player_sprite):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.
        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of MOVEMENT_SPEED.
        """

        if self.center_y < player_sprite.center_y:
            self.center_y += min(MOVEMENT_SPEED, player_sprite.center_y - self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(MOVEMENT_SPEED, self.center_y - player_sprite.center_y)

        if self.center_x < player_sprite.center_x:
            self.center_x += min(MOVEMENT_SPEED, player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(MOVEMENT_SPEED, self.center_x - player_sprite.center_x)