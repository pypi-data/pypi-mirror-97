"""
    binalyzer_vmf.cli
    ~~~~~~~~~~~~~~~~~

    CLI extension for the *binalyzer* command.
"""
import click
import io

from binalyzer import (
    Binalyzer,
    ExpandedFile,
    BasedIntParamType,
)


@click.command()
@click.option('--input-file', '-i', required=True, type=ExpandedFile("rb"), help='The binary file to convert.')
@click.option('--output-file', '-o', required=True, type=ExpandedFile("w"), help='The VMF file to create.')
@click.option('--start-offset', '-s', type=BasedIntParamType(), default="0x00", show_default=True, help='Specifes the start offset')
def vmf(input_file, output_file, start_offset):
    """Convert a binary file to a VMF file.
    """
    binalyzer = Binalyzer(data=input_file)
    output_file.write(f"@{start_offset:06X}\n")
    for data_byte in binalyzer.template.value:
        output_file.write(f"{data_byte:02X}\n")
