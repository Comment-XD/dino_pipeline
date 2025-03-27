import pydicom
import nibabel as nib
import numpy as np

import matplotlib.pyplot as plt
import glob
import os


import argparse

def parser():
    parser = argparse.ArgumentParser()
    
    
    parser.add_argument("-dataset", "-d", 
                        type=str,
                        choices=["lidc_idri", "luna16"],
                        default=None,
                        help="What dataset to use")
        
    parser.add_argument("-root_path", "-r", 
                        type=str,
                        default=None,
                        help="Root path to dataset")
    
    parser.add_argument("-json_save_path", "-j", 
                        type=str,
                        default="/home/comet/research/dino_research/dino_pipeline/jsons",
                        help="Json save path for dataset path")

    parser.add_argument("-nii_save_path", "-n", 
                        type=str,
                        default="/home/comet/research/dino_research/dino_pipeline/nii",
                        help="Nii save path for dataset path")
    
    parser.add_argument("--affine", "-a",
                        type=str,
                        default="identity",
                        help="Nii save path for dataset path")
    
    return parser.parse_args()

def save_nii_to_json(args):
    pass


def dicom_to_nii(args):
    # TODO: Determining the Format for the images for the 
    
    
    if args.dataset == "lidc_idri":
        dicom_paths = glob.glob("*/*/*/*.dcm", root_dir=args.root_path, recursive=True)
        
        for path in dicom_paths:
            
            img_path = os.path.join(args.root_path, path)
            dicom_data = pydicom.dcmread(img_path)
            
            try:
                img_data = dicom_data.pixel_array
                
                affine = np.eye(4)
                
                nifti_image = nib.Nifti1Image(img_data, affine)

                # Save the NIfTI image to file
                nii_file = '.nii'
                nii_save_path = os.path.join(args.nii_save_path, nii_file)
                nib.save(nifti_image, nii_save_path)
                
            except:
                 print("Dicom data does not contain image metadata 'pixel array'")
    
        
if __name__ == "__main__":
    
    lidc_root_path = "/mnt/d/Datasets/brats-research-datasets/LIDC-IDRI/manifest-1600709154662/LIDC-IDRI/"
    nii_save_path = "/home/comet/research/dino_research/dino_pipeline/nii"
    
    dcm_files = glob.glob("*/*/*/*.dcm", root_dir=lidc_root_path, recursive=True)
    
    dicom_path = os.path.join(lidc_root_path, dcm_files[0])
    dicom_data = pydicom.dcmread(dicom_path)
    
    try:
        img_data = dicom_data.pixel_array
        affine = np.eye(4)
                
        nifti_image = nib.Nifti1Image(img_data, affine)

                # Save the NIfTI image to file
        nii_file = 'output_image.nii'
        nii_save_path = os.path.join(nii_save_path, nii_file)
        nib.save(nifti_image, nii_save_path)
        
    
    except:
        print("Dicom image does not have image pixels")
        
    plt.imshow(dicom_data.pixel_array, cmap="gray")
    plt.title("DICOM Image")
    plt.axis("off")
    plt.show()