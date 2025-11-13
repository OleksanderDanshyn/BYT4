import unittest
import os

from extentbase import ExtentBase


class TestEntity(ExtentBase):
    def __init__(self, name):
        super().__init__()
        self.name = name


class TestItem(ExtentBase):
    def __init__(self, value):
        super().__init__()
        self.value = value


class TestExtentBase(unittest.TestCase):


    def tearDown(self):
        TestEntity.clear_extent()
        TestItem.clear_extent()

        for filename in ['testentitys.dat', 'testitems.dat', 'custom_test.dat']:
            if os.path.exists(filename):
                os.remove(filename)


    def test_object_added_to_extent_on_creation(self):
        entity1 = TestEntity("Hero")
        entity2 = TestEntity("Villain")
        item1 = TestItem(100)
        item2 = TestItem(200)

        entity_extent = TestEntity.get_extent()
        item_extent = TestItem.get_extent()

        self.assertEqual(len(entity_extent), 2)
        self.assertEqual(len(item_extent), 2)
        self.assertIn(entity1, entity_extent)
        self.assertIn(entity2, entity_extent)
        self.assertIn(item1, item_extent)
        self.assertIn(item2, item_extent)
        self.assertNotIn(item1, entity_extent)
        self.assertNotIn(entity1, item_extent)


    def test_delete_removes_object_from_extent(self):
        entity1 = TestEntity("Hero")
        entity2 = TestEntity("Villain")

        self.assertEqual(len(TestEntity.get_extent()), 2)

        entity1.delete()
        extent = TestEntity.get_extent()

        self.assertEqual(len(extent), 1)
        self.assertNotIn(entity1, extent)
        self.assertIn(entity2, extent)


    def test_delete_object_not_in_extent(self):
        entity = TestEntity("Hero")
        entity.delete()

        try:
            entity.delete()
        except Exception as e:
            self.fail(f"delete() raised exception: {e}")


    def test_clear_extent(self):
        TestEntity("Hero")
        TestEntity("Villain")
        TestEntity("Monster")

        self.assertEqual(len(TestEntity.get_extent()), 3)

        TestEntity.clear_extent()

        self.assertEqual(len(TestEntity.get_extent()), 0)


    def test_save_extent_to_file(self):
        TestEntity("Hero")
        TestEntity("Villain")

        TestEntity.save_extent()

        self.assertTrue(os.path.exists('testentitys.dat'))


    def test_load_extent_from_file(self):
        TestEntity("Hero")
        TestEntity("Villain")

        TestEntity.save_extent()
        TestEntity.clear_extent()

        self.assertEqual(len(TestEntity.get_extent()), 0)

        TestEntity.load_extent()
        extent = TestEntity.get_extent()

        self.assertEqual(len(extent), 2)
        self.assertEqual(extent[0].name, "Hero")
        self.assertEqual(extent[1].name, "Villain")

