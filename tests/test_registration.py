

from backend.controllers.register_controller import register_user


if __name__ == "__main__":

    user_id = "user_02"
    name = "Jitendar Verma"
    department = "BCA"

    register_user(user_id, name, department)