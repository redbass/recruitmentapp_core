class User(object):

    def __init__(self, _id):
        self.id = _id
        self.password = self._create_password(_id)

    def check_password(self, password):
        return password == self.id + "_secret"

    @staticmethod
    def _create_password(_id):
        return _id + "_secret"


users = {key: User(key) for key in ['luca', 'claudia']}
