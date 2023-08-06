import matplotlib.pyplot as plt

# ----------------------------------------------------------

def plot_ma(df,range=[2,5]):
    
    """
    Util to create and plot Mov Avg against Closing prices.
    
    Args:
        df (pd.DataFrame): Pandas dataframe with 1. Closing price column labelled as 'Close' 2. Datetime Index.
        range (list, optional): Pass two int values in list to calc moving avg. Defaults to [2,5].
    """
    df[f'MA_{range[0]}'] = df['Close'].rolling(range[0]).mean()
    df[f'MA_{range[1]}'] = df['Close'].rolling(range[1]).mean()
    df.dropna(inplace=True)

    plt.figure(figsize=[40,10])
    plt.grid(True)
    plt.plot(df['Close'],label='data')
    plt.plot(df[f'MA_{range[0]}'],label=f'MA {range[0]}')
    plt.plot(df[f'MA_{range[1]}'],label=f'MA {range[1]}')
    plt.legend(loc=2)

    return

# ----------------------------------------------------------