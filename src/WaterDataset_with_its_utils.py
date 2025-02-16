# -*- coding: utf-8 -*-
"""Untitled14.ipynb

Automatically generated by Colaboratory.

"""

import os
import cv2
import numpy as np

import utils


# function which do both the steps 1 and 2 in inspect_and_make_the_data_ready.ipynb

def remove_noise_and_get_masks(mask_1_ch):
  
  # do opening and closing
  kernel = np.ones((2,2),np.uint8)
  opening = cv2.morphologyEx(mask_1_ch, cv2.MORPH_OPEN, kernel)
  closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

  combined_mask = closing.copy()
  

  # get different masks using connected components
  max_positive_area = 0
  index_with_max_area = -1
  index = 0

  masks = []

  ret, labels = cv2.connectedComponents(combined_mask)

  for label in np.unique(labels):

    mask = np.zeros((448, 448), dtype='uint8')
    mask[labels == label] = 1

    positive_area = mask.sum()
    #print(max_positive_area)

    if positive_area>max_positive_area:
      max_positive_area = positive_area
      index_with_max_area = index

    # <200 will be ignored to not get the noisy components 
    if positive_area>=200:
      masks.append(mask)

    else:
      continue

    index += 1

  # removed the mask for backgroung which I have assumed will be the biggest (from all regions of water) in all images 
  masks.pop(index_with_max_area)

  return combined_mask, masks


def get_thresholded_masks(mask_image):

  # Thresholding the mask_image by taking valuing of just one channel, as I have have checked all channels have same values
  mask_1_ch = mask_image[:,:,0].copy()
  temp_mask_1_ch = mask_1_ch.copy()
  mask_1_ch[temp_mask_1_ch >= 127] = 1
  mask_1_ch[temp_mask_1_ch < 127] = 0

  return mask_1_ch


class WaterDataset(utils.Dataset):

  def load_dataset(self, dataset_dir):

    self.add_class("water_dataset", 1, "water")

    images_dir = os.path.join(dataset_dir, 'images')
    masks_dir = os.path.join(dataset_dir, 'masks')

    for filename in os.listdir(images_dir):

      if 'nonwater' in filename:
        continue

      mask_image = cv2.imread(os.path.join(masks_dir, filename))
      mask_1_ch = get_thresholded_masks(mask_image)
      _, different_masks = remove_noise_and_get_masks(mask_1_ch)

      if len(different_masks)==0:
        continue

      image_id = filename[:-4]

      image_path = os.path.join(images_dir, filename)
      mask_path = os.path.join(masks_dir, filename)


      self.add_image('water_dataset', image_id = image_id, path = image_path, width= 448, height= 448, annotation= mask_path)


  def load_mask(self, image_id):

    mask_path = self.image_info[image_id]['annotation']
    mask_image = cv2.imread(mask_path)

    mask_1_ch = get_thresholded_masks(mask_image)

    _, different_masks = remove_noise_and_get_masks(mask_1_ch)

    masks = np.array(different_masks)
    masks = np.moveaxis(masks, 0, -1)
    

    class_ids = []
    
    for i in different_masks: 
      class_ids.append(self.class_names.index('water'))

    return masks, np.asarray(class_ids, dtype='int32')

  def image_reference(self, image_id):
      info = self.image_info[image_id]
      return info['path']
