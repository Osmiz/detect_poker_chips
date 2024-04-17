import os
import cv2
import supervision as sv
from ultralytics import YOLO
import numpy as np
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from collections import Counter
from kivy.uix.relativelayout import RelativeLayout
class ChipDetector(App):

    def build(self):
        # Create the main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create a label for instructions
        instructions_1 = Label(
            text='1. Please spread your poker chips on the table \n 2. Point the camera at the poker chips and \n 3. Press "Detect Chips"')
        instructions_1.size_hint_y = None  # Fix the height
        instructions_1.height = '48dp'  # Set a fixed height
        layout.add_widget(instructions_1)

        # Create a layout to hold the camera and count_chips label
        camera_layout = RelativeLayout()

        # Create the camera widget
        self.camera = Camera(play=True)
        camera_layout.add_widget(self.camera)

        # Position the camera to fill the entire layout
        self.camera.pos_hint = {'x': 0, 'y': 0}
        self.camera.size_hint = (1, 1)

        # Create the count_chips label
        self.count_chips = Label(text='', size_hint=(None, None), size=('300dp', '80dp'))
        camera_layout.add_widget(self.count_chips)

        # Position the count_chips label on the left side of the camera screen
        self.count_chips.pos_hint = {'x': 0.7, 'center_y': 0.5}  # Adjust the 'x' value as needed

        # Add the camera layout to the main layout
        layout.add_widget(camera_layout)

        # Create a button to detect chips
        detect_button = Button(text='Detect Chips')
        detect_button.size_hint_y = None  # Fix the height
        detect_button.height = '48dp'  # Set a fixed height
        detect_button.bind(on_press=self.detect_chips)
        layout.add_widget(detect_button)

        self.total_value_label = Label(text='')
        self.total_value_label.size_hint_y = None  # Fix the height
        self.total_value_label.height = '48dp'  # Set a fixed height
        layout.add_widget(self.total_value_label)

        return layout

    def detect_chips(self, instance):
        Clock.schedule_once(self.detect_chips_delayed, 0.1)

    def detect_chips_delayed(self, dt):
        # Capture the current frame from the camera
        frame_texture = self.camera.texture
        if frame_texture:
            frame_data = frame_texture.pixels
            frame_format = frame_texture.colorfmt
            frame_size = frame_texture.size

            # Convert frame data to a numpy array
            frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = frame.reshape(frame_size[1], frame_size[0], -1)

            # Convert the frame to BGR format (OpenCV uses BGR by default)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

            # Call the detect_chips function
            self.detect_chips_opencv(frame)

    def detect_chips_opencv(self, frame):
        # Load YOLO model
        model = YOLO(r'..\app\train5\weights\best.pt')

        cv2.imwrite('../app/frame.jpg', frame)

        image_path = os.path.abspath('../app/frame.jpg')

        # Load image
        image_path = image_path

        image = cv2.imread(image_path)

        # Perform Object Detection
        results = model(image)[0]

        # Convert detections
        detections = sv.Detections.from_ultralytics(results)

        # Annotate Bounding Boxes
        bounding_box_annotator = sv.BoundingBoxAnnotator()
        annotated_image = bounding_box_annotator.annotate(scene=image, detections=detections)

        # Annotate Labels
        label_annotator = sv.LabelAnnotator()
        labels = [model.names[class_id] for class_id in detections.class_id]
        annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections, labels=labels)

        chips_list = []

        total_value = 0
        for label in labels:
            chips_list.append(label)
            if label == '1':
                total_value += int(label)
            else:
                total_value += (int(label)/100)

        counts = Counter(chips_list)

        counts_text = 'You have:\n'
        for element, count in counts.items():
            pluralized_element = f"{element}s" if count > 1 else element
            counts_text += f"{count}: {pluralized_element}\n"
        self.count_chips.text =counts_text

        # Update total chip value label
        self.total_value_label.text = f'Total value of chips: {total_value}₪'





if __name__ == '__main__':
    ChipDetector().run()
