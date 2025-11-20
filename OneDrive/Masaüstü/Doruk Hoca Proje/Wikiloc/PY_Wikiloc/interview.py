import pandas as pd


#df = pd.read_parquet(r'C:\Users\aylin\Downloads\datasets-technical-test-decathlon\data\bu_feat.parquet')
#df_test = pd.read_parquet(r'C:\Users\aylin\Downloads\datasets-technical-test-decathlon\data\test.parquet')
#df_train = pd.read_parquet(r'C:\Users\aylin\Downloads\datasets-technical-test-decathlon\data\train.parquet')

#print(df.head())
#df.to_excel("output.xlsx", index=False)
#df_test.to_excel("test.xlsx", index=False)
#df_train.to_excel("train.xlsx", index=False)


df3 = pd.read_excel(r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\PY_Wikiloc\test.xlsx')
df2 = pd.read_excel(r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\PY_Wikiloc\train.xlsx')
df1 = pd.read_excel(r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\PY_Wikiloc\output.xlsx')

merged_df = pd.merge(df2, df3, on='dpt_num_department', how='left')

# Merge the result with df3
merged_df = pd.merge(merged_df, df3, on='but_num_business_unit', how='inner')

# Show the result
print(list(merged_df.columns))









