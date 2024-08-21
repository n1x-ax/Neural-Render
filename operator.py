import bpy
import os
import replicate
import tempfile
import requests

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

            # Run the Replicate model
            with open(temp_path, "rb") as file:
                output = client.run(
                    "philz1337x/clarity-upscaler:dfad41707589d68ecdccd1dfa600d55a208f9310748e44bfe35b4a6291453d5e",
                    input={
                        "image": file,
                        "seed": scene.replicate_seed,
                        "prompt": scene.replicate_positive_prompt,
                        "negative_prompt": scene.replicate_negative_prompt,
                        "num_inference_steps": scene.replicate_steps,
                        "scheduler": scene.replicate_scheduler,
                        "scale_factor": scene.replicate_scale_factor,
                        "dynamic": scene.replicate_dynamic,
                        "creativity": scene.replicate_creativity,
                        "resemblance": scene.replicate_resemblance,
                        "tiling_width": int(scene.replicate_tiling_width),
                        "tiling_height": int(scene.replicate_tiling_height),
                        "sd_model": scene.replicate_sd_model,
                        "downscaling": scene.replicate_downscaling,
                        "downscaling_resolution": scene.replicate_downscaling_resolution,
                        "lora_links": scene.replicate_lora_links,
                        "custom_sd_model": scene.replicate_custom_sd_model,
                        "sharpen": scene.replicate_sharpen,
                        "handfix": scene.replicate_handfix,
                        "pattern": scene.replicate_pattern,
                        "output_format": scene.replicate_output_format
                    }
                )
            
            # Process the output
            if isinstance(output, list) and len(output) > 0 and isinstance(output[0], str) and output[0].startswith('http'):
                output_url = output[0]
                
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
                response = requests.get(output_url)
                if response.status_code == 200:
                    with open(ai_output_path, 'wb') as f:
                        f.write(response.content)
                    self.report({'INFO'}, f"Processed image saved: {ai_output_path}")
                else:
                    raise RuntimeError(f"Failed to download the processed image. Status code: {response.status_code}")
            else:
                raise ValueError(f"Unexpected output from Replicate: {output}")

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