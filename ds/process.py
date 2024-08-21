import pandas as pd

df = pd.read_csv("./pre-model_data_final.csv")


def convert_string_to_list(array_str : str) -> list[float]:

    print(array_str)
    array_str = array_str.replace("[", "")
    array_str = array_str.replace("]", "")
    array_str = array_str.split(", ")
    return list(map(float, array_str))

df['embedding'] = df.apply(lambda row: convert_string_to_list(row['embedding']), axis=1 )


print(type(df['embedding'][100]))





