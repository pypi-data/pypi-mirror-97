from typing import Tuple, Union, Dict, List
from flowty.constants import ObjSense, OptimizationStatus, Where

from flowty.interop import ffi, libFlowty, checked
from flowty.entities import Var, Constr, LinExpr, LinEqua, Graph

callbackRegistry: Dict = {}


class CallbackModel:
    """
    The callback model to interact with the algorithm during the callback function.

    Use [setCallback][flowty.model.Model.setCallback] to set a callback function. The
    callback function will be invoked with an initialized callback model.
    """

    def __init__(self, model: ffi.CData, callbackModel: ffi.CData = ffi.NULL):
        self.__model = model
        self.__callbackModel = callbackModel

    def getResource(self, name: str) -> float:
        """
        Get the current resource value.

        Parameters:
            name: The name of the resource.

        Returns:
            The resource value.

        Note:
            Only applicable in the dynamic programming algorithm.
        """

        value = ffi.new("double *")
        checked(
            libFlowty.FLWT_CallbackModel_getResource(
                self.__callbackModel, name.encode("utf-8"), value
            )
        )
        return value[0]

    def setResource(self, name: str, value: float):
        """
        Set the current resource value.

        Parameters:
            name: The name of the resource.
            value: The new value to set.

        Note:
            Only applicable in the dynamic programming algorithm.
        """

        checked(
            libFlowty.FLWT_CallbackModel_setResource(
                self.__callbackModel, name.encode("utf-8"), value
            )
        )

    def getResourceOther(self, name: str) -> float:
        """
        Get the current resource of another label in dominance.

        Parameters:
            name: The name of the resource.

        Returns:
            The resource value of the other label.

        Note:
            Only valid in
            [DPDominate][flowty.constants.Where.DPDominate].
        """

        value = ffi.new("double *")
        checked(
            libFlowty.FLWT_CallbackModel_getResourceOther(
                self.__callbackModel, name.encode("utf-8"), value
            )
        )
        return value[0]

    def skip(self):
        """
        Invoking this function has different meanings depending on
        [Where][flowty.constants.Where]:

        In the dynamic programming algorithm

        - For [DPExtend][flowty.constants.Where.DPExtend] then discard a label if it is
        **infeasible**.

        In the path MIP algorithm

        - For [PathMIPSolution][flowty.constants.Where.PathMIPSolution] then skip a
        solution if is **infeasible**.
        - For [PathMIPSubproblem][flowty.constants.Where.PathMIPSubproblem] then
        **skip** calls to the internal dynamic programming algorithm. Only paths added
        with [addPath][flowty.model.CallbackModel.addPath] are then present in the path
        MIP.

        Note:
            Only valid in [DPExtend][flowty.constants.Where.DPExtend],
            [PathMIPSolution][flowty.constants.Where.PathMIPSolution], or
            [PathMIPSubproblem][flowty.constants.Where.PathMIPSubproblem].
        """
        checked(libFlowty.FLWT_CallbackModel_skip(self.__callbackModel))

    def keep(self) -> None:
        """
        Indicate that the label under consideration to be dominated should be kept.
        That is, if the other label is **not dominated** then this function should be
        invoked.

        Note:
            Only valid in [DPDominate][flowty.constants.Where.DPDominate]
        """
        checked(libFlowty.FLWT_CallbackModel_keep(self.__callbackModel))

    def addCut(self, equa: LinEqua) -> None:
        """
        Add a cut to the model.

        Parameters:
            equa: The cut as a linear equation.

        Note:
            Only valid in [PathMIPCuts][flowty.constants.Where.PathMIPCuts]
        """

        checked(
            libFlowty.FLWT_CallbackModel_addCut(
                self.__callbackModel, equa._LinEqua__linEqua
            )
        )

    @property
    def k(self) -> int:
        """
        The current graph index.

        Returns:
            The graph id.
        """
        value = ffi.new("int *")
        checked(libFlowty.FLWT_CallbackModel_getK(self.__callbackModel, value))
        return value[0]

    @property
    def vertex(self) -> int:
        """
        The current vertex in the graph.

        Returns:
            The vertex id.

        Note:
            Only applicable in the dynamic programming algorithm.
        """

        value = ffi.new("int *")
        checked(libFlowty.FLWT_CallbackModel_getVertex(self.__callbackModel, value))
        return value[0]

    @property
    def edge(self) -> int:
        """
        The current edge in the graph on which extension of state is happening.

        Returns:
            The edge id.

        Note:
            Only valid in [DPExtend][flowty.constants.Where.DPExtend].
        """

        value = ffi.new("int *")
        checked(libFlowty.FLWT_CallbackModel_getEdge(self.__callbackModel, value))
        return value[0]

    @property
    def haveArtificialCost(self) -> bool:
        """
        Verify if the edge costs are artifical. This happens when the path MIP attempts
        to restore feasibility. Correct costs are recalculated when feasiblity is
        restored.

        If the path cost have non-edge components, like resource dependent non-linear
        costs, those must be skipped when calculating artificial reduced costs.

        Returns:
            A boolean flag indicating if edge cost is artificial.

        Note:
            Only applicable in the dynamic programming algorithm when solving a path
            MIP.
        """
        value = ffi.new("int *")
        checked(
            libFlowty.FLWT_CallbackModel_haveArtificialCost(self.__callbackModel, value)
        )
        return bool(value[0])

    @property
    def x(self) -> List[float]:
        """
        The current variable values.

        - For [PathMIPCuts][flowty.constants.Where.PathMIPCuts] or
        [PathMIPHeuristic][flowty.constants.Where.PathMIPHeuristic] it is the **current
        relaxation**
        - For [PathMIPSolution][flowty.constants.Where.PathMIPSolution] it is a
        **solution candidate**.

        Returns:
            A list with values for all variables.

        Note:
            Only valid in [PathMIPCuts][flowty.constants.Where.PathMIPCuts],
        [PathMIPHeuristic][flowty.constants.Where.PathMIPHeuristic], or
        [PathMIPSolution][flowty.constants.Where.PathMIPSolution].
        """
        num = ffi.new("int *")
        checked(libFlowty.FLWT_Model_getNumVars(self.__model, num))
        num = num[0]
        array = ffi.new("const double []", num)
        checked(libFlowty.FLWT_CallbackModel_getX(self.__callbackModel, array, num))
        return [array[i] for i in range(num)]

    @property
    def reducedCost(self) -> List[float]:
        """
        The current reduced cost for a subproblem.

        Access [k][flowty.model.CallbackModel.k] to get information of the current
        subproblem and use [convexDual][flowty.model.CallbackModel.convexDual] to get
        the current convex dual value.

        Returns:
            A list with values for all variables.

        Note:
            Only valid in [PathMIPSubproblem][flowty.constants.Where.PathMIPSubproblem].
        """
        num = ffi.new("int *")
        checked(libFlowty.FLWT_Model_getNumVars(self.__model, num))
        num = num[0]
        array = ffi.new("double []", num)
        checked(
            libFlowty.FLWT_CallbackModel_getReducedCost(
                self.__callbackModel, array, num
            )
        )
        return [array[i] for i in range(num)]

    @property
    def convexDual(self) -> float:
        """
        The convex dual value for a subproblem.

        Returns:
            A list with values for all variables.

        Note:
            Only valid in [PathMIPSubproblem][flowty.constants.Where.PathMIPSubproblem].
        """
        value = ffi.new("double *")
        checked(libFlowty.FLWT_CallbackModel_getConvexDual(self.__callbackModel, value))
        return value[0]

    @property
    def zeroEdges(self) -> List[int]:
        """
        The current list of edges with values fixed to zero.

        Returns:
            A list of edge indices.

        Note:
            Only valid in [PathMIPSubproblem][flowty.constants.Where.PathMIPSubproblem].
        """
        num = ffi.new("int *")
        checked(libFlowty.FLWT_CallbackModel_getNumZeroEdges(self.__callbackModel, num))
        num = num[0]

        if num == 0:
            return []

        array = ffi.new("int []", num)
        checked(
            libFlowty.FLWT_CallbackModel_getZeroEdges(self.__callbackModel, array, num)
        )
        return [array[i] for i in range(num)]

    def setStatus(self, status: OptimizationStatus) -> None:
        """
        Set the optimization status if using a custom subproblem algorithm.

        Parameters:
            status: The optimization status

        Note:
            Only valid in [PathMIPSubproblem][flowty.constants.Where.PathMIPSubproblem].
        """
        checked(
            libFlowty.FLWT_CallbackModel_setStatus(self.__callbackModel, status.value)
        )

    def addPath(self, cost: float, eids: List[int]) -> None:
        """
        Add a path to a subproblem during initialization or if using a custom subproblem
        algorithm.

        The cost of the path is given

        - For [PathMIPSubproblem][flowty.constants.Where.PathMIPSubproblem] as the
          **reduced cost**
        - For [PathMIPInit][flowty.constants.Where.PathMIPInit] as the **actual cost**

        Parameters:
            cost: The cost of the path.
            eids: A list of edge indices.

        Note:
            Only valid in [PathMIPSubproblem][flowty.constants.Where.PathMIPSubproblem]
            or [PathMIPInit][flowty.constants.Where.PathMIPInit].
        """
        size = len(eids)
        array = ffi.new("int []", eids)
        checked(
            libFlowty.FLWT_CallbackModel_addPath(
                self.__callbackModel, cost, array, size
            )
        )

    def addSolution(self, cost: float, x: List[float]) -> None:
        """
        Add a solution to the problem.

        Parameters:
            cost: The objective value of the solution.
            x: A list of variable values.

        Note:
            Only valid in [PathMIPHeuristic][flowty.constants.Where.PathMIPHeuristic].
        """
        size = len(x)
        array = ffi.new("double []", x)
        checked(
            libFlowty.FLWT_CallbackModel_addSolution(
                self.__callbackModel, cost, array, size
            )
        )


