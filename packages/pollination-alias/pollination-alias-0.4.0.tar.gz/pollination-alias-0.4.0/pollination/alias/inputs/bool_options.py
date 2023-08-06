from pollination_dsl.alias import InputAlias
from queenbee.io.common import IOAliasHandler


"""Alias for yes/no inputs about whether to filter design days."""
filter_des_days_input = [
    InputAlias.any(
        name='filter_des_days',
        description='Either a boolean or one of two text strings: filter-des-days, '
        'all-des-days.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.bool_options',
                function='filter_des_days_to_str'
            )
        ]
    )
]


"""Alias for yes/no inputs about whether to use multipliers."""
use_multiplier_input = [
    InputAlias.any(
        name='use_multiplier',
        description='Either a boolean or one of two text strings: multiplier, '
        'full-geometry.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.bool_options',
                function='use_multiplier_to_str'
            )
        ]
    )
]


"""Alias for yes/no inputs about whether a building is residential."""
is_residential_input = [
    InputAlias.any(
        name='is_residential',
        description='Either a boolean or one of two text strings: residential, '
        'nonresidential.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.bool_options',
                function='is_residential_to_str'
            )
        ]
    )
]


"""Alias for yes/no inputs about whether a comfort map should be for SET."""
write_set_map_input = [
    InputAlias.any(
        name='write_set_map',
        description='Either a boolean or one of two text strings: write-op-map, '
        'write-set-map.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.bool_options',
                function='write_set_map_to_str'
            )
        ]
    )
]
