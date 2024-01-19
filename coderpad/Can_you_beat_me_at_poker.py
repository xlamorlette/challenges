from collections import deque


def shuffle_cards_pile(initial_pile: list[str]) -> list[str]:
    result_queue = deque()
    add_on_top = True
    for card in initial_pile[::-1]:
        if add_on_top:
            result_queue.append(card)
        else:
            result_queue.appendleft(card)
        add_on_top = not add_on_top
    return list(result_queue)


def test_shuffle_five_cards():
    initial_pile: list[str] = ["Ace of Spades", "5 of Hearts", "Queen of Clubs", "10 of Diamonds", "2 of Hearts"]
    result_pile: list[str] = shuffle_cards_pile(initial_pile)
    assert result_pile == ["5 of Hearts", "10 of Diamonds", "2 of Hearts", "Queen of Clubs", "Ace of Spades"]


def test_shuffle_empty_pile():
    assert shuffle_cards_pile([]) == []


if __name__ == "__main__":
    test_shuffle_five_cards()
    test_shuffle_empty_pile()

