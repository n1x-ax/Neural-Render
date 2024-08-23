import subprocess
import sys
import os

bl_info = {
    "name": "Neural Render",
    "author": "Alex Nix",
    "version": (1, 0),
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
from .panel import ReplicateImageToImagePanel
from .preferences import ReplicateAddonPreferences
from .models import available_models

classes = (
    ReplicateAddonPreferences,
    ReplicateImageToImageOperator,
    ReplicateImageToImagePanel,
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
        bpy.utils.register_class(cls)
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

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.replicate_model
    for model in available_models:
        for param in model.parameters:
            if param.name not in ["control_image", "mask"]:  # Skip both control_image and mask parameters
                delattr(bpy.types.Scene, f"replicate_{param.name}")
    del bpy.types.Scene.replicate_return_preprocessed_image

if __name__ == "__main__":
    register()