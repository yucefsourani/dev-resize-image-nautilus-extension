#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  resize-and-convert-image-to-png-nautilus-extension.py
#  
#  Copyright 2020 yucef sourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 
import gi
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Nautilus, GObject, Gio, GdkPixbuf
import os

SUPPORTED_FORMATS = dict([(i.get_mime_types()[0],i.get_name()) for i in GdkPixbuf.Pixbuf.get_formats() if i]+[("image/jpg","jpg",)])
SIZE = ("8x8","16x16","22x22","24x24","32x32","38x36","42x42","64x64","72x72","96x96","128x128","256x256","512x512")


class ResizeImageExtension(GObject.GObject, Nautilus.MenuProvider):
    def get_file_items(self, files):
        if len(files) != 1:
            return
        file_ = files[0]

        mime_type = file_.get_mime_type()
        if not  mime_type in SUPPORTED_FORMATS.keys():
            return

        if file_.get_uri_scheme() != 'file':
            return
            
        menu = Nautilus.Menu.new()
        item = Nautilus.MenuItem(name='Nautilus::resize-and-convert-image-to-png',
                                 label='Resize Image',
                                 tip='Resize Image')
        item.set_submenu(menu)
        
        for size in SIZE:
            item2 = Nautilus.MenuItem(name='Nautilus::resize-and-convert-image-to-png_size_'+size,
                                 label=size,
                                 tip='Resize current image to '+size)
        
            menu.append_item(item2)
            item2.connect('activate', self.resize_and_save, file_,size,mime_type)

        item2 = Nautilus.MenuItem(name='Nautilus::resize-and-convert-image-to-png_size_all',
                            label="all",
                            tip='Resize current image to all size')
        
        menu.append_item(item2)
        item2.connect('activate', self.resize_and_save, file_,"all",mime_type)
        return item,

    # Current versions of Nautilus will throw a warning if get_background_items
    # isn't present
    def get_background_items(self, file_):
        return None

    def resize_and_save(self,menu,file_,size,mime_type,ignore_aspect_ration=False):
        image           = file_.get_location().get_path()
        filename        = os.path.splitext(file_.get_name())[0]
        parent_location = file_.get_parent_location().get_path()
        if size == "all":
            try :
                for s in SIZE:
                    folder_location = os.path.join(parent_location,filename+"_resize_n","hicolor" ,s,"apps")
                    os.makedirs(folder_location, exist_ok=True)
                    width,height= s.split("x")
                    saveas = os.path.join(folder_location,filename+".png")
                    im = GdkPixbuf.Pixbuf.new_from_file_at_scale(image,int(width),int(height),ignore_aspect_ration)
                    #if not im.savev(saveas,SUPPORTED_FORMATS[mime_type],[],[]):
                    if not im.savev(saveas,"png",[],[]):
                        return False
            except Exception as e:
                print("ERROR: {}.\nResize: {} Faild".format(e,image))
                return False
        else:
            try:
                folder_location = os.path.join(parent_location,filename+"_resize_n","hicolor" ,size,"apps")
                os.makedirs(folder_location, exist_ok=True)
                width,height= size.split("x")
                saveas = os.path.join(folder_location,filename+".png")
                im = GdkPixbuf.Pixbuf.new_from_file_at_scale(image,int(width),int(height),ignore_aspect_ration)
                #if not im.savev(saveas,SUPPORTED_FORMATS[mime_type],[],[]):
                if not im.savev(saveas,"png",[],[]):
                    return False
            except Exception as e:
                print("ERROR: {}.\nResize: {} Faild".format(e,image))
                return False
        return saveas
