"""
PRE-02: Pipeline Eksperimen Prediksi Probabilitas Keterlambatan Proyek
Studi Kasus: Portofolio Modul Super ERP Farm Nation Enterprise (FNE) 2026

Script Mandiri (Standalone Scientific ML Pipeline):
- 100% Bebas Dependensi Eksternal yang Rentan Blokir DLL (Tidak bergantung pada C-extensions pandas/sklearn)
- Menggunakan built-in csv, math, random, serta numpy dan matplotlib (Agg backend)
- Mengimplementasikan 5 Skenario Eksperimen (sesuai Deskripsi_Penelitian.md & 01_Flow_dan_Skenario_Eksperimen.md):
  1. Logistic Regression (Baseline, L2 C=1.0, solver Newton-Raphson)
  2. Random Forest (Ensemble Tree predict_proba & Feature Importance)
  3. Gradient Boosting (Log-loss deviance, regression trees, subsample 0.8)
  4. Multi-Layer Perceptron (Neural Network 16-8, ReLU, Adam, Output Sigmoid)
  5. Kalibrasi Probabilitas (Platt Scaling & Isotonic Regression) + Threshold Analysis (Youden J) & EWS
"""

import os
import sys
import csv
import math
import random
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ============================================================
# 1. STRUKTUR DATA & UTILITIES
# ============================================================

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)

def sigmoid(z):
    z = np.clip(z, -30.0, 30.0)
    return 1.0 / (1.0 + np.exp(-z))

def logit(p, eps=1e-6):
    p = np.clip(p, eps, 1.0 - eps)
    return np.log(p / (1.0 - p))

def compute_roc_auc(y_true, y_prob):
    """Kalkulasi ROC-AUC dengan aturan trapesium; probabilitas yang sama (ties) diproses sebagai satu ambang batas"""
    y_true = np.array(y_true)
    y_prob = np.array(y_prob)
    n_pos = int(np.sum(y_true))
    n_neg = len(y_true) - n_pos
    if n_pos == 0 or n_neg == 0:
        return 0.5, [0.0, 1.0], [0.0, 1.0]

    tpr_list, fpr_list = [0.0], [0.0]
    for thresh in np.unique(y_prob)[::-1]:
        pred = y_prob >= thresh
        tpr_list.append(float(np.sum(pred & (y_true == 1))) / n_pos)
        fpr_list.append(float(np.sum(pred & (y_true == 0))) / n_neg)

    auc = 0.0
    for i in range(1, len(fpr_list)):
        width = fpr_list[i] - fpr_list[i - 1]
        avg_height = (tpr_list[i] + tpr_list[i - 1]) / 2.0
        auc += width * avg_height
    return auc, fpr_list, tpr_list

def compute_brier_score(y_true, y_prob):
    return float(np.mean((np.array(y_prob) - np.array(y_true)) ** 2))

def compute_log_loss(y_true, y_prob, eps=1e-15):
    y_prob = np.clip(y_prob, eps, 1.0 - eps)
    y_true = np.array(y_true)
    return float(-np.mean(y_true * np.log(y_prob) + (1.0 - y_true) * np.log(1.0 - y_prob)))

def compute_ece(y_true, y_prob, n_bins=5):
    """Menghitung Expected Calibration Error (ECE)"""
    y_prob = np.array(y_prob)
    y_true = np.array(y_true)
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    n = len(y_true)

    bin_confs, bin_accs = [], []
    for i in range(n_bins):
        mask = (y_prob >= bins[i]) & (y_prob < bins[i+1]) if i < n_bins - 1 else (y_prob >= bins[i]) & (y_prob <= bins[i+1])
        if np.any(mask):
            acc = float(np.mean(y_true[mask]))
            conf = float(np.mean(y_prob[mask]))
            weight = np.sum(mask) / n
            ece += weight * abs(acc - conf)
            bin_confs.append(conf)
            bin_accs.append(acc)
    return float(ece), bin_confs, bin_accs

def compute_classification_metrics(y_true, y_prob, threshold=0.5):
    """Confusion matrix, Precision, Recall (Sensitivity), Specificity, F1 pada ambang batas operasional"""
    y_true = np.array(y_true)
    pred_bin = (np.array(y_prob) >= threshold).astype(int)
    tp = int(np.sum((pred_bin == 1) & (y_true == 1)))
    fp = int(np.sum((pred_bin == 1) & (y_true == 0)))
    tn = int(np.sum((pred_bin == 0) & (y_true == 0)))
    fn = int(np.sum((pred_bin == 0) & (y_true == 1)))
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    f1 = 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
    acc = (tp + tn) / len(y_true)
    return {'Accuracy': acc, 'Precision': prec, 'Recall': rec, 'Specificity': spec, 'F1_Score': f1,
            'TP': tp, 'FP': fp, 'TN': tn, 'FN': fn}

def evaluate_probs(y_true, y_prob):
    auc, _, _ = compute_roc_auc(y_true, y_prob)
    ece, _, _ = compute_ece(y_true, y_prob, n_bins=5)
    metrics = {
        'ROC_AUC': auc,
        'Brier_Score': compute_brier_score(y_true, y_prob),
        'Log_Loss': compute_log_loss(y_true, y_prob),
        'ECE': ece,
    }
    metrics.update(compute_classification_metrics(y_true, y_prob))
    return metrics

