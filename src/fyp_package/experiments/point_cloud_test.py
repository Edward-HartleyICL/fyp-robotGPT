from PIL import Image
from fyp_package import langsam_model_utils as langsam_utils, config
import numpy as np
import torch
import matplotlib.pyplot as plt


source_image_path = "./assets/pybullet_tabletop_2.png"
source_depth_path = "./assets/pybullet_tabletop_2.npy"

successful_mask_path = "./assets/pybullet_tabletop_2_mask_0_mask.png"
unsuccessful_mask_path = "./assets/pybullet_tabletop_2_mask_2_mask.png"

def detect_objects_in_image(image_path, depth_path, camera_position, camera_orientation_q, mask_path):
    image = Image.open(image_path).convert("RGB")
    depth_array = np.load(depth_path)
    # plot top left of the depth array
    # plt.imshow(depth_array[200:400, 0:200])
    # plt.show()

    mask_image = Image.open(mask_path).convert("L")
    model_prediction_tensor = torch.from_numpy(np.array(mask_image)).float()
    model_predictions = [model_prediction_tensor]

    masks = langsam_utils.get_segmentation_mask(model_predictions, config.segmentation_threshold)
    # plt.imshow(masks[0])
    # plt.show()

    bounding_cubes_world_coordinates, bounding_cubes_orientations = langsam_utils.get_bounding_cube_from_point_cloud(image, masks, depth_array, camera_position, camera_orientation_q)

    results = [{}]

    for i, bounding_cube_world_coordinates in enumerate(bounding_cubes_world_coordinates):

# i don't get why this is necessary
#        bounding_cube_world_coordinates[4][2] -= config.depth_offset

        object_width = np.around(np.linalg.norm(bounding_cube_world_coordinates[1] - bounding_cube_world_coordinates[0]), 3)
        object_length = np.around(np.linalg.norm(bounding_cube_world_coordinates[2] - bounding_cube_world_coordinates[1]), 3)
        object_height = np.around(np.linalg.norm(bounding_cube_world_coordinates[5] - bounding_cube_world_coordinates[0]), 3)

        print("Position of " + "red bowl" + ":", list(np.around(bounding_cube_world_coordinates[4], 3)))
        results[i]['position'] = list(np.around(bounding_cube_world_coordinates[4], 3))

        print("Dimensions:")
        print("Width:", object_width)
        print("Length:", object_length)
        print("Height:", object_height)
        results[i]['dimensions'] = {'width': object_width, 'length': object_length, 'height': object_height}

        if object_width < object_length:
            print("Orientation along shorter side (width):", np.around(bounding_cubes_orientations[i][0], 3))
            print("Orientation along longer side (length):", np.around(bounding_cubes_orientations[i][1], 3), "\n")
            results[i]['orientation'] = {'width': np.around(bounding_cubes_orientations[i][0], 3), 'length': np.around(bounding_cubes_orientations[i][1], 3)}
        else:
            print("Orientation along shorter side (length):", np.around(bounding_cubes_orientations[i][1], 3))
            print("Orientation along longer side (width):", np.around(bounding_cubes_orientations[i][0], 3), "\n")
            results[i]['orientation'] = {'length': np.around(bounding_cubes_orientations[i][1], 3), 'width': np.around(bounding_cubes_orientations[i][0], 3)}

detect_objects_in_image(source_image_path, source_depth_path, config.camera_position, config.camera_orientation_q, unsuccessful_mask_path)
detect_objects_in_image(source_image_path, source_depth_path, config.camera_position, config.camera_orientation_q, successful_mask_path)


# bowl should have dimensions [0.12325251 0.125995   0.04312475]