import tkinter as tk
import win32gui
import win32con

def set_window_shape(hwnd, width, height):
    region = win32gui.CreateRoundRectRgn(0, 0, width, height, width, height)
    win32gui.SetWindowRgn(hwnd, region, True)

def create_circular_widget(root, size, color):
    widget = tk.Canvas(root, width=size, height=size, highlightthickness=0)
    widget.create_oval(0, 0, size, size, fill=color)
    widget.pack()
    return widget

# Create the main window
root = tk.Tk()

# Set the window size and position
window_size = 300
root.geometry(f"{window_size}x{window_size}+100+100")

# Remove window decorations (title bar, minimize, close buttons)
root.overrideredirect(True)

# Create a circular widget
window_color = "blue"
circular_widget = create_circular_widget(root, window_size, window_color)

# Get the window handle
hwnd = win32gui.GetForegroundWindow()

# Set the window shape to a circle
set_window_shape(hwnd, window_size, window_size)

# Set the window attributes to allow transparency
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)

# Run the GUI event loop
root.mainloop()
