import bpy
import os
import replicate
import tempfile
import requests

#type:ignore

from .models import available_models, clarity_upscaler

class ReplicateImageToImageOperator(bpy.types.Operator):
    bl_idname = "render.replicate_image_to_image"
    bl_label = "Process Image"
    bl_description = "Process the current image using the selected AI model"

    def invoke(self, context, event):
        try:
            return self.execute(context)
        except Exception as e:
            self.report({'ERROR'}, f"Error in operator: {str(e)}")
            return {'CANCELLED'}

    def execute(self, context):
        try:
            scene = context.scene
            preferences = context.preferences.addons[__package__].preferences

            if not preferences.api_key:
                self.report({'ERROR'}, "Replicate API key not set. Please set it in the add-on preferences.")
                return {'CANCELLED'}

            api_key = preferences.api_key

            # Determine if we're upscaling or using the original functionality
            is_upscaling = context.area.type == 'IMAGE_EDITOR'

            if is_upscaling:
                # Use the current image in the Image Editor
                image = context.space_data.image
                if not image:
                    self.report({'ERROR'}, "No image selected in Image Editor")
                    return {'CANCELLED'}
                
                # Save the current image to a temporary file
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                    temp_path = temp_file.name
                image.save_render(temp_path)
            else:
                # Create a temporary file to save the render
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                    temp_path = temp_file.name

                # Store the original render path
                original_path = scene.render.filepath

                # Set the render path to our temporary file
                scene.render.filepath = temp_path

                # Render the image
                bpy.ops.render.render(write_still=True)

                # Restore the original render path
                scene.render.filepath = original_path

            # Check if the file exists
            if not os.path.exists(temp_path):
                raise FileNotFoundError(f"Image not found at {temp_path}")
            
            # Create a new Replicate client with the API key
            client = replicate.Client(api_token=api_key)

            if is_upscaling:
                # Use Clarity Upscaler for upscaling
                selected_model = clarity_upscaler
                input_params = {
                    "image": open(temp_path, "rb"),
                    "scale_factor": scene.upscale_scale_factor,
                    "prompt": scene.upscale_prompt,
                    "negative_prompt": scene.upscale_negative_prompt,
                    "seed": scene.upscale_seed,
                    "num_inference_steps": scene.upscale_num_inference_steps,
                    "scheduler": scene.upscale_scheduler,
                    "dynamic": scene.upscale_dynamic,
                    "creativity": scene.upscale_creativity,
                    "resemblance": scene.upscale_resemblance,
                }
            else:
                # Get the selected model for the original functionality
                selected_model = next((model for model in available_models if model.name == scene.replicate_model), None)
                if not selected_model:
                    raise ValueError(f"Selected model '{scene.replicate_model}' not found")

                # Prepare input parameters
                input_params = {}
                for param in selected_model.parameters:
                    if param.name not in ["control_image", "mask"]:  # Skip both control_image and mask parameters
                        param_value = getattr(scene, f"replicate_{param.name}")
                        if param.type == "enum" and param.name in ["tiling_width", "tiling_height"]:
                            param_value = int(param_value)
                        input_params[param.name] = param_value

                # Handle the image parameter differently for each model
                if selected_model.name == "Clarity Upscaler":
                    input_params["image"] = open(temp_path, "rb")
                elif selected_model.name == "Control Net":
                    input_params["image"] = open(temp_path, "rb")
                    input_params["control_image"] = open(temp_path, "rb")  # Use the rendered image as control image
                elif selected_model.name == "Flux Control Net":
                    input_params["image"] = open(temp_path, "rb")
                    input_params["control_image"] = open(temp_path, "rb")

            # Run the Replicate model
            output = client.run(
                selected_model.model_id,
                input=input_params
            )

            # Process the output
            if isinstance(output, list):
                if selected_model.name == "Control Net":
                    # For Control Net, always use the second image (index 1)
                    image_url = output[1] if len(output) > 1 else None
                else:
                    # For other models, use the first image
                    image_url = output[0] if output else None
            else:
                image_url = output
            
            # Determine the output path
            if is_upscaling:
                output_dir = os.path.dirname(bpy.path.abspath(image.filepath))
                original_filename = os.path.basename(image.filepath)
            else:
                output_dir = os.path.dirname(bpy.path.abspath(original_path))
                original_filename = os.path.basename(original_path)

            if not output_dir:
                output_dir = bpy.path.abspath("//")  # Get the directory of the current .blend file
            if not output_dir:
                output_dir = tempfile.gettempdir()  # Fall back to system temp directory if no .blend file is saved
            
            # Use the original filename with a suffix
            name, ext = os.path.splitext(original_filename)
            output_format = scene.replicate_output_format if hasattr(scene, 'replicate_output_format') else 'png'
            output_filename = f"{name}_{'upscaled' if is_upscaling else 'ai'}.{output_format}"
            ai_output_path = os.path.join(output_dir, output_filename)
            
            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Download the image from the URL and save it
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(ai_output_path, 'wb') as f:
                    f.write(response.content)
                self.report({'INFO'}, f"Processed image saved: {ai_output_path}")
                self.open_image_in_new_window(ai_output_path)
            else:
                raise RuntimeError(f"Failed to download the processed image. Status code: {response.status_code}")

        except Exception as e:
            self.report({'ERROR'}, f"Error processing image: {str(e)}")
            return {'CANCELLED'}
        finally:
            # Clean up the temporary file
            if 'temp_path' in locals():
                try:
                    os.unlink(temp_path)
                except Exception as e:
                    self.report({'WARNING'}, f"Failed to delete temporary file: {str(e)}")

        return {'FINISHED'}

    def open_image_in_new_window(self, image_path):
        # Load the image
        image = bpy.data.images.load(image_path)
        
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
        
        self.report({'INFO'}, f"Processed image opened in a new window")

def register():
    bpy.utils.register_class(ReplicateImageToImageOperator)

def unregister():
    bpy.utils.unregister_class(ReplicateImageToImageOperator)

if __name__ == "__main__":
    register()