### Step 1 of 4 for Amazon Search Term Report ###
import pandas as pd
from datetime import datetime as dt
from collections import Counter
DateString = dt.now().strftime("%Y%m%d-%I%M%S%p")
###### Step 1 Local Data Preparation. Pick the columns "Search Term" and "Search Frequency Rank" from Amazon Search Report and find most common keyword ######
df_input = pd.read_csv(r"C:\Users\alis\Downloads\Amazon Search Terms_null_IN (4).csv", encoding ='ISO-8859-1',skiprows=1)
print("Starting to Read Amazon Search Term file, Removing first Row and delete Department column")
df_input= df_input.drop('Department',axis=1)
#df_input_step1 = df_input[['Search Term','Search Frequency Rank']]
df_input_step1 = df_input
print("Count of Rows in Amazon Search Term file: ", len(df_input_step1))
df_input_step1['#1 Conversion Share'] = df_input_step1['#1 Conversion Share'].apply(lambda x: x.replace('%',''))
df_input_step1['#2 Conversion Share'] = df_input_step1['#2 Conversion Share'].apply(lambda x: x.replace('%',''))
df_input_step1['#3 Conversion Share'] = df_input_step1['#3 Conversion Share'].apply(lambda x: x.replace('%',''))
df_input_step1['#1 Conversion Share']=pd.to_numeric(df_input_step1['#1 Conversion Share'], errors='coerce')
df_input_step1['#2 Conversion Share']=pd.to_numeric(df_input_step1['#2 Conversion Share'], errors='coerce')
df_input_step1['#3 Conversion Share']=pd.to_numeric(df_input_step1['#3 Conversion Share'], errors='coerce')
df_input_step1['#All Conversion Share']=df_input_step1['#1 Conversion Share']+df_input_step1['#2 Conversion Share']+df_input_step1['#3 Conversion Share']

df_input_step1['#1 Click Share'] = df_input_step1['#1 Click Share'].apply(lambda x: x.replace('%',''))
df_input_step1['#2 Click Share'] = df_input_step1['#2 Click Share'].apply(lambda x: x.replace('%',''))
df_input_step1['#3 Click Share'] = df_input_step1['#3 Click Share'].apply(lambda x: x.replace('%',''))
df_input_step1['#1 Click Share']=pd.to_numeric(df_input_step1['#1 Click Share'], errors='coerce')
df_input_step1['#2 Click Share']=pd.to_numeric(df_input_step1['#2 Click Share'], errors='coerce')
df_input_step1['#3 Click Share']=pd.to_numeric(df_input_step1['#3 Click Share'], errors='coerce')
df_input_step1['#All Click Share']=df_input_step1['#1 Click Share']+df_input_step1['#2 Click Share']+df_input_step1['#3 Click Share']

###### Step 2 Remove Bad Search Terms ######
df_exclusion_list = pd.read_csv(r"C:\Users\alis\OneDrive - Dun and Bradstreet\Desktop\Personal-Local\AmazonSearchTerm\Exclusing_List.csv")
print("Starting to Read Exclusing list file")
print("Exclusing list word count: ", len(df_exclusion_list))
df_exclusing_list_b1000 = df_exclusion_list[df_exclusion_list['Id'] != 1000]
df_exclusing_list_a1000 = df_exclusion_list[df_exclusion_list['Id'] == 1000]
df_input_step2 = df_input_step1[df_input_step1['Search Term'].str.contains('|'.join(df_exclusing_list_b1000['Exclusion_List']),case=False)==False]
try:
	#df_input_step2 = df_input_step2[df_input_step2['Search Term'].str.match(pat = '|'.join(df_exclusing_list_a1000['Exclusion_List']),case=False)==False]
    df_input_step2 = df_input_step2[~df_input_step2['Search Term'].isin(list(df_exclusing_list_a1000['Exclusion_List']))]
except Exception as E:
	print("Exception while trying to match string: ",E)
print("Count of words in Step 2 after exluding bad words: ",len(df_input_step2))
df_input_step2['Word Count'] = df_input_step2['Search Term'].str.split().str.len()
df_input_step2['Search Frequency Rank'] = df_input_step2['Search Frequency Rank'].apply(lambda x: x.replace(',',''))
labels_50k = ["{0} - {1}".format(i, i + 49999) for i in range(0, 600000, 50000)]
labels_10k = ["{0} - {1}".format(i, i + 9999) for i in range(0, 600000, 10000)]
labels_1k = ["{0} - {1}".format(i, i + 999) for i in range(0, 600000, 1000)]
print(df_input_step2.dtypes)
df_input_step2['Search Frequency Rank']=pd.to_numeric(df_input_step2['Search Frequency Rank'], errors='coerce')
print(df_input_step2.dtypes)
df_input_step2["50k_Slicer"] = pd.cut(df_input_step2['Search Frequency Rank'], range(0, 600010, 50000), right=False, labels=labels_50k)
df_input_step2["10k_Slicer"] = pd.cut(df_input_step2['Search Frequency Rank'], range(0, 600010, 10000), right=False, labels=labels_10k)
df_input_step2["1k_Slicer"] = pd.cut(df_input_step2['Search Frequency Rank'], range(0, 600010, 1000), right=False, labels=labels_1k)
print(df_input_step2.head(10))
df_input_step2.to_csv(r"C:\Users\alis\OneDrive - Dun and Bradstreet\Desktop\Personal-Local\AmazonSearchTerm\files\Step1_4_Output_After_BadKeywords"+DateString+".csv", index=False)

###### Step 3 Lookup for Category keywords ######
try:
    print("Starting to read file")
    df_CategoryKeywords = pd.read_csv(r"C:\Users\alis\OneDrive - Dun and Bradstreet\Desktop\Personal-Local\AmazonSearchTerm\Category_Keywords.csv")
    print("Reading file successful")
    print("Started reading Category Keyword file, count of rows in Category Keyword are: ",len(df_CategoryKeywords))
    df_input_step3 = df_input_step2[df_input_step2['Search Term'].str.contains('|'.join(df_CategoryKeywords['Category_Keywords']),case=False)==True]
    print("Number of Rows after doing vlookup with Category Keywords are: ",len(df_input_step4))
    df_input_step3.to_csv(r"C:\Users\alis\OneDrive - Dun and Bradstreet\Desktop\Personal-Local\AmazonSearchTerm\files\Step1_4_Output_Filtered_Keywords"+DateString+".csv", index=False)
except:
    print("Step 4: Except Block. Category Keyword doesnt exist")
    df_input_step4 = df_input_step3
    df_input_step4.to_csv(r"C:\Users\alis\OneDrive - Dun and Bradstreet\Desktop\Personal-Local\AmazonSearchTerm\files\Step1_4_Output_Filtered_Keywords"+DateString+".csv", index=False)

