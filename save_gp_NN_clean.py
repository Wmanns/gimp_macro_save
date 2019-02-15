#!/usr/bin/env python
# -*- coding: utf-8 -*-

# save_gp_NN vs 1.00 2015-04-19
#
# Copyright 2015 by wmanns
# based on the code of:
# Michael Schönitzer, Akkana Peck (GIMP plugin save-mod), which is
# Copyrighted 2013 by Michael Schönitzer, Akkana Peck
#
# You may use and distribute this plug-in under the terms of the GPL v2
# or, at your option, any later GPL version.
#
# C:\Program Files\GIMP 2.9\lib\gimp\2.0\plug-ins
# or
# ..\PortableApps\GIMPPortable\App\gimp\lib\gimp\2.0\plug-ins
#
# When saving an image file the script appends a token at the end the filename
# with the form '_gp_NN', with NN as a number {'01' .. '99'}.
# If this token already exists, NN is incremented.
# If there is no such token, '_gp_01' is appended.
#
# The script by itself does not check if it is overwriting an existing file.
#

from gimpfu import *
import gtk
import os
import collections
import re

def make_regex():
    re1='(_gp_)'   # Word 1
    re2='(\\d+$)'  # Integer 1 at end of string

    reg_exp = re.compile(re1+re2)
    return reg_exp

def make_new_fn_base(fn_base):
    default_tail = '_gp_01'
    reg_exp      = make_regex()
    if not (len(fn_base) > 6):
        new_fn_base = fn_base + default_tail
    else:
        m = reg_exp.search(fn_base)
        if m:
            word1 = m.group(1)
            int1  = m.group(2)
            str_tail = word1 + int1
            int1 = int1.lstrip('0')
            if not int1:
                int1 = '0'
            int2 = str(int(int1) + 1)
            new_fn_base = fn_base[:-len(str_tail)] + '_gp_' + int2.zfill(2)
        else:
            new_fn_base = fn_base + default_tail
    print fn_base ; print new_fn_base ; print '------'
    return new_fn_base

def python_save_gp_NN_clean(img, drawable) :
    fn = img.filename

    # If the file has no filename yet, ask user
    if not fn :
        chooser = gtk.FileChooserDialog(title=None,
                                        action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                        buttons=(gtk.STOCK_CANCEL,
                                                 gtk.RESPONSE_CANCEL,
                                                 gtk.STOCK_OPEN,
                                                 gtk.RESPONSE_OK))
        # Might want to set a current folder:
        save_dir = choose_likely_save_dir()
        if save_dir :
            chooser.set_current_folder(save_dir)

        response = chooser.run()
        if response != gtk.RESPONSE_OK:
            return

        fn = chooser.get_filename()
        img.filename = fn
        chooser.destroy()
    # Otherwise we appand a string to the filename
    else:
        # We don't want to save it in xcf format
        if os.path.splitext(fn)[1] == ".xcf" :
           fn = os.path.splitext(fn)[0] + ".png"

        fn_base  = os.path.splitext(fn)[0] # filename without extension
        fn_ext   = os.path.splitext(fn)[1] # filenameextension

    new_filename = make_new_fn_base(fn_base) + fn_ext

    # We want to save all layers,
    # so first duplicate the picture, then merge all layers
    exportimg = pdb.gimp_image_duplicate(img)
    layer = pdb.gimp_image_merge_visible_layers(exportimg, CLIP_TO_IMAGE)

    # save file and unset the 'unsaved'-flag
    pdb.gimp_file_save(exportimg, layer, new_filename, new_filename)
    pdb.gimp_image_clean_all(img)
    img.filename = new_filename

# Guess the save directory
def choose_likely_save_dir() :
    counts = collections.Counter()
    for img in gimp.image_list() :
        if img.filename :
            counts[os.path.dirname(img.filename)] += 1

    try :
        return counts.most_common(1)[0][0]
    except :
        return None

register(
        "python_fu_save_gpNN_clean",
        "Save current image with gp extension, then mark it clean.",
        "Save current image with gp extension, then mark it clean.",
        "wmanns",
        "wmanns",
        "2015",
        "Save with __gp__NN & clean",
        "*",
        [
            (PF_IMAGE, "image", "Input image", None),
            (PF_DRAWABLE, "drawable", "Input drawable", None),
        ],
        [],
        python_save_gp_NN_clean,
        menu = "<Image>/File/Save/"
)

main()
