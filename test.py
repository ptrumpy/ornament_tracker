s = '2022 Star Wars Storyteller - Princess Leia Organa - A New Hope'
s_split = s.split(' ')
year = s_split[0]
series = s_split[1] + ' ' + s_split[2]
desc = s_split[3:]
print(year,series,desc)
