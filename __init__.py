bl_info = {
    "name": "Neural Render",
    "author": "Alex Nix",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "Properties > Render > Neural Render",
    "description": "Process rendered images with AI",
    "warning": "CAUTION: Using this plugin with Replicate API may incur costs. Users are responsible for their usage and any associated charges. Carefully manage your settings to avoid high usage and costs. Refer to the documentation for optimization tips.",
    "doc_url": "https://github.com/n1x-ax/neural-render-blender-addon/readme.md",
    "category": "Render",
}

import bpy
from .operator import ReplicateImageToImageOperator
from .panel import ReplicateImageToImagePanel
from .preferences import ReplicateAddonPreferences

classes = (
    ReplicateAddonPreferences,
    ReplicateImageToImageOperator,
    ReplicateImageToImagePanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.replicate_positive_prompt = bpy.props.StringProperty(
        name="Positive Prompt",
        default="anime style",
        description="Prompt for the image generation"
    )
    bpy.types.Scene.replicate_negative_prompt = bpy.props.StringProperty(
        name="Negative Prompt",
        default="(worst quality, low quality, normal quality:2) JuggernautNegative-neg",
        description="Negative prompt for the image generation"
    )
    bpy.types.Scene.replicate_seed = bpy.props.IntProperty(
        name="Seed",
        default=0,
        description="Seed for random number generator, 0 means random"
    )
    bpy.types.Scene.replicate_steps = bpy.props.IntProperty(
        name="Steps",
        default=20,
        min=1,
        max=100,
        description="Number of steps"
    )
    bpy.types.Scene.replicate_denoising = bpy.props.FloatProperty(
        name="Denoising",
        default=0.75,
        min=0.0,
        max=1.0,
        description="Denoising value"
    )
    bpy.types.Scene.replicate_scheduler = bpy.props.EnumProperty(
        name="Scheduler",
        items=[
            ("DPM++ 2M Karras", "DPM++ 2M Karras", ""),
            ("DPM++ SDE Karras", "DPM++ SDE Karras", ""),
            ("DPM++ 2M SDE Exponential", "DPM++ 2M SDE Exponential", ""),
            ("DPM++ 2M SDE Karras", "DPM++ 2M SDE Karras", ""),
            ("Euler a", "Euler a", ""),
            ("Euler", "Euler", ""),
            ("LMS", "LMS", ""),
            ("Heun", "Heun", ""),
            ("DPM2", "DPM2", ""),
            ("DPM2 a", "DPM2 a", ""),
            ("DPM++ 2S a", "DPM++ 2S a", ""),
            ("DPM++ 2M", "DPM++ 2M", ""),
            ("DPM++ SDE", "DPM++ SDE", ""),
            ("DPM++ 2M SDE", "DPM++ 2M SDE", ""),
            ("DPM++ 2M SDE Heun", "DPM++ 2M SDE Heun", ""),
            ("DPM++ 2M SDE Heun Karras", "DPM++ 2M SDE Heun Karras", ""),
            ("DPM++ 2M SDE Heun Exponential", "DPM++ 2M SDE Heun Exponential", ""),
            ("DPM++ 3M SDE", "DPM++ 3M SDE", ""),
            ("DPM++ 3M SDE Karras", "DPM++ 3M SDE Karras", ""),
            ("DPM++ 3M SDE Exponential", "DPM++ 3M SDE Exponential", ""),
            ("DPM fast", "DPM fast", ""),
            ("DPM adaptive", "DPM adaptive", ""),
            ("LMS Karras", "LMS Karras", ""),
            ("DPM2 Karras", "DPM2 Karras", ""),
            ("DPM2 a Karras", "DPM2 a Karras", ""),
            ("DPM++ 2S a Karras", "DPM++ 2S a Karras", ""),
            ("Restart", "Restart", ""),
            ("DDIM", "DDIM", ""),
            ("PLMS", "PLMS", ""),
            ("UniPC", "UniPC", "")
        ],
        default="DPM++ 3M SDE Karras",
        description="Scheduler for the diffusion process"
    )
    bpy.types.Scene.replicate_sampler_name = bpy.props.EnumProperty(
        name="Sampler Name",
        items=[
            ('euler', 'Euler', 'Euler sampler'),
            ('euler_ancestral', 'Euler Ancestral', 'Euler Ancestral sampler'),
            ('heun', 'Heun', 'Heun sampler'),
            ('dpm_2', 'DPM 2', 'DPM 2 sampler'),
            ('dpm_2_ancestral', 'DPM 2 Ancestral', 'DPM 2 Ancestral sampler'),
            ('lms', 'LMS', 'LMS sampler'),
            ('dpm_fast', 'DPM Fast', 'DPM Fast sampler'),
            ('dpm_adaptive', 'DPM Adaptive', 'DPM Adaptive sampler'),
            ('dpmpp_2s_ancestral', 'DPM++ 2S Ancestral', 'DPM++ 2S Ancestral sampler'),
            ('dpmpp_sde', 'DPM++ SDE', 'DPM++ SDE sampler'),
            ('dpmpp_2m', 'DPM++ 2M', 'DPM++ 2M sampler'),
        ],
        default='euler',
        description="Sampler"
    )
    bpy.types.Scene.replicate_scale_factor = bpy.props.FloatProperty(
        name="Scale Factor",
        default=2.0,
        min=1.0,
        max=4.0,
        description="Scale factor for upscaling"
    )
    bpy.types.Scene.replicate_dynamic = bpy.props.FloatProperty(
        name="Dynamic",
        default=6.0,
        min=1.0,
        max=50.0,
        description="HDR, try from 3 - 9"
    )
    bpy.types.Scene.replicate_creativity = bpy.props.FloatProperty(
        name="Creativity",
        default=0.35,
        min=0.0,
        max=1.0,
        description="Creativity, try from 0.3 - 0.9"
    )
    bpy.types.Scene.replicate_resemblance = bpy.props.FloatProperty(
        name="Resemblance",
        default=0.6,
        min=0.0,
        max=3.0,
        description="Resemblance, try from 0.3 - 1.6"
    )
    bpy.types.Scene.replicate_tiling_width = bpy.props.EnumProperty(
        name="Tiling Width",
        items=[(str(i), str(i), "") for i in range(16, 257, 16)],
        default="112",
        description="Fractality, set lower tile width for a high Fractality"
    )
    bpy.types.Scene.replicate_tiling_height = bpy.props.EnumProperty(
        name="Tiling Height",
        items=[(str(i), str(i), "") for i in range(16, 257, 16)],
        default="144",
        description="Fractality, set lower tile height for a high Fractality"
    )
    bpy.types.Scene.replicate_sd_model = bpy.props.EnumProperty(
        name="SD Model",
        items=[
            ("epicrealism_naturalSinRC1VAE.safetensors [84d76a0328]", "Epic Realism", ""),
            ("juggernaut_reborn.safetensors [338b85bc4f]", "Juggernaut Reborn", ""),
            ("flat2DAnimerge_v45Sharp.safetensors", "Flat 2D Animerge", "")
        ],
        default="juggernaut_reborn.safetensors [338b85bc4f]",
        description="Stable Diffusion model checkpoint"
    )
    bpy.types.Scene.replicate_downscaling = bpy.props.BoolProperty(
        name="Downscaling",
        default=False,
        description="Downscale the image before upscaling"
    )
    bpy.types.Scene.replicate_downscaling_resolution = bpy.props.IntProperty(
        name="Downscaling Resolution",
        default=768,
        min=256,
        max=2048,
        description="Downscaling resolution"
    )
    bpy.types.Scene.replicate_lora_links = bpy.props.StringProperty(
        name="LoRA Links",
        default="",
        description="Link to LoRA files, separated by commas"
    )
    bpy.types.Scene.replicate_custom_sd_model = bpy.props.StringProperty(
        name="Custom SD Model",
        default="",
        description="Custom Stable Diffusion model link"
    )
    bpy.types.Scene.replicate_sharpen = bpy.props.FloatProperty(
        name="Sharpen",
        default=0.0,
        min=0.0,
        max=10.0,
        description="Sharpen the image after upscaling"
    )
    bpy.types.Scene.replicate_mask = bpy.props.StringProperty(
        name="Mask",
        default="",
        description="Mask image URL to mark areas that should be preserved during upscaling"
    )
    bpy.types.Scene.replicate_handfix = bpy.props.EnumProperty(
        name="Hand Fix",
        items=[
            ("disabled", "Disabled", ""),
            ("hands_only", "Hands Only", ""),
            ("image_and_hands", "Image and Hands", "")
        ],
        default="disabled",
        description="Use clarity to fix hands in the image"
    )
    bpy.types.Scene.replicate_pattern = bpy.props.BoolProperty(
        name="Pattern",
        default=False,
        description="Upscale a pattern with seamless tiling"
    )
    bpy.types.Scene.replicate_output_format = bpy.props.EnumProperty(
        name="Output Format",
        items=[
            ("webp", "WebP", ""),
            ("jpg", "JPEG", ""),
            ("png", "PNG", "")
        ],
        default="png",
        description="Format of the output images"
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.replicate_positive_prompt
    del bpy.types.Scene.replicate_negative_prompt
    del bpy.types.Scene.replicate_seed
    del bpy.types.Scene.replicate_steps
    del bpy.types.Scene.replicate_denoising
    del bpy.types.Scene.replicate_scheduler
    del bpy.types.Scene.replicate_sampler_name
    del bpy.types.Scene.replicate_scale_factor
    del bpy.types.Scene.replicate_dynamic
    del bpy.types.Scene.replicate_creativity
    del bpy.types.Scene.replicate_resemblance
    del bpy.types.Scene.replicate_tiling_width
    del bpy.types.Scene.replicate_tiling_height
    del bpy.types.Scene.replicate_sd_model
    del bpy.types.Scene.replicate_downscaling
    del bpy.types.Scene.replicate_downscaling_resolution
    del bpy.types.Scene.replicate_lora_links
    del bpy.types.Scene.replicate_custom_sd_model
    del bpy.types.Scene.replicate_sharpen
    del bpy.types.Scene.replicate_mask
    del bpy.types.Scene.replicate_handfix
    del bpy.types.Scene.replicate_pattern
    del bpy.types.Scene.replicate_output_format

if __name__ == "__main__":
    register()