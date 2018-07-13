def getRVtimes(period,l,currentrow):
    t = currentrow[6]
    barTime = t.time()
    reverse = list(reversed(l))
    indexOfRow = reverse.index(currentrow)
    f = []
    print("Row Date: {}\n"
          "Index:     {}"
          "Volume:    {}".format(reverse[indexOfRow][6],indexOfRow,currentrow[5]))


    for index, row in enumerate(reverse[(indexOfRow+1):]):
         d = row[6]
         dTime = d.time()
         if(dTime == barTime) and len(f)<period:
             print("D: {}\n"
                   "V:  {}".format(d,row[5]))
             f.append(row[5])

         if len(f) == period:
             print(len(f))
             break