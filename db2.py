import psycopg2 
import PySimpleGUI as ui

def add_record():
    con = psycopg2.connect(
    database = "Ornaments",
    user = "postgres",
    password = "Erj020912"
    )

    cur = con.cursor()

    cur.execute("Insert into ornaments VALUES (%s, %s, %s, %s, %s, %s)",
        (upc.get(),series.get(),year.get(),description.get(), quantity.get(), notes.get()
        )
    )       

    con.commit()

    con.close

#build search function
def search():
    con = psycopg2.connect(
    database = "Ornaments",
    user = "postgres",
    password = "Erj020912",
    host = "192.168.4.28",
    port = "5432"
    )

    cur = con.cursor()
    if len(description.get())>0:
        search_sql = "lower(\"Description\") like %s "
        desc_search = "%"
        desc_search += description.get().lower()
        desc_search += '%'
        where_list = [search_sql]
        where_search = [desc_search]
    if len(series.get())>0:
        series_sql = "lower(\"Series\") like %s "
        series_search  = '%'
        series_search += series.get().lower()
        series_search += '%'
        where_list.append(series_sql)
        where_search.append(series_search)
    if len(year.get())>0:
        year_sql = "\"Year\" = %s "
        year_search = year.get()
        where_list.append(year_sql)
        where_search.append(year_search)
    if len(quantity.get())>0:
        qty_sql = "\"Quantity\" = %s "
        qty_search = quantity.get()
        where_list.append(qty_sql)
        where_search.append(qty_search)
 
     

    s = "and "
    where_sql = s.join(where_list)
    #print(where_sql)
    #print(where_search)
    sql = "Select * from Ornaments where " + where_sql
    sql += "order by \"Year\""
    global current_sql_statement 
    current_sql_statement = sql
    #print(cur.mogrify(sql + " order by \"Year\"",(desc_search)))
    cur.execute(sql,where_search)
    cur.query
    rows = cur.fetchall()
    window['-TABLE-'].Update(values=rows)
    con.commit()
    con.close
    #print(rows)
#connect to db
con = psycopg2.connect(
    database = "Ornaments",
    user = "postgres",
    password = "Erj020912",
    host = "192.168.4.28",
    port = "5432"
)

#build delete pop up function
def delete_popup(title, text):
    window = ui.Window(title,
        [[ui.Text(text)],
        [ui.Button('Yes'), ui.Button('No')]
        ])

    while True:
      event = window.read()
      if event == ui.WIN_CLOSED or event == 'No': # if user closes window or clicks cancel
        window.close()
        break
      if event == 'Yes':
          window.close()
          return
   

#build delete function
def delete_records():
    con = psycopg2.connect(
    database = "Ornaments",
    user = "postgres",
    password = "Erj020912",
    host = "192.168..4.28",
    port = "5432"
    )

    cur = con.cursor()
    
    row_index = 0
    for num in values['-TABLE-']:
        row_index = num 
    # Returns nested list of all Table rows
    all_table_vals = window.Element('-TABLE-').get()

        # Index the selected row 
    selected_row = all_table_vals[row_index]
    #print(selected_row)

    # [0] to Index the goal_name of my selected Row
    upc_to_delete = selected_row[0]
    sure = 'Are you sure you want to delete UPC ' + upc_to_delete 
    delete_popup('Delete Record', sure)
    sql = "Delete from Ornaments where \"upc_code\" = '" + upc_to_delete + "'"
    #print(sql)
    cur.execute(sql)
    
    cur.execute(current_sql_statement, current_args)
    rows = cur.fetchall()
    window['-TABLE-'].Update(values=rows)
        
    con.commit()
    con.close

