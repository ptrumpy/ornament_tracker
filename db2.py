import psycopg2
import PySimpleGUI as ui
import database


#check input function to check which fields to update or search_sql
def check_field(field):
    if field !="":
        return True
def clear_inputs():
    window['upc'].update('')
    window['year'].update('')
    window['desc'].update('')
    window['qty'].update('')
    window['notes'].update('')


#build delete pop up function
def delete_popup(title, text):
    window = ui.Window(title,
        [[ui.Text(text)],
        [ui.Button('Yes'), ui.Button('No')]
        ])

    while True:
      event,values = window.read()
      if event == ui.WIN_CLOSED or event == 'No': # if user closes window or clicks cancel
          window.close()
          break
      if event == 'Yes':
          window.close()
          database.delete_records(upc_to_delete)
          return


rows = database.initial_data()

upc = ui.InputText(justification='r', text_color='grey', background_color='white',size=(25,1), key='upc'
)
series = ui.Combo(values=database.populate_series_dropdown(),text_color='grey',background_color='white',size=(25,1),default_value='Star Wars')
year = ui.InputText(justification='r', text_color='grey', background_color='white',size=(25,1), key='year')
description = ui.InputText(justification='r', text_color='grey',background_color='white',size=(25,1), key='desc')
quantity = ui.InputText(justification='r', text_color='grey',background_color='white',size=(25,1), key='qty')
notes = ui.InputText(justification='r', text_color='grey',background_color='white',size=(50,3), key='notes')

#for r in rows:
#    print(f"SKU {r[0]} Description {r[1]}")


#form = ui.FlexForm("Ornament Tracker", auto_size_text=True, size=(1200,1200))
col_1 = [[ui.Text("UPC Code", justification='l')],
          [ui.Text("Series",justification='l')],
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
           [ui.Table(values=rows, headings=headings,col_widths=[15,15,5,50,10,50],def_col_width=20,justification='center',auto_size_columns=False,num_rows=40,key='-TABLE-')],
            [ui.Button("Add"), ui.Button("Delete"), ui.Button("Update"), ui.Button("Search"), ui.Button("Clear"), ui.Button("Exit")]]
# Create the window
window = ui.Window('Ornament Tracker', layout, finalize=True, size=(1200,1000))

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
    if event == 'Clear':
        clear_inputs()
    if event == 'Add':
        database.add_record(upc.get(),series.get(),year.get(),description.get(), quantity.get(), notes.get())
        rows = database.initial_data()
        window['-TABLE-'].Update(values=rows)
        clear_inputs()
    if event == 'Search':
        search = {}
        search_like = {}
        if check_field(year.get()):
            search['year']= year.get()
        if check_field(series.get()):
            search['series']= series.get()
        if check_field(description.get()):
            search_like['description']= "%" + description.get() + "%"
        if check_field(quantity.get()):
            search['qty']= quantity.get()
        if check_field(notes.get()):
            search_like['notes']= "%" + notes.get() + "%"
        #print(search_like)
        rows = database.search_records(search, search_like)
        window['-TABLE-'].Update(values=rows)
        clear_inputs()
    if event == 'Delete':
        row_index = 0
        for num in values['-TABLE-']:
            row_index = num
        # Returns nested list of all Table rows
        all_table_vals = window.Element('-TABLE-').get()
        selected_row = all_table_vals[row_index]
        upc_to_delete = selected_row[0]
        #print(upc_to_delete)
        sure = 'Are you sure you want to delete UPC ' + upc_to_delete
        delete_popup('Delete Record', sure)
        rows = database.initial_data()
        window['-TABLE-'].Update(values=rows)
    if event == 'Update':
        row_index = 0
        for num in values['-TABLE-']:
            row_index = num
        all_table_vals = window.Element('-TABLE-').get()
        selected_row = all_table_vals[row_index]
        print(selected_row)
        upc_to_update = selected_row[0]

        #get all values needing to be updated
        #dict to hold columns and calues to be updated
        upd = {}
        if check_field(year.get()):
            upd['year']= year.get()
        if check_field(series.get()):
            upd['series']= series.get()
        if check_field(description.get()):
            upd['description']= description.get()
        if check_field(quantity.get()):
            upd['qty']= quantity.get()
        if check_field(notes.get()):
            upd['notes']= notes.get()
        #print(upd)
        database.update_records(upc_to_update,upd)
        rows = database.initial_data()
        window['-TABLE-'].Update(values=rows)
        clear_inputs()
window.close()
