"""
Testing Variational Quantum Circuits.
"""
import numpy as np
import pytest
from qibo.config import get_threads, set_threads
from qibo import gates
from qibo.models import Circuit, VQE
from qibo.hamiltonians import XXZ
from qibo import models, hamiltonians
from qibo.optimizers import optimize
from qibo.tests import utils
from scipy.linalg import expm


test_names = "method,options,compile,filename"
test_values = [("Powell", {'maxiter': 1}, True, 'vqc_powell.out'),
               ("Powell", {'maxiter': 1}, False, 'vqc_powell.out'),
               ("BFGS", {'maxiter': 1}, True, 'vqc_bfgs.out'),
               ("BFGS", {'maxiter': 1}, False, 'vqc_bfgs.out')]
@pytest.mark.parametrize(test_names, test_values)
def test_vqc(method, options, compile, filename):
    """Performs a VQE circuit minimization test."""

    def myloss(parameters, circuit, target):
        circuit.set_parameters(parameters)
        state = circuit().tensor
        return 1 - np.abs(np.dot(np.conj(target), state))

    nqubits = 6
    nlayers  = 4

    # Create variational circuit
    c = models.Circuit(nqubits)
    for l in range(nlayers):
        c.add((gates.RY(q, theta=0) for q in range(nqubits)))
        c.add((gates.CZ(q, q+1) for q in range(0, nqubits-1, 2)))
        c.add((gates.RY(q, theta=0) for q in range(nqubits)))
        c.add((gates.CZ(q, q+1) for q in range(1, nqubits-2, 2)))
        c.add(gates.CZ(0, nqubits-1))
    c.add((gates.RY(q, theta=0) for q in range(nqubits)))

    # Optimize starting from a random guess for the variational parameters
    np.random.seed(0)
    x0 = np.random.uniform(0, 2*np.pi, 2*nqubits*nlayers + nqubits)
    data = np.random.normal(0, 1, size=2**nqubits)

    # perform optimization
    best, params = optimize(myloss, x0, args=(c, data), method=method,
                            options=options, compile=compile)
    if filename is not None:
        utils.assert_regression_fixture(params, filename)


test_names = "method,options,compile,filename"
test_values = [("Powell", {'maxiter': 1}, True, 'vqe_powell.out'),
               ("Powell", {'maxiter': 1}, False, 'vqe_powell.out'),
               ("BFGS", {'maxiter': 1}, True, 'vqe_bfgs.out'),
               ("BFGS", {'maxiter': 1}, False, 'vqe_bfgs.out'),
               ("parallel_L-BFGS-B", {'maxiter': 1}, True, None),
               ("parallel_L-BFGS-B", {'maxiter': 1}, False, None),
               ("cma", {"maxfevals": 2}, False, None),
               ("sgd", {"nepochs": 5}, False, None),
               ("sgd", {"nepochs": 5}, True, None)]
@pytest.mark.parametrize(test_names, test_values)
def test_vqe(method, options, compile, filename):
    """Performs a VQE circuit minimization test."""
    import qibo
    if method == 'parallel_L-BFGS-B':
        if 'GPU' in qibo.get_device(): # pragma: no cover
            pytest.skip("unsupported configuration")
        import os
        if os.name == 'nt': # pragma: no cover
            pytest.skip("Parallel L-BFGS-B not supported on Windows.")
        qibo.set_threads(1)

    original_backend = qibo.get_backend()
    if method == "sgd" or compile:
        qibo.set_backend("matmuleinsum")

    original_threads = get_threads()
    nqubits = 6
    layers  = 4

    circuit = Circuit(nqubits)
    for l in range(layers):
        for q in range(nqubits):
            circuit.add(gates.RY(q, theta=1.0))
        for q in range(0, nqubits-1, 2):
            circuit.add(gates.CZ(q, q+1))
        for q in range(nqubits):
            circuit.add(gates.RY(q, theta=1.0))
        for q in range(1, nqubits-2, 2):
            circuit.add(gates.CZ(q, q+1))
        circuit.add(gates.CZ(0, nqubits-1))
    for q in range(nqubits):
        circuit.add(gates.RY(q, theta=1.0))

    hamiltonian = XXZ(nqubits=nqubits)
    np.random.seed(0)
    initial_parameters = np.random.uniform(0, 2*np.pi, 2*nqubits*layers + nqubits)
    v = VQE(circuit, hamiltonian)
    best, params = v.minimize(initial_parameters, method=method,
                              options=options, compile=compile)
    if method == "cma":
        # remove `outcmaes` folder
        import shutil
        shutil.rmtree("outcmaes")
    if filename is not None:
        utils.assert_regression_fixture(params, filename)
    qibo.set_backend(original_backend)
    qibo.set_threads(original_threads)


