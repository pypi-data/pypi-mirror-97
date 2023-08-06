"""Utilities for opentea additionnal processing in tabs"""
import os
import sys
import yaml

from tiny_3d_engine import load_file_as_scene, Scene3D


__all__ = ["process_tab", "update_3d_callback", "rec_fusion"]


def process_tab(func_to_call):
    """Execute the function of an external process.external.

    func_to_call : see above for a typical function
    to be called by openTea GUIS

    A typical callback scriptwill look like this:

    ::
        def template_aditional_process(nob_in):
            nob_out = nob_in.copy()
            # Your actions here to change the content of nob_out
            # nob_out["foobar"] = 2 * nob_in["foobar"]
            # (...)
            return nob_out


        if __name__ == "__main__":
            process_tab(template_aditional_process)


    """
    with open(sys.argv[1], "r") as fin:
        data = yaml.load(fin, Loader=yaml.SafeLoader)
    data_out = func_to_call(data)
    with open(".dataset_to_gui.yml", "w") as fout:
        yaml.dump(data_out, fout, default_flow_style=False)


def update_3d_callback(func_to_call):
    """Execute the function of an external process.external.

    func_to_call : see above for a typical function
    to be called by openTea GUIS

    A typical call back will look like this:

    ::

        def update_3d_scene1(nob_in, scene):
            SIZE = 50
            LENGTH= 200.
            points = list()
            conn = list()
            dx = LENGTH/SIZE
            edges = 0
            for i in range(SIZE):
                for j in range(SIZE):
                    index = len(points)
                    points.append([i*dx, j*dx, 0])
                    points.append([(i+1)*dx, j*dx, 0])
                    points.append([i*dx, (j+1)*dx, 0])
                    points.append([(i+1)*dx, (j+1)*dx, 0])
                    #conn.append([index, index+1, index+2])
                    #conn.append([index+3, index+1, index+2])
                    conn.append([index, index+1])
                    conn.append([index+3, index+1])
                    edges += 1
            scene.add_or_update_part("square1", points, conn, color="#0000ff")
            return scene

        if __name__ == "__main__":
            update_3d_callback(update_3d_scene1)

    """
    with open(sys.argv[1], "r") as fin:
        data = yaml.load(fin, Loader=yaml.SafeLoader)
    fname = sys.argv[2]
    if fname == "no_scene":
        print("   Update3d: no initial scene.")
        scene_in = Scene3D()
    elif not os.path.exists(fname):
        print(f"   Update3d: empty or non existing file {fname}")
        scene_in = Scene3D()
    else:
        print(f"  Update3d: loading {fname}")
        scene_in = load_file_as_scene(fname)

    scene_out = func_to_call(data, scene_in)
    try:
        scene_out.dump(".scene_to_gui")
    except RuntimeError:
        print("Scene is void, nothing to dump.")


def rec_fusion(dat_, add_dat_):
    """Recutsive function for the fusion of schemas

    For Dicts and usual leafs (strings, numbers)
    - if the data is only in dat_ > Kept
    - if the data is both in dat_ and add_dat_> Replaced
    - if the data is only in add_dat_ > Added

    For a list, add_dat_ items are concatenated after dat_, no fusion.
    """
    if isinstance(dat_, dict):
        # Replace identical keys
        for key in dat_:
            if key in add_dat_:
                dat_[key] = rec_fusion(dat_[key], add_dat_[key])
        # add additionnal keys
        for key in add_dat_:
            if key not in dat_:
                dat_[key] = add_dat_[key]

    # extend lists
    elif isinstance(dat_, list):
        dat_.extend(add_dat_)
    else:
        if dat_ != add_dat_:
            dat_ = add_dat_
    return dat_
