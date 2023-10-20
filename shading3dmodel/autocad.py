from OCC.Extend.DataExchange import read_step_file
from OCC.Display.SimpleGui import init_display
import os
import tempfile

def capture_views(display, temp_dir):
    views = {
        'top': (1, 1, 1),
        'bottom': (-1, -1, -1),
        'left': (0, -1, 0),
        'right': (0, 1, 0),
        'front': (1, 0, 0),
        'rear': (-1, 0, 0),
    }
    
    for view_name, (x, y, z) in views.items():
        display.View.SetProj(x, y, z)
        display.View.Dump(os.getcwd()+f"/static/screenshot/{view_name}.png")


def generate_images(file_path):
    shape = read_step_file(file_path)
    display, start_display, add_menu, add_function_to_menu = init_display()
    display.DisplayShape(shape, update=True)
    dir_path = tempfile.mkdtemp()
    all_images=capture_views(display,dir_path)
    return all_images