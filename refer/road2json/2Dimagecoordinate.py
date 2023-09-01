sample_annotation = {
    "imgWidth": 2048,
    "imgHeight": 1024,
    "sensor": {
        "sensor_T_ISO_8855": [
            [
                0.9990881051503779,
                -0.01948468779721943,
                -0.03799085532693703,
                -1.6501524664770573
            ],
            [
                0.019498764210995674,
                0.9998098810245096,
                0.0,
                -0.1331288872611436
            ],
            [
                0.03798363254444427,
                -0.0007407747301939942,
                0.9992780868764849,
                -1.2836173638418473
            ]
        ],
        "fx": 2262.52,
        "fy": 2265.3017905988554,
        "u0": 1096.98,
        "v0": 513.137,
        "baseline": 0.209313
    },
    "objects": [
        {
            "2d": {
                "modal": [
                    375,
                    424,
                    207,
                    136
                ],
                "amodal": [
                    357,
                    418,
                    232,
                    145
                ]
            },
            "3d": {
                "center": [
                    28.15,
                    6.74,
                    0.54
                ],
                "dimensions": [
                    4.0,
                    1.65,
                    1.45
                ],
                "rotation": [
                    0.009871597131612439,
                    0.00524838342290069,
                    -0.024995833604157247,
                    -0.9996250368733021
                ],
                "type": "Small Size Car",
                "format": "CRS_ISO8855"
            },
            "occlusion": 0.0,
            "truncation": 0.0,
            "instanceId": 26013,
            "label": "car",
            "score": 1.0
        },
    ]
}

import numpy as np
from cityscapesscripts.helpers.annotation import CsBbox3d
from cityscapesscripts.helpers.box3dImageTransform import (
    Camera, 
    Box3dImageTransform,
    CRS_V,
    CRS_C,
    CRS_S
)

camera = Camera(fx=sample_annotation["sensor"]["fx"],
                fy=sample_annotation["sensor"]["fy"],
                u0=sample_annotation["sensor"]["u0"],
                v0=sample_annotation["sensor"]["v0"],
                sensor_T_ISO_8855=sample_annotation["sensor"]["sensor_T_ISO_8855"])

# Create the Box3dImageTransform object
box3d_annotation = Box3dImageTransform(camera=camera)

# Create a CsBox3d object for the 3D annotation
obj = CsBbox3d()
obj.fromJsonText(sample_annotation["objects"][0])

# Initialize the 3D box with an annotation in coordinate system V. 
# You can alternatively pass CRS_S or CRS_C if you want to initalize the box in a different coordinate system.
# Please note that the object's size is always given as [L, W, H] independently of the used coodrinate system.
box3d_annotation.initialize_box_from_annotation(obj, coordinate_system=CRS_V)
size_V, center_V, rotation_V = box3d_annotation.get_parameters(coordinate_system=CRS_V)

# Get the vertices of the 3D box in the requested coordinate frame
box_vertices_V = box3d_annotation.get_vertices(coordinate_system=CRS_V)
box_vertices_C = box3d_annotation.get_vertices(coordinate_system=CRS_C)
box_vertices_S = box3d_annotation.get_vertices(coordinate_system=CRS_S)

# Print the vertices of the box.
# loc is encoded with a 3-char code
#   0: B/F: Back or Front
#   1: L/R: Left or Right
#   2: B/T: Bottom or Top
# BLT -> Back left top of the object

# Print in V coordinate system
print("Vertices in V:")
print("     {:>8} {:>8} {:>8}".format("x[m]", "y[m]", "z[m]"))
for loc, coord in box_vertices_V.items():
    print("{}: {:8.2f} {:8.2f} {:8.2f}".format(loc, coord[0], coord[1], coord[2]))
    
