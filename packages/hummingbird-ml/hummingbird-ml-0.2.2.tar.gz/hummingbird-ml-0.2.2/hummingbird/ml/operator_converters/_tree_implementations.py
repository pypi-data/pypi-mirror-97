# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
Base classes for tree algorithm implementations.
"""
from abc import abstractmethod
from enum import Enum
import numpy as np
import torch

from . import constants
from ._physical_operator import PhysicalOperator


class TreeImpl(Enum):
    """
    Enum definig the available implementations for tree scoring.
    """

    gemm = 1
    tree_trav = 2
    perf_tree_trav = 3


class AbstracTreeImpl(PhysicalOperator):
    """
    Abstract class definig the basic structure for tree-base models.
    """

    def __init__(self, logical_operator, **kwargs):
        super().__init__(logical_operator, **kwargs)

    @abstractmethod
    def aggregation(self, x):
        """
        Method defining the aggregation operation to execute after the model is evaluated.

        Args:
            x: An input tensor

        Returns:
            The tensor result of the aggregation
        """
        pass


class AbstractPyTorchTreeImpl(AbstracTreeImpl, torch.nn.Module):
    """
    Abstract class definig the basic structure for tree-base models implemented in PyTorch.
    """

    def __init__(self, logical_operator, tree_parameters, n_features, classes, n_classes, **kwargs):
        """
        Args:
            tree_parameters: The parameters defining the tree structure
            n_features: The number of features input to the model
            classes: The classes used for classification. None if implementing a regression model
            n_classes: The total number of used classes
        """
        super(AbstractPyTorchTreeImpl, self).__init__(logical_operator, **kwargs)

        # Set up the variables for the subclasses.
        # Each subclass will trigger different behaviours by properly setting these.
        self.perform_class_select = False
        self.binary_classification = False
        self.classes = classes
        self.base_prediction = None
        # Are we doing anomaly detection, regression or classification?
        if self.anomaly_detection:
            self.n_classes = 1  # so that we follow the regression pattern and later do manual class selection
            self.classes = torch.nn.Parameter(torch.IntTensor(classes), requires_grad=False)
        elif classes is None:
            self.regression = True
            self.n_classes = 1 if n_classes is None else n_classes
        else:
            self.classification = True
            self.n_classes = len(classes) if n_classes is None else n_classes
            if min(classes) != 0 or max(classes) != len(classes) - 1:
                self.classes = torch.nn.Parameter(torch.IntTensor(classes), requires_grad=False)
                self.perform_class_select = True


class GEMMTreeImpl(AbstractPyTorchTreeImpl):
    """
    Class implementing the GEMM strategy in PyTorch for tree-base models.
    """

    def __init__(self, logical_operator, tree_parameters, n_features, classes, n_classes=None, extra_config={}, **kwargs):
        """
        Args:
            tree_parameters: The parameters defining the tree structure
            n_features: The number of features input to the model
            classes: The classes used for classification. None if implementing a regression model
            n_classes: The total number of used classes
        """
        # If n_classes is not provided we induce it from tree parameters. Multioutput regression targets are also treated as separate classes.
        n_classes = n_classes if n_classes is not None else tree_parameters[0][0][2].shape[0]
        super(GEMMTreeImpl, self).__init__(logical_operator, tree_parameters, n_features, classes, n_classes, **kwargs)

        # Initialize the actual model.
        hidden_one_size = 0
        hidden_two_size = 0
        hidden_three_size = self.n_classes

        for weight, bias in tree_parameters:
            hidden_one_size = max(hidden_one_size, weight[0].shape[0])
            hidden_two_size = max(hidden_two_size, weight[1].shape[0])

        n_trees = len(tree_parameters)
        weight_1 = np.zeros((n_trees, hidden_one_size, n_features))
        bias_1 = np.zeros((n_trees, hidden_one_size))
        weight_2 = np.zeros((n_trees, hidden_two_size, hidden_one_size))
        bias_2 = np.zeros((n_trees, hidden_two_size))
        weight_3 = np.zeros((n_trees, hidden_three_size, hidden_two_size))

        for i, (weight, bias) in enumerate(tree_parameters):
            if len(weight[0]) > 0:
                weight_1[i, 0 : weight[0].shape[0], 0 : weight[0].shape[1]] = weight[0]
                bias_1[i, 0 : bias[0].shape[0]] = bias[0]
                weight_2[i, 0 : weight[1].shape[0], 0 : weight[1].shape[1]] = weight[1]
                bias_2[i, 0 : bias[1].shape[0]] = bias[1]
                weight_3[i, 0 : weight[2].shape[0], 0 : weight[2].shape[1]] = weight[2]

        self.n_trees = n_trees
        self.n_features = n_features
        self.hidden_one_size = hidden_one_size
        self.hidden_two_size = hidden_two_size
        self.hidden_three_size = hidden_three_size

        self.weight_1 = torch.nn.Parameter(torch.from_numpy(weight_1.reshape(-1, self.n_features).astype("float32")))
        self.bias_1 = torch.nn.Parameter(torch.from_numpy(bias_1.reshape(-1, 1).astype("float32")))

        self.weight_2 = torch.nn.Parameter(torch.from_numpy(weight_2.astype("float32")))
        self.bias_2 = torch.nn.Parameter(torch.from_numpy(bias_2.reshape(-1, 1).astype("float32")))

        self.weight_3 = torch.nn.Parameter(torch.from_numpy(weight_3.astype("float32")))

        # We register also base_prediction here so that tensor will be moved to the proper hardware with the model.
        # i.e., if cuda is selected, the parameter will be automatically moved on the GPU.
        if constants.BASE_PREDICTION in extra_config:
            self.base_prediction = extra_config[constants.BASE_PREDICTION]

    def aggregation(self, x):
        return x

    def forward(self, x):
        x = x.t()
        x = torch.mm(self.weight_1, x) < self.bias_1
        x = x.view(self.n_trees, self.hidden_one_size, -1)
        x = x.float()

        x = torch.matmul(self.weight_2, x)

        x = x.view(self.n_trees * self.hidden_two_size, -1) == self.bias_2
        x = x.view(self.n_trees, self.hidden_two_size, -1)
        x = x.float()

        x = torch.matmul(self.weight_3, x)
        x = x.view(self.n_trees, self.hidden_three_size, -1)

        x = self.aggregation(x)

        if self.regression:
            return x

        if self.anomaly_detection:
            # Select the class (-1 if negative) and return the score.
            return torch.where(x.view(-1) < 0, self.classes[0], self.classes[1]), x

        if self.perform_class_select:
            return torch.index_select(self.classes, 0, torch.argmax(x, dim=1)), x
        else:
            return torch.argmax(x, dim=1), x


class TreeTraversalTreeImpl(AbstractPyTorchTreeImpl):
    """
    Class implementing the Tree Traversal strategy in PyTorch for tree-base models.
    """

    def _expand_indexes(self, batch_size):
        indexes = self.nodes_offset
        indexes = indexes.expand(batch_size, self.num_trees)
        return indexes.reshape(-1)

    def __init__(
        self, logical_operator, tree_parameters, max_depth, n_features, classes, n_classes=None, extra_config={}, **kwargs
    ):
        """
        Args:
            tree_parameters: The parameters defining the tree structure
            max_depth: The maximum tree-depth in the model
            n_features: The number of features input to the model
            classes: The classes used for classification. None if implementing a regression model
            n_classes: The total number of used classes
            extra_config: Extra configuration used to properly implement the source tree
        """
        # If n_classes is not provided we induce it from tree parameters. Multioutput regression targets are also treated as separate classes.
        n_classes = n_classes if n_classes is not None else tree_parameters[0][6].shape[1]
        super(TreeTraversalTreeImpl, self).__init__(
            logical_operator, tree_parameters, n_features, classes, n_classes, **kwargs
        )

        # Initialize the actual model.
        self.n_features = n_features
        self.max_tree_depth = max_depth
        self.num_trees = len(tree_parameters)
        self.num_nodes = max([len(tree_parameter[1]) for tree_parameter in tree_parameters])

        lefts = np.zeros((self.num_trees, self.num_nodes), dtype=np.int64)
        rights = np.zeros((self.num_trees, self.num_nodes), dtype=np.int64)

        features = np.zeros((self.num_trees, self.num_nodes), dtype=np.int64)
        thresholds = np.zeros((self.num_trees, self.num_nodes), dtype=np.float32)
        values = np.zeros((self.num_trees, self.num_nodes, self.n_classes), dtype=np.float32)

        for i in range(self.num_trees):
            lefts[i][: len(tree_parameters[i][0])] = tree_parameters[i][2]
            rights[i][: len(tree_parameters[i][0])] = tree_parameters[i][3]
            features[i][: len(tree_parameters[i][0])] = tree_parameters[i][4]
            thresholds[i][: len(tree_parameters[i][0])] = tree_parameters[i][5]
            values[i][: len(tree_parameters[i][0])][:] = tree_parameters[i][6]

        self.lefts = torch.nn.Parameter(torch.from_numpy(lefts).view(-1), requires_grad=False)
        self.rights = torch.nn.Parameter(torch.from_numpy(rights).view(-1), requires_grad=False)

        self.features = torch.nn.Parameter(torch.from_numpy(features).view(-1), requires_grad=False)
        self.thresholds = torch.nn.Parameter(torch.from_numpy(thresholds).view(-1))
        self.values = torch.nn.Parameter(torch.from_numpy(values).view(-1, self.n_classes))

        nodes_offset = [[i * self.num_nodes for i in range(self.num_trees)]]
        self.nodes_offset = torch.nn.Parameter(torch.LongTensor(nodes_offset), requires_grad=False)

        # We register also base_prediction here so that tensor will be moved to the proper hardware with the model.
        # i.e., if cuda is selected, the parameter will be automatically moved on the GPU.
        if constants.BASE_PREDICTION in extra_config:
            self.base_prediction = extra_config[constants.BASE_PREDICTION]

    def aggregation(self, x):
        return x

    def forward(self, x):
        indexes = self._expand_indexes(x.size()[0])

        for _ in range(self.max_tree_depth):
            tree_nodes = indexes
            feature_nodes = torch.index_select(self.features, 0, tree_nodes).view(-1, self.num_trees)
            feature_values = torch.gather(x, 1, feature_nodes)

            thresholds = torch.index_select(self.thresholds, 0, indexes).view(-1, self.num_trees)
            lefts = torch.index_select(self.lefts, 0, indexes).view(-1, self.num_trees)
            rights = torch.index_select(self.rights, 0, indexes).view(-1, self.num_trees)

            indexes = torch.where(torch.ge(feature_values, thresholds), rights, lefts).long()
            indexes = indexes + self.nodes_offset
            indexes = indexes.view(-1)

        output = torch.index_select(self.values, 0, indexes).view(-1, self.num_trees, self.n_classes)

        output = self.aggregation(output)

        if self.regression:
            return output

        if self.anomaly_detection:
            # Select the class (-1 if negative) and return the score.
            return torch.where(output.view(-1) < 0, self.classes[0], self.classes[1]), output

        if self.perform_class_select:
            return torch.index_select(self.classes, 0, torch.argmax(output, dim=1)), output
        else:
            return torch.argmax(output, dim=1), output


class PerfectTreeTraversalTreeImpl(AbstractPyTorchTreeImpl):
    """
    Class implementing the Perfect Tree Traversal strategy in PyTorch for tree-base models.
    """

    def __init__(
        self, logical_operator, tree_parameters, max_depth, n_features, classes, n_classes=None, extra_config={}, **kwargs
    ):
        """
        Args:
            tree_parameters: The parameters defining the tree structure
            max_depth: The maximum tree-depth in the model
            n_features: The number of features input to the model
            classes: The classes used for classification. None if implementing a regression model
            n_classes: The total number of used classes
        """
        # If n_classes is not provided we induce it from tree parameters. Multioutput regression targets are also treated as separate classes.
        n_classes = n_classes if n_classes is not None else tree_parameters[0][6].shape[1]
        super(PerfectTreeTraversalTreeImpl, self).__init__(
            logical_operator, tree_parameters, n_features, classes, n_classes, **kwargs
        )

        # Initialize the actual model.
        self.max_tree_depth = max_depth
        self.num_trees = len(tree_parameters)
        self.n_features = n_features

        node_maps = [tp[0] for tp in tree_parameters]

        weight_0 = np.zeros((self.num_trees, 2 ** max_depth - 1))
        bias_0 = np.zeros((self.num_trees, 2 ** max_depth - 1))
        weight_1 = np.zeros((self.num_trees, 2 ** max_depth, self.n_classes))

        for i, node_map in enumerate(node_maps):
            self._get_weights_and_biases(node_map, max_depth, weight_0[i], weight_1[i], bias_0[i])

        node_by_levels = [set() for _ in range(max_depth)]
        self._traverse_by_level(node_by_levels, 0, -1, max_depth)

        self.root_nodes = torch.nn.Parameter(torch.from_numpy(weight_0[:, 0].flatten().astype("int64")), requires_grad=False)
        self.root_biases = torch.nn.Parameter(-1 * torch.from_numpy(bias_0[:, 0].astype("float32")), requires_grad=False)

        tree_indices = np.array([i for i in range(0, 2 * self.num_trees, 2)]).astype("int64")
        self.tree_indices = torch.nn.Parameter(torch.from_numpy(tree_indices), requires_grad=False)

        self.nodes = []
        self.biases = []
        for i in range(1, max_depth):
            nodes = torch.nn.Parameter(
                torch.from_numpy(weight_0[:, list(sorted(node_by_levels[i]))].flatten().astype("int64")), requires_grad=False
            )
            biases = torch.nn.Parameter(
                torch.from_numpy(-1 * bias_0[:, list(sorted(node_by_levels[i]))].flatten().astype("float32")),
                requires_grad=False,
            )
            self.nodes.append(nodes)
            self.biases.append(biases)

        self.nodes = torch.nn.ParameterList(self.nodes)
        self.biases = torch.nn.ParameterList(self.biases)

        self.leaf_nodes = torch.nn.Parameter(
            torch.from_numpy(weight_1.reshape((-1, self.n_classes)).astype("float32")), requires_grad=False
        )

        # We register also base_prediction here so that tensor will be moved to the proper hardware with the model.
        # i.e., if cuda is selected, the parameter will be automatically moved on the GPU.
        if constants.BASE_PREDICTION in extra_config:
            self.base_prediction = extra_config[constants.BASE_PREDICTION]

    def aggregation(self, x):
        return x

    def forward(self, x):
        prev_indices = (torch.ge(torch.index_select(x, 1, self.root_nodes), self.root_biases)).long()
        prev_indices = prev_indices + self.tree_indices
        prev_indices = prev_indices.view(-1)

        factor = 2
        for nodes, biases in zip(self.nodes, self.biases):
            gather_indices = torch.index_select(nodes, 0, prev_indices).view(-1, self.num_trees)
            features = torch.gather(x, 1, gather_indices).view(-1)
            prev_indices = factor * prev_indices + torch.ge(features, torch.index_select(biases, 0, prev_indices)).long()

        output = torch.index_select(self.leaf_nodes, 0, prev_indices).view(-1, self.num_trees, self.n_classes)

        output = self.aggregation(output)

        if self.regression:
            return output

        if self.anomaly_detection:
            # Select the class (-1 if negative) and return the score.
            return torch.where(output.view(-1) < 0, self.classes[0], self.classes[1]), output

        if self.perform_class_select:
            return torch.index_select(self.classes, 0, torch.argmax(output, dim=1)), output
        else:
            return torch.argmax(output, dim=1), output

    def _traverse_by_level(self, node_by_levels, node_id, current_level, max_level):
        current_level += 1
        if current_level == max_level:
            return node_id
        node_by_levels[current_level].add(node_id)
        node_id += 1
        node_id = self._traverse_by_level(node_by_levels, node_id, current_level, max_level)
        node_id = self._traverse_by_level(node_by_levels, node_id, current_level, max_level)
        return node_id

    def _get_weights_and_biases(self, nodes_map, tree_depth, weight_0, weight_1, bias_0):
        def depth_f_traversal(node, current_depth, node_id, leaf_start_id):
            weight_0[node_id] = node.feature
            bias_0[node_id] = -node.threshold
            current_depth += 1
            node_id += 1

            if node.left.feature == -1:
                node_id += 2 ** (tree_depth - current_depth - 1) - 1
                v = node.left.value
                weight_1[leaf_start_id : leaf_start_id + 2 ** (tree_depth - current_depth - 1)] = (
                    np.ones((2 ** (tree_depth - current_depth - 1), self.n_classes)) * v
                )
                leaf_start_id += 2 ** (tree_depth - current_depth - 1)
            else:
                node_id, leaf_start_id = depth_f_traversal(node.left, current_depth, node_id, leaf_start_id)

            if node.right.feature == -1:
                node_id += 2 ** (tree_depth - current_depth - 1) - 1
                v = node.right.value
                weight_1[leaf_start_id : leaf_start_id + 2 ** (tree_depth - current_depth - 1)] = (
                    np.ones((2 ** (tree_depth - current_depth - 1), self.n_classes)) * v
                )
                leaf_start_id += 2 ** (tree_depth - current_depth - 1)
            else:
                node_id, leaf_start_id = depth_f_traversal(node.right, current_depth, node_id, leaf_start_id)

            return node_id, leaf_start_id

        depth_f_traversal(nodes_map[0], -1, 0, 0)


# Desision \ ensemble tree implementations.
class GEMMDecisionTreeImpl(GEMMTreeImpl):
    """
    Class implementing the GEMM strategy in PyTorch for decision tree models.

    """

    def __init__(self, logical_operator, tree_parameters, n_features, classes=None):
        """
        Args:
            tree_parameters: The parameters defining the tree structure
            n_features: The number of features input to the model
            classes: The classes used for classification. None if implementing a regression model
        """
        super(GEMMDecisionTreeImpl, self).__init__(logical_operator, tree_parameters, n_features, classes)

    def aggregation(self, x):
        output = x.sum(0).t()

        return output


class TreeTraversalDecisionTreeImpl(TreeTraversalTreeImpl):
    """
    Class implementing the Tree Traversal strategy in PyTorch for decision tree models.
    """

    def __init__(self, logical_operator, tree_parameters, max_depth, n_features, classes=None, extra_config={}):
        """
        Args:
            tree_parameters: The parameters defining the tree structure
            max_depth: The maximum tree-depth in the model
            n_features: The number of features input to the model
            classes: The classes used for classification. None if implementing a regression model
            extra_config: Extra configuration used to properly implement the source tree
        """
        super(TreeTraversalDecisionTreeImpl, self).__init__(
            logical_operator, tree_parameters, max_depth, n_features, classes, extra_config=extra_config
        )

    def aggregation(self, x):
        output = x.sum(1)

        return output


class PerfectTreeTraversalDecisionTreeImpl(PerfectTreeTraversalTreeImpl):
    """
    Class implementing the Perfect Tree Traversal strategy in PyTorch for decision tree models.
    """

    def __init__(self, logical_operator, tree_parameters, max_depth, n_features, classes=None):
        """
        Args:
            tree_parameters: The parameters defining the tree structure
            max_depth: The maximum tree-depth in the model
            n_features: The number of features input to the model
            classes: The classes used for classification. None if implementing a regression model
        """
        super(PerfectTreeTraversalDecisionTreeImpl, self).__init__(
            logical_operator, tree_parameters, max_depth, n_features, classes
        )

    def aggregation(self, x):
        output = x.sum(1)

        return output


# GBDT implementations
class GEMMGBDTImpl(GEMMTreeImpl):
    """
    Class implementing the GEMM strategy (in PyTorch) for GBDT models.
    """

    def __init__(self, logical_operator, tree_parameters, n_features, classes=None, extra_config={}):
        """
        Args:
            tree_parameters: The parameters defining the tree structure
            n_features: The number of features input to the model
            classes: The classes used for classification. None if implementing a regression model
            extra_config: Extra configuration used to properly implement the source tree
        """
        super(GEMMGBDTImpl, self).__init__(logical_operator, tree_parameters, n_features, classes, 1, extra_config)

        self.n_gbdt_classes = 1
        self.post_transform = lambda x: x

        if constants.POST_TRANSFORM in extra_config:
            self.post_transform = extra_config[constants.POST_TRANSFORM]

        if classes is not None:
            self.n_gbdt_classes = len(classes) if len(classes) > 2 else 1

        self.n_trees_per_class = len(tree_parameters) // self.n_gbdt_classes

    def aggregation(self, x):
        output = torch.squeeze(x).t().view(-1, self.n_gbdt_classes, self.n_trees_per_class).sum(2)

        return self.post_transform(output)


class TreeTraversalGBDTImpl(TreeTraversalTreeImpl):
    """
    Class implementing the Tree Traversal strategy in PyTorch.
    """

    def __init__(self, logical_operator, tree_parameters, max_detph, n_features, classes=None, extra_config={}):
        """
        Args:
            tree_parameters: The parameters defining the tree structure
            max_depth: The maximum tree-depth in the model
            n_features: The number of features input to the model
            classes: The classes used for classification. None if implementing a regression model
            extra_config: Extra configuration used to properly implement the source tree
        """
        super(TreeTraversalGBDTImpl, self).__init__(
            logical_operator, tree_parameters, max_detph, n_features, classes, 1, extra_config
        )

        self.n_gbdt_classes = 1
        self.post_transform = lambda x: x

        if constants.POST_TRANSFORM in extra_config:
            self.post_transform = extra_config[constants.POST_TRANSFORM]

        if classes is not None:
            self.n_gbdt_classes = len(classes) if len(classes) > 2 else 1

        self.n_trees_per_class = len(tree_parameters) // self.n_gbdt_classes

    def aggregation(self, x):
        output = x.view(-1, self.n_gbdt_classes, self.n_trees_per_class).sum(2)

        return self.post_transform(output)


class PerfectTreeTraversalGBDTImpl(PerfectTreeTraversalTreeImpl):
    """
    Class implementing the Perfect Tree Traversal strategy in PyTorch.
    """

    def __init__(self, logical_operator, tree_parameters, max_depth, n_features, classes=None, extra_config={}):
        """
        Args:
            tree_parameters: The parameters defining the tree structure
            max_depth: The maximum tree-depth in the model
            n_features: The number of features input to the model
            classes: The classes used for classification. None if implementing a regression model
            extra_config: Extra configuration used to properly implement the source tree
        """
        super(PerfectTreeTraversalGBDTImpl, self).__init__(
            logical_operator, tree_parameters, max_depth, n_features, classes, 1, extra_config
        )

        self.n_gbdt_classes = 1
        self.post_transform = lambda x: x

        if constants.POST_TRANSFORM in extra_config:
            self.post_transform = extra_config[constants.POST_TRANSFORM]

        if classes is not None:
            self.n_gbdt_classes = len(classes) if len(classes) > 2 else 1

        self.n_trees_per_class = len(tree_parameters) // self.n_gbdt_classes

    def aggregation(self, x):
        output = x.view(-1, self.n_gbdt_classes, self.n_trees_per_class).sum(2)

        return self.post_transform(output)
