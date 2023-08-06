from pollination_dsl.alias import OutputAlias
from queenbee.io.common import IOAliasHandler


"""Alias for thermal comfort mapping percent outputs.

This includes Thermal Comfort PErcent (TCP), Heat Sensation Percent (HSP), and
Cold Sensation Percent (CSP).
"""
comfort_percent_output = [
    OutputAlias.any(
        name='thermal_comfort_percent',
        description='Thermal comfort percent values.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.outputs.comfort',
                function='read_comfort_percent_from_folder'
            )
        ]
    )
]
