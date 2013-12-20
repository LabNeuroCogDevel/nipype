# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from nipype.testing import assert_equal
from nipype.interfaces.camino.dti import PicoPDFs
def test_PicoPDFs_inputs():
    input_map = dict(ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    luts=dict(mandatory=True,
    argstr='-luts %s',
    ),
    out_file=dict(position=-1,
    genfile=True,
    argstr='> %s',
    ),
    args=dict(argstr='%s',
    ),
    inputmodel=dict(position=2,
    usedefault=True,
    argstr='-inputmodel %s',
    ),
    maxcomponents=dict(units='NA',
    argstr='-maxcomponents %d',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    in_file=dict(position=1,
    mandatory=True,
    argstr='< %s',
    ),
    directmap=dict(argstr='-directmap',
    ),
    numpds=dict(units='NA',
    argstr='-numpds %d',
    ),
    pdf=dict(position=4,
    usedefault=True,
    argstr='-pdf %s',
    ),
    terminal_output=dict(mandatory=True,
    nohash=True,
    ),
    )
    inputs = PicoPDFs.input_spec()

    for key, metadata in input_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(inputs.traits()[key], metakey), value
def test_PicoPDFs_outputs():
    output_map = dict(pdfs=dict(),
    )
    outputs = PicoPDFs.output_spec()

    for key, metadata in output_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(outputs.traits()[key], metakey), value