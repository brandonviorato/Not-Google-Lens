import cv2
import numpy as np

def calculate_font_scale(text, font, box_width, box_height):
    font_scale = 0.5
    font_thickness = 1
    ((text_width, text_height), _) = cv2.getTextSize(text, font, font_scale, font_thickness)

    while text_width > box_width or text_height > box_height:
        font_scale -= 0.05
        if font_scale <= 0.1:
            break  # prevent invisible text
        ((text_width, text_height), _) = cv2.getTextSize(text, font, font_scale, font_thickness)
    
    return font_scale, font_thickness, text_width, text_height

def overlay_text_boxes(image, ocr_results, output_path):
    # Colors
    box_color=(255, 255, 255)
    text_color=(0, 0, 0)
    border_color=(0, 0, 0)

    for box, text, confidence in ocr_results:
        # Convert box coordinates to np.int32 format
        points = np.array(box, dtype=np.int32)

        # Get top left and bottom right coordinates
        x_min = min([point[0] for point in points])
        y_min = min([point[1] for point in points])
        x_max = max([point[0] for point in points])
        y_max = max([point[1] for point in points])

        box_start = (x_min, y_max)
        box_end = (x_max, y_min)

        # Draw box
        cv2.rectangle(image, box_start, box_end, box_color, thickness=-1) # Filled
        # Draw border
        cv2.rectangle(image, box_start, box_end, border_color)

        box_width = x_max - x_min
        box_height = y_max - y_min

        font = cv2.FONT_HERSHEY_SIMPLEX

        font_scale, font_thickness, text_width, text_height = calculate_font_scale(text, font, box_width, box_height)

        # Calculate centered position in box
        x_text = x_min + (box_width - text_width) // 2
        y_text = y_min + (box_height + text_height) // 2

        # Draw the text inside the filled box
        cv2.putText(image, text, (x_text, y_text), font, font_scale, text_color, font_thickness, lineType=cv2.LINE_AA)

    # Save image
    cv2.imwrite(output_path, image)
    print(f"Image saved to: {output_path}")
