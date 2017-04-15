from hypatia import class_get, class_default, class_override

class TestClassOverriding:
    def test_default_class_added_to_list(self):
        @class_default
        class TestClass:
            pass

        assert class_get("TestClass") == TestClass

    def test_overriding_class_works(self):
        @class_default
        class TestClass:
            pass

        @class_override("TestClass")
        class OverrideClass(class_get("TestClass")):
            pass

        assert class_get("TestClass") == OverrideClass
