import bpy

class ReplicateImageToImagePanel(bpy.types.Panel):
    bl_label = "Neural Render"
    bl_idname = "RENDER_PT_replicate_image_to_image"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "replicate_positive_prompt")
        layout.prop(scene, "replicate_negative_prompt")
        layout.prop(scene, "replicate_seed")
        layout.prop(scene, "replicate_steps")
        layout.prop(scene, "replicate_scheduler")
        layout.prop(scene, "replicate_scale_factor")
        layout.prop(scene, "replicate_dynamic")
        layout.prop(scene, "replicate_creativity")
        layout.prop(scene, "replicate_resemblance")
        layout.prop(scene, "replicate_tiling_width")
        layout.prop(scene, "replicate_tiling_height")
        layout.prop(scene, "replicate_sd_model")
        layout.prop(scene, "replicate_downscaling")
        layout.prop(scene, "replicate_downscaling_resolution")
        layout.prop(scene, "replicate_lora_links")
        layout.prop(scene, "replicate_custom_sd_model")
        layout.prop(scene, "replicate_sharpen")
        layout.prop(scene, "replicate_mask")
        layout.prop(scene, "replicate_handfix")
        layout.prop(scene, "replicate_pattern")
        layout.prop(scene, "replicate_output_format")

        layout.operator("render.replicate_image_to_image")