import sys, getopt
import argparse
import json
try:
    import gphoto2 as gp
except ModuleNotFoundError:
    print("There is no gphoto2 module installed")

args = None

def parse_args():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=str, nargs=1,
                    help='port that the camera is connected to')
    parser.add_argument('--file', type=str, nargs=1,
                    help='where to store the file')
    args = parser.parse_args()

def update_property():
    global args
    file = args.file[0]
    addr = args.port[0]
    print (addr)
    camera = gp.Camera()
    port_info_list = gp.PortInfoList()
    port_info_list.load()
    idx = port_info_list.lookup_path(addr)
    camera.set_port_info(port_info_list[idx])
    camera.init()
    print('Capturing image')
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    event_data_type = file_path.name.split(".")[1]
    target = file + "." + event_data_type
    print('Copying image to', target)
    camera_file = camera.file_get(
        file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
    camera_file.save(target)
    camera.file_delete(file_path.folder, file_path.name)
    camera.exit()
    return True

if __name__ == "__main__":
    parse_args()
    status = update_property()
    if not status:
        sys.exit(2)
