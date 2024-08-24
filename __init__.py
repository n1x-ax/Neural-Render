import subprocess
import sys
import os

bl_info = {
    "name": "Neural Render",
    "author": "Alex Nix",
    "version": (1, 0, 1),
    "blender": (4, 2, 0),
    "location": "Properties > Render > Neural Render",
    "description": "Process rendered images with AI",
    "warning": "Requires internet; may incur API costs; manage settings carefully and refer to docs for optimization.",
    "doc_url": "https://github.com/n1x-ax/Neural-Render",
    "category": "Render",
    "license": "GPL-3.0-or-later",
}

import bpy
from .operator import ReplicateImageToImageOperator
from .panel import ReplicateImageToImagePanel, UpscaleImagePanel, UpscaleRenderResultPanel, OpenLastRenderOperator
from .preferences import ReplicateAddonPreferences
from .models import available_models

classes = (
    ReplicateAddonPreferences,
    ReplicateImageToImageOperator,
    ReplicateImageToImagePanel,
    UpscaleImagePanel,
    UpscaleRenderResultPanel,
    OpenLastRenderOperator,
)

def check_and_install_dependencies():
    required_packages = ['replicate', 'requests']
    
    # Get Blender's Python executable path
    python_exe = sys.executable
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} not found. Attempting to install...")
            try:
                subprocess.check_call([python_exe, "-m", "pip", "install", package])
                print(f"Successfully installed {package}")
            except subprocess.CalledProcessError:
                print(f"Failed to install {package}. Please install it manually.")
                return False
    return True

def register():
    if not check_and_install_dependencies():
        raise ImportError("Required dependencies are not installed. Please install them manually.")

    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError as e:
            # Class is already registered, so we'll unregister and re-register
            if "already registered" in str(e):
                bpy.utils.unregister_class(cls)
                bpy.utils.register_class(cls)
            else:
                raise e

    bpy.types.Scene.replicate_model = bpy.props.EnumProperty(
        name="AI Model",
        items=[(model.name, model.name, model.description) for model in available_models],
        default=available_models[0].name if available_models else "",
        description="Select the AI model to use"
    )

    for model in available_models:
        for param in model.parameters:
            if param.name not in ["control_image", "mask"]:  # Skip both control_image and mask parameters
                if param.type == "int":
                    setattr(bpy.types.Scene, f"replicate_{param.name}", bpy.props.IntProperty(
                        name=param.name.replace("_", " ").title(),
                        default=param.default,
                        description=param.description,
                        min=int(param.min) if param.min is not None else -2**31,
                        max=int(param.max) if param.max is not None else 2**31 - 1
                    ))
                elif param.type == "float":
                    setattr(bpy.types.Scene, f"replicate_{param.name}", bpy.props.FloatProperty(
                        name=param.name.replace("_", " ").title(),
                        default=param.default,
                        description=param.description,
                        min=param.min if param.min is not None else -float('inf'),
                        max=param.max if param.max is not None else float('inf')
                    ))
                elif param.type == "bool":
                    setattr(bpy.types.Scene, f"replicate_{param.name}", bpy.props.BoolProperty(
                        name=param.name.replace("_", " ").title(),
                        default=param.default,
                        description=param.description
                    ))
                elif param.type == "enum":
                    setattr(bpy.types.Scene, f"replicate_{param.name}", bpy.props.EnumProperty(
                        name=param.name.replace("_", " ").title(),
                        items=[(option, option, "") for option in param.options],
                        default=param.default,
                        description=param.description
                    ))
                else:  # string
                    setattr(bpy.types.Scene, f"replicate_{param.name}", bpy.props.StringProperty(
                        name=param.name.replace("_", " ").title(),
                        default=param.default,
                        description=param.description
                    ))

    bpy.types.Scene.replicate_return_preprocessed_image = bpy.props.BoolProperty(
        name="Return Preprocessed Image",
        description="Return the preprocessed image used to control the generation process",
        default=False
    )

    bpy.types.Scene.replicate_seed = bpy.props.IntProperty(
        name="Seed",
        default=0,
        description="Seed for random number generator, 0 means random"
    )
    bpy.types.Scene.upscale_scale_factor = bpy.props.FloatProperty(
        name="Scale Factor",
        default=2.0,
        min=1.0,
        max=4.0,
        description="Scale factor for upscaling"
    )
    bpy.types.Scene.upscale_prompt = bpy.props.StringProperty(
        name="Prompt",
        default="anime style",
        description="Prompt for the image generation"
    )
    bpy.types.Scene.upscale_negative_prompt = bpy.props.StringProperty(
        name="Negative Prompt",
        default="(worst quality, low quality, normal quality:2) JuggernautNegative-neg",
        description="Negative prompt for the image generation"
    )
    bpy.types.Scene.upscale_num_inference_steps = bpy.props.IntProperty(
        name="Steps",
        default=20,
        min=1,
        max=100,
        description="Number of inference steps"
    )
    bpy.types.Scene.upscale_scheduler = bpy.props.EnumProperty(
        name="Scheduler",
        items=[("DPM++ 3M SDE Karras", "DPM++ 3M SDE Karras", "")],
        default="DPM++ 3M SDE Karras",
        description="Scheduler for the diffusion process"
    )
    bpy.types.Scene.upscale_dynamic = bpy.props.FloatProperty(
        name="Dynamic",
        default=6.0,
        min=1.0,
        max=50.0,
        description="HDR, try from 3 - 9"
    )
    bpy.types.Scene.upscale_creativity = bpy.props.FloatProperty(
        name="Creativity",
        default=0.35,
        min=0.0,
        max=1.0,
        description="Creativity, try from 0.3 - 0.9"
    )
    bpy.types.Scene.upscale_resemblance = bpy.props.FloatProperty(
        name="Resemblance",
        default=0.6,
        min=0.0,
        max=3.0,
        description="Resemblance, try from 0.3 - 1.6"
    )
    bpy.types.Scene.upscale_seed = bpy.props.IntProperty(
        name="Seed",
        default=0,
        description="Seed for random number generator, 0 means random"
    )

def unregister():
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass  # Class is already unregistered, so we can ignore this error

    del bpy.types.Scene.replicate_model
    for model in available_models:
        for param in model.parameters:
            if param.name not in ["control_image", "mask"]:  # Skip both control_image and mask parameters
                delattr(bpy.types.Scene, f"replicate_{param.name}")
    del bpy.types.Scene.replicate_return_preprocessed_image
    del bpy.types.Scene.replicate_seed
    del bpy.types.Scene.upscale_scale_factor
    del bpy.types.Scene.upscale_prompt
    del bpy.types.Scene.upscale_negative_prompt
    del bpy.types.Scene.upscale_num_inference_steps
    del bpy.types.Scene.upscale_scheduler
    del bpy.types.Scene.upscale_dynamic
    del bpy.types.Scene.upscale_creativity
    del bpy.types.Scene.upscale_resemblance
    del bpy.types.Scene.upscale_seed

if __name__ == "__main__":
    register()