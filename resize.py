from PIL import Image
import os

class ImageResizer:
    def resize_image(self, image_path, new_width, new_height):
        image = Image.open(image_path)
        resized_image = image.resize((new_width, new_height))
        return resized_image

    def resize_and_save(self, image_path, new_width, new_height, output_path):
        image = Image.open(image_path)
        resized_image = image.resize((new_width, new_height))
        resized_image.save(output_path)

    def resize_all_images(self, folder_path, new_width, new_height):
        for filename in os.listdir(folder_path):
            if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".PNG"):
                image_path = os.path.join(folder_path, filename)
                output_path = os.path.join(folder_path, filename)
                self.resize_and_save(image_path, new_width, new_height, output_path)

if __name__ == "__main__":
    # Replace 'sprites' with the path to the folder containing the images you want to resize
    folder_path = 'images'
    new_width = 640
    new_height = 500

    resizer = ImageResizer()
    resizer.resize_all_images(folder_path, new_width, new_height)