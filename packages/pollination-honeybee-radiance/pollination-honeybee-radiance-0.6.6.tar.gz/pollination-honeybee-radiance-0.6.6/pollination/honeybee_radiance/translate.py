from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class CreateRadianceFolder(Function):
    """Create a Radiance folder from a HBJSON input file."""

    input_model = Inputs.file(
        description='Path to input HBJSON file.',
        path='model.hbjson'
    )

    sensor_grid = Inputs.str(
        description='A pattern to filter grids to be exported to radiance folder. By '
        'default all the grids will be exported.', default='*'
    )

    @command
    def hbjson_to_rad_folder(self):
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson ' \
            '--grid "{{self.sensor_grid}}"'

    model_folder = Outputs.folder(description='Radiance folder.', path='model')

    sensor_grids = Outputs.list(
        description='Sensor grids information.', path='model/grid/_info.json'
    )

    sensor_grids_file = Outputs.file(
        description='Sensor grids information JSON file.', path='model/grid/_info.json'
    )


@dataclass
class CreateRadiantEnclosureInfo(Function):
    """Create JSONs with radiant enclosure information from a HBJSON input file.

    This enclosure info is intended to be consumed by thermal mapping functions.
    """

    model = Inputs.file(
        description='Path to input HBJSON file.',
        path='model.hbjson'
    )

    @command
    def hbjson_to_radiant_enclosure_info(self):
        return 'honeybee-radiance translate model-radiant-enclosure-info model.hbjson ' \
            '--folder output --log-file enclosure_list.json'

    enclosure_list = Outputs.dict(
        description='A list of dictionaries that include information about generated '
        'radiant enclosure files.', path='enclosure_list.json'
    )

    enclosure_list_file = Outputs.file(
        description='A JSON file that includes information about generated radiant '
        'enclosure files.', path='enclosure_list.json'
    )

    output_folder = Outputs.folder(
        description='Output folder with the enclosure info JSONs for each grid.',
        path='output'
    )
