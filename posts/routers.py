class PostsRouter:

    def db_for_read(self, model, **hints):

        if model._meta.app_label == 'posts':
            return 'posts_db'
        return None

    def db_for_write(self, model, **hints):

        if model._meta.app_label == 'posts':
            return 'posts_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):

        if obj1._meta.app_label == 'posts' or \
                obj2._meta.app_label == 'posts':
            return True

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if app_label == 'posts':
            return db == 'posts_db'
        return None