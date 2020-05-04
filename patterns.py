class Pattern:
    """Represents a generic pattern.

    Attributes:
        buy_price (int): the buy price of turnips on Sunday
        CONS_DECREASE (float): the constant decrease delta;
            used in `decrease`
        DEC_UPPER (float): the amount to decrease per iteration of
            `decrease` for the upper bound
        DEC_LOWER (float): same as `DEC_UPPER` but for lower bound
        N_PHASES (int): number of phases, i.e. 12 = 6 days * 2 phases
        phase (int): 0-index value corresponding to day and period,
            e.g. Monday AM is 0, Monday PM is 1, etc.
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

    def __init__(self, buy_price: int, prices: List[int]) -> None:
        """Initialize using buy price and available prices.

        Args:
            buy_price (int): buy price on Sunday
            prices (List[int]): this week's prices excluding Sunday

        """
        self.buy_price = buy_price
        self.prices = prices
        self.possible = {}

    def in_range(self, delta: int) -> bool:
        """Is the actual price in range of predictions?
        If `self.prices[phase]` is 0 (an unknown), this will also
        return True.

        Args:
            delta (int): the difference of phase from current step

        Returns:
            bool: True if in range or data is 0; otherwise False

        """
        phase = self.phase + delta
        return (
            self.prices[phase] == 0
            or self.prices[phase] in range(self.lower, self.upper + 1)
            )

    def increase_phase(self, increase: int) -> None:
        """Increase the current phase.

        Args:
            increase (int): how much to increment phase by

        """
        self.phase += increase

    def reset_values(self) -> None:
        """Reset both guarantee, upper and lower bounds, and phase
        values to buy price."""
        self.max_guarantee = self.buy_price
        self.min_guarantee = self.buy_price
        self.upper = self.buy_price
        self.lower = self.buy_price
        self.phase = 0

    def check_guarantees(self) -> None:
        """Check guarantees and update them if they are lower (upper)
        or higher (lower) than the new values.

        """
        if self.upper > self.max_guarantee:
            self.max_guarantee = self.upper
        if self.lower < self.min_guarantee:
            self.min_guarantee = self.lower

    def modify(
        self, loops: int, upper_coef: float = None, lower_coef: float = None,
        disp: int = 0
        ) -> None:
        """Apply the modify strategy to upper and lower limits.
        If either `upper_coef` or `lower_coef` are None,
        `self.MOD_UPPER` and `self.MOD_LOWER` are respectiveliy used.

        Args:
            loops (int): number of loops to attempt
            upper_coef (float, optional): upper bound coefficient;
                defaults to None
            lower_coef (float, optional): lower bound coefficient;
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
            self.upper = ceil(upper_coef * self.upper) + disp
            self.lower = ceil(lower_coef * self.lower) + disp
            if not self.in_range(loop):
                raise ValueError

        self.check_guarantees()
        self.increase_phase(loops)

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
            on = 1 if i > 0 else 0
            self.upper = ceil((self.DEC_UPPER - u_coef * on) * self.upper)
            self.lower = ceil((self.DEC_LOWER - l_coef * on) * self.lower)
            if not self.in_range(loop):
                raise ValueError

        self.check_guarantees()
        self.increase_phase(loops)


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
                    for dec_b in range(5 - dec_a):
                        for inc_b in range(inc_b_c - inc_c):
                            self.reset_values()
                            try:
                                self.modify(inc_a)
                            except ValueError:
                                # This is a short circuit. Since this
                                # is the first step in the pattern, we
                                # should abort subsequent runs once it
                                # doesn't match.
                                return self.possible

                            try:
                                self.decrease(dec_a)
                                self.modify(inc_b)
                                self.decrease(dec_b)
                                self.modify(inc_c)
                            except ValueError:
                                continue

                            identifier = (
                                f'{inc_a}{dec_a}{inc_b}{dec_b}{inc_c}-'
                                f'{r_a}{r_b}'
                                )
                            self.possible[identifier] = (
                                self.max_guarantee,
                                self.min_guarantee,
                                )


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
            try:
                self.decrease(peak)
                for l_coef, u_coef in self.PAIRS:
                    self.modify(1, l_coef, u_coef)
                self.modify(
                    self.N_PHASES - peak, self.MOD_E, self.MOD_A
                    )
            except ValueError:
                continue

            identifier = f'{peak}'
            self.possible[identifier] = (
                self.max_guarantee,
                self.min_guarantee,
                )


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
        try:
            self.decrease(self.N_PHASES)
        except ValueError:
            return

        self.possible['1'] = (
            self.max_guarantee,
            self.min_guarantee,
            )


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
    MOD_D = 6.0
    MOD_E = 0.4

    DEC_UPPER = 0.9
    DEC_LOWER = 0.4

    def match(self, rate: float) -> None:
        """Checks whether the value matches in range, after multiplying
        both upper and lower bounds by `rate`. Similar to `modify`, but
        only used in pattern 3 and only iterates once.

        Args:
            rate (float): the rate to multiply; should be between
                1.4 and 2

        """
        self.upper = ceil(self.upper * rate)
        self.lower = ceil(self.lower * rate)
        if not self.in_range(0):
            raise ValueError

        self.phase += 1

    def run(self) -> POSSIBLE_PATTERNS:
        """Run every possible combination in this pattern.

        Returns:
            POSSIBLE_PATTERNS: represents pattern (keys) and
                guaranteed maximum and minimum (Tuple[int, int])

        """
        for peak in range(self.PEAK_START, self.PEAK_END):
            self.reset_values()
            try:
                self.decrease(peak)
                for _ in range(2):
                    self.modify(1, MOD_A, MOD_B)
                self.modify(3, MOD_B, MOD_C)
                self.decrease(self.N_PHASES - peak)
            except ValueError:
                continue

            identifier = f'{peak}'
            self.possible[identifier] = (
                self.max_guarantee,
                self.min_guarantee,
                )
