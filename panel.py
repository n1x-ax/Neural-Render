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

        layout.operator("render.replicate_image_to_image", text="Process Image")

class UpscaleImagePanel(bpy.types.Panel):
    bl_label = "Upscale Image"
    bl_idname = "IMAGE_PT_upscale"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "upscale_scale_factor")
        layout.prop(scene, "upscale_prompt")
        layout.prop(scene, "upscale_negative_prompt")
        layout.prop(scene, "upscale_seed")
        layout.prop(scene, "upscale_num_inference_steps")
        layout.prop(scene, "upscale_scheduler")
        layout.prop(scene, "upscale_dynamic")
        layout.prop(scene, "upscale_creativity")
        layout.prop(scene, "upscale_resemblance")

        layout.operator("render.replicate_image_to_image", text="Upscale Image")

class UpscaleRenderResultPanel(bpy.types.Panel):
    bl_label = "Upscale Render"
    bl_idname = "RENDER_PT_upscale"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        layout.operator("render.replicate_image_to_image", text="Upscale Render")
        layout.operator("render.open_last_render", text="Open Last Render")

class OpenLastRenderOperator(bpy.types.Operator):
    bl_idname = "render.open_last_render"
    bl_label = "Open Last Render"
    bl_description = "Open the last rendered image in a new window"

    def execute(self, context):
        last_render = bpy.data.images['Render Result']
        if last_render:
            self.open_image_in_new_window(last_render)
        else:
            self.report({'ERROR'}, "No render result available")
        return {'FINISHED'}

    def open_image_in_new_window(self, image):
        # Create a new window
        bpy.ops.screen.new()
        
        # Get the new window and change its type to IMAGE_EDITOR
        for window in bpy.context.window_manager.windows:
            if window.screen.name == 'temp':
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.type = 'IMAGE_EDITOR'
                        for space in area.spaces:
                            if space.type == 'IMAGE_EDITOR':
                                space.image = image
                        break
                break
        
        self.report({'INFO'}, f"Render result opened in a new window")

def register():
    bpy.utils.register_class(ReplicateImageToImagePanel)
    bpy.utils.register_class(UpscaleImagePanel)
    bpy.utils.register_class(UpscaleRenderResultPanel)
    bpy.utils.register_class(OpenLastRenderOperator)

def unregister():
    bpy.utils.unregister_class(ReplicateImageToImagePanel)
    bpy.utils.unregister_class(UpscaleImagePanel)
    bpy.utils.unregister_class(UpscaleRenderResultPanel)
    bpy.utils.unregister_class(OpenLastRenderOperator)