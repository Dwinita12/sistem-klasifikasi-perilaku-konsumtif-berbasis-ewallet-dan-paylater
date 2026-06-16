import pandas as pd
import numpy as np
from collections import Counter
import os

os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

from graphviz import Digraph


# =====================================================
# NODE CLASS
# =====================================================
class Node:

    def __init__(
        self,
        feature=None,
        children=None,
        label=None,
        gain_ratio=0
    ):

        self.feature = feature
        self.children = children or {}
        self.label = label
        self.gain_ratio = gain_ratio


# =====================================================
# ENTROPY
# =====================================================
def entropy(y):

    total = len(y)

    if total == 0:
        return 0

    counts = Counter(y)

    ent = 0

    for count in counts.values():

        p = count / total

        if p > 0:

            ent -= (
                p *
                np.log2(p)
            )

    return ent


# =====================================================
# INFORMATION GAIN
# =====================================================
def information_gain(
    data,
    feature,
    target
):

    total_entropy = entropy(
        data[target]
    )

    values = data[
        feature
    ].unique()

    weighted_entropy = 0

    for value in values:

        subset = data[
            data[feature] == value
        ]

        weight = (
            len(subset) /
            len(data)
        )

        weighted_entropy += (
            weight *
            entropy(
                subset[target]
            )
        )

    gain = (
        total_entropy -
        weighted_entropy
    )

    return gain


# =====================================================
# SPLIT INFO
# =====================================================
def split_info(
    data,
    feature
):

    total = len(data)

    value_counts = (
        data[feature]
        .value_counts()
    )

    split = 0

    for count in value_counts:

        p = count / total

        if p > 0:

            split -= (
                p *
                np.log2(p)
            )

    return split


# =====================================================
# GAIN RATIO
# =====================================================
def gain_ratio(
    data,
    feature,
    target
):

    gain = information_gain(
        data,
        feature,
        target
    )

    split = split_info(
        data,
        feature
    )

    if split == 0:
        return 0

    return gain / split
    # =====================================================
# CARI FITUR TERBAIK
# =====================================================
def best_feature(
    data,
    features,
    target
):

    best_attr = None

    best_ratio = -1

    detail_gain = []

    for feature in features:

        ratio = gain_ratio(
            data,
            feature,
            target
        )

        gain = information_gain(
            data,
            feature,
            target
        )

        split = split_info(
            data,
            feature
        )

        detail_gain.append({
            "feature": feature,
            "gain": round(
                gain,
                6
            ),
            "split_info": round(
                split,
                6
            ),
            "gain_ratio": round(
                ratio,
                6
            )
        })

        if ratio > best_ratio:

            best_ratio = ratio
            best_attr = feature

    detail_gain = sorted(
        detail_gain,
        key=lambda x:
        x["gain_ratio"],
        reverse=True
    )

    return (
        best_attr,
        best_ratio,
        detail_gain
    )


# =====================================================
# CEK APAKAH SEMUA KELAS SAMA
# =====================================================
def pure_class(
    data,
    target
):

    return (
        len(
            data[target]
            .unique()
        ) == 1
    )


# =====================================================
# MAJORITY CLASS
# =====================================================
def majority_class(
    data,
    target
):

    return (
        data[target]
        .value_counts()
        .idxmax()
    )
    # =====================================================
# BUILD TREE C4.5
# =====================================================
def build_tree(
    data,
    features,
    target,
    depth=0
):

    # semua data dalam node sama
    if pure_class(
        data,
        target
    ):

        return Node(
            label=data[target]
            .iloc[0]
        )

    # fitur habis
    if len(features) == 0:

        return Node(
            label=majority_class(
                data,
                target
            )
        )

    # cari gain ratio tertinggi
    best_attr, best_ratio, _ = (
        best_feature(
            data,
            features,
            target
        )
    )

    # gagal cari atribut
    if best_attr is None:

        return Node(
            label=majority_class(
                data,
                target
            )
        )

    # buat node baru
    node = Node(
        feature=best_attr,
        gain_ratio=best_ratio
    )

    # nilai unik atribut
    values = sorted(
        data[best_attr]
        .unique()
    )

    # fitur sisa
    remaining_features = [
        f
        for f in features
        if f != best_attr
    ]

    # buat cabang
    for value in values:

        subset = data[
            data[best_attr] == value
        ]

        # jika kosong
        if len(subset) == 0:

            node.children[value] = (
                Node(
                    label=majority_class(
                        data,
                        target
                    )
                )
            )

        else:

            child = build_tree(
                subset,
                remaining_features,
                target,
                depth + 1
            )

            node.children[value] = child

    return node
    # =====================================================
