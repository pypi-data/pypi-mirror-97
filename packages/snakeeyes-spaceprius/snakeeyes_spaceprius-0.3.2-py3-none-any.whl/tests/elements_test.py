import snakeeyes


class TestDieBools():
    @staticmethod
    def test_die():
        """
        Set the test test.

        Args:
            self: (todo): write your description
        """
        die = bool(snakeeyes.DiceGroup("28*15"))
        assert die is False
