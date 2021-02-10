'`matflow_abaqus.main.py`'

from abaqus_parse import materials
from abaqus_parse.parts import generate_compact_tension_specimen_parts
from abaqus_parse.steps import generate_compact_tension_specimen_steps
from abaqus_parse.writers import write_inp

from abaqus_parse.Generate_MK_mesh import Generate_MK_mesh
from abaqus_parse.Generate_FE_sample import Generate_FE_sample
from abaqus_parse.Generate_FE_features import Generate_FE_features
from abaqus_parse.Save_model_response import Save_model_response


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
	
	
###################################################################################
###################################################################################

	
@func_mapper(task='generate_Sample', method='default')
def Generate_sample(Sample_size, Inhomogeneity_factor, L_groove, L_slope, Material_angle, Groove_angle, Elastic_modulus, Poisson_ratio, Density, Barlat, Path_plastic_table):
    Sample_input = Generate_FE_sample(Sample_size, Inhomogeneity_factor, L_groove, L_slope, Material_angle, Groove_angle, Elastic_modulus, Poisson_ratio, Density, Barlat, Path_plastic_table)
    out = {
        'Sample_input_data': Sample_input
    }
    return out
    
        
@func_mapper(task='generate_FE_features', method='default')
def FE_features(mesh_size, bulk_parameters, elem_type, Strain_rate, total_time, Displacment_BC, Step_time):
    FE_input = Generate_FE_features(mesh_size, bulk_parameters, elem_type, Strain_rate, total_time, Displacment_BC, Step_time)
    out = {
        'FE_input_data': FE_input
    }
    return out

@input_mapper(input_file='inputs.inp', task='simulate_deformation', method='FE')
def write_MK_inputs_file(path, Sample_input_data, FE_input_data):
    Generate_MK_mesh(path, Sample_input_data, FE_input_data)
    
    
@output_mapper(output_name="model_response", task='simulate_deformation', method='FE')
def Generate_model_response(path):
    model_response = Save_model_response(path)
    out = {
        'model_response': model_response
    }
    return out