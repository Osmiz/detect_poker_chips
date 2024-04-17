
---

# Poker Chip Counter App

## Overview
an app designed to help you count the value of poker chips used in your poker nights with friends. The app utilizes a custom-trained object detection model based on YOLOv8 architecture to identify different denominations of chips. It then calculates the total value based on predefined denominations.

## Usage
1. **Setup**: Ensure you have Python and the required dependencies installed (listed in `requirements.txt`).
2. **Launch**: Run the `main.py` file to start the application in the app folder.
3. **Capture**: Use the app to take a picture of the poker chips placed on a flat surface with good lighting.
4. **Calculation**: The app will process the image, detect the chips, and display the total value based on the denominations recognized.

## Denominations
- **25**: Represents a quarter.
- **50**: Represents half a dollar.
- **1**: Represents one dollar.
- **500**: Represents two dollars.
- **5000**: Represents ten dollars.

## Customization
You can easily customize the app to recognize additional denominations or modify the existing ones by training the model with new images and updating the denomination mapping in the code.

## Technologies Used
- Python
- Kivy
- YOLOv8 object detection model
- Supervision
- OpenCV

## Credits
This project was inspired by our regular poker nights and developed by Oz Mizrahi.

---

Feel free to modify and expand upon this template to better suit your project and its details!
