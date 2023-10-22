from transformers import OneFormerProcessor, OneFormerForUniversalSegmentation
from PIL import Image
import warnings
import torch, glob, random, os
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

fig, ax = plt.subplots(2, 2)

# load OneFormer fine-tuned on ADE20k for universal segmentation
processor = OneFormerProcessor.from_pretrained("shi-labs/oneformer_ade20k_swin_tiny")
model = OneFormerForUniversalSegmentation.from_pretrained("shi-labs/oneformer_ade20k_swin_tiny")

global_png_exist = glob.glob1(r".\images", "*.png")
image = Image.open(os.path.join(r".\images", random.choice(global_png_exist)))

# Semantic Segmentation
inputs1 = processor(image, ["semantic"], return_tensors="pt")

with torch.no_grad():
    outputs1 = model(**inputs1)
# model predicts class_queries_logits of shape `(batch_size, num_queries)`
# and masks_queries_logits of shape `(batch_size, num_queries, height, width)`
# class_queries_logits1 = outputs1.class_queries_logits
# masks_queries_logits1 = outputs1.masks_queries_logits

# you can pass them to processor for semantic postprocessing
predicted_semantic_map = processor.post_process_semantic_segmentation(
    outputs1, target_sizes=[image.size[::-1]]
)[0]


inputs2 = processor(image, ["panoptic"], return_tensors="pt")

with torch.no_grad():
    outputs2 = model(**inputs2)
# model predicts class_queries_logits of shape `(batch_size, num_queries)`
# and masks_queries_logits of shape `(batch_size, num_queries, height, width)`
# class_queries_logits2 = outputs2.class_queries_logits
# masks_queries_logits2 = outputs2.masks_queries_logits

# you can pass them to processor for semantic postprocessing
Predicted_panoptic_map = processor.post_process_panoptic_segmentation(
    outputs2, target_sizes=[image.size[::-1]]
)[0]["segmentation"]


ax[0][0].imshow(image)
ax[0][0].axis("off")
ax[0][0].set_title("original image")

ax[0][1].imshow(predicted_semantic_map)
ax[0][1].axis("off")
ax[0][1].set_title("predicted_semantic image")

ax[1][0].imshow(Predicted_panoptic_map, cmap="jet")
ax[1][0].axis("off")
ax[1][0].set_title("Predicted_panoptic image")


ax[1][1].imshow(image)
ax[1][1].imshow(Predicted_panoptic_map, alpha=0.5, cmap="jet")
ax[1][1].axis("off")
ax[1][1].set_title("Predicted_panoptic image")
plt.show()
