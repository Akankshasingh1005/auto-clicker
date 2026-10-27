# AutoClicker

A simple Python auto-clicker which automates pressing the **Enter key** using image detection or a fixed time interval.

## Features
- Load and preview a target image.
- Detect matching images on the screen and press Enter automatically.
- Press Enter at custom intervals in seconds or minutes.
- Start and stop controls for both modes.

## Requirements
- Python 3.x
- PyAutoGUI
- Pillow

## Installation

```bash
pip install pyautogui pillow
```

## Run the Application

```bash
python main.py
```

## How to Use
1. Run the application.
2. Load an image of the button or icon you want to detect.
3. Start the pattern scanner to press Enter when the image is found.
4. Alternatively, set a time interval and start the interval pulse.
5. Use the stop buttons to stop either mode.

**Note:** Keep the target image clear and similar to what appears on your screen for better detection. Move the mouse to the top-left corner of the screen to trigger PyAutoGUI's emergency failsafe.
