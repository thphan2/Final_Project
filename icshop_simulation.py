import random

#preparation time=#S_icecream*prepartion_time+#M_icecream*preparation_time*1.5+#L_icecream*preparation_time*2
#queue time=sum(order_time(random)+thinking_time(random) for previous customers)

class Customer:
    #cust_order:dict {'small':1, 'medium':2 'large':1}
    def __init__(self, cust_id, arrival_time):
        self.cust_id = cust_id
        self.cust_order = {'S':random.randint(0,5),'M':random.randint(0,5),'L':random.randint(0,5)}
        self.arrival_time = arrival_time
        self.order_time=random.uniform(60,300)
        self.thinking_time = random.uniform(0,120)

    def get_cust_id(self):
        return self.cust_id

    def s_icecream_num(self):
        return self.cust_order['S']

    def m_icecream_num(self):
        return self.cust_order['M']

    def l_icecream_num(self):
        return self.cust_order['L']

    def get_arrivaltime(self):
        return self.arrival_time

    def get_order_time(self):
        return self.order_time

    def get_thinking_time(self):
        return self.thinking_time

    def get_serving_time(self):
        return self.order_time+self.thinking_time

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def getItem(self,index):
        return self.items[index]

class CustomerQueue(Queue):
    def check_queue_number(self,cust_id):
        for i in range(self.size()):
            if self.items[i].cust_id==cust_id:
                return i
        return 0

    def get_queue_time(self,cust:Customer):
        total_queue_time=0
        for i in range(1,self.size()):
            temp_cust=self.items[i]
            total_queue_time+=temp_cust.get_order_time()+temp_cust.get_thinking_time()
        return total_queue_time



class IceCreamShop:
    def __init__(self):
        self.emp_num=random.randint(1,3)
        self.ready_icecream=random.randint(0,5)
        self.current_cust=None
        self.remainingtime=0

    def is_serving(self):
        if self.current_cust!=None:
            return True
        return False

    def start_nextserving(self,next_cust:Customer):
        self.current_cust=next_cust
        self.remainingtime=next_cust.get_serving_time()

    def servingtime_tick(self):
        if self.current_cust!=None:
            self.remainingtime=self.remainingtime-1
            if self.remainingtime<=0:
                print("Customer %s completed ordering." %(self.current_cust.cust_id))
                self.current_cust=None



def icshop_simulation(second_count):
    icshop=IceCreamShop()
    cust_q=CustomerQueue()
    waitingtimes=[]
    cust_id=0
    print("Start simulating the ice cream shop for %s seconds..." %second_count)
    for current_second in range(second_count):
        if new_customer():
            new_cust=Customer(cust_id+1,current_second)
            cust_q.enqueue(new_cust)
            print("***New customer*** Customer %s comes in at second %s." % (new_cust.get_cust_id(), new_cust.get_arrivaltime()))
            queue_time=cust_q.get_queue_time(new_cust)
            if icshop.current_cust!=None:
                current_serving_remaintime = icshop.current_cust.get_serving_time() - (current_second - icshop.current_cust.get_arrivaltime())
            else:
                current_serving_remaintime=0
            waiting_time=queue_time+current_serving_remaintime
            waitingtimes.append(waiting_time)
            if waiting_time>0:
                print("Customer %s waits for %s seconds until his turn." %(new_cust.cust_id,waiting_time))
            else:
                print("***Icecream Ordered*** Done serving Customer %s in %s seconds" %(new_cust.cust_id,new_cust.get_serving_time()))
            cust_id+=1
        if not icshop.is_serving() and cust_q.size()>0:
            next_cust=cust_q.dequeue()
            icshop.start_nextserving(next_cust)
        icshop.servingtime_tick()
    #for testing, print out all the customers in the queue
    if cust_q.size()>0:
        print("List of Customers still in queue:")
        for cust in cust_q.items:
            print(cust.cust_id,cust.cust_order,cust.arrival_time,cust.order_time,cust.thinking_time)
    print("Waiting time of all customers: \n",waitingtimes)


def new_customer():
    num=random.randint(0,150)
    if num==50:
        return True
    else:
        return False

icshop_simulation(1000)



