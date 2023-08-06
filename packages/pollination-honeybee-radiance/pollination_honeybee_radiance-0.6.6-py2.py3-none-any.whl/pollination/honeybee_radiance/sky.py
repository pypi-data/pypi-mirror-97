from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class AddRemoveSkyMatrix(Function):
    """Remove direct sky from total sky and add direct sun."""

    total_sky_matrix = Inputs.file(
        description='Path to matrix for total sky contribution.',
        path='sky.ill', extensions=['ill', 'dc']
    )

    direct_sky_matrix = Inputs.file(
        description='Path to matrix for direct sky contribution.',
        path='sky_dir.ill', extensions=['ill', 'dc']
    )

    sunlight_matrix = Inputs.file(
        description='Path to matrix for direct sunlight contribution.',
        path='sun.ill', extensions=['ill', 'dc']
    )

    conversion = Inputs.str(
        description='Conversion as a string which will be passed to rmtxop -c option.',
        default=' '
    )

    output_format = Inputs.str(
        default='a', description='Output file format. a for ASCII, d for double, f for '
        'float and c for RGBE color.',
        spec={'type': 'string', 'enum': ['a', 'd', 'f', 'c']}
    )

    header = Inputs.str(
        default='remove',
        description='An input to indicate if header should be kept or removed from the'
        'output matrix.', spec={'type': 'string', 'enum': ['keep', 'remove']}
    )

    @command
    def create_matrix(self):
        return 'honeybee-radiance mtxop operate-three sky.ill sky_dir.ill sun.ill ' \
            '--operator-one "-" --operator-two "+" --{{self.header}}-header ' \
            '--conversion "{{self.conversion}}" --output-mtx final.ill ' \
            '--output-format {{self.output_format}}'

    results_file = Outputs.file(description='Radiance matrix file.', path='final.ill')


@dataclass
class AddSkyMatrix(Function):
    """Add indirect sky to direct sunlight."""

    indirect_sky_matrix = Inputs.file(
        description='Path to matrix for indirect sky contribution.',
        path='sky.ill', extensions=['ill', 'dc']
    )

    sunlight_matrix = Inputs.file(
        description='Path to matrix for direct sunlight contribution.',
        path='sun.ill', extensions=['ill', 'dc']
    )

    conversion = Inputs.str(
        description='Conversion as a string which will be passed to rmtxop -c option.',
        default=' '
    )

    output_format = Inputs.str(
        default='a', description='Output file format. a for ASCII, d for double, f for '
        'float and c for RGBE color.',
        spec={'type': 'string', 'enum': ['a', 'd', 'f', 'c']}
    )

    header = Inputs.str(
        default='remove',
        description='An input to indicate if header should be kept or removed from the'
        'output matrix.', spec={'type': 'string', 'enum': ['keep', 'remove']}
    )

    @command
    def create_matrix(self):
        return 'honeybee-radiance mtxop operate-two sky.ill sun.ill ' \
            '--operator + --{{self.header}}-header --conversion "{{self.conversion}}" ' \
            '--output-mtx final.ill --output-format {{self.output_format}}'

    results_file = Outputs.file(description='Radiance matrix file.', path='final.ill')


@dataclass
class GenSkyWithCertainIllum(Function):
    """Generates a sky with certain illuminance level."""

    illuminance = Inputs.float(
        default=100000,
        description='Sky illuminance level.'
    )

    @command
    def gen_overcast_sky(self):
        return 'honeybee-radiance sky illuminance {{self.illuminance}} --name overcast.sky'

    sky = Outputs.file(description='Generated sky file.', path='overcast.sky')


@dataclass
class CreateSkyDome(Function):
    """Create a skydome for daylight coefficient studies."""

    sky_density = Inputs.int(
        description='The density of generated sky. This input corresponds to gendaymtx '
        '-m option. -m 1 generates 146 patch starting with 0 for the ground and '
        'continuing to 145 for the zenith. Increasing the -m parameter yields a higher '
        'resolution sky using the Reinhart patch subdivision. For example, setting -m 4 '
        'yields a sky with 2305 patches plus one patch for the ground.', default=1,
        spec={'type': 'integer', 'minimum': 1}
    )

    @command
    def gen_sky_dome(self):
        return 'honeybee-radiance sky skydome --name rflux_sky.sky ' \
            '--sky-density {{self.sky_density}}'

    sky_dome = Outputs.file(
        description='A sky hemisphere with ground.', path='rflux_sky.sky'
    )


@dataclass
class CreateSkyMatrix(Function):
    """Generate a sun-up sky matrix."""

    north = Inputs.int(
        description='An angle for north direction. Default is 0.',
        default=0, spec={'type': 'integer', 'maximum': 360, 'minimum': 0}
    )

    sky_type = Inputs.str(
        description='A switch for generating sun-only sky or exclude sun '
        'contribution. The default is total sky which includes both.',
        default='total', spec={'type': 'string', 'enum': ['total', 'sun-only', 'no-sun']}
    )

    sky_density = Inputs.int(
        description='The density of generated sky. This input corresponds to gendaymtx '
        '-m option. -m 1 generates 146 patch starting with 0 for the ground and '
        'continuing to 145 for the zenith. Increasing the -m parameter yields a higher '
        'resolution sky using the Reinhart patch subdivision. For example, setting -m 4 '
        'yields a sky with 2305 patches plus one patch for the ground.', default=1,
        spec={'type': 'integer', 'minimum': 1}
    )

    cumulative = Inputs.str(
        description='An option to generate a cumulative sky instead of an hourly sky',
        default='hourly', spec={'type': 'string', 'enum': ['hourly', 'cumulative']}
    )

    output_type = Inputs.str(
        description='Output type which can be visible and or solar.', default='visible',
        spec={'type': 'string', 'enum': ['visible', 'solar']}
    )

    output_format = Inputs.str(
        description='Output file format. Options are float, double and ASCII.',
        default='ASCII', spec={'type': 'string', 'enum': ['float', 'double', 'ASCII']}
    )

    sun_up_hours = Inputs.str(
        description='An option to generate the sky for sun-up hours only. Default is '
        'for all the hours of the year.',
        default='all-hours',
        spec={'type': 'string', 'enum': ['all-hours', 'sun-up-hours']}
    )

    wea = Inputs.file(
        description='Path to a wea file.', extensions=['wea'], path='sky.wea'
    )

    @command
    def generate_sky_matrix(self):
        return 'honeybee-radiance sky mtx sky.wea --name sky --north {{self.north}} ' \
            '--sky-type {{self.sky_type}} --{{self.cumulative}} ' \
            '--{{self.sun_up_hours}} --{{self.output_type}} ' \
            '--output-format {{self.output_format}} --sky-density {{self.sky_density}}'

    sky_matrix = Outputs.file(description='Output Sky matrix', path='sky.mtx')
