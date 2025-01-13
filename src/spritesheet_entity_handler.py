from read_meta import *

# The animations should be defined in this kind of file
ANIMATIONS_FILE = "animations.meta"


""" Class for handling spritesheets """
class SpritesheetEntityHandler:
    """ Ctor just takes an entity as parameter """
    def __init__(self, entity):
        self.entity = entity # It's for an entity
        self.asset_manager = self.entity.asset_manager

        # Reads the animations
        self.animations = read_meta_file(self.asset_manager.get_entity_anim_meta_file(self.entity.type, self.entity.name))
        self.default_animation = self.animations.get(DEFAULT_ANIMATION) # Gets the default animation

        # Sets up some things
        self.setup()

    """ Spritesheet data """
    def get_spritesheet_data(self, value: str):
        try:
            return self.animations.get(value)
        except KeyError:
            print(f"Fatal error: {self.entity.name}: Spritesheet not found")

    """ Sets the current spritesheet """
    def set_spritesheet(self, value: str):
        self.current_animation_filename = self.get_spritesheet_data(value)
        self.current_animation = value
        self.current_surface = self.asset_manager.get_entity_surface(self.current_animation_filename, self.entity.type, self.entity.name)

    """ Reads the "size" field in the file """
    def setup_sprite_size(self):
        self.sprite_width = self.animations.get("size")[0]
        self.sprite_height = self.animations.get("size")[1]

    """ Some stuff for setting up things """
    def setup(self):
        self.current_animation_filename = self.default_animation # default_animation as filename, "idle.png"
        self.current_animation = DEFAULT_ANIMATION # current_animation as string, like "idle", "special2" or "walk"
        self.load_image(DEFAULT_ANIMATION) # Loads the image

        self.setup_sprite_size() # Gets the size of the sprite

        if DEFAULT_ANIMATION not in self.animations.keys():
            raise ValueError(f"Error: entity {self.entity} has to have a \"{DEFAULT_ANIMATION}\" variable declared in its meta file!")

    """ Loads a spritesheet """
    def load_image(self, animation: str):
        self.set_spritesheet(animation) # Sets current spritesheet
        # Loads the spritesheet
        self.current_surface = self.asset_manager.get_entity_surface(self.current_animation_filename, self.entity.type, self.entity.name)

