import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty

class ReplicateAddonPreferences(AddonPreferences):
    bl_idname = __package__

    api_key: StringProperty(
        name="Replicate API Key",
        description="Enter your Replicate API key",
        subtype='PASSWORD'
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "api_key")