from PIL import Image

new_width = 625
new_height = 448

def resize_image(image_file, new_image_file):
    im = Image.open(image_file)
    width, height = im.size  # Get dimensions

    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2

    im = im.crop((left, top, right, bottom))
    im.save(new_image_file)

resize_image("../../doc/images/summary/event_detection_differences_de.png", "../../doc/images/summary/cropped_event_detection_differences_de.png")
resize_image("../../doc/images/summary/event_detection_differences_en.png", "../../doc/images/summary/cropped_event_detection_differences_en.png")
resize_image("../../doc/images/summary/hdbscan_kmeans_de.png", "../../doc/images/summary/cropped_hdbscan_kmeans_de.png")
resize_image("../../doc/images/summary/hdbscan_kmeans_en.png", "../../doc/images/summary/cropped_hdbscan_kmeans_en.png")
