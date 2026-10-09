import unittest

from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):
    def setUp(self):
        self.fine = DuckFine("M001")

    # The typical generated suite (Week 6, Appendix A)

    def test_charge_returns_a_fee_for_a_late_duck(self):
        self.assertEqual(self.fine.charge(5), 1.50)

    def test_deluxe_duck_costs_more(self):
        self.assertTrue(self.fine.charge(5, deluxe=True) > 0)

    def test_no_fee_when_returned_on_time(self):
        self.assertEqual(self.fine.charge(0), 0.0)

    def test_negative_days_raises(self):
        with self.assertRaises(ValueError):
            self.fine.charge(-1)

    # Tests added in Part 2, one per fault the generated suite missed.
    # Expected values come from the brief, not from running the code.

    def test_fine_is_capped_at_five_dollars(self):
        # 30 days late = 28 chargeable days x $0.50 = $14, capped at $5
        self.assertEqual(self.fine.charge(30), 5.00)

    def test_fines_accumulate_against_the_member_account(self):
        self.fine.charge(5)   # $1.50
        self.fine.charge(4)   # $1.00
        self.assertEqual(self.fine.total_owed, 2.50)

    def test_deluxe_fee_is_exactly_double(self):
        # 5 days late = 3 chargeable days x $0.50 = $1.50, doubled = $3.00
        self.assertEqual(self.fine.charge(5, deluxe=True), 3.00)


if __name__ == "__main__":
    unittest.main()
