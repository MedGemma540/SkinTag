"""Evaluation metrics for robustness assessment."""

import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


def compute_accuracy(y_true, y_pred):
    """Compute overall accuracy."""
    return accuracy_score(y_true, y_pred)


def compute_per_group_accuracy(y_true, y_pred, groups):
    """Compute accuracy per demographic/condition group.

    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        groups: Group assignment for each sample

    Returns:
        Dictionary mapping group -> accuracy
    """
    unique_groups = np.unique(groups)
    group_acc = {}
    for group in unique_groups:
        mask = groups == group
        group_acc[group] = accuracy_score(y_true[mask], y_pred[mask])
    return group_acc


def compute_fairness_gap(group_accuracies: dict):
    """Compute max accuracy gap between groups."""
    accuracies = list(group_accuracies.values())
    return max(accuracies) - min(accuracies)


def robustness_report(y_true, y_pred, groups=None, class_names=None):
    """Generate full robustness evaluation report."""
    report = {
        "overall_accuracy": compute_accuracy(y_true, y_pred),
        "classification_report": classification_report(y_true, y_pred, target_names=class_names),
        "confusion_matrix": confusion_matrix(y_true, y_pred),
    }

    if groups is not None:
        group_acc = compute_per_group_accuracy(y_true, y_pred, groups)
        report["per_group_accuracy"] = group_acc
        report["fairness_gap"] = compute_fairness_gap(group_acc)

    return report
