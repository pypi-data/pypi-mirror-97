import snakeeyes


def test_roll():
    """
    Test whether the test

    Args:
    """
    return snakeeyes.Roll("1d20")


class TestMath():
    def test_add(self):
        """
        Returns the test test for the test.

        Args:
            self: (todo): write your description
        """
        return snakeeyes.Roll("1d20+5")

    def test_sub(self):
        """
        Returns the test sub - test test.

        Args:
            self: (todo): write your description
        """
        return snakeeyes.Roll("1d20-5")

    def test_mult(self):
        """
        Return the test test test test.

        Args:
            self: (todo): write your description
        """
        return snakeeyes.Roll("1d20*5")

    def test_div(self):
        """
        Return the test test.

        Args:
            self: (todo): write your description
        """
        return snakeeyes.Roll("1d20/5")

    def test_raw(self):
        """
        Returns raw test test test test.

        Args:
            self: (todo): write your description
        """
        return snakeeyes.Roll("25*3")

    def test_parenth(self):
        """
        Return the test test test.

        Args:
            self: (todo): write your description
        """
        return snakeeyes.Roll("(1d20+5)*20")

class TestMultiDice():
    @staticmethod
    def test_add():
        """
        Add test test to a test

        Args:
        """
        return snakeeyes.Roll("1d6+2d10")
    @staticmethod
    def test_subtract():
        """
        Subtract test test test test

        Args:
        """
        return snakeeyes.Roll("3d20-6d20")
    @staticmethod
    def test_divide():
        """
        Divide a test test.

        Args:
        """
        return snakeeyes.Roll("7d10/3d20")
    @staticmethod
    def test_mult():
        """
        Return a test test function

        Args:
        """
        return snakeeyes.Roll("3d20*2d10")
    @staticmethod
    def test_exp():
        """
        Return the test test.

        Args:
        """
        return snakeeyes.Roll("3d20x15*2d10x15")
    @staticmethod
    def test_succ():
        """
        Returns the test test suite.

        Args:
        """
        return snakeeyes.Roll("3d20>10+2d20>10")


class TestOperators():
    def test_success(self):
        """
        Return the test test.

        Args:
            self: (todo): write your description
        """
        return snakeeyes.Roll("1d20>5")

    def test_explode(self):
        """
        Return the test test.

        Args:
            self: (todo): write your description
        """
        return snakeeyes.Roll("100d20x10")