#build update function
def update_records():
    con = psycopg2.connect(
    database = "Ornaments",
    user = "postgres",
    password = "Erj020912",
    host = "192.168.4.28",
    port = "5432"
    )

    cur = con.cursor()
    
    row_index = 0
    for num in values['-TABLE-']:
        row_index = num 
    # Returns nested list of all Table rows
    all_table_vals = window.Element('-TABLE-').get()

        # Index the selected row 
    selected_row = all_table_vals[row_index]
    #print(selected_row)

    # [0] to Index the goal_name of my selected Row
    upc_to_update = selected_row[0]
    if year.get() =="":
        year_sql = ""
    else:
        year_sql = "\"Year\" = {}".format(year.get())

    if series.get() =="":
        series_sql = ""
    else:
        series_sql = ",\"Series\" = %s",(series.get())  

    if description.get() =="":
        description_sql = ""
    else:
        description_sql = ",\"Description\" = {}".format(description.get())  

    if quantity.get() =="":
        quantity_sql = ""
    else:
        quantity_sql = ",\"Quantity\" = {}".format(quantity.get())
    print(quantity_sql)

    if notes.get() =="":
        notes_sql = ""
    else:
        notes_sql = ",\"Notes\" = %s",(notes.get())    
      
    sql = "Update Ornaments "
    set_sql = year_sql + series_sql + description_sql + quantity_sql + notes_sql
    set_sql = set_sql.lstrip(',')
    print(set_sql)
    set_sql = "set " + set_sql
    where_sql =  " where \"upc_code\" = '" + upc_to_update + "'"
    print(sql + set_sql + where_sql)
    cur.execute(sql + set_sql + where_sql)
    
    cur.execute(current_sql_statement, current_args)
    rows = cur.fetchall()
    window['-TABLE-'].Update(values=rows)
        
    con.commit()
    con.close


con = psycopg2.connect(
    database = "Ornaments",
    user = "postgres",
    password = "Erj020912",
    host = "192.168.4.28",
    port = "5432"
)

cur = con.cursor()

global current_sql_statement 
current_sql_statement = "select * from Ornaments order by \"Year\"" #variable to hold current statement
global current_args 
current_args =  ""

cur.execute(current_sql_statement)

rows = cur.fetchall()

upc = ui.InputText(justification='r', text_color='grey', background_color='white',size=(25,1)#, key='-IN-'
)
series = ui.InputText(justification='r', text_color='grey',background_color='white',size=(25,1))
year = ui.InputText(justification='r', text_color='grey', background_color='white',size=(25,1))
description = ui.InputText(justification='r', text_color='grey',background_color='white',size=(25,1))
quantity = ui.InputText(justification='r', text_color='grey',background_color='white',size=(25,1))
notes = ui.InputText(justification='r', text_color='grey',background_color='white',size=(50,3))

#for r in rows:
#    print(f"SKU {r[0]} Description {r[1]}")

cur.close()

con.close()

#form = ui.FlexForm("Ornament Tracker", auto_size_text=True, size=(1200,1200)) 
col_1 = [[ui.Text("UPC Code", justification='l')],
          [ui.Text("Series", justification='l')],
          [ui.Text("Year", justification='l')],
          [ui.Text("Description", justification='l')],
          [ui.Text("Quantity", justification='l')],
          [ui.Text("Notes",size=(10,1))]]
col_1 = [[ui.Column(col_1,element_justification='l', pad=(0,0))]]

col_2 = [[upc],
          [series],
          [year],
          [description],
          [quantity],
          [notes]  ]
col_2 = [[ui.Column(col_2,element_justification='r',pad=(0,0))]]

data = ("UPC")
headings = ['UPC','Series','Year','Description','Quantity','Notes']
layout = [[ui.Column(col_1), ui.Column(col_2)],
           # [ui.Listbox(values=new_rows, size=(80,20))],
           [ui.Table(values=rows, headings=headings,col_widths=[15,15,5,50,10,50],def_col_width=20,justification='center',auto_size_columns=False,num_rows=10,key='-TABLE-')],
            [ui.Button("Add"), ui.Button("Delete"), ui.Button("Update"), ui.Button("Search"), ui.Button("Exit")]]
# Create the window
window = ui.Window('Ornament Tracker', layout, finalize=True, size=(1200,700))

window.bind('<FocusIn>', '+FOCUS IN+')
# Create an event loop

while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if  event == ui.WIN_CLOSED or event == 'Exit':
        break
    '''if event == '+FOCUS IN+':
        window['-IN-'].update('')
    '''    
    if event == 'Add':
        add_record()
    if event == 'Search':
        search()
    if event == 'Delete':
        delete_records()
    if event == 'Update':
        update_records()
        
    
window.close()