def test_vqe_custom_gates_errors():
    """Check that ``RuntimeError``s is raised when using custom gates."""
    import qibo
    from qibo.backends import AVAILABLE_BACKENDS
    if "custom" not in AVAILABLE_BACKENDS: # pragma: no cover
        pytest.skip("Custom backend not available.")

    original_backend = qibo.get_backend()
    qibo.set_backend("custom")

    nqubits = 6
    circuit = Circuit(nqubits)
    for q in range(nqubits):
        circuit.add(gates.RY(q, theta=0))
    for q in range(0, nqubits-1, 2):
        circuit.add(gates.CZ(q, q+1))

    hamiltonian = XXZ(nqubits=nqubits)
    initial_parameters = np.random.uniform(0, 2*np.pi, 2*nqubits + nqubits)
    v = VQE(circuit, hamiltonian)
    # compile with custom gates
    with pytest.raises(RuntimeError):
        best, params = v.minimize(initial_parameters, method="BFGS",
                                  options={'maxiter': 1}, compile=True)
    # use SGD with custom gates
    with pytest.raises(RuntimeError):
        best, params = v.minimize(initial_parameters, method="sgd",
                                  compile=False)
    qibo.set_backend(original_backend)


def test_initial_state(accelerators):
    h = hamiltonians.TFIM(3, h=1.0, trotter=True)
    qaoa = models.QAOA(h, accelerators=accelerators)
    qaoa.set_parameters(np.random.random(4))
    target_state = np.ones(2 ** 3) / np.sqrt(2 ** 3)
    final_state = qaoa.get_initial_state()
    np.testing.assert_allclose(final_state, target_state)


@pytest.mark.parametrize("solver,trotter",
                         [("exp", False),
                          ("rk4", False),
                          ("rk45", False),
                          ("exp", True),
                          ("rk4", True),
                          ("rk45", True)])
def test_qaoa_execution(solver, trotter, accel=None):
    h = hamiltonians.TFIM(4, h=1.0, trotter=trotter)
    m = hamiltonians.X(4, trotter=trotter)
    # Trotter and RK require small p's!
    params = 0.01 * (1 - 2 * np.random.random(4))
    state = utils.random_numpy_state(4)
    # set absolute test tolerance according to solver
    if "rk" in solver:
        atol = 1e-2
    elif trotter:
        atol = 1e-5
    else:
        atol = 0

    target_state = np.copy(state)
    h_matrix = h.matrix.numpy()
    m_matrix = m.matrix.numpy()
    for i, p in enumerate(params):
        if i % 2:
            u = expm(-1j * p * m_matrix)
        else:
            u = expm(-1j * p * h_matrix)
        target_state = u @ target_state

    qaoa = models.QAOA(h, mixer=m, solver=solver, accelerators=accel)
    qaoa.set_parameters(params)
    final_state = qaoa(np.copy(state))
    np.testing.assert_allclose(final_state, target_state, atol=atol)


def test_qaoa_distributed_execution(accelerators):
    test_qaoa_execution("exp", True, accelerators)


def test_qaoa_callbacks(accelerators):
    from qibo import callbacks
    # use ``Y`` Hamiltonian so that there are no errors
    # in the Trotter decomposition
    h = hamiltonians.Y(3)
    energy = callbacks.Energy(h)
    params = 0.1 * np.random.random(4)
    state = utils.random_numpy_state(3)

    ham = hamiltonians.Y(3, trotter=True)
    qaoa = models.QAOA(ham, callbacks=[energy], accelerators=accelerators)
    qaoa.set_parameters(params)
    final_state = qaoa(np.copy(state))

    h_matrix = h.matrix.numpy()
    m_matrix = qaoa.mixer.matrix.numpy()
    calc_energy = lambda s: (s.conj() * h_matrix.dot(s)).sum()
    target_state = np.copy(state)
    target_energy = [calc_energy(target_state)]
    for i, p in enumerate(params):
        if i % 2:
            u = expm(-1j * p * m_matrix)
        else:
            u = expm(-1j * p * h_matrix)
        target_state = u @ target_state
        target_energy.append(calc_energy(target_state))
    np.testing.assert_allclose(energy[:], target_energy)


def test_qaoa_errors():
    # Invalid Hamiltonian type
    with pytest.raises(TypeError):
        qaoa = models.QAOA("test")
    # Hamiltonians of different type
    h = hamiltonians.TFIM(4, h=1.0, trotter=True)
    m = hamiltonians.X(4, trotter=False)
    with pytest.raises(TypeError):
        qaoa = models.QAOA(h, mixer=m)
    # distributed execution with RK solver
    with pytest.raises(NotImplementedError):
        qaoa = models.QAOA(h, solver="rk4", accelerators={"/GPU:0": 2})
    # minimize with odd number of parameters
    qaoa = models.QAOA(h)
    with pytest.raises(ValueError):
        qaoa.minimize(np.random.random(5))


test_names = "method,options,trotter,filename"
test_values = [
    ("BFGS", {'maxiter': 1}, False, "qaoa_bfgs.out"),
    ("BFGS", {'maxiter': 1}, True, "trotter_qaoa_bfgs.out"),
    ("Powell", {'maxiter': 1}, True, "trotter_qaoa_powell.out"),
    ("sgd", {"nepochs": 5}, False, None)
    ]
@pytest.mark.parametrize(test_names, test_values)
def test_qaoa_optimization(method, options, trotter, filename):
    h = hamiltonians.XXZ(3, trotter=trotter)
    qaoa = models.QAOA(h)
    initial_p = [0.05, 0.06, 0.07, 0.08]
    best, params = qaoa.minimize(initial_p, method=method, options=options)
    if filename is not None:
        utils.assert_regression_fixture(params, filename)
