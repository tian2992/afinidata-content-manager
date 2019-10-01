from django.test import TestCase

class MyConfigLoadTest(TestCase):
    def test_imports(self):
        import content_manager.settings.local
        import content_manager.settings.production
