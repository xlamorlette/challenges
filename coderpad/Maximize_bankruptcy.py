idef get_maximal_loss(stock_prices: list[int]) -> int:
    maximum_buying_price = -1
    maximum_loss = 0
    for price in stock_prices:
        assert price >= 0
        maximum_buying_price = max(maximum_buying_price, price)
        maximum_loss = min(maximum_loss, price - maximum_buying_price)
    return maximum_loss


def test_empty_list():
    assert get_maximal_loss([]) == 0


def test_instructions_example():
    stock_prices = [3, 2, 4, 2, 1, 5]
    assert get_maximal_loss(stock_prices) == -3


def test_no_possible_loss():
    stock_prices = [1, 2, 3, 4]
    assert get_maximal_loss(stock_prices) == 0


if __name__ == "__main__":
    test_empty_list()
    test_instructions_example()
    test_no_possible_loss()

