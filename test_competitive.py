from competitive import CompetitiveGame


def test_score():
    game = CompetitiveGame(
        set(),
        {(2, 2)},
        {(2, 3)},
        (2, 1),
        (4, 4),
        2
    )

    game.step("East", "Stay")

    score1, score2 = game.get_score()
    assert (score1, score2) == (1, 0)


def test_agents_cannot_pass():
    game = CompetitiveGame(
        set(),
        set(),
        set(),
        (2, 2),
        (2, 3),
        1
    )

    game.step("East", "West")
    assert game.agent1 == (2, 2)
    assert game.agent2 == (2, 3)


def test_step_limit():
    game = CompetitiveGame(
        set(),
        set(),
        set(),
        (2, 1),
        (2, 4),
        2
    )

    game.step("Stay", "Stay")
    game.step("Stay", "Stay")
    game.step("East", "West")
    assert game.current_step == 2
    assert game.is_finished()


def test_take_box():
    game = CompetitiveGame(
        set(),
        {(2, 2)},
        {(2, 3)},
        (2, 1),
        (2, 5),
        12
    )

    game.step("East", "Stay")
    assert game.get_score() == (1, 0)

    game.step("South", "West")
    game.step("South", "West")
    assert game.get_score() == (0, 0)

    game.step("East", "South")
    game.step("East", "West")
    game.step("Stay", "West")
    game.step("Stay", "North")
    game.step("Stay", "East")
    assert game.get_score() == (0, 1)
    assert game.get_winner() == "Agent 2"


if __name__ == "__main__":
    test_score()
    test_agents_cannot_pass()
    test_step_limit()
    test_take_box()