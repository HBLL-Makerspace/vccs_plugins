#!/usr/bin/env python

# python-gphoto2 - Python interface to libgphoto2
# http://github.com/jim-easterbrook/python-gphoto2
# Copyright (C) 2019  Göktuğ Başaran
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License

# *******************************************************
# gp.camera_wait_for_event() function waits for
# a capture trigger to arrive. When it does, it downloads
# the image directly from the camera, without using SD
# card
#
# gp_camera_trigger_capture() or Trigger Button on the
# camera can be used to start capturing.
#
# gp_capture_image_and_download() method takes about 2 seconds
# to process since it saves the image to SD CARD
# first then downloads it, which takes a lot of time.
#
# "object oriented" version of wait-for-event.py
# *******************************************************

from __future__ import print_function

import os
import sys
import argparse

import gphoto2 as gp

args = None

def parse_args():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=str, nargs=1,
                    help='Camera port to tether to')
    parser.add_argument('--file', type=str, nargs=1,
                    help='filename including path to save captured picture DO NOT PUT TYPE')
    parser.add_argument("--timeout", type=int, nargs=1, help="Timeout in milliseconds to wait for camera input", default=60000)
    args = parser.parse_args()


def tether(addr, filename):
    # Init camera
    camera = gp.Camera()
    port_info_list = gp.PortInfoList()
    port_info_list.load()
    idx = port_info_list.lookup_path(addr)
    camera.set_port_info(port_info_list[idx])
    camera.init()
    event_captured = False
    while not event_captured:
        event_type, event_data = camera.wait_for_event(args.timeout)
        if event_type == gp.GP_EVENT_FILE_ADDED:
            event_data_type = event_data.name.split(".")[1]
            cam_file = camera.file_get(
                event_data.folder, event_data.name, gp.GP_FILE_TYPE_NORMAL)
            target_path = filename + "." + event_data_type
            print("Image is being saved to {}".format(target_path))
            cam_file.save(target_path)
            camera.file_delete(event_data.folder, event_data.name)
            event_captured = True
            camera.exit()
            return


if __name__ == "__main__":
    parse_args()
    if args is None:
        print("Failed to parse args")
        exit(1)
    # print("Tethering to camera on port: " + args.port)
    print(args.port[0])
    print(args.file[0])
    tether(str(args.port[0]), args.file[0])
    print("Done tethering")
    # sys.exit(0)
