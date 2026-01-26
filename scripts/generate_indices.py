import os

DOCS_DIR = "docs"

def create_index_if_missing(directory):
    index_path = os.path.join(directory, "index.md")
    if not os.path.exists(index_path):
        dirname = os.path.basename(directory)
        title = dirname.split(".", 1)[-1].strip() if "." in dirname else dirname
        content = f"# {title}\n\nWelcome to the {title} section.\n\n## Contents\n\n"
        
        # List children
        try:
            items = sorted(os.listdir(directory))
            for item in items:
                if item == "index.md" or item.startswith("."):
                    continue
                
                item_path = os.path.join(directory, item)
                item_name = item
                if item.endswith(".md"):
                    item_name = item[:-3]
                
                # Check link path
                link = item
                if os.path.isdir(item_path):
                     link = f"{item}/"
                
                content += f"- [{item_name}]({link})\n"
                
            with open(index_path, "w") as f:
                f.write(content)
            print(f"Created {index_path}")
        except Exception as e:
            print(f"Error processing {directory}: {e}")

def main():
    for root, dirs, files in os.walk(DOCS_DIR):
        if root == DOCS_DIR:
            continue
        # Skip assets/images/templates folders
        if any(x in root.lower() for x in ["assets", "images", "stylesheets"]):
             continue
             
        create_index_if_missing(root)

if __name__ == "__main__":
    main()