@ffi.callback("int(*)(FLWT_CallbackModel* model, int where, void* userdata)")
def globalCallback(callbackModel, where, userdata):
    handle = callbackRegistry[userdata]
    ffi.from_handle(handle).callback(
        CallbackModel(userdata, callbackModel), Where(where)
    )
    return 0


class Model:
    """
    The optimization model.

    Model regular linear constraints and variables like

    ```python
    m = Model()
    m += xsum(2 * m.addVar(lb=0, ub=1, obj=c[i], type="B") for i in range(2)) == 1
    ```

    Do graph stuff like

    ```python
    m = Model()
    g = m.addGraph(
        obj=c,
        edges=e,
        source=0,
        sink=n - 1,
        L=1,
        U=n - 2,
        type="B"
    )
    m.addResourceDisposable(
        graph=g,
        consumptionType="E",
        weight=t,
        boundsType="V",
        lb=a,
        ub=b,
        name="t",
    )
    ```
    """

    BUFFER_SIZE = 512

    def __init__(self, name: str = ""):
        """
        Initialize the optimization model.

        Parameters:
            name: The name of the model.
        """
        self.__model = ffi.new("FLWT_Model **")
        checked(libFlowty.FLWT_Model_new(self.__model))
        # dereferencing pointer
        self.__model = self.__model[0]
        self.__str_buffer = ffi.new("char[{}]".format(self.BUFFER_SIZE))
        self.callback = None

    def __del__(self):
        checked(libFlowty.FLWT_Model_delete(self.__model))

    def __iadd__(self, other) -> "Model":
        if isinstance(other, LinEqua):
            self.addConstr(other)
        elif isinstance(other, LinExpr):
            self.setObjective(other)
        elif isinstance(other, tuple):
            if isinstance(other[0], str) and isinstance(other[1], LinExpr):
                self.setObjective(other)
            elif isinstance(other[0], LinEqua) and isinstance(other[1], str):
                self.addConstr(other[0], other[1])

        return self

    @property
    def constr(self) -> List[Constr]:
        """The constraints of the model."""
        num = ffi.new("int *")
        checked(libFlowty.FLWT_Model_getNumConstrs(self.__model, num))
        num = num[0]
        array = ffi.new("FLWT_Constr *[]", num)
        checked(libFlowty.FLWT_Model_getConstrs(self.__model, array))
        return [Constr(array[i]) for i in range(num)]

    @property
    def graphs(self) -> List[Graph]:
        """The graphs of the model."""
        num = ffi.new("int *")
        checked(libFlowty.FLWT_Model_getNumGraphs(self.__model, num))
        num = num[0]
        array = ffi.new("FLWT_Graph *[]", num)
        checked(libFlowty.FLWT_Model_getGraphs(self.__model, array))
        return [Graph(array[i]) for i in range(num)]

    @property
    def name(self) -> str:
        """The model name."""
        checked(
            libFlowty.FLWT_Model_getName(
                self.__var, self.__str_buffer, self.BUFFER_SIZE
            )
        )
        return ffi.string(self.__str_buffer).decode("utf-8")

    @name.setter
    def name(self, name: str) -> None:
        checked(libFlowty.FLWT_Model_setName(self.__model, name.encode("utf-8")))

    @property
    def vars(self) -> List[Var]:
        """The variables of the model."""
        num = ffi.new("int *")
        checked(libFlowty.FLWT_Model_getNumVars(self.__model, num))
        num = num[0]
        array = ffi.new("FLWT_Var *[]", num)
        checked(libFlowty.FLWT_Model_getVars(self.__model, array))
        return [Var(array[i]) for i in range(num)]

    @property
    def objectiveValue(self) -> float:
        """The objective value."""
        value = ffi.new("double *")
        checked(libFlowty.FLWT_Model_getObjectiveValue(self.__model, value))
        return value[0]

    def setLicenseKey(self, user: str, key: str) -> None:
        """
        Set the user and license key. If no key is set the community license is used.

        Note:
            The community license is a free license to the general community which may
            have limited features and additional restrictions.

        Parameters:
            user: The user name.
            key: The license key.
        """
        checked(
            libFlowty.FLWT_Model_setLicenseKey(
                self.__model, user.encode("utf-8"), key.encode("utf-8")
            )
        )

    def setObjective(self, expr: Union[LinExpr, Tuple[str, LinExpr]]):
        """
        Set the objective function.

        Parameters:
            expr: Defaults to minimization. Otherwise set with tuple of a
                [ObjSense][flowty.constants.ObjSense] and a linear expression.
        """
        sense = ObjSense.Minimize

        if isinstance(expr, LinExpr):
            objExpr = expr
        elif isinstance(expr[0], str) and isinstance(expr[1], LinExpr):
            sense = (
                ObjSense.Minimize if expr[0] == ObjSense.Minimize else ObjSense.Maximize
            )
            objExpr = expr[1]
        checked(
            libFlowty.FLWT_Model_setObjective(
                self.__model, objExpr._LinExpr__linExpr, sense.value
            )
        )

    def addVar(
        self,
        lb: float = -float("inf"),
        ub: float = float("inf"),
        obj: float = 0,
        type: str = "C",
        name: str = "",
    ) -> Var:
        """
        Add variable to the model

        Parameters:
            lb: Lower bound
            ub: Upper bound
            obj: Objective coefficient
            type: Type as in [VarType][flowty.constants.VarType]. Values can be "C",
                "B", or "I" which is continuous, binary, or general integer type
                respectively
            name: Name of the variable

        Returns:
            The variable added
        """
        if type == "B":
            lb = 0
            ub = 1

        variable = ffi.new("FLWT_Var **")
        checked(
            libFlowty.FLWT_Model_addVar(
                self.__model,
                lb,
                ub,
                obj,
                type.encode("utf-8"),
                name.encode("utf-8"),
                variable,
            )
        )
        return Var(variable[0])

    def addConstr(self, equa: LinEqua, name: str = "") -> Constr:
        """
        Add constraint to the model

        Parameters:
            equa: The constraint as a linear equation.
            name: Name of the variable

        Returns:
            The constraint added
        """
        constr = ffi.new("FLWT_Constr **")
        checked(
            libFlowty.FLWT_Model_addConstr(
                self.__model, equa._LinEqua__linEqua, name.encode("utf-8"), constr
            )
        )
        return Constr(constr[0])

    def addGraph(
        self,
        obj: List[float] = [],
        edges: List[Tuple[int, int]] = [],
        source: int = 0,
        sink: int = -1,
        L: float = 1,
        U: float = 1,
        type: str = "B",
        names: Union[str, List[str]] = None,
    ) -> Graph:
        """
        Add a graph. Implicitly adds edges as variables.

        Parameters:
            obj: The edge cost to map into the objective function for each variable.
            edges: The list of edges given as tuples of vertex indices.
            source: The source vertex.
            sink: The sink vertex.
            L: Lower bound on path flow.
            U: Upper bound on path flow.
            type: Type as in [VarType][flowty.constants.VarType] for the path flow
                values. The type can be "C", "B" or "I" which is continuous, binary or
                integer path flow. For $`U > 1`$ this allows integer flow on paths.
                Enforcing a binary restriction in this case is a modeling decision.
            names: A prefix or a list of names for the edges.

        Returns:
            The graph added.
        """
        graph = ffi.new("FLWT_Graph **")

        if isinstance(obj, (float, int)):
            obj = [obj] * len(edges)

        objArray = ffi.new("double []", obj)
        fromArray = ffi.new("int []", [e[0] for e in edges])
        toArray = ffi.new("int []", [e[1] for e in edges])
        m = len(edges)

        namesArray_keepalive = ffi.NULL
        namesArray = ffi.NULL
        if isinstance(names, str):
            names = [f"{names}_{i}" for i in range(m)]
        if isinstance(names, list):
            namesArray_keepalive = [
                ffi.new("char []", n.encode("utf-8")) for n in names
            ]
            namesArray = ffi.new("char *[]", namesArray_keepalive)

        directed = True
        checked(
            libFlowty.FLWT_Model_addGraph(
                self.__model,
                int(directed),
                objArray,
                fromArray,
                toArray,
                m,
                source,
                sink,
                L,
                U,
                type.encode("utf-8"),
                namesArray,
                graph,
            )
        )
        return Graph(graph[0])

    def addResourceDisposable(
        self,
        graph: Graph,
        consumptionType: str = "V",
        weight: Union[float, List[float]] = 1,
        boundsType: str = "V",
        lb: Union[float, List[float]] = 0,
        ub: Union[float, List[float]] = 1,
        name: str = None,
    ) -> None:
        """
        Add a disposable resource constraint.

        Parameters:
            graph: The graph to add the resource constraint to.
            consumptionType: Where is the resource being consumed, edge `E` or vertex
                `V`.
            weight: The amount to consume.
            boundsType: Where is the resource being bounded, edge `E`, vertex `V` or
                none `N`.
            lb: Lower bound enforced as indicated by `boundsType`.
            ub: Upper bound enforced as indicated by `boundsType`.
            name: The resource name.
        """
        num = graph.n if consumptionType == "V" else graph.m

        if isinstance(weight, (float, int)):
            weight = [weight] * num

        num = graph.n if boundsType == "V" else graph.m
        if isinstance(lb, (float, int)):
            lb = [lb] * num
        if isinstance(ub, (float, int)):
            ub = [ub] * num

        obj = [0] * num

        weightArray = ffi.new("double []", weight)
        lbArray = ffi.new("double []", lb)
        ubArray = ffi.new("double []", ub)
        objArray = ffi.new("double []", obj)

        checked(
            libFlowty.FLWT_Model_addResourceDisposable(
                self.__model,
                graph._Graph__graph,
                consumptionType.encode("utf-8"),
                weightArray,
                boundsType.encode("utf-8"),
                lbArray,
                ubArray,
                objArray,
                name.encode("utf-8") if name else "".encode("utf-8"),
            )
        )

    def addResourceNonDisposable(
        self,
        graph: Graph,
        consumptionType: str = "V",
        weight: Union[float, List[float]] = 1,
        boundsType: str = "V",
        lb: Union[float, List[float]] = 0,
        ub: Union[float, List[float]] = 1,
        name: str = None,
    ) -> None:
        """
        Add a non-disposable resource constraint.

        Parameters:
            graph: The graph to add the resource constraint to.
            consumptionType: Where is the resource being consumed, edge `E` or vertex
                `V`.
            weight: The amount to consume.
            boundsType: Where is the resource being bounded, edge `E`, vertex `V` or
                none `N`.
            lb: Lower bound enforced as indicated by `boundsType`.
            ub: Upper bound enforced as indicated by `boundsType`.
            name: The resource name.
        """
        num = graph.n if consumptionType == "V" else graph.m

        if isinstance(weight, (float, int)):
            weight = [weight] * num

        num = graph.n if boundsType == "V" else graph.m
        if isinstance(lb, (float, int)):
            lb = [lb] * num
        if isinstance(ub, (float, int)):
            ub = [ub] * num

        obj = [0] * num

        weightArray = ffi.new("double []", weight)
        lbArray = ffi.new("double []", lb)
        ubArray = ffi.new("double []", ub)
        objArray = ffi.new("double []", obj)

        checked(
            libFlowty.FLWT_Model_addResourceNonDisposable(
                self.__model,
                graph._Graph__graph,
                consumptionType.encode("utf-8"),
                weightArray,
                boundsType.encode("utf-8"),
                lbArray,
                ubArray,
                objArray,
                name.encode("utf-8") if name else "".encode("utf-8"),
            )
        )

    def addResourceCustom(self, graph: Graph, name: str = "") -> None:
        """
        Add a custom resource constraint.

        Can be accessed using the name in callbacks.

        Parameters:
            graph: The graph to add the resource constraint to.
            name: The resource name.
        """
        checked(
            libFlowty.FLWT_Model_addResourceCustom(
                self.__model, graph._Graph__graph, name.encode("utf-8")
            )
        )

    def addPackingSet(self, packingSet: List[Var]) -> None:
        r"""
        Add a packing set $`B`$ where $`\sum_{i \in B} x_i \leq 1`$ holds true.

        Parameters:
            packingSet: The set of variables in $`B`$
        """
        variables = [v._Var__var for v in packingSet]
        size = len(packingSet)
        varArray = ffi.new("FLWT_Var *[]", variables)

        checked(libFlowty.FLWT_Model_addPackingSet(self.__model, varArray, size))

    def read(self, filename: str) -> None:
        """
        Read a model from file.

        Parameters:
            filename: The path to file.
        """
        checked(libFlowty.FLWT_Model_read(self.__model, filename.encode("utf-8")))

    def write(self, filename: str) -> None:
        """
        Write a model to file.

        Parameters:
            filename: The path to file.
        """
        checked(libFlowty.FLWT_Model_write(self.__model, filename.encode("utf-8")))

    def optimize(self) -> OptimizationStatus:
        """
        Optimize the model.

        Returns:
            The status of the optimization.
        """

        status = ffi.new("FLWT_OptimizationStatus *")
        checked(libFlowty.FLWT_Model_optimize(self.__model, status))
        status = status[0]
        return OptimizationStatus(status)

    def setParam(self, key: str, value: Union[str, int, float]) -> None:
        """
        Set a parameter. Valid parameters are

        | Name | Type | Description | Default |
        |-|-|-|-|
        | `Algorithm` | `str` | What algorithm to use. Options are `PathMIP` for the path MIP algorithm, `MIP` for the branch-and-cut algorithm, and `DP` for the dynamic programming algorithm. | `PathMIP` |
        | `Verbosity` | `str` | Turn verbosity on/off. | `On` |
        | `Threads` | `int` | The approximate number of threads to use. | `4` |
        | `NodeLimit` | `int`| The branch-and-bound node limit. If limit is reached optimization stops with status [NodeLimit][flowty.constants.OptimizationStatus.NodeLimit] | `inf` |
        | `SolutionLimit` | `int` |  The maximum number of solutions. If limit is reached optimization stops with status [SolutionLimit][flowty.constants.OptimizationStatus.SolutionLimit] | `inf` |
        | `TimeLimit` | `float` | The computation time limit in seconds. If limit is reached optimization stops with status [TimeLimit][flowty.constants.OptimizationStatus.TimeLimit] | `inf` |
        | `SubproblemTimeLimit` | `float` | The computation time limit in seconds for solving subproblems. If limit is reached and feasible solutions are found the optimization continues. Bounds are not calculated. If no feasible solutions are found the optimization stops with status [TimeLimit][flowty.constants.OptimizationStatus.TimeLimit] |  `inf` |
        | `Gap` | `float` | The absolute gap between objective upper and lower bound. | `1e-4` |
        | `CallbackDP` | `str` | If a callback function is set should it also be used in the dynamic programing algorithm. For performance reasons this should be avoided if not needed. | `Off` |
        | `MIPSolver` | `str` | Specify the underlying MIP solver. Options are `Cbc` for the [COIN Cbc](https://www.coin-or.org) solver or `Xpress` for [FICO Xpress](https://www.fico.com/en/products/fico-xpress-solver) solver. | `Cbc` | 

        Parameters:
            key: The name of the parameter to set.
            value: The value to assign.
        """  # noqa

        if isinstance(value, str):
            checked(
                libFlowty.FLWT_Model_setParam(
                    self.__model, key.encode("utf-8"), value.encode("utf-8")
                )
            )
        elif isinstance(value, int):
            checked(
                libFlowty.FLWT_Model_setParamInt(
                    self.__model, key.encode("utf-8"), value
                )
            )
        elif isinstance(value, float):
            checked(
                libFlowty.FLWT_Model_setParamDbl(
                    self.__model, key.encode("utf-8"), value
                )
            )
        else:
            raise ValueError(f"Unknown parameter key: {key}")

    def setCallback(self, callback) -> None:
        """
        Set a callback function with signature

        ```python
        def callback(callbackModel: CallbackModel, where: Where): -> None
            pass
        ```

        Use the [CallbackModel][flowty.model.CallbackModel] to get/set data. Use the
        [Where][flowty.constants.Where] to determine where in the algorithm flow the
        callback is invoked.
        """

        self.callback = callback
        handle = ffi.new_handle(self)
        self.__callback_handle = handle  # must be kept alive
        callbackRegistry[self.__model] = handle
        checked(
            libFlowty.FLWT_Model_setCallback(self.__model, globalCallback, self.__model)
        )


