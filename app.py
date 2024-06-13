from flask import Flask, request

app = Flask(__name__)

users = [{ "user_id": 1, "first_name": "John", "last_name": "Doe"},
         { "user_id": 2, "first_name": "Jane", "last_name": "Doe"}]

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

#/users

@app.route("/users", methods=['GET', 'POST'])
def get_users():
    try:
        if request.method == 'GET':
            return users
        else:
            user = request.json
            user["user_id"] = len(users) + 1
            users.append(user)
            return user, 200
    except Exception as e:
        print(e)
        return "Oops, something went wrong", 500

@app.route("/users/<int:user_id>", methods=['GET', 'PUT'])
def get_user(user_id):
    if request.method == 'GET':
        for user in users:
            if user["user_id"] == user_id:
                return user, 200
    else:
        for user in users:
            if user["user_id"] == user_id:
                user.update(request.json)
                return user, 200
    return {"user_id": 0, "first_name": "", "last_name": ""}, 404

if __name__ == '__main__':
    app.run(debug=True)