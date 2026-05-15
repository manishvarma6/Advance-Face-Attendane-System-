from backend.utils.camera_utils import capture_face_images
from backend.models.user_model import add_user


def register_user(user_id, name, department):

    print("🧑 Registering User...")

    # Save user in database
    add_user(user_id, name, department)

    # Capture images
    capture_face_images(user_id)

    print("✅ User Registered Successfully")