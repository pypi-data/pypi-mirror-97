from pollination_dsl.alias import InputAlias
from queenbee.io.common import IOAliasHandler


"""Alias for north inputs that can accept both an angle or a north vector."""
north_input = [
    InputAlias.any(
        name='north',
        description='Either a Vector2D for the north direction or a number between '
        '-360 and 360 for the counterclockwise difference between the North '
        'and the positive Y-axis in degrees.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.north',
                function='north_vector_to_angle'
            )
        ]
    )
]
