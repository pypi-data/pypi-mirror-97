import numpy as np


class MeanMetric:

    def __init__(self):
        self.acc = 0
        self.it = 0

    def __call__(self, value):
        self.acc += value
        self.it += 1

    def reset(self):
        self.acc = 0
        self.it = 0

    def result(self):
        return self.acc / self.it


class ConfusionMatrix:

    def __init__(self, num_classes, tags=None):
        self.num_classes = num_classes
        self.tags = tags if tags is not None else ['class_%d' % i for i in range(num_classes)]
        self.cm = np.zeros((self.num_classes, self.num_classes), dtype=int)

    def reset(self):
        self.cm = np.zeros((self.num_classes, self.num_classes), dtype=int)

    def update(self, gt_labels, pred_labels):
        np.add.at(self.cm, (gt_labels, pred_labels), 1)

    def get_normalized(self):

        scm = np.sum(self.cm, axis=1).astype(float)
        scm[scm == 0] = 1e-08  # avoid division by zero
        norm_conf_mat = self.cm / scm[:, None]
        norm_conf_mat[np.isnan(norm_conf_mat)] = 0
        return norm_conf_mat

    def plot(self, title='Confusion Matrix', normalized=True, to_file=None):
        import matplotlib.pyplot as plt
        import seaborn as sns

        if normalized:
            cm = self.get_normalized()
        else:
            cm = self.cm

        fmt = 'd' if np.issubdtype(cm.dtype, np.integer) else '.3f'
        plt.figure(figsize=(15, 15))
        sns.set(font_scale=1.5)
        ax = sns.heatmap(cm, annot=True, xticklabels=self.tags, yticklabels=self.tags, fmt=fmt, cmap='Blues', square=True, cbar=False)
        ax.set(xlabel='PREDICTED', ylabel='GROUND TRUTH')
        plt.title(title)
        plt.tight_layout()
        if to_file is None:
            plt.show()
        else:
            plt.savefig(to_file)

        return ax


class ConfusionMatrixTopK(ConfusionMatrix):

    def __init__(self, num_classes, k, tags=None):
        super().__init__(num_classes=num_classes, tags=tags)
        self.k = k

    def update(self, gt_labels, pred_probs):
        topk = np.argsort(-pred_probs, axis=1)[:, 0:self.k]

        correct_mask = np.any((topk - gt_labels[:, None]) == 0, axis=1)
        np.add.at(self.cm, (gt_labels[correct_mask], gt_labels[correct_mask]), 1)

        error_mask = ~correct_mask
        np.add.at(self.cm, (gt_labels[error_mask], topk[error_mask, 0]), 1)
