import os
import xml.etree.ElementTree as ET

def pascal_voc_to_opencv_annotation(xml_folder, output_file):
    with open(output_file, "w") as ann_file:
        for xml_file in os.listdir(xml_folder):
            if not xml_file.endswith(".xml"):
                continue

            xml_path = os.path.join(xml_folder, xml_file)
            tree = ET.parse(xml_path)
            root = tree.getroot()

            img_filename = os.path.splitext(xml_file)[0] + ".jpg"
            img_width = int(root.find("size/width").text)
            img_height = int(root.find("size/height").text)

            num_annotations = 0
            annotations_str = ""

            for obj in root.findall("object"):
                bbox = obj.find("bndbox")
                x_min = int(bbox.find("xmin").text)
                y_min = int(bbox.find("ymin").text)
                x_max = int(bbox.find("xmax").text)
                y_max = int(bbox.find("ymax").text)

                x_center = (x_min + x_max) // 2
                y_center = (y_min + y_max) // 2

                annotations_str += f" {x_min} {y_min} {x_max} {y_max}"
                num_annotations += 1

            if num_annotations > 0:
                line = f"{os.path.join(xml_folder, img_filename)} {num_annotations}{annotations_str}\n"
                ann_file.write(line)

if __name__ == "__main__":

    pascal_voc_folder = "/Users/artur/Develop/UncannyEyes_EyeData/EyeTracking-Output"
    output_file = "/Users/artur/Develop/UncannyEyes_EyeData/EyeTracking-Output/annotations.txt"
    pascal_voc_to_opencv_annotation(pascal_voc_folder, output_file)