# Print in C coordinate system
print("\nVertices in C:")
print("     {:>8} {:>8} {:>8}".format("x[m]", "y[m]", "z[m]"))
for loc, coord in box_vertices_C.items():
    print("{}: {:8.2f} {:8.2f} {:8.2f}".format(loc, coord[0], coord[1], coord[2]))
    
# Print in S coordinate system
print("\nVertices in S:")
print("     {:>8} {:>8} {:>8}".format("x[m]", "y[m]", "z[m]"))
for loc, coord in box_vertices_S.items():
    print("{}: {:8.2f} {:8.2f} {:8.2f}".format(loc, coord[0], coord[1], coord[2]))

# Similar to the box vertices, you can retrieve box parameters center, size and rotation in any coordinate system
size_V, center_V, rotation_V = box3d_annotation.get_parameters(coordinate_system=CRS_V)
# size_C, center_C, rotation_C = box3d_annotation.get_parameters(coordinate_system=CRS_C)
# size_S, center_S, rotation_S = box3d_annotation.get_parameters(coordinate_system=CRS_S)

print("Size:    ", size_V)
print("Center:  ", center_V)
print("Rotation:", rotation_V)

# Get the vertices of the 3D box in the image coordinates
box_vertices_I = box3d_annotation.get_vertices_2d()

# Print the vertices of the box.
# loc is encoded with a 3-char code
#   0: B/F: Back or Front
#   1: L/R: Left or Right
#   2: B/T: Bottom or Top
# BLT -> Back left top of the object

print("\n     {:>8} {:>8}".format("u[px]", "v[px]"))
for loc, coord in box_vertices_I.items():
    print("{}: {:8.2f} {:8.2f}".format(loc, coord[0], coord[1]))
    
# generate amodal 2D box from these values
xmin = int(min([p[0] for p in box_vertices_I.values()]))
ymin = int(min([p[1] for p in box_vertices_I.values()]))
xmax = int(max([p[0] for p in box_vertices_I.values()]))
ymax = int(max([p[1] for p in box_vertices_I.values()]))

bbox_amodal = [xmin, ymin, xmax, ymax]

print("Amodal 2D bounding box")
print(bbox_amodal)
# load from CsBbox3d object, these 2 bounding boxes should be the same
print(obj.bbox_2d.bbox_amodal)

# assert bbox_amodal == obj.bbox_2d.bbox_amodal

# # Initialize box in V
# box3d_annotation.initialize_box(size=sample_annotation["objects"][0]["3d"]["dimensions"],
#                               quaternion=sample_annotation["objects"][0]["3d"]["rotation"],
#                               center=sample_annotation["objects"][0]["3d"]["center"],
#                               coordinate_system=CRS_V)
# size_VV, center_VV, rotation_VV = box3d_annotation.get_parameters(coordinate_system=CRS_V)

# # Retrieve parameters in C, initialize in C and retrieve in V
# size_C, center_C, rotation_C = box3d_annotation.get_parameters(coordinate_system=CRS_C)
# box3d_annotation.initialize_box(size=size_C,
#                               quaternion=rotation_C,
#                               center=center_C,
#                               coordinate_system=CRS_C)
# size_VC, center_VC, rotation_VC = box3d_annotation.get_parameters(coordinate_system=CRS_V)

# # Retrieve parameters in S, initialize in S and retrieve in V
# size_S, center_S, rotation_S = box3d_annotation.get_parameters(coordinate_system=CRS_S)
# box3d_annotation.initialize_box(size=size_S,
#                               quaternion=rotation_S,
#                               center=center_S,
#                               coordinate_system=CRS_S)
# size_VS, center_VS, rotation_VS = box3d_annotation.get_parameters(coordinate_system=CRS_V)

# assert np.isclose(size_VV, size_VC).all() and np.isclose(size_VV, size_VS).all()
# assert np.isclose(center_VV, center_VC).all() and np.isclose(center_VV, center_VS).all()
# assert (rotation_VV == rotation_VC) and (rotation_VV == rotation_VS)