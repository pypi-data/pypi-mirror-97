import copy
from os import path
from typing import List, Tuple, Union

import numpy as np

from autoconf import conf
from autofit import exc
from autofit.mapper import model_mapper as mm
from autofit.mapper.prior import prior as p
from autofit.non_linear.abstract_search import Result
from autofit.non_linear.parallel import AbstractJob, Process, AbstractJobResult
from autofit.non_linear.paths import Paths


class GridSearchResult:

    def __init__(
            self,
            results: List[Result],
            lower_limit_lists: List[List[float]],
            physical_lower_limits_lists: List[List[float]],
    ):
        """
        The result of a grid search.

        Parameters
        ----------
        results
            The results of the non linear optimizations performed at each grid step
        lower_limit_lists
            A list of lists of values representing the lower bounds of the grid searched values at each step
        physical_lower_limits_lists
            A list of lists of values representing the lower physical bounds of the grid search values
            at each step.
        """
        self.lower_limit_lists = lower_limit_lists
        self.physical_lower_limits_lists = physical_lower_limits_lists
        self.results = results
        self.no_dimensions = len(self.lower_limit_lists[0])
        self.no_steps = len(self.lower_limit_lists)
        self.side_length = int(self.no_steps ** (1 / self.no_dimensions))

    def __getattr__(self, item: str) -> object:
        """
        We default to getting attributes from the best result. This allows promises to reference best results.
        """
        return getattr(self.best_result, item)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)

    @property
    def shape(self):
        return tuple([
            self.side_length
            for _ in range(
                self.no_dimensions
            )
        ])

    @property
    def best_result(self):
        """
        The best result of the grid search. That is, the result output by the non linear search that had the highest
        maximum figure of merit.

        Returns
        -------
        best_result: Result
        """
        best_result = None
        for result in self.results:
            if (
                    best_result is None
                    or result.log_likelihood > best_result.log_likelihood
            ):
                best_result = result
        return best_result

    @property
    def best_model(self):
        """
        Returns
        -------
        best_model: mm.ModelMapper
            The model mapper instance associated with the highest figure of merit from the grid search
        """
        return self.best_result.model

    @property
    def all_models(self):
        """
        Returns
        -------
        all_models: [mm.ModelMapper]
            All model mapper instances used in the grid search
        """
        return [result.model for result in self.results]

    @property
    def physical_step_sizes(self):

        physical_step_sizes = []

        # TODO : Make this work for all dimensions in a less ugly way.

        for dim in range(self.no_dimensions):

            values = [value[dim] for value in self.physical_lower_limits_lists]
            diff = [abs(values[n] - values[n - 1]) for n in range(1, len(values))]

            if dim == 0:
                physical_step_sizes.append(np.max(diff))
            elif dim == 1:
                physical_step_sizes.append(np.min(diff))
            else:
                raise exc.GridSearchException(
                    "This feature does not support > 2 dimensions"
                )

        return tuple(physical_step_sizes)

    @property
    def physical_centres_lists(self):
        return [
            [
                lower_limit[dim] + self.physical_step_sizes[dim] / 2
                for dim in range(self.no_dimensions)
            ]
            for lower_limit in self.physical_lower_limits_lists
        ]

    @property
    def physical_upper_limits_lists(self):
        return [
            [
                lower_limit[dim] + self.physical_step_sizes[dim]
                for dim in range(self.no_dimensions)
            ]
            for lower_limit in self.physical_lower_limits_lists
        ]

    @property
    def results_reshaped(self):
        """
        Returns
        -------
        likelihood_merit_array: np.ndarray
            An arrays of figures of merit. This arrays has the same dimensionality as the grid search, with the value in
            each entry being the figure of merit taken from the optimization performed at that point.
        """
        return np.reshape(
            np.array([result for result in self.results]),
            tuple(self.side_length for _ in range(self.no_dimensions)),
        )

    @property
    def max_log_likelihood_values(self):
        """
        Returns
        -------
        likelihood_merit_array: np.ndarray
            An arrays of figures of merit. This arrays has the same dimensionality as the grid search, with the value in
            each entry being the figure of merit taken from the optimization performed at that point.
        """
        return np.reshape(
            np.array([result.log_likelihood for result in self.results]),
            tuple(self.side_length for _ in range(self.no_dimensions)),
        )

    @property
    def log_evidence_values(self):
        """
        Returns
        -------
        likelihood_merit_array: np.ndarray
            An arrays of figures of merit. This arrays has the same dimensionality as the grid search, with the value in
            each entry being the figure of merit taken from the optimization performed at that point.
        """
        return np.reshape(
            np.array([result.samples.log_evidence for result in self.results]),
            tuple(self.side_length for _ in range(self.no_dimensions)),
        )


