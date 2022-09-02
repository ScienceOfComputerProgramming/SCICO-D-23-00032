import logging

from freneticlib.core.core import FreneticCore
from freneticlib.core.mutation.crossovers import Crossover
from freneticlib.core.mutation import exploiters
from freneticlib.core.mutation.mutators import FreneticMutator
from freneticlib.core.objective import MaxObjective
from freneticlib.executors.bicycle.bicycleexecutor import BicycleExecutor
from freneticlib.frenetic import Frenetic
from freneticlib.representations.kappa_generator import FixStepKappaGenerator
from freneticlib.stopcriteria.counter import CountingStop

# specify a logging format
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(message)s", datefmt="%H:%M:%S")


def run_example():
    # We want a FixStep Kappa representation
    representation = FixStepKappaGenerator(length=30, variation=5, step=10.0)
    # representation = CatmullRomGenerator(control_nodes=30, variation=5)

    # Setup an objective. Here: maximize the distance_from_center (i.e. push the vehicle off the road)
    objective = MaxObjective(
        feature="distance_from_center",
        # every simulation produces 10 records per second, we extract the maximum of this
        per_simulation_aggregator="max",
    )

    # Define the Frenetic core using representation, objective and the mutation operators
    core = FreneticCore(
        representation=representation,
        objective=objective,
        mutator=FreneticMutator(representation),
        exploiter=exploiters.FirstVariableExploiter(),
        crossover=Crossover(size=20, frequency=30),
    )

    # Define the Frenetic executor and the stop-criterion.
    frenetic = Frenetic(
        core,
        BicycleExecutor(
            representation=representation,
            objective=objective,
            # results_path="./sink/detailed"
        ),
        CountingStop(n_random=50, n_total=250),
    )

    # run the search
    frenetic.start()

    # store the results for later use
    frenetic.store_results("./sink/dev.csv")

    # Display the progress
    frenetic.plot()


if __name__ == "__main__":
    run_example()
