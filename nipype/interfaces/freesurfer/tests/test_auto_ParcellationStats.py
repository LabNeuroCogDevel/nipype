# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..utils import ParcellationStats


def test_ParcellationStats_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    aseg=dict(mandatory=True,
    ),
    brainmask=dict(mandatory=True,
    ),
    copy_inputs=dict(),
    cortex_label=dict(),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    hemisphere=dict(argstr='%s',
    mandatory=True,
    position=-2,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    in_annotation=dict(argstr='-a %s',
    xor=['in_label'],
    ),
    in_cortex=dict(argstr='-cortex %s',
    ),
    in_label=dict(argstr='-l %s',
    xor=['in_annotatoin', 'out_color'],
    ),
    lh_pial=dict(mandatory=True,
    ),
    lh_white=dict(mandatory=True,
    ),
    mgz=dict(argstr='-mgz',
    ),
    out_color=dict(argstr='-c %s',
    genfile=True,
    xor=['in_label'],
    ),
    out_table=dict(argstr='-f %s',
    genfile=True,
    requires=['tabular_output'],
    ),
    rh_pial=dict(mandatory=True,
    ),
    rh_white=dict(mandatory=True,
    ),
    ribbon=dict(mandatory=True,
    ),
    subject_id=dict(argstr='%s',
    mandatory=True,
    position=-3,
    usedefault=True,
    ),
    subjects_dir=dict(),
    surface=dict(argstr='%s',
    position=-1,
    ),
    tabular_output=dict(argstr='-b',
    ),
    terminal_output=dict(nohash=True,
    ),
    th3=dict(argstr='-th3',
    requires=['cortex_label'],
    ),
    thickness=dict(mandatory=True,
    ),
    transform=dict(mandatory=True,
    ),
    wm=dict(mandatory=True,
    ),
    )
    inputs = ParcellationStats.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value


def test_ParcellationStats_outputs():
    output_map = dict(out_color=dict(),
    out_table=dict(),
    )
    outputs = ParcellationStats.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
