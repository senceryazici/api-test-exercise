from APIClient import TestAPI

api = TestAPI()
api.initialize()

user, success = api.get_user("user1")
