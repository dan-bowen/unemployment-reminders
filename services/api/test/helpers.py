from api import create_app


class Helper:
    def __init__(self):
        self.app = create_app()
        self.client = self.app.test_client()

    # def clean_db(self):
    #     with self.app.app_context():
    #         db.drop_all()
    #         db.create_all()
