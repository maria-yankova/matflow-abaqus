'`matflow_abaqus.main.py`'

from abaqus_parse import materials 

from matflow_abaqus import (
    input_mapper,
    output_mapper,
    cli_format_mapper,
    register_output_file,
    func_mapper,
    software_versions,
)

# tells Matflow this function satisfies the requirements of the task
@func_mapper(task='generate_material_models', method='default')
def generate_material_models(materials_list):
    mat_mods = materials.generate_material_models(materials_list)
    out = {
        'material_models': mat_mods
    }
    return out