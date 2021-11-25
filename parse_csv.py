import pandas as pd

def prepare_data(fn: str) -> pd.DataFrame:
    data = pd.read_csv(fn, encoding='latin-1')

    for col in 'Largest_Contentful_Paint', 'First_Contentful_Paint',\
         'Speed_Index', 'Total_Blocking_Time', 'Time_to_Interactive', 'Dom_Size':
        data[col] = data[col].map(lambda x: float(str(x).split()[0].replace(',', '')))
    
    return data


def write_csv(output: str, df: pd.DataFrame, mode: str) -> None: 
    df.to_csv(output, index=False, header=(mode=='w'), mode=mode, encoding='latin-1')

if __name__ == '__main__':
    df1 = prepare_data('output1.csv')
    df2 = prepare_data('output2.csv')
    write_csv('output1_prepared.csv', df1, 'w')
    write_csv('output2_prepared.csv', df2, 'w')
