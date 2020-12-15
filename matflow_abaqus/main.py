'`matflow_abaqus.main.py`'

from abaqus_parse import materials
from abaqus_parse.parts import generate_compact_tension_specimen_parts
from abaqus_parse.steps import generate_compact_tension_specimen_steps
from abaqus_parse.writers import write_inp

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


@func_mapper(task='generate_specimen_parts', method='compact_tension_fracture')
def generate_parts(dimension, mesh_definition,
                     elem_type, size_type, fraction, specimen_material):
    specimen_parts = generate_compact_tension_specimen_parts(dimension, mesh_definition, elem_type, size_type, fraction, specimen_material)
    out = {
        'specimen_parts': specimen_parts
    }
    return out

@func_mapper(task='generate_steps', method='compact_tension_steps')
def generate_steps(applied_displacement, number_contours, time_increment_definition):
    compact_tension_steps = generate_compact_tension_specimen_steps(applied_displacement, number_contours, time_increment_definition)
    out = {
        'steps': compact_tension_steps
    }
    return out

@input_mapper(input_file='inputs.inp', task='simulate_deformation', method='FE')
def write_inputs_file(path, material_models, specimen_parts, steps):
    write_inp(path, material_models, specimen_parts, steps)

@cli_format_mapper(input_name="memory", task="simulate_deformation", method="FE")
def memory_formatter(memory):
    return f'memory={memory.replace(" ", "")}'