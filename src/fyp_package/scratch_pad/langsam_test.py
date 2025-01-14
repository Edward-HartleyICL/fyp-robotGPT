from PIL import Image
from lang_sam import LangSAM
import torch
import numpy as np

model = LangSAM(sam_type="vit_b")
image_pil = Image.open("./assets/pybullet_tabletop_2.png").convert("RGB")
text_prompt = "green bowl"
masks, boxes, phrases, logits = model.predict(image_pil, text_prompt)
print(masks, boxes, phrases, logits)
print(masks[0].shape)

image_tensor = torch.from_numpy(np.array(image_pil)).permute(2, 0, 1).float()  # Convert to tensor and permute to CxHxW

for i, mask in enumerate(masks):
    # Prepare the green filter overlay
    # Create a tensor of zeros with the same H and W as the mask and 3 channels for RGB
    green_filter = torch.zeros_like(image_tensor)
    # Set the green channel to 255 wherever the mask is True
    green_filter[1, mask] = 255  # Green channel is at index 1
    # Overlay the green filter on the original image
    # Only apply the green filter where the mask is True, keeping the original image intact elsewhere
    output_image_tensor = torch.where(mask.unsqueeze(0).repeat(3, 1, 1), green_filter, image_tensor)

    # Convert back to PIL Image for saving or displaying
    overlayed_image = Image.fromarray(output_image_tensor.byte().permute(1, 2, 0).numpy())

    # Save or display the overlayed image
    overlayed_image.save(f'./assets/pybullet_tabletop_2_mask_{i}.png')
    # Save the mask
    mask_image = Image.fromarray((mask * 255).byte().numpy())
    mask_image.save(f'./assets/pybullet_tabletop_2_mask_{i}_mask.png')
    np.save(f'./assets/pybullet_tabletop_2_mask_{i}_mask.npy', mask.numpy())