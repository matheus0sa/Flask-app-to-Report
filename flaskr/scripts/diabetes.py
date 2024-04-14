def R():
    import os
    import pandas as pd
    from sklearn.datasets import load_diabetes

    diabetes = load_diabetes()
    data = diabetes.data
    target = diabetes.target
    feature_names = diabetes.feature_names

    df = pd.DataFrame(data=data, columns=feature_names)
    df['target'] = target
    return df