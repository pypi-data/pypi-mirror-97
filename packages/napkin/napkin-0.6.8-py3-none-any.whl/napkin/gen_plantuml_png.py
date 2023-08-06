"""
Generate PlantUML script and PNG file
"""
from . import gen_plantuml_img


def generate(diagram_name, output_dir, sd_context, options=None):
    return gen_plantuml_img.generate(diagram_name, output_dir, sd_context,
                                     options, 'png')
