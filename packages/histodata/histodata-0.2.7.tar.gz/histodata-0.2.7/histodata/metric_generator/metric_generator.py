from typing import Dict
from typing import Optional as O
from typing import Sequence
from typing import Union as U

import sklearn
import sklearn.metrics
import torch


def pretty_print_confusion_matrix(cm):
    print(" Confusion Matrix ".center(26, "="))
    print("       " + "Actual Value".center(8 * len(cm), " "))
    for idx, row in enumerate(cm):
        if idx == 0:
            print("Pred.  ", end="")
        elif idx == 1:
            print("Value  ", end="")
        else:
            print("       ", end="")
        for _, element in enumerate(row):
            print(str(element).center(8, " "), end="")
        print()


class MetricGenerator:
    def __init__(
        self,
        num_of_labels: int = 2,
        *,
        return_accuracy: bool = True,
        return_details_for_classes: O[U[int, Sequence[int]]] = None,
        print_confusion_matrix: bool = False,
        return_recall: bool = False,
        return_precission: bool = False,
        return_f1: bool = False,
        return_roc: bool = False,
        # return_frocs=None,  # NotImplemented
        pre_name: O[str] = None,
    ) -> None:

        self.num_of_labels = num_of_labels
        self.return_accuracy = return_accuracy
        if isinstance(return_details_for_classes, list):
            self.return_details_for_classes = return_details_for_classes
        else:
            self.return_details_for_classes = []
        self.print_confusion_matrix = print_confusion_matrix
        self.return_recall = return_recall
        self.return_precission = return_precission
        self.return_f1 = return_f1
        self.return_roc = return_roc

        # if isinstance(return_frocs, list):
        #     self.return_frocs = return_frocs
        # else:
        #     self.return_frocs = []

        if pre_name == "":
            self.pre_name = None
        else:
            self.pre_name = pre_name

    def create_metric(self, predictions: torch.Tensor, labels: torch.Tensor) -> Dict[str, float]:
        pred = predictions.argmax(dim=1, keepdim=True)
        pred_eq = pred.eq(labels.view_as(pred))

        # the metric to return
        m = {}

        m["cross_entropy_loss"] = torch.nn.functional.cross_entropy(predictions, labels).item()

        if self.return_accuracy:
            m["accuracy"] = pred_eq.sum().item() / len(labels)

            for lbl in range(self.num_of_labels):
                if len(labels[labels == lbl]) > 0:
                    m[f"accuracy_c{lbl}"] = pred_eq[labels == lbl].sum().item() / len(
                        labels[labels == lbl]
                    )

        if self.print_confusion_matrix:
            cm = sklearn.metrics.confusion_matrix(pred, labels)
            pretty_print_confusion_matrix(cm)

        for lbl in self.return_details_for_classes:
            tp = torch.sum(pred_eq[labels == lbl]).item()
            fn = torch.sum(~pred_eq[labels == lbl]).item()
            # tn = torch.sum(pred[labels != lbl] != lbl).item()
            fp = torch.sum(pred[labels != lbl] == lbl).item()

            precision = None
            if (tp + fp) > 0:
                precision = tp / (tp + fp)
                if self.return_precission:
                    m[f"precision_c{lbl}"] = precision

            recall = None
            if (tp + fn) > 0:
                recall = tp / (tp + fn)
                if self.return_recall:
                    m[f"recall_c{lbl}"] = recall

            if self.return_f1 and precision is not None and recall is not None and m[f"precision_c{lbl}"] + m[f"recall_c{lbl}"] > 0.0:
                m[f"F1_c{lbl}"] = (2.0 * m[f"precision_c{lbl}"] * m[f"recall_c{lbl}"]) / (
                    m[f"precision_c{lbl}"] + m[f"recall_c{lbl}"]
                )

            if self.return_roc:
                # calculate the fpr and tpr for all thresholds of the classification
                fpr, tpr, _ = sklearn.metrics.roc_curve(labels == lbl, predictions[:, lbl])
                m[f"roc_auc_c{lbl}"] = sklearn.metrics.auc(fpr, tpr)

        if self.pre_name is not None:
            return {self.pre_name + e: m[e] for e in m}
        else:
            return m
