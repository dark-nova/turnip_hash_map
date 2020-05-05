from patterns import Pattern_0, Pattern_1, Pattern_2, Pattern_3, MIN, MAX

import yaml


N_EMOJI = '\N{combining enclosing keycap}'
PATTERNS = {
    f'0{N_EMOJI}': 'high, decreasing, high, decreasing, high (fluctuating)',
    f'1{N_EMOJI}': 'decreasing middle, high spike, random low',
    f'2{N_EMOJI}': 'consistently decreasing',
    f'3{N_EMOJI}': 'decreasing, spike, decreasing (small spike)',
    '❔': "if you don't know or don't remember your previous pattern",
    }

class Mapper:
    """Class module for mapping turnip prices."""
    patterns = [Pattern_0, Pattern_1, Pattern_2, Pattern_3]

    def __init__(self) -> None:
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
        self.possible_patterns = {}

    def run(self) -> None:
        """Run every pattern to find any matches."""
        for n, pattern in enumerate(self.patterns):
            self.possible_patterns[n] = {}
            for bp in range(MIN, MAX):
                self.possible_patterns[n][bp] = []
                p = pattern(bp)
                self.possible_patterns[n][bp].append(p.run())

        return self.possible_patterns


if __name__ == '__main__':
    mapper = Mapper()
    d = mapper.run()
    with open('turnips.yaml', 'w') as f:
        yaml.safe_dump(d, stream=f)
