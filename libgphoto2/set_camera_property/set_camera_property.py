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
    parser.add_argument('json_input', type=str, nargs=1,
                    help='JSON formatted input of camera port, model and property to change')
    args = parser.parse_args()

def update_property():
    print(args.json_input[0])
    json_val = json.loads(args.json_input[0])
    name = json_val["name"]
    addr = json_val["port"]
    camera = gp.Camera()
    port_info_list = gp.PortInfoList()
    port_info_list.load()
    idx = port_info_list.lookup_path(addr)
    camera.set_port_info(port_info_list[idx])
    camera.init()
    config = camera.get_config()
    for item in json_val["properties"]:
        try:
            OK, prop = gp.gp_widget_get_child_by_name(config, item["name"])
            if OK >= gp.GP_OK:
                prop.set_value(item["value"])
        except:
            pass
            # passed = False
    camera.set_config(config)
    return True

if __name__ == "__main__":
    parse_args()
    status = update_property()
    if not status:
        sys.exit(2)
