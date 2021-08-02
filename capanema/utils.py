
def join(df1, df2, column):

    df = df1.join(df2.set_index(column), on=column)

    return df