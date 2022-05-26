import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score,
                             confusion_matrix)
from sklearn.metrics import precision_recall_fscore_support as score

LOGO_MATCHING_THRESHOLD = 0.87

def add_label(df, label):
    df['label'] = [label for _ in range(len(df))]
    return df

def calc_stat(df_all):
    y_pred = df_all['phish'].to_numpy()
    y_true = df_all['label'].to_numpy()
    
    acc = accuracy_score(y_true, y_pred)
    prec, recall, fscore, _ = score(y_true, y_pred, average='binary', zero_division=0)

    print("Acc: {:.6f} | Prec: {:.6f} | Recall: {:.6f} | Micro-F1: {:.6f}".format(acc, prec, recall, fscore))

    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm[0, 0], cm[0, 1], cm[1, 0], cm[1, 1]
    # print(tn, fn, fp, tp)
    print(cm)
    tpr = tp / (tp + fn)
    fpr = fp / (fp + tn)
    print("ROC Stat | FPR: {:.6f} | TPR: {:6f}".format(fpr, tpr))
    # disp = ConfusionMatrixDisplay(cm)
    # disp.plot()
    # plt.show()

df_benign = pd.read_csv("./test_benign1.txt", sep="\t", encoding='ISO-8859-1')[['folder', 'url', 'phish']]
print(df_benign)
df_crp_phishing = pd.read_csv("./test_crp_phishing.txt", sep="\t", encoding='ISO-8859-1')[['folder', 'url', 'phish']]

df_benign = add_label(df_benign, 0)
df_crp_phishing = add_label(df_crp_phishing, 1)

df_all = pd.concat([df_benign, df_crp_phishing])

calc_stat(df_all)
