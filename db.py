import psycopg2 
import PySimpleGUI as ui

#connect to db
con = psycopg2.connect(
    database = "Ornaments",
    user = "postgres",
    password = "Erj020912"
)

cur = con.cursor()

cur.execute("select * from Ornaments")

rows = cur.fetchall()
#print(rows)

upc = [x[0] for x in rows]
series = [x[1] for x in rows]
year = [x[2] for x in rows]
description = [x[3] for x in rows]
quantity = [x[4] for x in rows]
notes = [x[5] for x in rows]

#for r in rows:
#    print(f"SKU {r[0]} Description {r[1]}")

cur.close()

con.close()
col_1 = [[ui.Text("UPC Code", justification='l')],
          [ui.Text("Series", justification='l')],
          [ui.Text("Year", justification='l')],
          [ui.Text("Description", justification='l')],
          [ui.Text("Quantity", justification='l')],
          [ui.Text("Notes",size=(10,3))]]
col_1 = [[ui.Column(col_1,element_justification='l', pad=(0,0))]]
col_2 = [[ui.Text(upc[0], justification='r', text_color='black', background_color='white',size=(12,1))],
          [ui.Text(series[0], justification='r', text_color='black',background_color='white',size=(12,1))],
          [ui.Text(year[0], justification='r', text_color='black', background_color='white')],
          [ui.Text(description[0], justification='r', text_color='black',background_color='white',size=(25,1))],
          [ui.Text(quantity[0], justification='r', text_color='black',background_color='white',size=(3,1))],
          [ui.Text(notes[0], justification='r', text_color='black',background_color='white',size=(25,3))]  ]
col_2 = [[ui.Column(col_2,element_justification='r', pad=(0,0))]]
layout = [[ui.Column(col_1), ui.Column(col_2)],
            [ui.Button("Previous"),ui.Button("Add"), ui.Button("Delete"), ui.Button("Update"), ui.Button("Next")]]
# Create the window
window = ui.Window("Ornament Tracker", layout, element_justification='c')

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if  event == ui.WIN_CLOSED:
        break
    
window.close()