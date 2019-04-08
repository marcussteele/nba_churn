from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import f1_score,confusion_matrix

def seperate_this_year(df,this_year):
    df_this_year = df[df['Year']==this_year]
    df_this_year.drop('Churn',axis=1,inplace=True)
    df_before = df[df['Year']!=this_year]
    return df_before, df_this_year

def scale_and_split(X,y):
    scaler = StandardScaler()
    X1 = scaler.fit_transform(X)
    pca = PCA(n_components=3).fit(X1)
    reduced = pca.transform(X1)
    km = KMeans(n_clusters=3)
    km.fit(reduced)
    labels = km.predict(reduced)
    return reduced,labels

def split_groups(X,y,labels,group_num):
    features = X[labels==group_num]
    targets = y[labels==group_num]
    return features, targets

def get_threshold(prob,y_test):
    score = []
    thresholds = []
    sorted_prob = sorted(prob)
    for thresh in sorted_prob:
        predicted_label = prob > thresh
        score.append(f1_score(y_test.values,predicted_label))
        thresholds.append(thresh)
    max_score = max(score)
    max_index = score.index(max_score)
    final_thresh = thresholds[max_index]
    return final_thresh

def get_preds_and_f1(probs,y_test):
    thresh = get_threshold(probs,y_test)
    pred = (probs > thresh).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test,pred).ravel()
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * (precision * recall)/(precision+recall)
    return pred,f1