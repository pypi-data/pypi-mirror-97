from pollination_dsl.alias import InputAlias
from queenbee.io.common import IOAliasHandler


"""Alias inputs that expect a HBJSON model file as the recipe input."""
hbjson_model_input = [
    # grasshopper Alias
    InputAlias.any(
        name='model',
        description='A path to a HBJSON file or a HB model object built with Python or'
        ' dotnet libraries.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_to_json'
            ),
            IOAliasHandler(
                language='csharp', module='HoneybeeSchema.Handlers',
                function='HBModelToJSON'
            )
        ]
    ),
    # Rhino alias
    InputAlias.linked(
        name='model',
        description='This input links the model to Rhino model.',
        platform=['rhino'],
        handler=[
            IOAliasHandler(
                language='csharp', module='HoneybeeRhino.Handlers',
                function='RhinoHBModelToJSON'
            )
        ]
    )
]


"""Alias inputs that expect a DFJSON model file as the recipe input."""
dfjson_model_input = [
    # grasshopper Alias
    InputAlias.any(
        name='model',
        description='A path to a DFJSON file or a DF model object built with Python '
        ' libraries.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_dragonfly_to_json'
            )
        ]
    )
]
