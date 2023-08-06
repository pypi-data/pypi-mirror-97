from dataclasses import dataclass
from pollination_dsl.function import Inputs, Outputs, Function, command


@dataclass
class ModelToHoneybee(Function):
    """Translate a Dragonfly Model JSON file into several Honeybee Models."""

    model = Inputs.file(
        description='Dragonfly model in JSON format.', path='model.dfjson',
        extensions=['dfjson', 'json']
    )

    obj_per_model = Inputs.str(
        description='Text to describe how the input Model should be divided across the '
        'output Models. Choose from: District, Building, Story.', default='Story',
        spec={'type': 'string', 'enum': ['District', 'Building', 'Story']}
    )

    use_multiplier = Inputs.str(
        description='A switch to note whether the multipliers on each Building story '
        'should be passed along to the generated Honeybee Room objects or if full '
        'geometry objects should be written for each story in the building.',
        default='full-geometry',
        spec={'type': 'string', 'enum': ['full-geometry', 'multiplier']}
    )

    include_plenum = Inputs.str(
        description='A switch to indicate whether ceiling/floor plenums should be '
        'auto-generated for the Rooms.', default='no-plenum',
        spec={'type': 'string', 'enum': ['no-plenum', 'plenum']}
    )

    shade_dist = Inputs.float(
        description='A number to note the distance beyond which other buildings shade '
        'should be excluded from a given Honeybee Model. This number should always be '
        'in meters regardless of the input Dragonfly model units. If 0, shade from all '
        'neighboring buildings will be excluded from the resulting models.', default=50
    )

    @command
    def model_to_honeybee(self):
        return 'dragonfly translate model-to-honeybee model.dfjson ' \
            '--obj-per-model {{self.obj_per_model}} --{{self.use_multiplier}} ' \
            '--{{self.include_plenum}} --shade-dist {{self.shade_dist}} --folder output ' \
            '--log-file output/hbjson_info.json'

    hbjson_list = Outputs.dict(
        description='A JSON array that includes information about generated honeybee '
        'models.', path='output/hbjson_info.json'
    )

    output_folder = Outputs.folder(
        description='Output folder with the output HBJSON models.', path='output'
    )
