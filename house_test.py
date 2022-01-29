import numpy as np
import pandas as pd
import joblib
import sys

OUTPUT_PATH = 'output/predictions.csv'

def main():
    df = pd.read_csv(sys.argv[1])
    X = df.drop('SalePrice', axis=1)
    model = joblib.load('a3_pipeline.joblib')
    print(model)
    y = model.predict(X)
    df['SalePrice'] = y
    df = df[['Id','SalePrice']]
    df.to_csv(OUTPUT_PATH, index=False)
    sys.exit(0)

if __name__ == '___main___':
    main()

