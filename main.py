import arcade

# Set Tile Size
TILE_SIZE = 64

# Map as 2D array
MAP: list[list[str]] = [
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", "C", "C", "C", "C", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", "C", "C", "C", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", "P", " ", " ", " ", " ", " ", " ", " ", " ", "C", " ", " ", " "],
    [" ", " ", " ", "C", " ", " ", " ", "C", " ", " ", "C", " ", " ", " "],
    ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G"],
]


# PLayer class with player sprite
class Player(arcade.Sprite):
    def __init__(self, scale: float = 1):
        super().__init__(
            ":resources:images/animated_characters/robot/robot_idle.png",
            scale,
        )


# Obstacle class that takes the sprite & position and create an obstacle
class Obstacle(arcade.Sprite):
    def __init__(
        self, filename: str, position: tuple[float, float], scale: float = 0.5
    ) -> None:
        super().__init__(filename, scale)

        self.position = position


# Game window class
class Game(arcade.Window):

    # Initializer
    def __init__(self):
        super().__init__(len(MAP[0]) * TILE_SIZE, len(MAP) * TILE_SIZE)  # type: ignore

        # Define scene & physics engine
        self.scene: arcade.Scene
        self.engine: arcade.PhysicsEnginePlatformer

        # Define player sprite & camera
        self.player: arcade.Sprite
        self.camera: arcade.Camera

        # Set background colour
        arcade.set_background_color((200, 200, 255))

    def setup(self):
        # Assign scene & Obstacle list
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Obstacle", use_spatial_hash=True)

        # Assign player & player list
        self.player = Player()
        self.scene.add_sprite("Player", self.player)

        # Assign camera
        self.camera = arcade.Camera(self.width, self.height)

        # Loop through the 2D map array & generate map
        for row_idx, row in enumerate(reversed(MAP)):
            for col_idx, col in enumerate(row):

                # Place player
                if col == "P":
                    self.player.position = (
                        col_idx * TILE_SIZE + TILE_SIZE // 2,
                        row_idx * TILE_SIZE + TILE_SIZE // 2,
                    )

                # Generate ground tile
                if col == "G":
                    self.scene.add_sprite(
                        "Obstacle",
                        Obstacle(
                            ":resources:images/tiles/grassMid.png",
                            (
                                col_idx * TILE_SIZE + TILE_SIZE // 2,
                                row_idx * TILE_SIZE + TILE_SIZE // 2,
                            ),
                        ),
                    )

                # Generate Crate tiles
                if col == "C":
                    self.scene.add_sprite(
                        "Obstacle",
                        Obstacle(
                            ":resources:images/tiles/boxCrate_single.png",
                            (
                                col_idx * TILE_SIZE + TILE_SIZE // 2,
                                row_idx * TILE_SIZE + TILE_SIZE // 2,
                            ),
                        ),
                    )

        # Create physics engine with player & obstacles
        self.engine = arcade.PhysicsEnginePlatformer(
            self.player, self.scene.get_sprite_list("Obstacle")
        )

    def on_key_press(self, symbol: int, modifiers: int):

        # Check if up is pressed & player is on ground
        if symbol == arcade.key.UP and self.engine.can_jump():
            self.player.change_y = 10

        # Check if left key is pressed
        elif symbol == arcade.key.LEFT:
            self.player.change_x = -5

        # Check if right key is pressed
        elif symbol == arcade.key.RIGHT:
            self.player.change_x = 5

    def on_key_release(self, symbol: int, modifiers: int):

        # Stop moving when right is released
        if symbol == arcade.key.LEFT:
            self.player.change_x = 0

        # Stop moving when right is released
        elif symbol == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_draw(self) -> None:
        self.clear()
        self.camera.use()
        self.scene.draw()  # type: ignore

    def on_update(self, delta_time: float):
        self.engine.update()
        self.center_camera_to_player()

    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (
            self.camera.viewport_width / 2
        )
        screen_center_y = self.player.center_y - (
            self.camera.viewport_height / 2
        )

        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)


def main() -> None:
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
