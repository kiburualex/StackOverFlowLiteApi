class User():
    def __init__(self, api):
        self.api = api
        self.users = [
            {
                "id": 1,
                "name": "Alex Kiburu",
                "email": "alexkiburu18@gmail.com",
                "password": "saf&&#d12"
            }
        ]

    def get(self, user_id):
        for user in self.users:
            if user['id'] == user_id:
                return user
        self.api.abort(404, "User {} doesn't exist".format(user_id))

    def create(self, data):
        user = dict()
        user['name'] = str(data.get('name'))
        user['email'] = str(data.get('email'))
        user['password'] = str(data.get('password'))

        """ Ensure table id column value is unique """
        try:
            user['id'] = int(self.user[-1].get('id')) + 1
        except Exception as e:
            user['id'] = 1

            self.users.append(user)

        return user

    def update(self, id, data):
        user = self.get(id)
        user.update(data)
        return user

    def delete(self, id):
        user = self.get(id)
        self.users.remove(user)