# PREDICT SATU DATA
# =====================================================
def predict(
    node,
    sample
):

    # leaf node
    if node.label is not None:
        return node.label

    feature = node.feature

    value = sample.get(
        feature
    )

    # debu
    # print(
    #     "Feature =",
    #     feature,
    #     "| Value =",
    #     value,
    #     "| Children =",
    #     list(node.children.keys())
    # )

    # jika cabang tidak ditemukan
    if value not in node.children:

        # print(
        #     "CABANG TIDAK DITEMUKAN :",
        #     feature,
        #     "=",
        #     value
        # )

        semua_label = []

        def ambil_label(child):

            if child.label is not None:

                semua_label.append(
                    child.label
                )

            else:

                for c in child.children.values():

                    ambil_label(c)

        for child in node.children.values():

            ambil_label(child)

        if semua_label:

            return Counter(
                semua_label
            ).most_common(1)[0][0]

        # fallback
        return 2

    return predict(
        node.children[value],
        sample
    )

# =====================================================
# PREDICT BANYAK DATA
# =====================================================
def predict_batch(
    node,
    X
):

    hasil = []

    for _, row in (
        X.iterrows()
    ):

        prediksi = predict(
            node,
            row.to_dict()
        )

        hasil.append(
            prediksi
        )

    return hasil


# =====================================================
# HITUNG AKURASI
# =====================================================
def accuracy(
    y_true,
    y_pred
):

    benar = 0

    total = len(
        y_true
    )

    for a, b in zip(
        y_true,
        y_pred
    ):

        if a == b:

            benar += 1

    if total == 0:
        return 0

    return round(
        (benar / total) * 100,
        2
    )
    # =====================================================
# GENERATE RULES IF THEN
# =====================================================
def generate_rules(
    node,
    current_rule="",
    rules=None
):

    if rules is None:
        rules = []

    # leaf
    if node.label is not None:

        rules.append(
            f"IF {current_rule} THEN Status = {node.label}"
        )

        return rules

    for value, child in (
        node.children.items()
    ):

        kondisi = (
            f"{node.feature} = {value}"
        )

        if current_rule == "":

            new_rule = kondisi

        else:

            new_rule = (
                current_rule
                +
                " AND "
                +
                kondisi
            )

        generate_rules(
            child,
            new_rule,
            rules
        )

    return rules


# =====================================================
# POHON KE TEKS
# =====================================================
def tree_to_text(
    node,
    level=0
):

    hasil = ""

    indent = "|   " * level

    if node.label is not None:

        hasil += (
            indent
            +
            "=> "
            +
            str(node.label)
            +
            "\n"
        )

        return hasil

    hasil += (
        indent
        +
        "["
        +
        str(node.feature)
        +
        "]"
        +
        "\n"
    )

    for value, child in (
        node.children.items()
    ):

        hasil += (
            indent
            +
            f"|-- {value}\n"
        )

        hasil += tree_to_text(
            child,
            level + 1
        )

    return hasil


# =====================================================
# NODE DETAIL
# =====================================================
def collect_node_details(
    data,
    features,
    target,
    node_id=0,
    results=None
):

    if results is None:
        results = []

    if pure_class(
        data,
        target
    ):

        results.append({
            "node_id": node_id,
            "feature": "-",
            "entropy": round(
                entropy(
                    data[target]
                ),
                6
            ),
            "gain": "-",
            "split_info": "-",
            "gain_ratio": "-",
            "samples": len(data),
            "label": str(
                data[target]
                .iloc[0]
            )
        })

        return results

    if len(features) == 0:

        results.append({
            "node_id": node_id,
            "feature": "-",
            "entropy": round(
                entropy(
                    data[target]
                ),
                6
            ),
            "gain": "-",
            "split_info": "-",
            "gain_ratio": "-",
            "samples": len(data),
            "label": str(
                majority_class(
                    data,
                    target
                )
            )
        })

        return results

    best_attr = None
    best_gain = -1
    best_split = -1
    best_ratio = -1

    for feature in features:

        gain = information_gain(
            data,
            feature,
            target
        )

        split = split_info(
            data,
            feature
        )

        ratio = gain_ratio(
            data,
            feature,
            target
        )

        if ratio > best_ratio:

            best_attr = feature
            best_gain = gain
            best_split = split
            best_ratio = ratio

    results.append({
        "node_id": node_id,
        "feature": best_attr,
        "entropy": round(
            entropy(
                data[target]
            ),
            6
        ),
        "gain": round(
            best_gain,
            6
        ),
        "split_info": round(
            best_split,
            6
        ),
        "gain_ratio": round(
            best_ratio,
            6
        ),
        "samples": len(data),
        "label": "-"
    })

    next_id = node_id + 1

    values = data[
        best_attr
    ].unique()

    remaining_features = [
        f
        for f in features
        if f != best_attr
    ]

    for value in values:

        subset = data[
            data[best_attr] == value
        ]

        collect_node_details(
            subset,
            remaining_features,
            target,
            next_id,
            results
        )

        next_id += 1

    return results
    # =====================================================