class GridSearch:

    def __init__(self, search, paths=None, number_of_steps=4, number_of_cores=1):
        """
        Performs a non linear optimiser search for each square in a grid. The dimensionality of the search depends on
        the number of distinct priors passed to the fit function. (1 / step_size) ^ no_dimension steps are performed
        per an optimisation.

        Parameters
        ----------
        number_of_steps: int
            The number of steps to go in each direction
        search: class
            The class of the search that is run at each step
        """

        if paths is None:
            self.paths = search.paths
        else:
            self.paths = paths

        self.number_of_cores = number_of_cores

        if self.number_of_cores == 1:
            self.parallel = False
        else:
            self.parallel = True

        self.number_of_steps = number_of_steps
        self.search = search
        self.prior_passer = search.prior_passer

    @property
    def step_size(self):
        """
        Returns
        -------
        step_size: float
            The size of a step in any given dimension in hyper space.
        """
        return 1 / self.number_of_steps

    def make_physical_lists(self, grid_priors) -> List[List[float]]:
        lists = self.make_lists(grid_priors)
        return [
            [prior.value_for(value) for prior, value in zip(grid_priors, l)]
            for l in lists
        ]

    def make_lists(self, grid_priors):
        """
        Produces a list of lists of floats, where each list of floats represents the values in each dimension for one
        step of the grid search.

        Parameters
        ----------
        grid_priors: [p.Prior]
            A list of priors that are to be searched using the grid search.

        Returns
        -------
        lists: [[float]]
        """
        return make_lists(
            len(grid_priors), step_size=self.step_size, centre_steps=False
        )

    def make_arguments(self, values, grid_priors):
        arguments = {}
        for value, grid_prior in zip(values, grid_priors):
            if (
                    float("-inf") == grid_prior.lower_limit
                    or float("inf") == grid_prior.upper_limit
            ):
                raise exc.PriorException(
                    "Priors passed to the grid search must have definite limits"
                )
            lower_limit = grid_prior.lower_limit + value * grid_prior.width
            upper_limit = (
                    grid_prior.lower_limit
                    + (value + self.step_size) * grid_prior.width
            )
            prior = p.UniformPrior(lower_limit=lower_limit, upper_limit=upper_limit)
            arguments[grid_prior] = prior
        return arguments

    def model_mappers(self, model, grid_priors):
        grid_priors = list(set(grid_priors))
        lists = self.make_lists(grid_priors)
        for values in lists:
            arguments = self.make_arguments(values, grid_priors)
            yield model.mapper_from_partial_prior_arguments(arguments)

    def fit(self, model, analysis, grid_priors):
        """
        Fit an analysis with a set of grid priors. The grid priors are priors associated with the model mapper
        of this instance that are replaced by uniform priors for each step of the grid search.

        Parameters
        ----------
        model
        analysis: autofit.non_linear.non_linear.Analysis
            An analysis used to determine the fitness of a given model instance
        grid_priors: [p.Prior]
            A list of priors to be substituted for uniform priors across the grid.

        Returns
        -------
        result: GridSearchResult
            An object that comprises the results from each individual fit
        """
        func = self.fit_parallel if self.parallel else self.fit_sequential
        return func(
            model=model,
            analysis=analysis,
            grid_priors=grid_priors
        )

    def fit_parallel(self, model, analysis, grid_priors):
        """
        Perform the grid search in parallel, with all the optimisation for each grid square being performed on a
        different process.

        Parameters
        ----------
        analysis
            An analysis
        grid_priors
            Priors describing the position in the grid

        Returns
        -------
        result: GridSearchResult
            The result of the grid search
        """

        grid_priors = list(set(grid_priors))
        results = []
        lists = self.make_lists(grid_priors)
        physical_lists = self.make_physical_lists(grid_priors)

        results_list = [
            ["index"]
            + list(map(model.name_for_prior, grid_priors))
            + ["likelihood_merit"]
        ]

        jobs = list()

        for index, values in enumerate(lists):
            jobs.append(
                self.job_for_analysis_grid_priors_and_values(
                    analysis=copy.deepcopy(analysis),
                    model=model,
                    grid_priors=grid_priors,
                    values=values,
                    index=index,
                )
            )

        for result in Process.run_jobs(
                jobs,
                self.number_of_cores
        ):
            results.append(result)
            results = sorted(results)
            results_list.append(result.result_list_row)
            self.write_results(results_list)

        return GridSearchResult(
            [
                result.result
                for result
                in results
            ],
            lists,
            physical_lists
        )

    def fit_sequential(self, model, analysis, grid_priors):
        """
        Perform the grid search sequentially, with all the optimisation for each grid square being performed on the
        same process.

        Parameters
        ----------
        analysis
            An analysis
        grid_priors
            Priors describing the position in the grid

        Returns
        -------
        result: GridSearchResult
            The result of the grid search
        """

        grid_priors = list(sorted(set(grid_priors), key=lambda prior: prior.id))
        results = []
        lists = self.make_lists(grid_priors)
        physical_lists = self.make_physical_lists(grid_priors)

        results_list = [
            ["index"]
            + list(map(model.name_for_prior, grid_priors))
            + ["max_log_likelihood"]
        ]

        for index, values in enumerate(lists):
            job = self.job_for_analysis_grid_priors_and_values(
                analysis=analysis,
                model=model,
                grid_priors=grid_priors,
                values=values,
                index=index,
            )

            result = job.perform()

            results.append(result.result)
            results_list.append(result.result_list_row)

            self.write_results(results_list)

        return GridSearchResult(results, lists, physical_lists)

    def write_results(self, results_list):

        with open(path.join(self.paths.output_path, "results"), "w+") as f:
            f.write(
                "\n".join(
                    map(
                        lambda ls: ", ".join(
                            map(
                                lambda value: "{:.2f}".format(value)
                                if isinstance(value, float)
                                else str(value),
                                ls,
                            )
                        ),
                        results_list,
                    )
                )
            )

    def job_for_analysis_grid_priors_and_values(
            self, model, analysis, grid_priors, values, index
    ):
        arguments = self.make_arguments(values=values, grid_priors=grid_priors)
        model = model.mapper_from_partial_prior_arguments(arguments=arguments)

        labels = []
        for prior in sorted(arguments.values(), key=lambda pr: pr.id):
            labels.append(
                "{}_{:.2f}_{:.2f}".format(
                    model.name_for_prior(prior), prior.lower_limit, prior.upper_limit
                )
            )

        name_path = path.join(
            self.paths.name,
            self.paths.tag,
            self.paths.non_linear_tag,
            "_".join(labels),
        )

        search_instance = self.search_instance(name_path=name_path)

        return Job(
            search_instance=search_instance,
            model=model,
            analysis=analysis,
            arguments=arguments,
            index=index,
        )

    def search_instance(self, name_path):
        search_instance = self.search.copy_with_paths(
            Paths(
                name=name_path,
                tag=self.paths.tag,
                path_prefix=self.paths.path_prefix,
                remove_files=self.paths.remove_files,
            )
        )

        for key, value in self.__dict__.items():
            if key not in ("model", "instance", "paths"):
                try:
                    setattr(search_instance, key, value)
                except AttributeError:
                    pass
        return search_instance


