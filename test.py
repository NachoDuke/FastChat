from collections import Counter
import statistics

def latency(path):
    with open(path,'r') as inp:
        lines = inp.readlines()
        time = 0
        length = len(lines)
        for line in lines:
            listinlist =  line.split(' ',2)
            time += float(listinlist[0])-float(listinlist[1])
        return time/length
        
def create_bins(lower_bound, width, quantity):
    """ create_bins returns an equal-width (distance) partitioning. 
        It returns an ascending list of tuples, representing the intervals.
        A tuple bins[i], i.e. (bins[i][0], bins[i][1])  with i > 0 
        and i < quantity, satisfies the following conditions:
            (1) bins[i][0] + width == bins[i][1]
            (2) bins[i-1][0] + width == bins[i][0] and
                bins[i-1][1] + width == bins[i][1]
    """
    bins = []
    for l in range(quantity):
        bins.append((lower_bound+l*width,lower_bound+(l+1)*width))
    # for low in range(lower_bound, 
    #                  lower_bound + quantity*width+ 1, width):
    #     bins.append((low, low+width))
    return bins

def find_bin(value, bins):
    """ bins is a list of tuples, like [(0,20), (20, 40), (40, 60)],
        binning returns the smallest index i of bins so that
        bin[i][0] <= value < bin[i][1]
    """
    
    for i in range(0, len(bins)):
        if bins[i][0] <= value < bins[i][1]:
            return i
    return -1

def binner(lower_bound, width, quantity, weights_of_persons):
    # bins = create_bins(lower_bound=50,
    #                 width=4,
    #                 quantity=10)
    bins = create_bins(lower_bound, width,quantity)
    # weights_of_persons = [73.4, 69.3, 64.9, 75.6, 74.9, 80.3, 
                        # 78.6, 84.1, 88.9, 90.3, 83.4, 69.3, 
                        # 52.4, 58.3, 67.4, 74.0, 89.3, 63.4]

    binned_weights = []

    for value in weights_of_persons:
        bin_index = find_bin(value, bins)
        binned_weights.append(bin_index)
        
    frequencies = Counter(binned_weights)

def throughput(list):
    window_size = 2
    time = 0.01
    list.sort()
    med = statistics.median(list)
    min_ = max(list[0],med/10)
    max_ = min(list[-1],med*10)
    sum = 0
    numberWindows = int((max_-window_size-min_)/time)
    for i in range(numberWindows):
        windowstart = min_+time*i
        count = 0
        for c in list:
            if c>windowstart and c<=windowstart+window_size:
                count+=1
        sum+=count
    return sum/(numberWindows*window_size)

if __name__=='__main__':
    sendTimelist = []
    receiveTimeList = []
    with open("out.txt",'r') as o:
        content = o.readlines()
        for c in content:
            info_message = c.split('&&&',1)
            info = info_message[0]
            message = info_message[1]
            receive_send = info.split(': ',1)
            sendTime = receive_send[1]
            sendTimelist.append(float(sendTime))
            receiveTime  = receive_send[0].split('-',1)[0]
            receiveTimeList.append(float(receiveTime))
            f = open("outs.txt",'a')
            f.write(receiveTime.strip()+" "+sendTime.strip()+" "+message)
    print("Latency",latency("outs.txt"))
    receiveTimeList.sort()
    sendTimelist.sort()
    width =0.01
    # binner(receiveTimeList[0],width,int((receiveTimeList[-1]-receiveTimeList[0])/width) ,receiveTimeList)
    # binner(sendTimelist[0],width,int((sendTimelist[-1]-sendTimelist[0])/width) , sendTimelist)
    # print(sendTimelist)
    print("InputThroughput",throughput(sendTimelist))
    print("OutputThroughPut",throughput(receiveTimeList))

