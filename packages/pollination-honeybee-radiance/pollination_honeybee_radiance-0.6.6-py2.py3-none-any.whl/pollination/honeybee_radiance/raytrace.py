from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class RayTracingDaylightFactor(Function):
    """Run ray-tracing and post-process the results for a daylight factor simulation."""

    radiance_parameters = Inputs.str(
        description='Radiance parameters. -I and -h are already included in the command.',
        default='-ab 2'
    )

    sky_illum = Inputs.int(
        description='Sky illuminance level for the sky included in octree.',
        default=100000
    )

    fixed_radiance_parameters = Inputs.str(
        description='Parameters that should not be overwritten by radiance_parameters '
        'input.', default='-I -h'
    )

    grid = Inputs.file(description='Input sensor grid.', path='grid.pts')

    scene_file = Inputs.file(
        description='Path to an octree file to describe the scene.', path='scene.oct'
    )

    @command
    def ray_tracing(self):
        return 'honeybee-radiance raytrace daylight-factor scene.oct grid.pts ' \
            '--rad-params "{{self.radiance_parameters}}" --rad-params-locked ' \
            '"{{self.fixed_radiance_parameters}}" --sky-illum {{self.sky_illum}} ' \
            '--output grid.res'

    result = Outputs.file(
        description='Daylight factor results file. The results for each sensor is in a '
        'new line.', path='grid.res'
    )
