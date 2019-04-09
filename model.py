from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import f1_score,confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier
from cleaning import *
from import_data import *
import datetime
from sklearn.model_selection import train_test_split

def seperate_this_year(df,this_year):
    df_this_year = df[df['Year']==this_year]
    df_this_year.drop('Churn',axis=1,inplace=True)
    df_before = df[df['Year']!=this_year]
    df_this_year.to_pickle('this_year.p')
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

def get_preds(probs,y_test):
    thresh = get_threshold(probs,y_test)
    pred = (probs > thresh).astype(int)
    return pred

def model_zero_fit(X0_train,y0_train):
    '''
    Fits model for cluster 0.
    INPUT: X_train and y_train
    OUTPUT: Trained model
    '''
    model = GradientBoostingClassifier(learning_rate=0.1,max_depth=12,max_features='sqrt',n_estimators=250,subsample=0.75)
    model.fit(X0_train,y0_train)
    return model

def model_one_fit(X1_train,y1_train):
    '''
    Fits model for cluster 1.
    INPUT: X_train and y_train
    OUTPUT: Trained model
    '''
    model1 = GradientBoostingClassifier(learning_rate=0.005,max_depth=2,max_features='sqrt',n_estimators=20,subsample=0.75)
    model1.fit(X1_train,y1_train)
    return model1
def model_two_fit(X2_train,y2_train):
    '''
    Fits model for cluster 2.
    INPUT: X_train and y_train
    OUTPUT: Trained model
    '''
    model2 = GradientBoostingClassifier(learning_rate=0.005,max_depth=15,max_features='sqrt',n_estimators=250,subsample=0.75)
    model2.fit(X2_train,y2_train)
    return model2

if __name__ == '__main__':
    now = datetime.datetime.now()
    this_year = now.year
    this_year
    salary = get_data('data/salary.p')
    stats = get_data('data/stats.p')
    free_agents = get_data('data/free_agents.p')
    add_features(stats)
    data = combine_data(salary,stats,free_agents)
    final_data = cleaning(data)
    dummies_data = pd.get_dummies(final_data,columns=['Type','Pos.'],drop_first=True)
    final_data1,fa_this_year = seperate_this_year(dummies_data,this_year)
    X = final_data1.drop(['Churn'],axis=1)
    y = final_data1['Churn']
    X_1, x_val, y_1, y_val = train_test_split(X,y,test_size=0.1)
    nba_reduced,labels = scale_and_split(X_1,y_1)
    group0, y0 = split_groups(X_1,y_1,labels,0)
    X0_train, X0_test, y0_train, y0_test = train_test_split(group0,y0)
    group1, y1 = split_groups(X_1,y_1,labels,1)
    X1_train, X1_test, y1_train, y1_test = train_test_split(group1,y1)
    group2, y2 = split_groups(X_1,y_1,labels,2)
    X2_train, X2_test, y2_train, y2_test = train_test_split(group2,y2)
    model = model_zero_fit(X0_train,y0_train)
    model1 = model_one_fit(X1_train,y1_train)
    model2 = model_two_fit(X2_train,y2_train)
    probs = model.predict_proba(X0_test)
    probs1 = model1.predict_proba(X1_test)
    probs2 = model2.predict_proba(X2_test)
    preds = get_preds(probs,y0_test)
    preds1 = get_preds(probs1,y1_test)
    preds2 = get_preds(probs2,y2_test)
