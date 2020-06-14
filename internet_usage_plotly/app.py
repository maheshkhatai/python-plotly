import dash
from dash.dependencies import Input,Output
import dash_table
import dash_core_components as dcc 
import dash_html_components as dhc 
import plotly.express as px 
import pandas as pd

#---------------------------------------------------
# Import Data and perform Operations 

df=pd.read_csv('internet_cleaned.csv')

df=df[df['year']== 2019]

# Create ID column in DF 
df['id']=df['iso_alpha3']
df.set_index('id',inplace=True,drop=False)

#---------------------------------------------------
# App Layout 

app=dash.Dash(__name__,prevent_initial_callbacks=True)

# Sorting the data 

app.layout=dhc.Div(
    [
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[
                {"name":i,"id":i,"deletable":True,"selectable":True,"hideable":True}
                if i =="iso_aplha3" or i == "year" or i =="id"
                else {"name":i,"id":i,"deletable":True,"selectable":True}
                for i in df.columns
            ],
            data=df.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="single",
            column_selectable="multi",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=6,
            style_cell={"minWidth":95,"maxWidth":95,"width":95},
            style_cell_conditional=[
                {
                    'if':{'column_id':c},
                    'textAlign':'left'
                }for c in ['country','iso_alpha']
            ],
            style_data={
                'whiteSpace':'normal',
                'height':'auto'
            }
        ),

        dhc.Br(),
        dhc.Br(),
        dhc.Div(id='bar-container'),
        dhc.Div(id='choromap-container')
    ])


#------------------------------------------------------------------------
# Create App Callback Module 
# Create Bar Chart
@app.callback(
    Output(component_id='bar-container',component_property='children'),
    [Input(component_id='datatable-interactivity',component_property='derived_virtual_data'),
     Input(component_id='datatable-interactivity',component_property='derived_virtual_selected_rows'),
     Input(component_id='datatable-interactivity',component_property='derived_virtual_selected_row_ids'),
     Input(component_id='datatable-interactivity',component_property='selected_rows'),
     Input(component_id='datatable-interactivity',component_property='derived_virtual_indices'),
     Input(component_id='datatable-interactivity',component_property='derived_virtual_row_ids'),
     Input(component_id='datatable-interactivity',component_property='active_cell'),
     Input(component_id='datatable-interactivity',component_property='selected_cells')]
)

def update_bar(all_rows_data,slcted_row_indices,slcted_row_names,slcted_rows,
                order_of_rows_indices,order_of_row_names,actv_cells,slcted_cells):
    print("************************************************************************")
    print("Data across all cells pre or post filtering: {}".format(all_rows_data))
    print("------------------------------------------------")
    print("Indices of Selected Rows after if part of table after filtering:{}".format(slcted_row_indices))
    print("Names of selected Rows if part of table after filtering:{}".format(slcted_row_names))
    print("Indices of selected rows regardless of filtering:{}".format(slcted_rows))
    print("------------------------------------------------")
    print("Indices of all rows pre or post filtering:{}".format(order_of_rows_indices))
    print("Name of all rows pre or post filtering:{}".format(order_of_row_names))
    print("------------------------------------------------")
    print("Complete Data of Active Cells:{}".format(actv_cells))
    print("Complete Data of all selected cells:{}".format(slcted_cells))

    dff=pd.DataFrame(all_rows_data)
    
    # used to highlight selected countries on bar chart
    colors=['#7FDBFF' if i in slcted_row_indices else '#0074D9'
             for i in range(len(dff))]

    if "country" in dff and "did online course" in dff:
        return [
            dcc.Graph(id='bar-chart',
                      figure=px.bar(
                          data_frame=dff,
                          x="country",
                          y="did online course",
                          labels={"did online course":"% of Pop took the online course"}
                      ).update_layout(showlegend=False,xaxis={"categoryorder":"total ascending"})  
                       .update_traces(marker_color=colors,hovertemplate="<b>%{y}%</b><extra></extra>")
            )   
        ]

# Create Choropleth Chart
@app.callback(
    Output(component_id='choromap-container',component_property='children'),
    [Input(component_id='datatable-interactivity',component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity',component_property="derived_virtual_selected_rows")]
)

def update_map(all_rows_data,slcted_row_indices):
    dff=pd.DataFrame(all_rows_data)

    # Highlight the selected borders 

    borders=[5 if i in slcted_row_indices else 1 
             for i in range(len(dff))]

    if "iso_alpha3" in dff and "internet daily" in dff  and "country" in dff:
        return [
            dcc.Graph(id='choropleth',
            style={"height": 700},
            figure=px.choropleth(
                data_frame=dff,
                locations="iso_alpha3",
                scope="europe",
                color="internet daily",
                title="% of Pop that uses Internet Daily",
                template="plotly_dark",
                hover_data=['country','internet daily']
                ).update_layout(showlegend=False,title=dict(font=dict(size=28),x=0.5,xanchor='center'))
                 .update_traces(marker_line_width=borders,hovertemplate="<b>%{customdata[0]}</b><br><br>" +
                                                                        "%{customdata[1]}" + "")
            )
        ]

#--------------------------------------------------------------------------
# Highlight Selected Column
@app.callback(
    Output('datatable-interactivity','style_data_conditional'),
    [Input('datatable-interactivity','selected_columns')]
)

def update_styles(selected_columns):
    return [{
        'if': {"column_id":i},
        'background_color':'#D2F3FF'
    }for i in selected_columns]


#-------------------------------------------------------------------------

if __name__=="__main__":
    app.run_server(debug=True)