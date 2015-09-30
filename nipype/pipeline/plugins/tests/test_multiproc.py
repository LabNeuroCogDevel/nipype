import os
import nipype.interfaces.base as nib
from tempfile import mkdtemp
from shutil import rmtree

from nipype.testing import assert_equal, assert_less_equal
import nipype.pipeline.engine as pe

class InputSpec(nib.TraitedSpec):
    input1 = nib.traits.Int(desc='a random int')
    input2 = nib.traits.Int(desc='a random int')

class OutputSpec(nib.TraitedSpec):
    output1 = nib.traits.List(nib.traits.Int, desc='outputs')

class TestInterface(nib.BaseInterface):
    input_spec = InputSpec
    output_spec = OutputSpec

    def _run_interface(self, runtime):
        runtime.returncode = 0
        return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['output1'] = [1, self.inputs.input1]
        return outputs

def test_run_multiproc():
    cur_dir = os.getcwd()
    temp_dir = mkdtemp(prefix='test_engine_')
    os.chdir(temp_dir)

    pipe = pe.Workflow(name='pipe')
    mod1 = pe.Node(interface=TestInterface(),name='mod1')
    mod2 = pe.MapNode(interface=TestInterface(),
                      iterfield=['input1'],
                      name='mod2')
    pipe.connect([(mod1,mod2,[('output1','input1')])])
    pipe.base_dir = os.getcwd()
    mod1.inputs.input1 = 1
    pipe.config['execution']['poll_sleep_duration'] = 2
    execgraph = pipe.run(plugin="MultiProc")
    names = ['.'.join((node._hierarchy,node.name)) for node in execgraph.nodes()]
    node = execgraph.nodes()[names.index('pipe.mod1')]
    result = node.get_output('output1')
    yield assert_equal, result, [1, 1]
    os.chdir(cur_dir)
    rmtree(temp_dir)



#################################


class InputSpecSingleNode(nib.TraitedSpec):
    input1 = nib.traits.Int(desc='a random int')
    input2 = nib.traits.Int(desc='a random int')

class OutputSpecSingleNode(nib.TraitedSpec):
    output1 = nib.traits.Int(desc='a random int')


class TestInterfaceSingleNode(nib.BaseInterface):
    input_spec = InputSpecSingleNode
    output_spec = OutputSpecSingleNode

    def _run_interface(self, runtime):
        runtime.returncode = 0
        return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['output1'] =  self.inputs.input1
        return outputs


def parse_log(filename, measure):
    import json
    from dateutil.parser import parse
    from datetime import datetime
    import datetime as d

    json_data = open(filename).read()
    data = json.loads(json_data)
    total_duration = int(float(data['duration'])) #total duration in seconds

    total = []
    for i in range(total_duration):
        total.append(0)

    now = parse(data['start'])
    for i in range(total_duration):
        start_index = 0
        node_start = None
        node_finish = None

        x = now

        for j in range(start_index, len(data['nodes'])):
            node_start = parse(data['nodes'][j]['start'])
            node_finish = parse(data['nodes'][j]['finish'])

            if node_start < x and node_finish > x:
                total[i] += data['nodes'][j][measure]
                start_index = j

            if node_start > x:
                break

        now += d.timedelta(seconds=1)

    return total


import os
from nipype.pipeline.plugins.callback_log import log_nodes_cb, convert_logcb_to_json
import logging
import logging.handlers
def test_do_not_use_more_memory_then_specified():
    LOG_FILENAME = 'callback.log'
    my_logger = logging.getLogger('callback')
    my_logger.setLevel(logging.DEBUG)

    # Add the log message handler to the logger
    handler = logging.FileHandler(LOG_FILENAME)
    my_logger.addHandler(handler)

    max_memory = 10
    pipe = pe.Workflow(name='pipe')
    n1 = pe.Node(interface=TestInterfaceSingleNode(), name='n1')
    n2 = pe.Node(interface=TestInterfaceSingleNode(), name='n2')
    n3 = pe.Node(interface=TestInterfaceSingleNode(), name='n3')
    n4 = pe.Node(interface=TestInterfaceSingleNode(), name='n4')

    n1.interface.memory = 1
    n2.interface.memory = 1
    n3.interface.memory = 10
    n4.interface.memory = 1

    pipe.connect(n1, 'output1', n2, 'input1')
    pipe.connect(n1, 'output1', n3, 'input1')
    pipe.connect(n2, 'output1', n4, 'input1')
    pipe.connect(n3, 'output1', n4, 'input2')
    n1.inputs.input1 = 10
    pipe.config['execution']['poll_sleep_duration'] = 1
    pipe.run(plugin='ResourceMultiProc', plugin_args={'memory': max_memory, 'status_callback': log_nodes_cb})

    convert_logcb_to_json(LOG_FILENAME)
    #memory usage in every second
    memory = parse_log(LOG_FILENAME + '.json' , 'memory')

    result = True
    for m in memory:
        if m > max_memory:
            result = False
            break

    yield assert_equal, result, True

    os.remove(LOG_FILENAME)
    os.remove(LOG_FILENAME + '.json') 


def test_do_not_use_more_threads_then_specified():
    LOG_FILENAME = 'callback.log'
    my_logger = logging.getLogger('callback')
    my_logger.setLevel(logging.DEBUG)

    # Add the log message handler to the logger
    handler = logging.FileHandler(LOG_FILENAME)
    my_logger.addHandler(handler)

    max_threads = 10
    pipe = pe.Workflow(name='pipe')
    n1 = pe.Node(interface=TestInterfaceSingleNode(), name='n1')
    n2 = pe.Node(interface=TestInterfaceSingleNode(), name='n2')
    n3 = pe.Node(interface=TestInterfaceSingleNode(), name='n3')
    n4 = pe.Node(interface=TestInterfaceSingleNode(), name='n4')

    n1.interface.num_threads = 1
    n2.interface.num_threads = 1
    n3.interface.num_threads = 10
    n4.interface.num_threads = 1

    pipe.connect(n1, 'output1', n2, 'input1')
    pipe.connect(n1, 'output1', n3, 'input1')
    pipe.connect(n2, 'output1', n4, 'input1')
    pipe.connect(n3, 'output1', n4, 'input2')
    n1.inputs.input1 = 10
    pipe.config['execution']['poll_sleep_duration'] = 1
    pipe.run(plugin='ResourceMultiProc', plugin_args={'n_procs': max_threads, 'status_callback': log_nodes_cb})

    convert_logcb_to_json(LOG_FILENAME)
    #threads usage in every second
    threads = parse_log(LOG_FILENAME + '.json' , 'num_threads')

    result = True
    for t in threads:
        if t > max_threads:
            result = False
            break

    yield assert_equal, result, True

    os.remove(LOG_FILENAME)
    os.remove(LOG_FILENAME + '.json')