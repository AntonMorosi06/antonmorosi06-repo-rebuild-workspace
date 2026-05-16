from python_snake_collection.core import Direction, Point, SnakeGame, direction_from_key


def test_game_initializes_snake():
    game = SnakeGame(width=12, height=10, seed=1)

    assert len(game.snake) == 3
    assert not game.game_over
    assert game.score == 0


def test_direction_cannot_reverse_immediately():
    game = SnakeGame(width=12, height=10, seed=1)

    game.turn(Direction.LEFT)

    assert game.pending_direction == Direction.RIGHT


def test_step_moves_head_right_initially():
    game = SnakeGame(width=12, height=10, seed=1)
    old_head = game.snake[0]

    game.step()

    assert game.snake[0] == Point(old_head.x + 1, old_head.y)


def test_food_growth_increases_score_and_length():
    game = SnakeGame(width=12, height=10, seed=1)
    head = game.snake[0]
    game.food = Point(head.x + 1, head.y)

    old_length = len(game.snake)
    game.step()

    assert game.score == 1
    assert len(game.snake) == old_length + 1


def test_wall_collision_sets_game_over():
    game = SnakeGame(width=8, height=8, seed=1)

    for _ in range(20):
        game.step()
        if game.game_over:
            break

    assert game.game_over


def test_direction_from_key_supports_wasd_and_arrows():
    assert direction_from_key("w") == Direction.UP
    assert direction_from_key("ArrowLeft") == Direction.LEFT
    assert direction_from_key("down") == Direction.DOWN
    assert direction_from_key("d") == Direction.RIGHT
