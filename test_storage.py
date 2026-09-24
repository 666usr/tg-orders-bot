import os
import tempfile
import unittest

import storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        handle, self.path = tempfile.mkstemp(suffix=".db")
        os.close(handle)
        storage.init_db(self.path)

    def tearDown(self):
        os.unlink(self.path)

    def test_add_and_count(self):
        self.assertEqual(storage.count_orders(self.path), 0)
        order_id = storage.add_order(1, "user", "Анна", "@anna", "Нужен бот", db_path=self.path)
        self.assertEqual(order_id, 1)
        self.assertEqual(storage.count_orders(self.path), 1)

    def test_list_orders_newest_first(self):
        storage.add_order(1, "a", "Первая", "1", "текст", db_path=self.path)
        storage.add_order(2, "b", "Вторая", "2", "текст", db_path=self.path)
        orders = storage.list_orders(self.path)
        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0]["name"], "Вторая")

    def test_status_is_new_by_default(self):
        storage.add_order(1, "a", "Анна", "1", "текст", db_path=self.path)
        orders = storage.list_orders(self.path)
        self.assertEqual(orders[0]["status"], "новая")


if __name__ == "__main__":
    unittest.main()
