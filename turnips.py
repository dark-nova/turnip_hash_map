
# Ported from:
#   https://gist.github.com/Treeki/85be14d297c80c8b3c0a76375743325b

MIN = 90
MAX = 110 + 1 # This is for open-interval range().

N_EMOJI = '\N{combining enclosing keycap}'
PATTERNS = {
    f'0{N_EMOJI}': 'high, decreasing, high, decreasing, high (fluctuating)',
    f'1{N_EMOJI}': 'decreasing middle, high spike, random low',
    f'2{N_EMOJI}': 'consistently decreasing',
    f'3{N_EMOJI}': 'decreasing, spike, decreasing (small spike)',
    '❔': "if you don't know or don't remember your previous pattern",
    }

class Calculator:
    """Class module for calculating turnip prices."""

    def __init__(self, prices: List[int]) -> None:
        """Initialize the calculator given current prices, including
        last week's pattern. The list structure corresponds to a row
        in the database:

        last_pattern, buy_price, monday_am, monday_pm, ..., saturday_pm

        last_pattern can be -1 (unknown) or 1 through 4 (known).
        buy_price will be between 90 and 110 inclusive.
        Other prices can be 0 to represent an unknown and is a default.

        Args:
            prices (List[int]): this week's prices

                Patterns are as follows:
                - 0: high, decreasing, high, decreasing, high
                - 1: decreasing middle, high spike, random low
                - 2: consistently decreasing
                - 3: decreasing, spike, decreasing

        """
        self.buy_price = prices[1]
        self.prices = prices[2:]
        self.possible_patterns = []

    def run(self) -> None:
        """Run every pattern to find any matches."""
        for pattern in [Pattern_0, Pattern_1, Pattern_2, Pattern_3]:
            p = pattern(self.buy_price, self.prices)
            self.possible_patterns.append(p.run())


