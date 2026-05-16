from tetris_pygame.core import ActivePiece, TetrisGame


def test_game_initializes_with_active_piece():
    game = TetrisGame(seed=1)

    assert game.active is not None
    assert not game.game_over
    assert game.score == 0
    assert game.level == 1


def test_move_left_changes_piece_x():
    game = TetrisGame(seed=1)
    start_x = game.active.x

    moved = game.move(-1, 0)

    assert moved
    assert game.active.x == start_x - 1


def test_hard_drop_locks_piece():
    game = TetrisGame(seed=1)

    distance = game.hard_drop()

    assert distance > 0
    assert game.pieces_locked == 1
    assert game.active is not None


def test_clear_lines_updates_score_and_lines():
    game = TetrisGame(seed=1)

    game.board[-1] = ["I" for _ in range(game.width)]
    cleared = game.clear_lines()
    game.apply_score(cleared)

    assert cleared == 1
    assert game.lines == 1
    assert game.score == 100


def test_hold_piece_sets_hold_slot():
    game = TetrisGame(seed=1)
    active_name = game.active.name

    result = game.hold()

    assert result
    assert game.hold_piece == active_name
    assert game.hold_used


def test_rotate_does_not_crash():
    game = TetrisGame(seed=1)

    result = game.rotate(clockwise=True)

    assert isinstance(result, bool)


def test_visible_cells_contains_active_piece_cells():
    game = TetrisGame(seed=1)

    cells = game.visible_cells()

    assert cells
    assert game.active.name in set(cells.values())
