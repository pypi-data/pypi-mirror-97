from pollination.honeybee_radiance.raytrace import RayTracingDaylightFactor
from queenbee.plugin.function import Function


def test_ray_tracing_daylightFactor():
    function = RayTracingDaylightFactor().queenbee
    assert function.name == 'ray-tracing-daylight-factor'
    assert isinstance(function, Function)
