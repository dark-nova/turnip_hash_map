from math import ceil
from typing import Dict, List, Tuple, Union


# Ported from:
#   https://gist.github.com/Treeki/85be14d297c80c8b3c0a76375743325b

MIN = 90
MAX = 110 + 1 # This is for open-interval range().

# Some patterns may not match, so None is a valid return type
POSSIBLE_PATTERNS = Union[Dict[str, Tuple[int, int]], None]

class Pattern:
    """Represents a generic pattern.

    Attributes:
        buy_price (int): the buy price of turnips on Sunday
        current (List[Tuple[int]]): a list of min- and max prices in
            the current iteration, with index 0 as Monday AM and
            index 11 (last) as Saturday PM
        CONS_DECREASE (float): the constant decrease delta;
            used in `decrease`
        DEC_UPPER (float): the amount to decrease per iteration of
            `decrease` for the upper bound
        DEC_LOWER (float): same as `DEC_UPPER` but for lower bound
        N_PHASES (int): number of phases, i.e. 12 = 6 days * 2 phases
        possible (POSSIBLE_PATTERNS): possible market outcomes
        prices (List[int]): prices from Monday AM through Saturday PM
        RAND_DECREASE (float): maximum random decrease; used in
            `decrease`

    """
    N_PHASES = 12

    DEC_UPPER = 0.90
    DEC_LOWER = 0.85
    CONS_DECREASE = 0.03
    RAND_DECREASE = 0.02

    def __init__(self, buy_price: int) -> None:
        """Initialize using buy price and available prices.

        Args:
            buy_price (int): buy price on Sunday
            prices (List[int]): this week's prices excluding Sunday

        """
        self.buy_price = buy_price
        self.current = []
        self.possible = []

    def reset_values(self) -> None:
        """Reset both guarantee, upper and lower bounds, and phase
        values to buy price."""
        self.max_guarantee = self.buy_price
        self.min_guarantee = self.buy_price
        self.upper = self.buy_price
        self.lower = self.buy_price
        self.current = []

    def check_guarantees(self) -> None:
        """Check guarantees and update them if they are lower (upper)
        or higher (lower) than the new values.

        """
        if self.upper > self.max_guarantee:
            self.max_guarantee = self.upper
        if self.lower < self.min_guarantee:
            self.min_guarantee = self.lower
        self.current.append((self.lower, self.upper))

    def modify(
        self, loops: int, lower_coef: float = None, upper_coef: float = None,
        disp: int = 0
        ) -> None:
        """Apply the modify strategy to upper and lower limits.
        If either `upper_coef` or `lower_coef` are None,
        `self.MOD_UPPER` and `self.MOD_LOWER` are respectiveliy used.

        Args:
            loops (int): number of loops to attempt
            lower_coef (float, optional): lower bound coefficient;
                defaults to None
            upper_coef (float, optional): upper bound coefficient;
                defaults to None
            disp (int, optional): displaces value, used in pattern 3

        Raises:
            ValueError: if the actual price doesn't fall within bounds

        """
        if not upper_coef:
            upper_coef = self.MOD_UPPER
        if not lower_coef:
            lower_coef = self.MOD_LOWER

        for loop in range(loops):
            self.upper = ceil(upper_coef * self.buy_price) + disp
            self.lower = ceil(lower_coef * self.buy_price) + disp
            self.check_guarantees()

    def decrease(self, loops: int) -> None:
        """Apply the decrease strategy to upper and lower limits,
        for both patterns 0 and 1. Unlike `modify`, `decrease` has
        slightly different bounds. The lower bound should use the
        highest "random" drop.

        Args:
            loops (int): number of loops to attempt

        Raises:
            ValueError: if the actual price doesn't fall within bounds

        """
        u_coef = self.CONS_DECREASE
        l_coef = u_coef + self.RAND_DECREASE
        for loop in range(loops):
            on = 1 if loop > 0 else 0
            self.upper = ceil((self.DEC_UPPER - u_coef * on) * self.buy_price)
            self.lower = ceil((self.DEC_LOWER - l_coef * on) * self.buy_price)
            self.check_guarantees()

    def convert_current(self) -> None:
        """Convert self.current to dicts of depth 12, equal to number
        of total phases from Monday AM through Saturday PM.

        Once converted, sets self.possible to this new dict.

        """
        for i, (lower, upper) in enumerate(self.current[::-1]):
            if i != 0:
                current = {
                    (lower, upper): last
                    }
                last = current
            else:
                last = [lower, lower]
        self.possible.append(last)


