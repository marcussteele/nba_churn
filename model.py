from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import f1_score, confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier
from cleaning import *
from import_data import *
import datetime
from sklearn.model_selection import train_test_split

def seperate_this_year(df):
    '''
    INPUT: DataFrame
    Seperates data from this year. Used for when you don't have complete data
    for the current year.
    OUTPUT: DataFrame of all data excluding this year, DataFrame of all data for current year
    '''
    now = datetime.datetime.now()
    this_year = now.year
    this_year
    df_this_year = df[df['Year']==this_year]
    df_this_year.drop('Churn',axis=1,inplace=True)
    df_before = df[df['Year']!=this_year]
    df_this_year.to_pickle('this_year.p')
    return df_before, df_this_year

def get_threshold(prob, y_test):
    '''
    INPUT: array of probabilities, actual target values
    Finds the optimal probability.
    OUTPUT: threshold that maximizes f1 score
    '''
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

def get_preds(probs, y_test):
    '''
    INPUT: array of probabilities, actual target values

    OUTPUT: threshold, predicted values
    '''
    thresh = get_threshold(probs,y_test)
    pred = (probs > thresh).astype(int)
    return thresh,pred

def predict(X_train, y_train, X_test, y_test, testing=True):
    gbc = GradientBoostingClassifier(learning_rate=0.05,max_depth=10,max_features='sqrt',n_estimators=75,subsample=0.75)
    if testing == True:
        gbc.fit(X_train,y_train)
        probs = gbc.predict_proba(X_train)[:, 1]
        thresh,preds = get_preds(probs,y_train)
        f_score = f1_score(y_test,preds)
        accur = sum(preds==y_test)/len(y_test)
        print('Tesing Scores')
        print('F1 Score: ' + str(f_score))
        print('Accuracy: ' + str(accur))
    elif testing == False:
        gbc.fit(X_train,y_train)
        probs = gbc.predict_proba(X_train)[:, 1]
        thresh,preds = get_preds(probs,y_train)
        f_score = f1_score(y_test,preds)
        accur = sum(preds==y_test)/len(y_test)
        print('Trainging Scores')
        print('F1 Score: ' + str(f_score))
        print('Accuracy: ' + str(accur))
    return gbc, thresh

if __name__ == '__main__':
    now = datetime.datetime.now()
    this_year = now.year
    salary = get_data('data/salary.p')
    stats = get_data('data/stats.p')
    free_agents = get_data('data/free_agents.p')
    add_features(stats)
    data = combine_data(salary,stats,free_agents)
    final_data = cleaning(data)
    dummies_data = pd.get_dummies(final_data,columns=['Type','Pos.'],drop_first=True)
    final_data1,fa_this_year = seperate_this_year(dummies_data)
    X = final_data1.drop(['Churn','Tm','Year','Salary'],axis=1)
    y = final_data1['Churn']
    X_1, x_val, y_1, y_val = train_test_split(X,y,test_size=0.1)
    X_train, X_test, y_train, y_test = train_test_split(X_1,y_1)
    gbc,thresh = predict(X_train,y_train,X_test,y_test)
    _,thresh_train = predict(X_train,y_train,X_test,y_test,testing=False)
    # X_this = fa_this_year.drop(['Churn','Year','Salary','Tm'],axis=1)
    # this_year_probs = gbc.predict_proba(X_this)
    # this_year_preds = (this_year_probs[:,1]>thresh).astype(int)
    # this_year_final = pd.concat([pd.Series(fa_this_year.index),pd.Series(this_year_probs[:,1]),pd.Series(this_year_preds)],axis=1)
    # this_year_final.rename({0:'Player',1:'Probability',2:'Prediction'},axis=1,inplace=True)
    # this_year_final.set_index('Player',inplace=True)
    # players_staying = this_year_final[this_year_final['Prediction']==0]
    # players_staying.sort_values('Probability',ascending=False)
    # players_leaving = this_year_final[this_year_final['Prediction']==1]
    # players_leaving[:50].sort_values('Probability',ascending=False)