import bpy
from bpy.app.handlers import persistent

def get_api_key(preferences):
    return preferences.api_key

@persistent
def load_handler(dummy):
    # This function will be called when a new file is loaded
    # You can use it to set up any necessary environment variables or perform other initialization tasks
    pass

def register_handlers():
    bpy.app.handlers.load_post.append(load_handler)

def unregister_handlers():
    bpy.app.handlers.load_post.remove(load_handler)
