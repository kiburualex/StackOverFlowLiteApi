
class User():
    def __init__(self, api):
        self.api = api
        self.counter = 0
        self.users = [
            {
                'id': 1, 
                'name': 'Alex Kiburu', 
                'email': 'alexkiburu18@gmail.com',
                'password': 'saf&&#d12'
            },
            {
                'id': 2, 
                'name': 'James Konan', 
                'email': 'jk@gmail.com',
                'password': '1121**#d12'
            },
        ]

    def get(self, id):
        for user in self.users:
            if user['id'] == id:
                return user
        self.api.abort(404, "User {} doesn't exist".format(id))

    def create(self, data):
        user = data
        user['id'] = self.counter = self.counter + 1
        self.users.append(user)
        return user

    def update(self, id, data):
        user = self.get(id)
        user.update(data)
        return user

    def delete(self, id):
        user = self.get(id)
        self.users.remove(user)