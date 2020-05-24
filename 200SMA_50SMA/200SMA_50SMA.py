import pandas as pd


def model1():

    # Part 1 - get the data
    df = pd.read_csv(
        './EUR_USD.csv')
    df.columns = df.columns.str.strip()

    # Part 2 - Calculate inputs that go into the model like 200sma and 50sma
    df['% change'] = df['Close'].pct_change()
    df['200 sma'] = df['Close'].rolling(window=200).mean().round(5)
    df['50 sma'] = df['Close'].rolling(window=50).mean().round(5)

    # Part 3 - Models' criteria
    df['Criteria 1'] = df['Close'] >= df['200 sma']
    df['Criteria 2'] = (df['50 sma'] >= df['200 sma']
                        ) | df['Criteria 1'] == True

    # Part 4 - Calculate the models
    df['Buy and hold'] = 100*(1+df['% change']).cumprod()
    df['200 sma model'] = 100 * \
        (1+df['Criteria 1'].shift(1)*df['% change']).cumprod()
    df['200 sma + crossover model'] = 100 * \
        (1+df['Criteria 2'].shift(1)*df['% change']).cumprod()

    # Part 5 - Calculate the models' returns

    # 200 sma models' returns
    start_model1 = df['200 sma model'].iloc[200]
    end_model1 = df['200 sma model'].iloc[-1]
    years = (df['200 sma model'].count()+1-200)/252
    model1_average_return = (end_model1/start_model1)**(1/years)-1
    print('"200 sma model" yields an average of ',
          model1_average_return*100, '% per year.')

    # 200 sma + crossover models' returns
    start_model2 = df['200 sma + crossover model'].iloc[200]
    end_model2 = df['200 sma + crossover model'].iloc[-1]
    model2_average_return = (end_model2/start_model2)**(1/years)-1
    print('"200 sma + crossover model" yields an average of ',
          model2_average_return*100, '% per year.')

    # buy and hold's returns
    start_spx = df['Buy and hold'].iloc[200]
    end_spx = df['Buy and hold'].iloc[-1]
    spx_average_return = (end_spx/start_spx)**(1/years)-1
    print('"Buy and hold model" yields an average of ',
          spx_average_return*100, '% per year.')

    # Part 6 - plot the models
    # df[['Buy and hold', '200 sma model', '200 sma + crossover model']
    #    ].plot(grid=True, kind='line', title='Different models')


model1()
