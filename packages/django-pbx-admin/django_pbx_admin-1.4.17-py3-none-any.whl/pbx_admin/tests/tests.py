from django.test import TestCase
from pbx_admin.views.mixins import PaginationMixin


class AdminListViewTests(TestCase):
    def test_adjacent_pages(self):
        self.assertEqual(
            PaginationMixin._get_adjacent_pages(7, range(1, 12), 2), ([5, 6], [8, 9])
        )
        self.assertEqual(PaginationMixin._get_adjacent_pages(3, range(1, 7), 2), ([2], [4, 5]))

    def test_page_hiding(self):
        self.assertEqual(
            PaginationMixin._hide_page_numbers(7, range(1, 12), 2), ([2, 3, 4], [10])
        )
        self.assertEqual(PaginationMixin._hide_page_numbers(3, range(1, 7), 2), ([], []))
        self.assertEqual(
            PaginationMixin._hide_page_numbers(3, range(1, 11), 3), ([], [7, 8, 9])
        )
