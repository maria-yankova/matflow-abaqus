'`matflow_abaqus.main.py`'

from abaqus_parse import materials
from abaqus_parse.parts import generate_compact_tension_specimen_parts
from abaqus_parse.steps import generate_compact_tension_specimen_steps
from abaqus_parse.writers import write_inp

from abaqus_parse.generate_MK_mesh import generate_MK_mesh
from abaqus_parse.generate_FE_input import generate_FE_input
from abaqus_parse.save_model_response import save_model_response
from abaqus_parse.compute_forming_limit_curve import compute_forming_limit_curve


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
    specimen_parts = generate_compact_tension_specimen_parts(
        dimension, mesh_definition, elem_type, size_type, fraction, specimen_material)
    out = {
        'specimen_parts': specimen_parts
    }
    return out


@func_mapper(task='generate_steps', method='compact_tension_steps')
def generate_steps(applied_displacement, number_contours, time_increment_definition):
    compact_tension_steps = generate_compact_tension_specimen_steps(
        applied_displacement, number_contours, time_increment_definition)
    out = {
        'steps': compact_tension_steps
    }
    return out


@cli_format_mapper(input_name="memory", task="simulate_deformation", method="FE")
def memory_formatter(memory):
    return f'memory={memory.replace(" ", "")}'


###################################################################################
###################################################################################


@func_mapper(task='generate_MK_model', method='default')
def generate_sample(sample_size, inhomogeneity_factor, L_groove, L_slope, material_angle, groove_angle, elastic_modulus, poisson_ratio, density, law, path_plastic_table, mesh_size, bulk_parameters, elem_type, strain_rate, total_time, displacment_BC, time_step, nb_el_thickness, max_plastic_strain):
    Model_input = generate_FE_input(sample_size, inhomogeneity_factor, L_groove, L_slope, material_angle, groove_angle, elastic_modulus, poisson_ratio, density,
                                    law, path_plastic_table, mesh_size, bulk_parameters, elem_type, strain_rate, total_time, displacment_BC, time_step, nb_el_thickness, max_plastic_strain)
    out = {
        'FE_input_data': Model_input
    }
    return out


@input_mapper(input_file='inputs.inp', task='simulate_MK_deformation', method='FE')
def write_MK_inputs_file(path, FE_input_data):
    generate_MK_mesh(path, FE_input_data)


@output_mapper(output_name="model_response", task='simulate_MK_deformation', method='FE')
def generate_model_response(path):
    model_response = save_model_response(path)
    return model_response


@func_mapper(task='find_forming_limit_curve', method='strain_rate_ratio')
def forming_limit_curve(all_model_responses, strain_rate_ratio_threshold,
                        num_groove_angles):
    flc = compute_forming_limit_curve(
        all_model_responses,
        strain_rate_ratio_threshold,
        num_groove_angles
    )
    out = {
        'forming_limit_curve': flc
    }
    return out


@cli_format_mapper(input_name="memory", task="simulate_MK_deformation", method="FE")
def memory_formatter(memory):
    return f'memory={memory.replace(" ", "")}'