class JobResult(AbstractJobResult):
    def __init__(self, result, result_list_row, number):
        """
        The result of a job

        Parameters
        ----------
        result
            The result of a grid search
        result_list_row
            A row in the result list
        """
        super().__init__(number)
        self.result = result
        self.result_list_row = result_list_row


class Job(AbstractJob):
    def __init__(self, search_instance, model, analysis, arguments, index):
        """
        A job to be performed in parallel.

        Parameters
        ----------
        search_instance
            An instance of an optimiser
        analysis
            An analysis
        arguments
            The grid search arguments
        """
        super().__init__()
        self.search_instance = search_instance
        self.analysis = analysis
        self.model = model
        self.arguments = arguments
        self.index = index

    def perform(self):
        result = self.search_instance.fit(model=self.model, analysis=self.analysis)
        result_list_row = [
            self.index,
            *[prior.lower_limit for prior in self.arguments.values()],
            result.log_likelihood,
        ]

        return JobResult(result, result_list_row, self.number)


def grid(fitness_function, no_dimensions, step_size):
    """
    Grid2D search using a fitness function over a given number of dimensions and a given step size between inclusive
    limits of 0 and 1.

    Parameters
    ----------
    fitness_function: function
        A function that takes a tuple of floats as an argument
    no_dimensions: int
        The number of dimensions of the grid search
    step_size: float
        The step size of the grid search

    Returns
    -------
    best_arguments: tuple[float]
        The tuple of arguments that gave the highest fitness
    """
    best_fitness = float("-inf")
    best_arguments = None

    for arguments in make_lists(no_dimensions, step_size):
        fitness = fitness_function(tuple(arguments))
        if fitness > best_fitness:
            best_fitness = fitness
            best_arguments = tuple(arguments)

    return best_arguments


def make_lists(
        no_dimensions: int,
        step_size: Union[Tuple[float], float],
        centre_steps=True
):
    """
        Returns a list of lists of floats covering every combination across no_dimensions of points of integer step size
    between 0 and 1 inclusive.

    Parameters
    ----------
    no_dimensions
        The number of dimensions, that is the length of the lists
    step_size
        The step size. This can be a float or a tuple with the same number of dimensions
    centre_steps

    Returns
    -------
    lists: [[float]]
        A list of lists
    """
    if isinstance(step_size, float):
        step_size = tuple(
            step_size
            for _
            in range(no_dimensions)
        )

    if no_dimensions == 0:
        return [[]]

    sub_lists = make_lists(
        no_dimensions - 1,
        step_size[1:],
        centre_steps=centre_steps
    )
    step_size = step_size[0]
    return [
        [
            step_size * value + (
                0.5 * step_size
                if centre_steps
                else 0)
        ] + sub_list
        for value in range(int((1 / step_size)))
        for sub_list in sub_lists
    ]
