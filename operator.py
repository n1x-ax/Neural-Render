import bpy
import os
import replicate
import tempfile
import requests

from .models import available_models

class ReplicateImageToImageOperator(bpy.types.Operator):
    bl_idname = "render.replicate_image_to_image"
    bl_label = "Render"

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
                raise FileNotFoundError(f"Rendered image not found at {temp_path}")
            
            # Create a new Replicate client with the API key
            client = replicate.Client(api_token=api_key)

            # Get the selected model
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
            output_dir = os.path.dirname(bpy.path.abspath(original_path))
            if not output_dir:
                output_dir = bpy.path.abspath("//")  # Get the directory of the current .blend file
            if not output_dir:
                output_dir = tempfile.gettempdir()  # Fall back to system temp directory if no .blend file is saved
            
            # Use the original filename with a suffix
            original_filename = os.path.basename(original_path)
            name, ext = os.path.splitext(original_filename)
            output_format = scene.replicate_output_format
            output_filename = f"{name}_ai.{output_format}"
            ai_output_path = os.path.join(output_dir, output_filename)
            
            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Download the image from the URL and save it
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(ai_output_path, 'wb') as f:
                    f.write(response.content)
                self.report({'INFO'}, f"Processed image saved: {ai_output_path}")
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

def register():
    bpy.utils.register_class(ReplicateImageToImageOperator)

def unregister():
    bpy.utils.unregister_class(ReplicateImageToImageOperator)

if __name__ == "__main__":
    register()

#type:ignore