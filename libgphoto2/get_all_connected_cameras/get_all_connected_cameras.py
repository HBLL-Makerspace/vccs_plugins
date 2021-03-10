#!/usr/bin/env python3

import sys, getopt
import json
try:
    import gphoto2 as gp
except ModuleNotFoundError:
    print("There is no gphoto2 module installed")

verbose = False

def parse_args(argv):
   try:
      opts, args = getopt.getopt(argv,"v",["verbose"])
   except getopt.GetoptError:
      print("Failed to parse args")
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-v", "--verbose"):
        verbose = True
    

def _recursive_get_properties(widget):
    count = widget.count_children()
    properties = {}
    properties["name"] = widget.get_name()
    properties["label"] = widget.get_label()
    properties["type"] = widget.get_type()
    if properties["type"] == gp.GP_WIDGET_SECTION:
        pass
    elif properties["type"] == gp.GP_WIDGET_TEXT:
        properties["value"] = widget.get_value()
        properties["readOnly"] = widget.get_readonly()

    elif properties["type"] == gp.GP_WIDGET_RANGE:
        properties["readOnly"] = widget.get_readonly()
        lo, hi, inc = widget.get_range()
        properties["low"] = lo
        properties["high"] = hi
        properties["inc"] = inc
        properties["value"] = widget.get_value()

    elif properties["type"] == gp.GP_WIDGET_TOGGLE:
        properties["readOnly"] = widget.get_readonly()
        properties["value"] = widget.get_value() == 1

    elif properties["type"] == gp.GP_WIDGET_RADIO:
        properties["readOnly"] = widget.get_readonly()
        properties["value"] = widget.get_value()
        properties["choices"] = []
        for i in widget.get_choices():
            properties["choices"].append(i)

    elif properties["type"] == gp.GP_WIDGET_MENU:
        properties["readOnly"] = widget.get_readonly()
        properties["value"] = widget.get_value()
        properties["choices"] = []
        for i in widget.get_choices():
            properties["choices"].append(i)

    elif properties["type"] == gp.GP_WIDGET_DATE:
        properties["readOnly"] = widget.get_readonly()
        properties["value"] = widget.get_value()
    else:
        pass
    properties["children"] = []
    for child in widget.get_children():
        child_prop = _recursive_get_properties(child)
        if child_prop is not None:
            properties["children"].append(child_prop) 
    return properties;


def get_camera_properties(camera):
    try:
        name, addr = camera
        camera = gp.Camera()
        # search ports for camera port name
        port_info_list = gp.PortInfoList()
        port_info_list.load()
        idx = port_info_list.lookup_path(addr)
        camera.set_port_info(port_info_list[idx])
        camera.init()
        config = camera.get_config()
        return {"model": name, "port": addr, "config": _recursive_get_properties(config)}
    except:
        return None

def get_connected_cameras():
    cameralist = []
    if verbose:
        print("Getting cameras")
    cameras = gp.Camera.autodetect()
    for n, camera in enumerate(cameras):
        cam_and_prop = get_camera_properties(camera)
        if (cam_and_prop is not None):
            cameralist.append(cam_and_prop)
    return cameralist


if __name__ == "__main__":
   parse_args(sys.argv[1:])
   cameras_and_props = get_connected_cameras()
   if (cameras_and_props is None or cameras_and_props is []):
       print("There are no cameras connected")
       sys.exit(2)
   print(json.dumps(cameras_and_props))