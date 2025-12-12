from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeVigoV2, FakeTorino, FakeGeneva, FakeBrisbane

def run(qc, shots=1024, more_info=False):
    """
    runs the job results for a `qc` QuantumCircuit on the ideal simulator AerSimulator. 
    `shots` lets you specify how many times should the simulation run. 
    if `more_info` is set to True, it will return a dict sorted by 
    """
    sim_backend = AerSimulator()
    pm = generate_preset_pass_manager(backend=sim_backend)
    isa_qc = pm.run(qc)
    sampler = Sampler(mode=sim_backend)

    job = sampler.run([isa_qc], shots=shots)
    results = job.result()
    data = results[0].data

    if (more_info):
        counts = {}
        for name in dir(data):
            if name.startswith("_"):
                continue
            reg_obj = getattr(data, name)
            if hasattr(reg_obj, "get_counts"):
                counts[name] = reg_obj.get_counts()
    else:
        reg_name = list(data.__dict__.keys())[0]
        counts = getattr(data, reg_name).get_counts()
    return counts

def vigo_run(qc, shots=1024):
    """
    runs the job results for a `qc` QuantumCircuit the ideal simulator FakeVigoV2. 
    `shots` lets you specify how many times should the simulation run.
    """
    sim_backend = FakeVigoV2()
    pm = generate_preset_pass_manager(backend=sim_backend)
    isa_qc = pm.run(qc)
    sampler = Sampler(mode=sim_backend)

    job = sampler.run([isa_qc], shots=shots)
    results = job.result()
    counts = results[0].data.c.get_counts()
    return counts

def torino_run(qc, shots=1024):
    """
    runs the job results for a `qc` QuantumCircuit the ideal simulator FakeTorino. 
    `shots` lets you specify how many times should the simulation run.
    """
    sim_backend = FakeTorino()
    pm = generate_preset_pass_manager(backend=sim_backend)
    isa_qc = pm.run(qc)
    sampler = Sampler(mode=sim_backend)

    job = sampler.run([isa_qc], shots=shots)
    results = job.result()
    counts = results[0].data.c.get_counts()
    return counts

def geneva_run(qc, shots=1024):
    """
    runs the job results for a `qc` QuantumCircuit the ideal simulator FakeGeneva. 
    `shots` lets you specify how many times should the simulation run.
    """
    sim_backend = FakeGeneva()
    pm = generate_preset_pass_manager(backend=sim_backend)
    isa_qc = pm.run(qc)
    sampler = Sampler(mode=sim_backend)

    job = sampler.run([isa_qc], shots=shots)
    results = job.result()
    counts = results[0].data.c.get_counts()
    return counts

def brisbane_run(qc, shots=1024):
    """
    runs the job results for a `qc` QuantumCircuit the ideal simulator FakeBrisbane. 
    `shots` lets you specify how many times should the simulation run.
    """
    sim_backend = FakeBrisbane()
    pm = generate_preset_pass_manager(backend=sim_backend)
    isa_qc = pm.run(qc)
    sampler = Sampler(mode=sim_backend)

    job = sampler.run([isa_qc], shots=shots)
    results = job.result()
    counts = results[0].data.c.get_counts()
    return counts