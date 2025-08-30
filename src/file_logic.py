import os
import shutil


def copy_static_to_public(src_dir_path, dest_dir_path, first_time = True):
    if os.path.exists(src_dir_path) == False:
        raise Exception(f"Source directory does not exist:{src_dir_path}")
    if os.path.exists(dest_dir_path) == False:
        raise Exception(f"Destination directory does not exist:{dest_dir_path}")
    
    src_dir_contents = os.listdir(src_dir_path)
    if first_time == True:
        shutil.rmtree(dest_dir_path)
        os.mkdir(dest_dir_path)

    for fso in src_dir_contents:
        fso_path = f"{src_dir_path}/{fso}"
        
        if os.path.isfile(fso_path):
            shutil.copy(fso_path, dest_dir_path)
            
        #If File System Object is a Directory, recursive call with updated src and dest paths with the folder name
        elif os.path.isdir(fso_path):
            os.mkdir(f"{dest_dir_path}/{fso}")
            copy_static_to_public(f"{src_dir_path}/{fso}", f"{dest_dir_path}/{fso}")
        
        else:
            raise Exception(f"File System Object is neither a file or directory:{fso} in {src_dir_path}")


def extract_title(markdown):
    lines = markdown.split("\n")
    title_text = ""
    for line in lines:
        if line.startswith("# "):
            title_text = line.split("# ", 1)[1]
            break
    return title_text
    