# CONFUSION MATRIX MANUAL
# =====================================================
def confusion_matrix_manual(
    y_true,
    y_pred
):

    classes = sorted(
        list(
            set(y_true)
        )
    )

    matrix = []

    for actual in classes:

        row = []

        for predicted in classes:

            total = 0

            for yt, yp in zip(
                y_true,
                y_pred
            ):

                if (
                    yt == actual
                    and
                    yp == predicted
                ):

                    total += 1

            row.append(total)

        matrix.append(row)

    return matrix


# =====================================================
# CLASSIFICATION REPORT
# =====================================================
def classification_report_manual(
    y_true,
    y_pred
):

    classes = sorted(
        list(
            set(y_true)
        )
    )

    report = {}

    for cls in classes:

        tp = 0
        fp = 0
        fn = 0

        for yt, yp in zip(
            y_true,
            y_pred
        ):

            if yt == cls and yp == cls:
                tp += 1

            elif yt != cls and yp == cls:
                fp += 1

            elif yt == cls and yp != cls:
                fn += 1

        precision = (
            tp / (tp + fp)
            if (tp + fp) > 0
            else 0
        )

        recall = (
            tp / (tp + fn)
            if (tp + fn) > 0
            else 0
        )

        f1 = (
            (
                2 *
                precision *
                recall
            )
            /
            (
                precision +
                recall
            )
            if (
                precision +
                recall
            ) > 0
            else 0
        )

        report[str(cls)] = {

            "precision":
                round(
                    precision,
                    4
                ),

            "recall":
                round(
                    recall,
                    4
                ),

            "f1-score":
                round(
                    f1,
                    4
                ),

            "support":
                int(
                    sum(
                        1
                        for y
                        in y_true
                        if y == cls
                    )
                )
        }

    return report


# =====================================================
# DISTRIBUSI LABEL
# =====================================================
def distribusi_kelas(
    y
):

    hasil = {}

    for kelas in sorted(
        list(
            set(y)
        )
    ):

        hasil[str(kelas)] = int(
            sum(
                1
                for v in y
                if v == kelas
            )
        )

    return hasil

    # =====================================================
# HITUNG TOTAL NODE
# =====================================================
def count_nodes(node):

    if node is None:
        return 0

    total = 1

    for child in node.children.values():
        total += count_nodes(child)

    return total


# =====================================================
# HITUNG LEAF NODE
# =====================================================
def count_leaf_nodes(node):

    if node.label is not None:
        return 1

    total = 0

    for child in node.children.values():
        total += count_leaf_nodes(child)

    return total


# =====================================================
# HITUNG DEPTH TREE
# =====================================================
def tree_depth(node):

    if node.label is not None:
        return 0

    return 1 + max(
        tree_depth(child)
        for child in node.children.values()
    )


# =====================================================
# SUMMARY TREE
# =====================================================
def tree_summary(tree):

    return {

        "total_nodes":
            count_nodes(tree),

        "leaf_nodes":
            count_leaf_nodes(tree),

        "max_depth":
            tree_depth(tree)
    }
    from graphviz import Digraph

def export_tree_graph(node):

    dot = Digraph(
        comment="Decision Tree C4.5",
        format="png"
    )

    def add_node(node, parent=None, edge_label=""):

        node_id = str(id(node))

        if node.label is not None:

            dot.node(
                node_id,
                f"Status={node.label}",
                shape="box"
            )

        else:

            dot.node(
                node_id,
                node.feature,
                shape="ellipse"
            )

        if parent is not None:

            dot.edge(
                parent,
                node_id,
                label=str(edge_label)
            )

        for value, child in node.children.items():

            add_node(
                child,
                node_id,
                value
            )

    add_node(node)

    return dot