def maximize(expr: LinExpr) -> Tuple[ObjSense, LinExpr]:
    """
    Creates a maximization objective function of a linear expression.

    Note:
        Only applicable in the MIP algorithm.

    Parameters:
        expr: A linear expression

    Returns:
        A tuple of [Maximize][flowty.constants.ObjSense.Maximize] and the linear
        expression.
    """
    return (ObjSense.Maximize, expr)


def minimize(expr: LinExpr) -> Tuple[ObjSense, LinExpr]:
    """
    Creates a minimization objective function of a linear expression.

    Parameters:
        expr: A linear expression

    Returns:
        A tuple of [Minimize][flowty.constants.ObjSense.Minimize] and the linear
        expression.
    """
    return (ObjSense.Minimize, expr)


def xsum(terms: List[Union[Tuple[float, Var], Var, LinExpr]]) -> LinExpr:
    """
    Sums up the terms into a linear expression.

    Usage is:

    ```python
    expr = xsum( 3 * x + 4 * y + z - otherExpr)
    ```

    Parameters:
        terms: A list of terms to sum

    Returns:
        A linear expression
    """
    result = LinExpr()
    for term in terms:
        if isinstance(term, tuple):
            result.addTerm(term[0], term[1])
        elif isinstance(term, Var):
            result.addTerm(1, term)
        elif isinstance(term, LinExpr):
            result.addExpr(term)
        else:
            raise ValueError("Unknown term. Must be 'Var' or 'LinExpr'")
    return result
