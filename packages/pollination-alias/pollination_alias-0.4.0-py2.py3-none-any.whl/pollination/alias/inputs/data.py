from pollination_dsl.alias import InputAlias
from queenbee.io.common import IOAliasHandler


"""Alias for inputs that can be either a single number or a data collection."""
value_or_data = [
    InputAlias.any(
        name='value',
        description='Either a single numerical value or data collection.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.data',
                function='value_or_data_to_str'
            )
        ]
    )
]
