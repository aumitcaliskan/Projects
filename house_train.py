import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import joblib
from sklearn import tree, pipeline, preprocessing, compose, linear_model, impute, model_selection, ensemble, svm, metrics

df = pd.read_csv("data/training.csv")
df.info()

# dropping columns

df.drop(['Alley','FireplaceQu','PoolQC','Fence','MiscFeature'], axis=1, inplace=True)

# pre transformer

df.select_dtypes(include=['object']).columns
categorical_columns = ['MSZoning', 'Street', 'LotShape', 'LandContour', 'Utilities',
       'LotConfig', 'LandSlope', 'Neighborhood', 'Condition1', 'Condition2',
       'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl', 'Exterior1st',
       'Exterior2nd', 'MasVnrType', 'ExterQual', 'ExterCond', 'Foundation',
       'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2',
       'Heating', 'HeatingQC', 'CentralAir', 'Electrical', 'KitchenQual',
       'Functional', 'GarageType', 'GarageFinish', 'GarageQual', 'GarageCond',
       'PavedDrive', 'SaleType', 'SaleCondition']

df.select_dtypes(include=['int64','float']).columns
numerical_columns = ['Id', 'MSSubClass', 'LotFrontage', 'LotArea', 'OverallQual',
       'OverallCond', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea', 'BsmtFinSF1',
       'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF',
       'LowQualFinSF', 'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath',
       'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd',
       'Fireplaces', 'GarageYrBlt', 'GarageCars', 'GarageArea', 'WoodDeckSF',
       'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea',
       'MiscVal', 'MoSold', 'YrSold']

def make_pipeline():

    categorical = impute.SimpleImputer(strategy='most_frequent')
    coder = preprocessing.OneHotEncoder(sparse=False,handle_unknown='ignore')

    kategorici = pipeline.Pipeline(
        [
            ('impute', categorical),
            ('encode', coder)
            ]
    )

    numerical = impute.KNNImputer()

    numerikci = pipeline.Pipeline(
        [
            ('impute', numerical),
            ('scale', preprocessing.StandardScaler())

            ]
    )
    transformer = compose.ColumnTransformer([
        ("num", numerikci, numerical_columns),
        ("cat", kategorici, categorical_columns)
    ])

    rfg_model = ensemble.RandomForestRegressor()

    grid = model_selection.GridSearchCV(
        rfg_model,
        param_grid={
            'n_estimators': [1,100,500],
            'n_jobs': [-1]
        },
        cv=10,
        return_train_score=True
    )

    p = pipeline.Pipeline([
        ('pre', transformer),
        ('model', grid)    
    ])
    return p

def main():
    df = pd.read_csv(sys.argv[1])
    X = df.drop('SalePrice', axis=1)
    y = df['SalePrice']
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2, random_state=101)
    yol = make_pipeline()
    print(pd.DataFrame(grid.cv_results_))
    yol.fit(X_train,y_train)
    joblib.dump(yol, "data/a3_pipeline.joblib")
    sys.exit(0)

if __name__ == '___main___':
    main()