class Pattern_0(Pattern):
    """Represents turnip pattern 0:
    high, decreasing, high, decreasing, high.

    """
    MOD_UPPER = 1.4
    MOD_LOWER = 0.9
    DEC_UPPER = 0.8
    DEC_LOWER = 0.6
    CONS_DECREASE = 0.04
    RAND_DECREASE = 0.06

    def run(self) -> POSSIBLE_PATTERNS:
        """Run every possible combination in this pattern.

        Returns:
            POSSIBLE_PATTERNS: represents pattern (keys) and
                guaranteed maximum and minimum (Tuple[int, int])

        """
        for inc_a in range(6):
            inc_b_c = 7 - inc_a
            for dec_a in [2, 3]:
                for inc_c in range(inc_b_c - 1):
                    dec_b = 5 - dec_a
                    inc_b = inc_b_c - inc_c
                    self.reset_values()
                    self.modify(inc_a)
                    self.decrease(dec_a)
                    self.modify(inc_b)
                    self.decrease(dec_b)
                    self.modify(inc_c)
                    self.convert_current()
        return self.possible


class Pattern_1(Pattern):
    """Represents turnip pattern 1:
    decreasing middle, high spike, random low.

    """
    PEAK_START = 3 - 2
    PEAK_END = 9 - 2 + 1

    MOD_A = 0.9
    MOD_B = 1.4
    MOD_C = 2.0
    MOD_D = 6.0
    MOD_E = 0.4

    PAIRS = [
        (MOD_A, MOD_B),
        (MOD_B, MOD_C),
        (MOD_C, MOD_D),
        (MOD_B, MOD_C),
        (MOD_A, MOD_B),
        ]

    def run(self) -> POSSIBLE_PATTERNS:
        """Run every possible combination in this pattern.

        Returns:
            POSSIBLE_PATTERNS: represents pattern (keys) and
                guaranteed maximum and minimum (Tuple[int, int])

        """
        for peak in range(self.PEAK_START, self.PEAK_END):
            self.reset_values()
            self.decrease(peak)
            for l_coef, u_coef in self.PAIRS:
                self.modify(1, l_coef, u_coef)
            self.modify(
                self.N_PHASES - peak - len(self.PAIRS), self.MOD_E, self.MOD_A
                )
            self.convert_current()
        return self.possible


class Pattern_2(Pattern):
    """Represents turnip pattern 2:
    consistently decreasing.

    Unlike other patterns, pattern 2 does not have variance,
    so if the pattern doesn't match, immediately return.

    """
    def run(self) -> POSSIBLE_PATTERNS:
        """Run the pattern.

        Returns:
            POSSIBLE_PATTERNS: represents pattern (keys) and
                guaranteed maximum and minimum (Tuple[int, int])

        """
        self.reset_values()
        self.decrease(self.N_PHASES)
        self.convert_current()
        return self.possible


class Pattern_3(Pattern):
    """Represents turnip pattern 3:
    decreasing, spike, decreasing.

    This pattern is very alike to pattern 1, so few changes were made.

    """
    PEAK_START = 2 - 2
    PEAK_END = 9 - 2 + 1

    MOD_A = 0.9
    MOD_B = 1.4
    MOD_C = 2.0

    DEC_UPPER = 0.9
    DEC_LOWER = 0.4

    def run(self) -> POSSIBLE_PATTERNS:
        """Run every possible combination in this pattern.

        Returns:
            POSSIBLE_PATTERNS: represents pattern (keys) and
                guaranteed maximum and minimum (Tuple[int, int])

        """
        for peak in range(self.PEAK_START, self.PEAK_END):
            self.reset_values()
            self.decrease(peak)
            self.modify(2, self.MOD_A, self.MOD_B)
            self.modify(3, self.MOD_B, self.MOD_C)
            self.decrease(self.N_PHASES - peak - 5)
            self.convert_current()
        return self.possible
