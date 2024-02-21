import arcade

TILE_SIZE = 64
MAP: list[list[str]] = [
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", "C", "C", " ", " ", "C", "C", "C", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", "P", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G"],
]


class Player(arcade.Sprite):
    def __init__(self, position: tuple[float, float], scale: float = 0.5):
        super().__init__(
            ":resources:images/animated_characters/robot/robot_idle.png",
            scale,
        )

        self.position = position


class Obstacle(arcade.Sprite):
    def __init__(
        self, filename: str, position: tuple[float, float], scale: float = 0.5
    ) -> None:
        super().__init__(filename, scale)

        self.position = position


class Game(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(len(MAP[0]) * TILE_SIZE, len(MAP) * TILE_SIZE)  # type: ignore

        self.player_list: arcade.SpriteList
        self.active_sprite: arcade.SpriteList
        self.obstacle_spite: arcade.SpriteList

        arcade.set_background_color((200, 200, 200))

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.active_sprite = arcade.SpriteList()
        self.obstacle_spite = arcade.SpriteList(use_spatial_hash=True)

        for row_idx, row in enumerate(reversed(MAP)):
            for col_idx, col in enumerate(row):
                if col == "P":
                    player = Player(
                        (col_idx * TILE_SIZE, row_idx * TILE_SIZE // 2)
                    )

                    self.player_list.append(player)
                    self.active_sprite.append(player)

                if col == "G":
                    obstacle = Obstacle(
                        ":resources:images/tiles/grassMid.png",
                        (
                            col_idx * TILE_SIZE + TILE_SIZE // 2,
                            row_idx * TILE_SIZE + TILE_SIZE // 2,
                        ),
                    )

                    self.active_sprite.append(obstacle)
                    self.obstacle_spite.append(obstacle)

                if col == "C":
                    obstacle = Obstacle(
                        ":resources:images/tiles/boxCrate_single.png",
                        (
                            col_idx * TILE_SIZE + TILE_SIZE // 2,
                            row_idx * TILE_SIZE + TILE_SIZE // 2,
                        ),
                    )

                    self.active_sprite.append(obstacle)
                    self.obstacle_spite.append(obstacle)

    def on_draw(self) -> None:
        self.clear()

        self.active_sprite.draw()  # type: ignore


def main() -> None:
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