def youden_threshold(y_true, y_prob):
    """Ambang batas optimal theta* = argmax J (Sensitivity + Specificity - 1); tie-break: terdekat ke 0.5.
    Kandidat ambang = titik tengah antar-probabilitas unik, sehingga theta* berada di tengah interval optimal."""
    y_true = np.array(y_true)
    y_prob = np.array(y_prob)
    uniq = np.unique(y_prob)
    candidates = np.concatenate([[uniq[0]], (uniq[:-1] + uniq[1:]) / 2.0])
    best = None
    for thresh in candidates:
        m = compute_classification_metrics(y_true, y_prob, threshold=thresh)
        j = m['Recall'] + m['Specificity'] - 1.0
        key = (round(j, 10), -abs(thresh - 0.5))
        if best is None or key > best[0]:
            best = (key, float(thresh), j, m['Recall'], m['Specificity'])
    _, thresh, j, sens, spec = best
    return thresh, j, sens, spec

# ============================================================
# 2. STANDARISASI & STRATIFIED K-FOLD
# ============================================================

class CustomStandardScaler:
    def fit(self, X):
        self.mean = np.mean(X, axis=0)
        self.std = np.std(X, axis=0)
        self.std[self.std == 0.0] = 1.0
        return self

    def transform(self, X):
        return (X - self.mean) / self.std

def stratified_k_fold(y, n_splits=5, seed=42):
    rng = random.Random(seed)
    pos_idx = [i for i, val in enumerate(y) if val == 1]
    neg_idx = [i for i, val in enumerate(y) if val == 0]

    rng.shuffle(pos_idx)
    rng.shuffle(neg_idx)

    pos_folds = [pos_idx[i::n_splits] for i in range(n_splits)]
    neg_folds = [neg_idx[i::n_splits] for i in range(n_splits)]

    folds = []
    for i in range(n_splits):
        test_idx = pos_folds[i] + neg_folds[i]
        train_idx = [j for j in range(len(y)) if j not in test_idx]
        folds.append((train_idx, test_idx))
    return folds

def stratified_train_test_split(y, test_size=0.2, seed=42):
    rng = random.Random(seed)
    pos_idx = [i for i, val in enumerate(y) if val == 1]
    neg_idx = [i for i, val in enumerate(y) if val == 0]
    rng.shuffle(pos_idx)
    rng.shuffle(neg_idx)
    n_pos_test = max(1, int(round(len(pos_idx) * test_size)))
    n_neg_test = max(1, int(round(len(neg_idx) * test_size)))
    test_idx = pos_idx[:n_pos_test] + neg_idx[:n_neg_test]
    train_idx = [j for j in range(len(y)) if j not in test_idx]
    return train_idx, test_idx

# ============================================================
# 3. IMPLEMENTASI ALGORITMA MACHINE LEARNING
# ============================================================

class CustomLogisticRegression:
    """Regresi logistik L2 (setara sklearn penalty='l2', C=1.0).
    Fungsi objektif konveks diminimalkan hingga konvergen dengan Newton-Raphson,
    sehingga solusi optimumnya identik dengan solver L-BFGS."""
    def __init__(self, C=1.0, max_iter=1000, tol=1e-8):
        self.C = C
        self.max_iter = max_iter
        self.tol = tol
        self.weights = None
        self.bias = 0.0

    def fit(self, X, y):
        n_samples, n_features = X.shape
        Xb = np.hstack([X, np.ones((n_samples, 1))])
        theta = np.zeros(n_features + 1)
        reg = np.eye(n_features + 1) / self.C
        reg[-1, -1] = 0.0  # bias tidak diregularisasi

        for _ in range(self.max_iter):
            p = sigmoid(Xb @ theta)
            grad = Xb.T @ (p - y) + reg @ theta
            hess = Xb.T @ (Xb * (p * (1.0 - p))[:, None]) + reg + 1e-10 * np.eye(n_features + 1)
            step = np.linalg.solve(hess, grad)
            theta -= step
            if np.max(np.abs(step)) < self.tol:
                break
        self.weights = theta[:-1]
        self.bias = theta[-1]
        return self

    def predict_proba(self, X):
        linear = np.dot(X, self.weights) + self.bias
        return sigmoid(linear)


