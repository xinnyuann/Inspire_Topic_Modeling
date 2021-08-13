##################################################################################################################
#Data_Fetching.py includes following steps and functions:
#             Get text data from inspire ds database
#             Slicing data into mini-batches for higher loading and computation speed
##################################################################################################################
#Import modules###################################################################################################
import pandas as pd
import aspyr
##################################################################################################################
#UDF##############################################################################################################
#Create data batches and save as .csv files in path (./data_batches)
def slicer(df, n):
    j = 1
    for i in range(0, df.shape[0],n):
        df_output = df[i:i+n]
        df_output.to_csv("./data_batches/post17_19_{}.csv".format(j) , index=False)
        j = j+1
##################################################################################################################
##################################################################################################################
#Connect to database
redshift = aspyr.db_connect.get_redshift_dw_connection()
aurora = aspyr.db_connect.get_aurora_dw_connection()

#Query data from 3 tables (ds.posts, ds.post_text, bc.groups)
#Shape of data: 182263 rows, 7 columns(post_key, post_id, group_name, post_type, title, body, modr_status)
df = pd.read_sql(
    """SELECT p.post_key,p.post_id,g.name, p.post_type, pt.title, pt.body, p.modr_status
    FROM ds.posts AS p
    LEFT JOIN ds.post_text AS pt ON p.post_key = pt.post_key
    LEFT JOIN bc.groups AS g ON p.group_id = g.group_id
    WHERE EXTRACT(YEAR FROM p.t_created) IN (2017,2018,2019) AND p.post_type IN ('disc','jrnl')""", redshift)

#Slicing data into 10 mini-batches (20000 rows per batch) and save as .csv files
slicer(df, 20000)
