import bpy
from .models import available_models, ModelParameter

class ReplicateImageToImagePanel(bpy.types.Panel):
    bl_label = "Neural Render"
    bl_idname = "RENDER_PT_replicate_image_to_image"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "replicate_model")

        selected_model = next((model for model in available_models if model.name == scene.replicate_model), None)
        if selected_model:
            for param in selected_model.parameters:
                if param.name not in ["control_image", "mask"]:  # Skip both control_image and mask parameters
                    if param.type == "enum":
                        layout.prop(scene, f"replicate_{param.name}")
                    elif param.type == "bool":
                        layout.prop(scene, f"replicate_{param.name}")
                    else:
                        layout.prop(scene, f"replicate_{param.name}")

        layout.operator("render.replicate_image_to_image")