class DecisionNode:
    def __init__(self, feature=None, threshold=None, left=None, right=None, prob=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.prob = prob

    @property
    def is_leaf(self):
        return self.prob is not None

class CustomDecisionTree:
    def __init__(self, max_depth=3, min_samples_split=2, max_features=None):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features
        self.root = None
        self.feature_importances_ = None

    def _gini(self, y):
        if len(y) == 0:
            return 0.0
        p = np.mean(y)
        return 1.0 - (p ** 2 + (1.0 - p) ** 2)

    def _best_split(self, X, y, feat_indices):
        best_gain = -1.0
        best_feat, best_thresh = None, None
        current_gini = self._gini(y)
        n = len(y)

        for feat in feat_indices:
            thresholds = np.unique(X[:, feat])
            for thresh in thresholds:
                left_mask = X[:, feat] <= thresh
                right_mask = ~left_mask
                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue

                gini_left = self._gini(y[left_mask])
                gini_right = self._gini(y[right_mask])
                weighted_gini = (np.sum(left_mask)/n) * gini_left + (np.sum(right_mask)/n) * gini_right
                gain = current_gini - weighted_gini

                if gain > best_gain:
                    best_gain = gain
                    best_feat = feat
                    best_thresh = thresh

        return best_feat, best_thresh, best_gain

    def _build_tree(self, X, y, depth=0):
        n_samples, n_features = X.shape
        if depth >= self.max_depth or n_samples < self.min_samples_split or len(np.unique(y)) == 1:
            leaf_prob = float(np.mean(y)) if len(y) > 0 else 0.5
            return DecisionNode(prob=leaf_prob)

        feat_pool = list(range(n_features))
        if self.max_features and self.max_features < n_features:
            feat_indices = random.sample(feat_pool, self.max_features)
        else:
            feat_indices = feat_pool

        best_feat, best_thresh, gain = self._best_split(X, y, feat_indices)
        if best_feat is None or gain <= 1e-6:
            return DecisionNode(prob=float(np.mean(y)))

        self.feature_importances_[best_feat] += gain * n_samples

        left_mask = X[:, best_feat] <= best_thresh
        right_mask = ~left_mask
        left_child = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_child = self._build_tree(X[right_mask], y[right_mask], depth + 1)
        return DecisionNode(feature=best_feat, threshold=best_thresh, left=left_child, right=right_child)

    def fit(self, X, y):
        self.feature_importances_ = np.zeros(X.shape[1])
        self.root = self._build_tree(X, y, depth=0)
        total_imp = np.sum(self.feature_importances_)
        if total_imp > 0:
            self.feature_importances_ /= total_imp
        return self

    def _predict_row(self, node, x):
        if node.is_leaf:
            return node.prob
        if x[node.feature] <= node.threshold:
            return self._predict_row(node.left, x)
        return self._predict_row(node.right, x)

    def predict_proba(self, X):
        return np.array([self._predict_row(self.root, row) for row in X])


class CustomRandomForest:
    def __init__(self, n_estimators=100, max_depth=3, seed=42):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.seed = seed
        self.trees = []
        self.feature_importances_ = None

    def fit(self, X, y):
        random.seed(self.seed)
        np.random.seed(self.seed)
        n_samples, n_features = X.shape
        max_feat = max(1, int(math.sqrt(n_features)))

        self.trees = []
        all_importances = np.zeros(n_features)

        for _ in range(self.n_estimators):
            # Bootstrap sampling
            boot_idx = np.random.choice(n_samples, size=n_samples, replace=True)
            X_b, y_b = X[boot_idx], y[boot_idx]

            tree = CustomDecisionTree(max_depth=self.max_depth, max_features=max_feat)
            tree.fit(X_b, y_b)
            self.trees.append(tree)
            all_importances += tree.feature_importances_

        total = np.sum(all_importances)
        self.feature_importances_ = all_importances / total if total > 0 else np.ones(n_features)/n_features
        return self

    def predict_proba(self, X):
        # Rata-rata probabilitas daun seluruh pohon (setara sklearn RandomForestClassifier.predict_proba)
        tree_preds = np.array([tree.predict_proba(X) for tree in self.trees])
        return np.mean(tree_preds, axis=0)


class CustomRegressionTree:
    """Pohon regresi (kriteria reduksi SSE) untuk pseudo-residual Gradient Boosting.
    Nilai daun memakai langkah Newton Friedman (2001): gamma = sum(r) / sum(p(1-p))."""
    def __init__(self, max_depth=2, min_samples_leaf=1):
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.root = None

    def _leaf(self, r, h):
        return DecisionNode(prob=float(np.sum(r) / (np.sum(h) + 1e-12)))

    def _build(self, X, r, h, depth):
        n = len(r)
        if depth >= self.max_depth or n < 2 * self.min_samples_leaf:
            return self._leaf(r, h)

        best_gain, best_feat, best_thresh = 1e-12, None, None
        total_sse = np.sum((r - np.mean(r)) ** 2)
        for feat in range(X.shape[1]):
            for thresh in np.unique(X[:, feat])[:-1]:
                left_mask = X[:, feat] <= thresh
                n_left = np.sum(left_mask)
                if n_left < self.min_samples_leaf or n - n_left < self.min_samples_leaf:
                    continue
                r_left, r_right = r[left_mask], r[~left_mask]
                sse = np.sum((r_left - r_left.mean()) ** 2) + np.sum((r_right - r_right.mean()) ** 2)
                gain = total_sse - sse
                if gain > best_gain:
                    best_gain, best_feat, best_thresh = gain, feat, thresh

        if best_feat is None:
            return self._leaf(r, h)
        left_mask = X[:, best_feat] <= best_thresh
        return DecisionNode(feature=best_feat, threshold=best_thresh,
                            left=self._build(X[left_mask], r[left_mask], h[left_mask], depth + 1),
                            right=self._build(X[~left_mask], r[~left_mask], h[~left_mask], depth + 1))

    def fit(self, X, r, h):
        self.root = self._build(X, r, h, 0)
        return self

    def _predict_row(self, node, x):
        if node.is_leaf:
            return node.prob
        if x[node.feature] <= node.threshold:
            return self._predict_row(node.left, x)
        return self._predict_row(node.right, x)

    def predict(self, X):
        return np.array([self._predict_row(self.root, row) for row in X])


class CustomGradientBoosting:
    """Gradient Tree Boosting dengan loss deviance (log-loss) biner dan stochastic subsampling baris."""
    def __init__(self, n_estimators=100, lr=0.05, max_depth=2, subsample=0.8, seed=42):
        self.n_estimators = n_estimators
        self.lr = lr
        self.max_depth = max_depth
        self.subsample = subsample
        self.seed = seed
        self.trees = []
        self.base_pred = 0.0

    def fit(self, X, y):
        rng = np.random.RandomState(self.seed)
        n_samples = len(y)
        p_mean = np.clip(np.mean(y), 1e-6, 1.0 - 1e-6)
        self.base_pred = math.log(p_mean / (1.0 - p_mean))

        F = np.full(n_samples, self.base_pred)
        self.trees = []
        n_sub = max(2, int(round(self.subsample * n_samples)))

        for _ in range(self.n_estimators):
            prob = sigmoid(F)
            residuals = y - prob            # gradien negatif log-loss
            hessian = prob * (1.0 - prob)

            idx = rng.choice(n_samples, size=n_sub, replace=False)
            tree = CustomRegressionTree(max_depth=self.max_depth).fit(X[idx], residuals[idx], hessian[idx])
            self.trees.append(tree)
            F += self.lr * tree.predict(X)
        return self

    def predict_proba(self, X):
        F = np.full(len(X), self.base_pred)
        for tree in self.trees:
            F += self.lr * tree.predict(X)
        return sigmoid(F)


class CustomMLP:
    """MLP 2 lapis tersembunyi (ReLU) + output sigmoid, dioptimasi Adam (full-batch),
    regularisasi L2 alpha seperti sklearn MLPClassifier."""
    def __init__(self, hidden=(16, 8), lr=0.01, alpha=0.01, max_iter=1000, seed=42):
        self.hidden = hidden
        self.lr = lr
        self.alpha = alpha
        self.max_iter = max_iter
        self.seed = seed
        self.params = None

    def _forward(self, X):
        w1, b1, w2, b2, w3, b3 = self.params
        z1 = X @ w1 + b1
        a1 = np.maximum(0.0, z1)
        z2 = a1 @ w2 + b2
        a2 = np.maximum(0.0, z2)
        return z1, a1, z2, a2, sigmoid(a2 @ w3 + b3)

    def fit(self, X, y):
        rng = np.random.RandomState(self.seed)
        n_samples, n_feat = X.shape
        h1, h2 = self.hidden

        # He initialization
        self.params = [
            rng.randn(n_feat, h1) * math.sqrt(2.0 / n_feat), np.zeros(h1),
            rng.randn(h1, h2) * math.sqrt(2.0 / h1), np.zeros(h2),
            rng.randn(h2) * math.sqrt(2.0 / h2), np.zeros(1),
        ]
        beta1, beta2, eps = 0.9, 0.999, 1e-8
        m = [np.zeros_like(p) for p in self.params]
        v = [np.zeros_like(p) for p in self.params]

        for t in range(1, self.max_iter + 1):
            w1, b1, w2, b2, w3, b3 = self.params
            z1, a1, z2, a2, a3 = self._forward(X)

            # Backpropagation
            dz3 = (a3 - y) / n_samples
            dw3 = a2.T @ dz3 + (self.alpha / n_samples) * w3
            db3 = np.array([np.sum(dz3)])
            dz2 = np.outer(dz3, w3) * (z2 > 0)
            dw2 = a1.T @ dz2 + (self.alpha / n_samples) * w2
            db2 = np.sum(dz2, axis=0)
            dz1 = (dz2 @ w2.T) * (z1 > 0)
            dw1 = X.T @ dz1 + (self.alpha / n_samples) * w1
            db1 = np.sum(dz1, axis=0)
            grads = [dw1, db1, dw2, db2, dw3, db3]

            # Adam update
            for i, g in enumerate(grads):
                m[i] = beta1 * m[i] + (1.0 - beta1) * g
                v[i] = beta2 * v[i] + (1.0 - beta2) * g ** 2
                m_hat = m[i] / (1.0 - beta1 ** t)
                v_hat = v[i] / (1.0 - beta2 ** t)
                self.params[i] = self.params[i] - self.lr * m_hat / (np.sqrt(v_hat) + eps)
        return self

    def predict_proba(self, X):
        return self._forward(X)[-1]

# ============================================================
# 4. KALIBRASI PROBABILITAS (SKENARIO 5)
# ============================================================

class PlattScaler:
    """Platt (1999): p_cal = 1 / (1 + exp(A f + B)), f = logit skor model,
    dengan target smoothing Platt untuk sampel kecil."""
    def fit(self, scores, y, max_iter=100):
        f = logit(scores)
        n_pos, n_neg = np.sum(y), len(y) - np.sum(y)
        t = np.where(y == 1, (n_pos + 1.0) / (n_pos + 2.0), 1.0 / (n_neg + 2.0))
        A, B = 0.0, math.log((n_neg + 1.0) / (n_pos + 1.0))
        for _ in range(max_iter):
            p = 1.0 / (1.0 + np.exp(np.clip(A * f + B, -30, 30)))
            # gradien & Hessian negative log-likelihood terhadap (A, B)
            d = t - p
            g = np.array([np.sum(d * f), np.sum(d)])
            w = p * (1.0 - p)
            H = np.array([[np.sum(w * f * f), np.sum(w * f)], [np.sum(w * f), np.sum(w)]]) + 1e-8 * np.eye(2)
            step = np.linalg.solve(H, g)
            A, B = A - step[0], B - step[1]
            if np.max(np.abs(step)) < 1e-10:
                break
        self.A, self.B = A, B
        return self

    def transform(self, scores):
        return 1.0 / (1.0 + np.exp(np.clip(self.A * logit(scores) + self.B, -30, 30)))


class IsotonicCalibrator:
    """Isotonic Regression via Pool Adjacent Violators (PAV), interpolasi linear antar-titik (seperti sklearn)."""
    def fit(self, scores, y):
        order = np.argsort(scores, kind='mergesort')
        xs, ys = np.array(scores)[order], np.array(y, dtype=float)[order]
        blocks = []  # [nilai, bobot, x_min, x_max]
        for xi, yi in zip(xs, ys):
            blocks.append([yi, 1.0, xi, xi])
            while len(blocks) > 1 and blocks[-2][0] >= blocks[-1][0]:
                v2, w2, lo2, hi2 = blocks.pop()
                v1, w1, lo1, hi1 = blocks.pop()
                blocks.append([(v1 * w1 + v2 * w2) / (w1 + w2), w1 + w2, lo1, hi2])
        self.x_knots, self.y_knots = [], []
        for v, _, lo, hi in blocks:
            self.x_knots += [lo, hi]
            self.y_knots += [v, v]
        return self

    def transform(self, scores):
        return np.clip(np.interp(scores, self.x_knots, self.y_knots), 0.0, 1.0)


class CalibratedModel:
    """Kalibrasi post-hoc tanpa kebocoran data: kalibrator dilatih pada prediksi out-of-fold
    (inner stratified 3-fold) dari fold training, lalu model dasar dilatih ulang pada seluruh fold training."""
    def __init__(self, base_ctor, method, inner_splits=3, seed=42):
        self.base_ctor = base_ctor
        self.method = method
        self.inner_splits = inner_splits
        self.seed = seed

    def fit(self, X, y):
        inner_scores = np.zeros(len(y))
        for tr, te in stratified_k_fold(y, n_splits=self.inner_splits, seed=self.seed):
            inner_scores[te] = self.base_ctor().fit(X[tr], y[tr]).predict_proba(X[te])
        self.calibrator = (PlattScaler() if self.method == 'Platt' else IsotonicCalibrator()).fit(inner_scores, y)
        self.base = self.base_ctor().fit(X, y)
        return self

    def predict_proba(self, X):
        return self.calibrator.transform(self.base.predict_proba(X))

# ============================================================
# 5. RUN PIPELINE EKSPERIMEN UTAMA
# ============================================================

EWS_LOW, EWS_HIGH = 0.35, 0.65
CALIBRATION_METHODS = ['Raw', 'Platt', 'Isotonic']

def ews_zone(p):
    if p < EWS_LOW:
        return "HIJAU (Low Risk)"
    if p < EWS_HIGH:
        return "KUNING (Watchlist)"
    return "MERAH (Critical Alert)"

def cv_predict(ctor, X_raw, y_raw, folds):
    """Prediksi out-of-fold dengan penskalaan terisolasi per fold"""
    oof_probs = np.zeros(len(y_raw))
    for train_idx, test_idx in folds:
        scaler = CustomStandardScaler().fit(X_raw[train_idx])
        model = ctor().fit(scaler.transform(X_raw[train_idx]), y_raw[train_idx])
        oof_probs[test_idx] = model.predict_proba(scaler.transform(X_raw[test_idx]))
    return oof_probs

def make_ctor(base_ctor, method):
    if method == 'Raw':
        return base_ctor
    return lambda: CalibratedModel(base_ctor, method)

def fmt_models(names):
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " dan " + names[-1]

def run_pipeline():
    set_seed(42)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(script_dir, "..", "dataset_pre02_fne.csv"),
        os.path.join(script_dir, "dataset_pre02_fne.csv"),
        os.path.abspath(os.path.join(script_dir, "..", "..", "MP-PRE-02-github", "dataset_pre02_fne.csv"))
    ]

    dataset_path = None
    for p in possible_paths:
        if os.path.exists(p):
            dataset_path = os.path.normpath(p)
            break

    if not dataset_path:
        print("[ERROR] File 'dataset_pre02_fne.csv' tidak ditemukan.")
        sys.exit(1)

    print(f"[INFO] Membaca dataset dari: {dataset_path}")

    rows = []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    feature_names = [
        'Planned_Duration_Days',
        'Planned_Effort_Hours',
        'Predecessor_Count',
        'Resource_Utilization_Rate',
        'Risk_Score',
        'SPI_Value',
        'Change_Request_Count'
    ]

    X_raw = np.array([[float(r[col]) for col in feature_names] for r in rows])
    y_raw = np.array([int(r['Status_Delay']) for r in rows])
    n_samples = len(y_raw)

    print(f"[INFO] Berhasil memuat {n_samples} baris task modul Super ERP FNE.")
    print(f"[INFO] Kelas Delay=1: {sum(y_raw)} ({sum(y_raw)/n_samples*100:.1f}%), Kelas Delay=0: {n_samples - sum(y_raw)} ({(n_samples-sum(y_raw))/n_samples*100:.1f}%)")

    # Output directory
    output_dir = os.path.join(script_dir, "hasil_eksperimen")
    os.makedirs(output_dir, exist_ok=True)

    # 5-Fold Cross Validation Folds
    folds = stratified_k_fold(y_raw, n_splits=5, seed=42)

    # Hyperparameter sesuai Matriks Hyperparameter (01_Flow_dan_Skenario_Eksperimen.md, Bagian 4.3)
    model_constructors = {
        'Logistic Regression (Baseline)': lambda: CustomLogisticRegression(C=1.0, max_iter=1000),
        'Random Forest': lambda: CustomRandomForest(n_estimators=100, max_depth=3, seed=42),
        'Gradient Boosting': lambda: CustomGradientBoosting(n_estimators=100, lr=0.05, max_depth=2, subsample=0.8, seed=42),
        'MLP Neural Network': lambda: CustomMLP(hidden=(16, 8), lr=0.01, alpha=0.01, max_iter=1000, seed=42)
    }
    model_names = list(model_constructors)

    results = []
    oof_predictions = {}  # key: (model, kalibrasi)

    print("\n" + "="*92)
    print(f"{'HASIL EVALUASI STRATIFIED 5-FOLD CROSS-VALIDATION (PRE-02)':^92}")
    print("="*92)
    print(f"{'Model':<30} | {'Kalibrasi':<9} | {'ROC-AUC':<7} | {'Brier':<6} | {'LogLoss':<7} | {'ECE':<6} | {'Akurasi':<7} | {'F1':<6}")
    print("-"*92)

    for name, base_ctor in model_constructors.items():
        for method in CALIBRATION_METHODS:
            oof_probs = cv_predict(make_ctor(base_ctor, method), X_raw, y_raw, folds)
            oof_predictions[(name, method)] = oof_probs
            m = evaluate_probs(y_raw, oof_probs)
            results.append({'Model': name, 'Kalibrasi': method, **m})
            print(f"{name:<30} | {method:<9} | {m['ROC_AUC']:.4f}  | {m['Brier_Score']:.4f} | {m['Log_Loss']:.4f}  | {m['ECE']:.4f} | {m['Accuracy']*100:5.1f}%  | {m['F1_Score']:.4f}")

    print("="*92)

    # 1. Simpan Tabel Metrik CSV
    metric_fields = ['Model', 'Kalibrasi', 'ROC_AUC', 'Brier_Score', 'Log_Loss', 'ECE', 'Accuracy',
                     'Precision', 'Recall', 'Specificity', 'F1_Score', 'TP', 'FP', 'TN', 'FN']
    metrics_csv = os.path.join(output_dir, "tabel_metrik_evaluasi.csv")
    with open(metrics_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=metric_fields)
        writer.writeheader()
        for r in results:
            writer.writerow(r)
    print(f"\n[INFO] Tabel metrik tersimpan di: {metrics_csv}")

    # Rekomendasi model dengan kalibrasi terbaik (Deskripsi_Penelitian.md, Eksperimen Kelima):
    # Brier Score terendah, tie-break ECE lalu Log Loss
    best = min(results, key=lambda r: (round(r['Brier_Score'], 6), round(r['ECE'], 6), r['Log_Loss']))
    best_key = (best['Model'], best['Kalibrasi'])
    best_label = f"{best['Model']} + {best['Kalibrasi']}" if best['Kalibrasi'] != 'Raw' else f"{best['Model']} (tanpa kalibrasi)"
    best_probs = oof_predictions[best_key]
    print(f"[INFO] Model rekomendasi (Brier terendah): {best_label}")

    # 2. Kurva ROC Comparison Plot (output mentah; kalibrasi monoton tidak mengubah urutan skor)
    plt.figure(figsize=(8, 6))
    colors = ['#1E4220', '#2B6CB0', '#E8A33D', '#B83280']
    for idx, name in enumerate(model_names):
        fpr, tpr = compute_roc_auc(y_raw, oof_predictions[(name, 'Raw')])[1:]
        auc_val = next(r['ROC_AUC'] for r in results if r['Model'] == name and r['Kalibrasi'] == 'Raw')
        plt.plot(fpr, tpr, color=colors[idx % len(colors)], lw=2.2, label=f"{name} (AUC = {auc_val:.3f})")
    plt.plot([0, 1], [0, 1], 'k--', lw=1.5, label='Random Chance (AUC = 0.500)')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (1 - Specificity)', fontsize=11)
    plt.ylabel('True Positive Rate (Sensitivity)', fontsize=11)
    plt.title('Kurva ROC Perbandingan 4 Algoritma PRE-02', fontsize=12, fontweight='bold')
    plt.legend(loc='lower right', fontsize=9.5)
    plt.grid(True, linestyle=':', alpha=0.6)
    roc_plot = os.path.join(output_dir, "kurva_roc_perbandingan.png")
    plt.savefig(roc_plot, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[INFO] Plot Kurva ROC tersimpan di: {roc_plot}")

    # 3. Calibration Curves (Reliability Diagram): kiri = 4 model mentah, kanan = Raw vs Platt vs Isotonic model rekomendasi
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    for idx, name in enumerate(model_names):
        _, bin_confs, bin_accs = compute_ece(y_raw, oof_predictions[(name, 'Raw')], n_bins=5)
        axes[0].plot(bin_confs, bin_accs, marker='o', lw=2, color=colors[idx % len(colors)], label=name)
    for idx, method in enumerate(CALIBRATION_METHODS):
        probs = oof_predictions[(best['Model'], method)]
        ece_val, bin_confs, bin_accs = compute_ece(y_raw, probs, n_bins=5)
        axes[1].plot(bin_confs, bin_accs, marker='o', lw=2, color=['#1E4220', '#E8A33D', '#4A7C59'][idx], label=f"{method} (ECE = {ece_val:.3f})")
    for ax, title in zip(axes, ['Output Mentah 4 Algoritma', f"Efek Kalibrasi: {best['Model']}"]):
        ax.plot([0, 1], [0, 1], 'k--', lw=1.5, label='Perfect Calibration')
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('Mean Predicted Probability', fontsize=11)
        ax.set_ylabel('Empirical Fraction of Delays', fontsize=11)
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.legend(loc='upper left', fontsize=9)
        ax.grid(True, linestyle=':', alpha=0.6)
    fig.suptitle('Diagram Reliabilitas (Calibration Curves) PRE-02, 5 bin', fontsize=12, fontweight='bold')
    cal_plot = os.path.join(output_dir, "kurva_kalibrasi_probabilitas.png")
    fig.savefig(cal_plot, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[INFO] Plot Kalibrasi tersimpan di: {cal_plot}")

    # 4. Feature Importance dari Random Forest (Full Dataset)
    scaler_full = CustomStandardScaler().fit(X_raw)
    X_full_scaled = scaler_full.transform(X_raw)
    rf_full = CustomRandomForest(n_estimators=100, max_depth=3, seed=42).fit(X_full_scaled, y_raw)

    fi = rf_full.feature_importances_
    sorted_idx = np.argsort(fi)
    top_features = [feature_names[i] for i in sorted_idx[::-1][:2]]

    plt.figure(figsize=(9, 5))
    y_pos = np.arange(len(sorted_idx))
    plt.barh(y_pos, fi[sorted_idx], height=0.55, color='#2C5F2D', edgecolor='#1E4220')
    plt.yticks(y_pos, [feature_names[i] for i in sorted_idx], fontsize=10)
    plt.xlabel('Relative Feature Importance (MDI Gini Reduction)', fontsize=11)
    plt.title('Feature Importance Pemicu Keterlambatan Modul Super ERP FNE', fontsize=12, fontweight='bold')
    plt.grid(True, axis='x', linestyle=':', alpha=0.6)
    fi_plot = os.path.join(output_dir, "feature_importance_comparison.png")
    plt.savefig(fi_plot, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[INFO] Plot Feature Importance tersimpan di: {fi_plot}")

    fi_csv = os.path.join(output_dir, "tabel_feature_importance.csv")
    with open(fi_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Feature', 'Importance_MDI'])
        for i in sorted_idx[::-1]:
            writer.writerow([feature_names[i], f"{fi[i]:.4f}"])
    print(f"[INFO] Tabel Feature Importance tersimpan di: {fi_csv}")

    # 5. Threshold Analysis (Youden J) & Tabel Prediksi Probabilitas per Aktivitas & Zonasi EWS
    theta, j_stat, sens, spec = youden_threshold(y_raw, best_probs)
    print(f"[INFO] Youden theta* = {theta:.4f} (J = {j_stat:.3f}, Sensitivity = {sens:.3f}, Specificity = {spec:.3f})")

    task_csv = os.path.join(output_dir, "tabel_prediksi_probabilitas_task.csv")
    zones = [ews_zone(p) for p in best_probs]
    with open(task_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Task_ID', 'Sub_Project', 'Task_Name', 'Status_Delay_Aktual',
                      'P_Delay_Logistic_Regression', 'P_Delay_Random_Forest',
                      'P_Delay_Gradient_Boosting', 'P_Delay_MLP', 'P_Delay_Rekomendasi', 'EWS_Risk_Zone']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i, r in enumerate(rows):
            writer.writerow({
                'Task_ID': r['Task_ID'],
                'Sub_Project': r['Sub_Project'],
                'Task_Name': r['Task_Name'],
                'Status_Delay_Aktual': r['Status_Delay'],
                'P_Delay_Logistic_Regression': f"{oof_predictions[('Logistic Regression (Baseline)', 'Raw')][i]:.4f}",
                'P_Delay_Random_Forest': f"{oof_predictions[('Random Forest', 'Raw')][i]:.4f}",
                'P_Delay_Gradient_Boosting': f"{oof_predictions[('Gradient Boosting', 'Raw')][i]:.4f}",
                'P_Delay_MLP': f"{oof_predictions[('MLP Neural Network', 'Raw')][i]:.4f}",
                'P_Delay_Rekomendasi': f"{best_probs[i]:.4f}",
                'EWS_Risk_Zone': zones[i]
            })
    print(f"[INFO] Tabel Prediksi Probabilitas per Task tersimpan di: {task_csv}")

    zone_counts = {}
    for z, y in zip(zones, y_raw):
        key = z.split()[0]
        zone_counts.setdefault(key, [0, 0])[int(y)] += 1  # [tepat waktu, delay]
    n_delay = int(np.sum(y_raw))
    red_hit, red_false = zone_counts.get('MERAH', [0, 0])[1], zone_counts.get('MERAH', [0, 0])[0]
    yellow_delay, yellow_ok = zone_counts.get('KUNING', [0, 0])[1], zone_counts.get('KUNING', [0, 0])[0]
    green_miss = zone_counts.get('HIJAU', [0, 0])[1]

    # 6. Validasi pembanding: Hold-out Stratified Train-Test Split 80:20 (01_Flow Bagian 4.2)
    tr_idx, te_idx = stratified_train_test_split(y_raw, test_size=0.2, seed=42)
    holdout_results = []
    for name, base_ctor in model_constructors.items():
        for method in CALIBRATION_METHODS:
            scaler = CustomStandardScaler().fit(X_raw[tr_idx])
            model = make_ctor(base_ctor, method)().fit(scaler.transform(X_raw[tr_idx]), y_raw[tr_idx])
            probs = model.predict_proba(scaler.transform(X_raw[te_idx]))
            holdout_results.append({'Model': name, 'Kalibrasi': method, **evaluate_probs(y_raw[te_idx], probs)})
    holdout_csv = os.path.join(output_dir, "tabel_metrik_holdout_80_20.csv")
    with open(holdout_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=metric_fields)
        writer.writeheader()
        for r in holdout_results:
            writer.writerow(r)
    print(f"[INFO] Tabel metrik hold-out 80:20 (n_test = {len(te_idx)}) tersimpan di: {holdout_csv}")

    # 7. Ringkasan Temuan Ilmiah (Markdown Report), seluruh kalimat diturunkan dari hasil di atas
    raw_results = [r for r in results if r['Kalibrasi'] == 'Raw']
    max_auc = max(r['ROC_AUC'] for r in raw_results)
    top_auc = [r['Model'] for r in raw_results if abs(r['ROC_AUC'] - max_auc) < 1e-9]
    min_auc = min(raw_results, key=lambda r: r['ROC_AUC'])
    best_raw = min(raw_results, key=lambda r: r['Brier_Score'])
    get = lambda name, method: next(r for r in results if r['Model'] == name and r['Kalibrasi'] == method)

    summary_md = os.path.join(output_dir, "00_RINGKASAN_TEMUAN_EKSPERIMEN.md")
    with open(summary_md, 'w', encoding='utf-8') as f:
        f.write("# RINGKASAN TEMUAN EKSPERIMEN PRE-02\n")
        f.write("## Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas\n\n")
        f.write("> Dokumen ini digenerate otomatis oleh `experiment_pipeline.py`; seluruh angka dan kalimat temuan diturunkan langsung dari hasil eksperimen.\n\n")
        f.write(f"**Dataset:** N = {n_samples} task ({n_delay} Delay : {n_samples - n_delay} On-Time). "
                "**Protokol:** Stratified 5-Fold Cross-Validation, seed 42, standardisasi per fold, "
                "kalibrasi dilatih pada inner 3-fold di dalam fold training.\n\n")
        f.write("### 1. Tabel Kinerja Evaluasi 5-Fold Cross-Validation\n\n")
        f.write("| Model Algoritma | Kalibrasi | ROC-AUC | Brier Score | Log Loss | ECE | Akurasi | Recall | Specificity | F1-Score |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
        for r in results:
            mark = "**" if (r['Model'], r['Kalibrasi']) == best_key else ""
            f.write(f"| {mark}{r['Model']}{mark} | {r['Kalibrasi']} | {r['ROC_AUC']:.4f} | {r['Brier_Score']:.4f} | {r['Log_Loss']:.4f} | {r['ECE']:.4f} | "
                    f"{r['Accuracy']*100:.1f}% | {r['Recall']:.3f} | {r['Specificity']:.3f} | {r['F1_Score']:.4f} |\n")
        f.write("\n*Metrik klasifikasi (Akurasi, Recall, Specificity, F1) dihitung pada ambang batas 0.5. Baris tebal = model rekomendasi.*\n")

        f.write("\n### 2. Temuan Kunci\n\n")
        f.write(f"1. **Kekuatan Diskriminasi (ROC-AUC, output mentah):** ROC-AUC tertinggi dicapai oleh {fmt_models(top_auc)} "
                f"({max_auc:.4f}); terendah {min_auc['Model']} ({min_auc['ROC_AUC']:.4f}).\n")
        f.write(f"2. **Kualitas Probabilitas sebelum kalibrasi:** Brier Score terendah dimiliki {best_raw['Model']} "
                f"(Brier = {best_raw['Brier_Score']:.4f}, ECE = {best_raw['ECE']:.4f}).\n")
        f.write("3. **Efek Kalibrasi (Brier Score Raw → Platt → Isotonic):**\n")
        for name in model_names:
            b = [get(name, m)['Brier_Score'] for m in CALIBRATION_METHODS]
            f.write(f"   - {name}: {b[0]:.4f} → {b[1]:.4f} → {b[2]:.4f}\n")
        f.write(f"4. **Rekomendasi model dengan kalibrasi terbaik:** {best_label} "
                f"(Brier = {best['Brier_Score']:.4f}, ECE = {best['ECE']:.4f}, Log Loss = {best['Log_Loss']:.4f}, ROC-AUC = {best['ROC_AUC']:.4f}).\n")
        f.write(f"5. **Prediktor Dominan (Feature Importance RF, MDI):** dua fitur dengan bobot tertinggi adalah "
                f"`{top_features[0]}` ({fi[feature_names.index(top_features[0])]:.3f}) dan `{top_features[1]}` ({fi[feature_names.index(top_features[1])]:.3f}).\n")
        f.write(f"6. **Threshold Analysis (Youden J):** pada model rekomendasi, ambang optimal θ* = {theta:.4f} "
                f"(J = {j_stat:.3f}; Sensitivity = {sens:.3f}; Specificity = {spec:.3f}).\n")
        f.write(f"7. **Early Warning System (Hijau < {EWS_LOW}, Kuning {EWS_LOW}–{EWS_HIGH}, Merah ≥ {EWS_HIGH}), model rekomendasi:** "
                f"zona Merah menangkap {red_hit} dari {n_delay} modul yang aktual terlambat dengan {red_false} alarm palsu; "
                f"zona Kuning berisi {yellow_delay} modul terlambat dan {yellow_ok} modul tepat waktu; "
                f"{green_miss} modul terlambat lolos ke zona Hijau.\n")

        f.write("\n### 3. Validasi Pembanding: Hold-out Stratified 80:20\n\n")
        f.write(f"n_train = {len(tr_idx)}, n_test = {len(te_idx)}. Karena data uji hanya {len(te_idx)} task, hasil ini bersifat indikatif dan "
                "tidak dipakai untuk pemilihan model (detail: `tabel_metrik_holdout_80_20.csv`).\n\n")
        f.write("| Model Algoritma | Kalibrasi | ROC-AUC | Brier Score | Akurasi |\n| :--- | :---: | :---: | :---: | :---: |\n")
        for r in holdout_results:
            f.write(f"| {r['Model']} | {r['Kalibrasi']} | {r['ROC_AUC']:.4f} | {r['Brier_Score']:.4f} | {r['Accuracy']*100:.1f}% |\n")

        f.write("\n### 4. Catatan Keterbatasan\n\n")
        f.write(f"- Ukuran sampel sangat kecil (N = {n_samples}); tiap fold uji hanya berisi ±{n_samples // 5} task, sehingga metrik memiliki varians tinggi.\n")
        if max_auc >= 0.99:
            f.write(f"- ROC-AUC ≈ {max_auc:.2f} menunjukkan kelas hampir terpisah sempurna pada data empiris-simulatif ini; "
                    "hasil perlu divalidasi pada data proyek riil sebelum digeneralisasi.\n")
        f.write("- Kalibrator dilatih pada ±20 sampel per fold; Isotonic Regression rawan overfitting pada ukuran ini, sehingga Platt Scaling lebih stabil secara teoretis (Niculescu-Mizil & Caruana, 2005).\n")
        f.write("- Pemilihan model rekomendasi dan θ* dilakukan pada prediksi out-of-fold yang sama dengan yang dilaporkan, sehingga estimasi kinerjanya sedikit optimistis.\n")

    print(f"[INFO] Dokumen Ringkasan Temuan tersimpan di: {summary_md}")
    print("\n[SUCCESS] Seluruh pipeline eksperimen PRE-02 berhasil dijalankan.")

if __name__ == "__main__":
    run_pipeline()
