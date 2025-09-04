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



    shutil.copy(from_path, dest_path)
    with open(dest_path, "w") as f:
        f.write(final_template)


def generate_pages_recursively(content_dir_path, template_path, dest_dir_path):
    

    content_dir_fsos = os.listdir(content_dir_path)
    print(content_dir_fsos)
    for fso in content_dir_fsos:
        if os.path.isfile(f"{content_dir_path}/{fso}"):
            fso_html = fso.replace(".md", ".html")
            shutil.copy(f"{content_dir_path}/{fso}", f"{dest_dir_path}/{fso_html}")
            
            template_file = open(template_path)
            template_content = template_file.read()
            md_file = open(f"{content_dir_path}/{fso}")
            md_content = md_file.read()

            md_title = extract_title(md_content)
            md_html_node = markdown_to_html(md_content)

            template_content = template_content.replace("{{ Title }}", md_title)
            template_content = template_content.replace("{{ Content }}", md_html_node.to_html())
            
            with open(f"{dest_dir_path}/{fso_html}", "w") as file:
                file.write(template_content)
            
        elif os.path.isdir(f"{content_dir_path}/{fso}"):
            os.mkdir(f"{dest_dir_path}/{fso}")
            generate_pages_recursively(f"{content_dir_path}/{fso}", template_path, f"{dest_dir_path}/{fso}")




