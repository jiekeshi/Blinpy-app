import os
import xml.etree.ElementTree as ET
from src.utils import db
from src.text_processor import text_processor

def bug_reader(bug_report_path, code_base_path, file_type):
  
    bug_data = {}
    fixed_files = {}

    tree = ET.parse(bug_report_path)
    root = tree.getroot()
    for child in root:
        try:
            bug_data[child.get("id")] = child[0].text + child[1].text
        except: 
            bug_data[child.get("id")] = child[0].text

        fixed_files[child.get("id")] = []
        for file_path in child[2].findall("file"):
            if file_path.text.split(".")[-1].strip() in file_type:
                fixed_files[child.get("id")].append(os.path.join(code_base_path, file_path.text))
    bug_data = text_processor(bug_data)
    for bug_id, bug_cont in bug_data.items():
        db.insert_one({"bug_id": bug_id, "bug_content": bug_cont, "fixed_files": fixed_files[bug_id]})
    return bug_data, fixed_files
