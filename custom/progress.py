from PIL import Image, ImageDraw, ImageFilter

def generate_progress_bar_image(percentage, width=300, height=20, scale_factor=4):  # Increased scale factor
    scaled_width = width * scale_factor
    scaled_height = height * scale_factor
    radius = scaled_height // 2
    padding = 2 * scale_factor

    background_color = '#F0F0F0'
    border_color = '#CCCCCC'
    fill_color_start = '#76cdd8'
    fill_color_end = '#3483eb'

    image = Image.new('RGBA', (scaled_width, scaled_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    bg_shape = [(0, 0), (scaled_width, scaled_height)]
    draw.rounded_rectangle(bg_shape, radius=radius, fill=background_color, outline=border_color, width=padding)

    fill_width = max(0, int((percentage / 100) * (scaled_width - 2 * (padding + 1))))
    fill_image = Image.new('RGBA', (fill_width, scaled_height - 2 * (padding + 1)), (0, 0, 0, 0))
    fill_draw = ImageDraw.Draw(fill_image)

    for i in range(fill_width):
        blend_factor = i / max(1, fill_width - 1)
        blend_color = tuple([
            int((int(fill_color_start[j:j+2], 16) * (1 - blend_factor) + int(fill_color_end[j:j+2], 16) * blend_factor))
            for j in (1, 3, 5)
        ]) + (255,)
        fill_draw.line([(i, 0), (i, fill_image.height)], fill=blend_color)

    mask = Image.new('L', (fill_width, fill_image.height), 0)
    mask_draw = ImageDraw.Draw(mask)
    if fill_width > 2 * radius:
        mask_draw.ellipse([(0, 0), (2 * radius, scaled_height - 2 * (padding + 1))], fill=255)
        mask_draw.rectangle([(radius, 0), (fill_width - radius, fill_image.height)], fill=255)
        mask_draw.ellipse([(fill_width - 2 * radius, 0), (fill_width, fill_image.height)], fill=255)
    else:
        mask_draw.ellipse([(0, 0), (fill_width, scaled_height - 2 * (padding + 1))], fill=255)

    fill_image.putalpha(mask)
    image.paste(fill_image, (padding + 1, padding + 1), fill_image)

    final_image = image.resize((width, height), Image.Resampling.LANCZOS)

    file_path = 'settings/images/progress_ultra_hd.png'
    final_image.save(file_path)
    return file_path
