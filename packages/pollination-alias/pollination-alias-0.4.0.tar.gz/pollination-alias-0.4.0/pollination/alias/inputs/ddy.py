from pollination_dsl.alias import InputAlias
from queenbee.io.common import IOAliasHandler


"""Alias for inputs that expect a .ddy file as the recipe input."""
ddy_input = [
    InputAlias.any(
        name='ddy',
        description='Either a DDY python object or the path to a ddy or an epw file.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.ddy',
                function='ddy_handler'
            )
        ]
    )
]
