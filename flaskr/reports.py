def iris():
    import os
    import pandas as pd
    from sklearn import datasets

    iris = datasets.load_iris()
    iris.keys()
    data = iris.data
    target = iris.target
    feature_names = iris.feature_names

    df = pd.DataFrame(data=data, columns=feature_names)
    df['target'] = target
    return df