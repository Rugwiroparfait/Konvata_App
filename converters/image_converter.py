from PIL import Image

def convert_image_format(input_file, target_format):
    img = Image.open(input_file)
    output_file = f"{input_file.rsplit('.', 1)[0]}.{target_format}"
    img.save(output_file, target_format.upper())
