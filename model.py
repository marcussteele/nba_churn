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
    return thresh,pred


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
    
    
