from datetime import datetime

s = "22/04/2001"


startDate = datetime.strptime(s, "%d/%m/%Y")

print(startDate.strftime("%d/%m/%Y"))





