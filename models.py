from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ModelParameter:
    name: str
    type: str
    default: Any
    description: str
    min: float = None
    max: float = None
    options: List[str] = None

@dataclass
class AIModel:
    name: str
    provider: str
    model_id: str
    description: str
    parameters: List[ModelParameter]

# Existing Clarity Upscaler model definition
clarity_upscaler = AIModel(
    name="Clarity Upscaler",
    provider="Replicate",
    model_id="philz1337x/clarity-upscaler:dfad41707589d68ecdccd1dfa600d55a208f9310748e44bfe35b4a6291453d5e",
    description="Upscale and enhance images using AI",
    parameters=[
        ModelParameter("seed", "int", 0, "Seed for random number generator, 0 means random"),
        ModelParameter("prompt", "string", "anime style", "Prompt for the image generation"),
        ModelParameter("negative_prompt", "string", "(worst quality, low quality, normal quality:2) JuggernautNegative-neg", "Negative prompt for the image generation"),
        ModelParameter("num_inference_steps", "int", 20, "Number of steps", 1, 100),
        ModelParameter("scheduler", "enum", "DPM++ 3M SDE Karras", "Scheduler for the diffusion process", options=[
            "DPM++ 2M Karras", "DPM++ SDE Karras", "DPM++ 2M SDE Exponential", "DPM++ 2M SDE Karras",
            "Euler a", "Euler", "LMS", "Heun", "DPM2", "DPM2 a", "DPM++ 2S a", "DPM++ 2M", "DPM++ SDE",
            "DPM++ 2M SDE", "DPM++ 2M SDE Heun", "DPM++ 2M SDE Heun Karras", "DPM++ 2M SDE Heun Exponential",
            "DPM++ 3M SDE", "DPM++ 3M SDE Karras", "DPM++ 3M SDE Exponential", "DPM fast", "DPM adaptive",
            "LMS Karras", "DPM2 Karras", "DPM2 a Karras", "DPM++ 2S a Karras", "Restart", "DDIM", "PLMS", "UniPC"
        ]),
        ModelParameter("scale_factor", "float", 2.0, "Scale factor for upscaling", 1.0, 4.0),
        ModelParameter("dynamic", "float", 6.0, "HDR, try from 3 - 9", 1.0, 50.0),
        ModelParameter("creativity", "float", 0.35, "Creativity, try from 0.3 - 0.9", 0.0, 1.0),
        ModelParameter("resemblance", "float", 0.6, "Resemblance, try from 0.3 - 1.6", 0.0, 3.0),
        ModelParameter("tiling_width", "enum", "112", "Fractality, set lower tile width for a high Fractality", options=[str(i) for i in range(16, 257, 16)]),
        ModelParameter("tiling_height", "enum", "144", "Fractality, set lower tile height for a high Fractality", options=[str(i) for i in range(16, 257, 16)]),
        ModelParameter("sd_model", "enum", "juggernaut_reborn.safetensors [338b85bc4f]", "Stable Diffusion model checkpoint", options=[
            "epicrealism_naturalSinRC1VAE.safetensors [84d76a0328]",
            "juggernaut_reborn.safetensors [338b85bc4f]",
            "flat2DAnimerge_v45Sharp.safetensors"
        ]),
        ModelParameter("downscaling", "bool", False, "Downscale the image before upscaling"),
        ModelParameter("downscaling_resolution", "int", 768, "Downscaling resolution", 256, 2048),
        ModelParameter("lora_links", "string", "", "Link to LoRA files, separated by commas"),
        ModelParameter("custom_sd_model", "string", "", "Custom Stable Diffusion model link"),
        ModelParameter("sharpen", "float", 0.0, "Sharpen the image after upscaling", 0.0, 10.0),
        ModelParameter("handfix", "enum", "disabled", "Use clarity to fix hands in the image", options=["disabled", "hands_only", "image_and_hands"]),
        ModelParameter("pattern", "bool", False, "Upscale a pattern with seamless tiling"),
        ModelParameter("output_format", "enum", "png", "Format of the output images", options=["webp", "jpg", "png"])
    ]
)

# New Control Net model
control_net = AIModel(
    name="Control Net",
    provider="Replicate",
    model_id="jagilley/controlnet-canny:aff48af9c68d162388d230a2ab003f68d2638d88307bdaf1c2f1ac95079c9613",
    description="Generate images using Control Net with various control types",
    parameters=[
        ModelParameter("seed", "int", 0, "Set a seed for reproducibility. Random by default."),
        ModelParameter("steps", "int", 28, "Number of steps", 1, 50),
        ModelParameter("prompt", "string", "", "Prompt for image generation"),
        ModelParameter("control_type", "enum", "depth", "Type of control net", options=["canny", "soft_edge", "depth"]),
        ModelParameter("output_format", "enum", "webp", "Format of the output images", options=["webp", "jpg", "png"]),
        ModelParameter("guidance_scale", "float", 3.5, "Guidance scale", 0, 5),
        ModelParameter("output_quality", "int", 80, "Quality of the output images, from 0 to 100", 0, 100),
        ModelParameter("negative_prompt", "string", "", "Things you do not want to see in your image"),
        ModelParameter("control_strength", "float", 0.5, "Strength of control net", 0, 3),
        ModelParameter("depth_preprocessor", "enum", "DepthAnything", "Preprocessor to use with depth control net", options=["Midas", "Zoe", "DepthAnything", "Zoe-DepthAnything"]),
        ModelParameter("soft_edge_preprocessor", "enum", "HED", "Preprocessor to use with soft edge control net", options=["HED", "TEED", "PiDiNet"]),
        ModelParameter("image_to_image_strength", "float", 0, "Strength of image to image control", 0, 1)
    ]
)

flux_control_net = AIModel(
    name="Flux Control Net",
    provider="Replicate",
    model_id="xlabs-ai/flux-dev-controlnet:f2c31c31d81278a91b2447a304dae654c64a5d5a70340fba811bb1cbd41019a2",
    description="Generate images using Flux Control Net with various control types",
    parameters=[
        ModelParameter("seed", "int", 0, "Set a seed for reproducibility. Random by default."),
        ModelParameter("steps", "int", 28, "Number of steps", 1, 50),
        ModelParameter("prompt", "string", "", "Prompt for image generation"),
        ModelParameter("control_type", "enum", "depth", "Type of control net", options=["canny", "soft_edge", "depth"]),
        ModelParameter("output_format", "enum", "webp", "Format of the output images", options=["webp", "jpg", "png"]),
        ModelParameter("guidance_scale", "float", 3.5, "Guidance scale", 0, 5),
        ModelParameter("output_quality", "int", 80, "Quality of the output images, from 0 to 100", 0, 100),
        ModelParameter("negative_prompt", "string", "", "Things you do not want to see in your image"),
        ModelParameter("control_strength", "float", 0.5, "Strength of control net", 0, 3),
        ModelParameter("depth_preprocessor", "enum", "DepthAnything", "Preprocessor to use with depth control net", options=["Midas", "Zoe", "DepthAnything", "Zoe-DepthAnything"]),
        ModelParameter("soft_edge_preprocessor", "enum", "HED", "Preprocessor to use with soft edge control net", options=["HED", "TEED", "PiDiNet"]),
        ModelParameter("image_to_image_strength", "float", 0, "Strength of image to image control", 0, 1)
    ]
)

# Update the available_models list
available_models = [clarity_upscaler, control_net, flux_control_net]