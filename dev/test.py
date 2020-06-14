import dash
import dash_table
import pandas as pd 

df=pd.read_csv('D:\\SampleData\\Ecommerce_Customers.csv')


app=dash.Dash(__name__)

app.layout= dash_table.DataTable(
    id='table',
    columns=[{"name":i,"id":i}for i in df.columns],
    data=df.to_dict('records'),
    page_size=20,
    fixed_rows={'headers': True},
    style_table={"height":'300px','overflowY':'auto'}

)

if __name__=="__main__":
    app.run_server(debug=True)

