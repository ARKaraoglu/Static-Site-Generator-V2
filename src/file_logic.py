import os
import shutil
from markdown_logic import markdown_to_html

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


def generate_page(from_path, template, dest_path):
    print(f"Generating HTML Page from {from_path} to {dest_path} using this template {template}")
    markdown_file = open(from_path)
    markdown_contents = markdown_file.read()
    
    template_file = open(template)
    template_contents = template_file.read()

    title_content = extract_title(markdown_contents)
    html_node = markdown_to_html(markdown_contents)
    # print(html_node)
    # print(f"\n{html_node.to_html()}")
    html_string = html_node.to_html()
    
    t1 = template_contents.replace("{{ Title }}", title_content)
    final_template = t1.replace("{{ Content }}", html_string)

    directories = dest_path.rsplit("/", 1)[0]
    os.makedirs(directories, exist_ok = True)

    # if os.path.exists(dest_path) == False:
    #     file_path_tree = dest_path.split("/")
    #     print(file_path_tree)
    #     if len(file_path_tree) == 1:
    #         pass
    #     else:
    #         current_path = ""
    #         for x in range(0, len(file_path_tree)):
    #             current_path += f"/{file_path_tree[x]}"
    #             print(f"-----{file_path_tree[x]}")
    #             if x + 1 == len(file_path_tree):
    #                 break
    #             elif os.path.exists(current_path) == False:
    #                 os.mkdir(current_path)


    shutil.copy(from_path, dest_path)
    with open(dest_path, "w") as f:
        f.write(final_template)





