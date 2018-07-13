import numpy
import confirmers

def jeremyCator(RelativeVolume,rv,currentTicker,row,TrueRange):


    if len(RelativeVolume) > 10:

        test = RelativeVolume[-5:-1]

        t = (rv / numpy.average(test)) * 100

        if (t > 300 and rv > 150):
            print(TrueRange[-10:])
            print("High Average RV Vol      : {}\n"
                  "At                       : {}\n"
                  "Relative Volume          : {}"
                  .format(currentTicker, row[6],rv))
def addTrueRange(row):
    high = row[2]
    low = row[3]
    tr = round((high-low),2)


    return tr
def getRelativeVolumeAverage(RVlist,period):

    if len(RVlist) > period:

        avg = numpy.average(RVlist[-period:])
        return round(avg,2)
    else:
        return 0

def getRelativeVolume(period,l,currentrow):
    t = currentrow[6]
    barTime = t.time()
    reverse = list(reversed(l))
    indexOfRow = reverse.index(currentrow)
    f = []
    # print("Row Date: {}\n"
    #       "Index:     {}".format(reverse[indexOfRow][6],indexOfRow))


    for index, row in enumerate(reverse[(indexOfRow+1):]):
         d = row[6]
         dTime = d.time()
         if(dTime == barTime) and len(f)<period:
             # print("D: {}\n"
             #       "V:  {}".format(d,row[5]))
             f.append(row[5])

         if len(f) == period:
             break

    avg = numpy.average(f)
    return (currentrow[5]/avg) * 100


def checkChurn(RV,TR,row,rvAvg,currentTicker,rv):
    c = TR[-1:][0] == min(TR[-3:]) and RV[-1:][0] == max(RV[-3:])
    if (c and rvAvg > 200 and rv > 200 and rv < 800):
        print("Churn for    : {}\n"
              "At           : {}\n"
              "RV           : {}".format(currentTicker, row[6], rv))

def swinglow(lastThree,ticker):
    #print(lastThree)
    midBar = lastThree[1]
    currentBar = lastThree[2]
    lows = [l[3] for l in lastThree]
    highs = [h[2] for h in lastThree]
    if(midBar[3]== min(lows) and midBar[2]==min(highs)):
        print("Swing Low for    :{}\n"
              "Ticker           :{}"
              .format(ticker,midBar[6]))
        #print(lastThree)

def churning(rvAvg,days,TR,currentTicker,row):
    #lastTen = days[-10:]
    if rvAvg > 125:
        reverse = list(reversed(days))
        i = days.index(row)
        t = reverse[-i - 1:-i + 9]
        highs = [h[2] for h in t]
        lows = [l[3] for l in t]

        avgTR = numpy.average(TR[-10:])
        stdev = numpy.std(avgTR)
        range = max(highs)-min(lows)
        if(range <= (avgTR * 2.5    )):
            #print(days[-1:])





            ds = [d[6]for d in t]
            #print(ds)
            print("CHURNING for    : {}\n"
                  "At           : {}\n"
                  "Range        : {}\n"
                  "Avg          : {}\n"
                  "High          : {}\n"
                  "Low         : {}"
                  .format(currentTicker, row[6],range,avgTR,max(highs),min(lows)))





