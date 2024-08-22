# Neural Render - Blender Addon

## Description
Neural Render is a Blender addon that integrates the Clarity Upscaler AI model from Replicate into your Blender workflow. It allows you to process rendered images with AI, enhancing their quality and resolution directly within Blender.

## Features
- Upscale and enhance rendered images using AI
- Customizable parameters for AI processing
- Seamless integration with Blender's render pipeline
- Support for various Stable Diffusion models
- Options for tiling, downscaling, and custom LoRA models

## Installation
1. Download the addon ZIP file
2. In Blender, go to Edit > Preferences > Add-ons
3. Click "Install" and select the downloaded ZIP file
4. Enable the "Render: Neural Render" addon

## Usage
1. Set up your Replicate API key in the addon preferences
2. Go to the Properties panel > Render tab > Neural Render section
3. Adjust the AI processing parameters as needed
4. Click the "Neural Render" button to render image with AI

## Requirements
- Blender 4.2.0 or higher
- Active internet connection
- Replicate account
- Replicate API key

## Getting Started with Replicate

1. Visit the Replicate website: https://replicate.com
2. Sign up for an account if you don't have one
3. Once logged in, go to your account settings
4. Find the API tokens section and generate a new API token
5. Copy this API token and keep it secure - you'll need it for the addon

Remember to never share your API token publicly. You can always generate a new token if needed.

## Configuration
- API Key: Enter your Replicate API key in the addon preferences
- Positive Prompt: Describe what you want to enhance in the image
- Negative Prompt: Describe what you want to avoid in the image
- Seed: Set a seed for reproducible results
- Steps: Number of inference steps
- Scheduler: Choose the AI scheduler algorithm
- Scale Factor: Set the upscaling factor
- Other parameters: Adjust creativity, resemblance, tiling, etc.

## Support
For issues, feature requests, or contributions, please visit the GitHub repository.

## Usage Recommendations and Cautions

### CAUTION
Using this plugin with Replicate API may incur costs. Users are responsible for their usage and any associated charges. Carefully manage your settings to avoid high usage and costs.

### Usage Recommendations
- You can render very low quality without downscaling for fast speed and low pricing.
- Use downscale when rendering more than 1024 pixels in size.
- To keep details while downscaling, you can render up to any resolutions (2-6k), but it's very important to use downscale to maintain details while saving usage and costs.
- If using a scale factor more than 2, make sure your rendered images have low resolution.

### Useful Tips
- Change the seed to diversify your generation.
- Lower creativity and resemblance values will only upscale/enhance your render. For creative outputs, try increasing these numbers and don't hesitate to experiment.

## Parameter Descriptions

- Positive Prompt: Describe what you want to enhance or add to the image.
- Negative Prompt: Describe what you want to avoid or remove from the image.
- Seed: Set a seed for reproducible results (0 means random).
- Steps: Number of inference steps (higher values may produce better quality but take longer).
- Scheduler: Choose the AI scheduler algorithm for the diffusion process.
- Scale Factor: Set the upscaling factor for the image.
- Dynamic: Adjusts the HDR effect, try values from 3 to 9.
- Creativity: Controls the level of creative interpretation, try values from 0.3 to 0.9.
- Resemblance: Determines how closely the output resembles the input, try values from 0.3 to 1.6.
- Tiling Width/Height: Affects the fractality of the image, lower values result in higher fractality.
- SD Model: Choose the Stable Diffusion model checkpoint.
- Downscaling: Enable to downscale the image before upscaling (recommended for large images).
- Downscaling Resolution: Set the resolution for downscaling.
- LoRA Links: Add links to LoRA files for additional fine-tuning.
- Custom SD Model: Provide a link to a custom Stable Diffusion model.
- Sharpen: Apply sharpening to the image after upscaling.
- Mask: Provide a mask image URL to preserve specific areas during upscaling.
- Hand Fix: Use Clarity to fix hands in the image.
- Pattern: Enable for upscaling patterns with seamless tiling.
- Output Format: Choose the format for the output images (WebP, JPEG, or PNG).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits
- Developed by Alex Nix
- Powered by Replicate and the Clarity Upscaler model
- Built for Blender, the free and open source 3D creation suite

## Disclaimer
This addon requires an active Replicate account and API usage may incur costs. Please refer to Replicate's pricing for more information.
