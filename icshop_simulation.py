import random
import time
#preparation time=#S_icecream*prepartion_time+#M_icecream*preparation_time*1.5+#L_icecream*preparation_time*2
#queue time=sum(order_time(random)+thinking_time(random) for previous customers)

class Customer:
    #cust_order:dict {'small':1, 'medium':2 'large':1}
    def __init__(self, cust_id, arrival_time):
        self.cust_id = cust_id
        self.cust_order = {'S':random.randint(0,3),'M':random.randint(0,3),'L':random.randint(0,3)}
        self.arrival_time = arrival_time
        self.order_time=random.uniform(60,300)
        self.thinking_time = random.uniform(0,120)

    def get_cust_id(self):
        return self.cust_id

    def get_total_icecream(self):
        return self.s_icecream_num()+self.m_icecream_num()+self.l_icecream_num()

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

class OrderingQueue(Queue):
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

class Chef:
    def __init__(self,is_experience=True):
        self.is_experience=is_experience
        if self.is_experience:
            self.s_prep_time=random.uniform(300,600)
        else:
            self.s_prep_time = random.uniform(450, 750)

    def make_ic_duration(self,icecream:list):
        if icecream[2]=='L':
            return self.s_prep_time*2
        elif icecream[2]=='M':
            return self.s_prep_time*1.5
        else:
            return self.s_prep_time


    def make_ic_alone_duration(self,s_ic_num,m_ic_num,l_ic_num):
        return self.s_prep_time*(s_ic_num+1.5*m_ic_num+2*l_ic_num)

class IceCreamShop:
    __chef_list=[]
    def __init__(self):
        self.exp_chef_num=random.randint(1,2)
        self.new_chef_num=random.randint(0,2)
        #self.ready_icecream=random.randint(0,5)
        self.current_cust=None
        self.remainingtime=0
        self.ic_waiting_q=Queue()
        self.current_ic=None
        self.ic_remainingtime=0
        self.complete_icecream=0
        for i in range(self.exp_chef_num):
            IceCreamShop.__chef_list.append(Chef())
        for i in range(self.new_chef_num):
            IceCreamShop.__chef_list.append(Chef(is_experience=False))

    def is_serving(self):
        if self.current_cust!=None:
            return True
        return False

    def start_nextserving(self,next_cust:Customer):
        self.current_cust=next_cust
        #print(">>> Start serving customer %s. Order: %s icecream size S, %s icecream size M and %s icecream size L"
        #      %(self.current_cust.cust_id,self.current_cust.s_icecream_num(),self.current_cust.m_icecream_num(),self.current_cust.l_icecream_num()))
        self.remainingtime=next_cust.get_serving_time()

    def servingtime_tick(self,current_second):
        if self.current_cust!=None:
            self.remainingtime=self.remainingtime-1
            if self.remainingtime<=0:
                print("*** %s: Customer %s completed ordering." %(time.strftime('%H:%M:%S', time.gmtime(36000+current_second)),self.current_cust.cust_id))
                self.add_icecream(self.current_cust)
                #print("Customer %s's order will be ready in %s seconds." %(self.current_cust.cust_id,max(self.make_ic_together_duration(self.current_cust))))
                self.current_cust=None

    def is_preparing_ic(self):
        if self.current_ic!=None:
            return True
        else:
            return False

    def start_nexticecream(self, next_ic: list):
        self.current_ic = next_ic
        self.ic_remainingtime = IceCreamShop.__chef_list[0].make_ic_duration(next_ic)

    def ic_preparingtime_tick(self):
        if self.current_ic!=None:
            self.ic_remainingtime=self.ic_remainingtime-1
        if self.ic_remainingtime<=0:
            self.current_ic=None

    def add_icecream(self,cust:Customer):
        for size in cust.cust_order.keys():
            if cust.cust_order[size]>0:
                for i in range(cust.cust_order[size]):
                    self.ic_waiting_q.enqueue([cust.cust_id,1,size])

    #not using
    def make_ic_together_duration(self,cust:Customer):
        prepare_time_list=[]
        if len(IceCreamShop.__chef_list)==1:
            return IceCreamShop.__chef_list[0].make_ic_alone_duration(cust.s_icecream_num(),cust.m_icecream_num(),cust.l_icecream_num())
        else:
            #[3,3,2,2]
            #[Chef1, Chef2, Chef3, Chef4]
            #{S:3,M:5,L:2}
            task_list=self.split_order(cust)
            ic_num_list=[cust.l_icecream_num(),cust.m_icecream_num(),cust.s_icecream_num()]
            for i in range(len(IceCreamShop.__chef_list)):
                temp_cust_order=[0,0,0]
                self.match_ic_to_chef(ic_num_list,task_list,temp_cust_order,i,0)
                print(temp_cust_order)
                prepare_time_list.append(IceCreamShop.__chef_list[i].make_ic_alone_duration(temp_cust_order[2],temp_cust_order[1],temp_cust_order[0]))
        return prepare_time_list

    #not using
    def match_ic_to_chef(self,ic_num_list,task_list,temp_cust_order,i,j):
        if j < 3:
            if ic_num_list[j] >= task_list[i]:
                temp_cust_order[j] = task_list[i]
                ic_num_list[j] = ic_num_list[j] - task_list[i]
                task_list[i] = 0
            else:
                temp_cust_order[j] = ic_num_list[j]
                task_list[i] = task_list[i] - ic_num_list[j]
                ic_num_list[j] = 0
                self.match_ic_to_chef(ic_num_list, task_list, temp_cust_order, i, j + 1)


    def split_order(self,cust:Customer):
        task_list=[cust.get_total_icecream()//len(IceCreamShop.__chef_list)]*len(IceCreamShop.__chef_list)
        remainder=cust.get_total_icecream()%len(IceCreamShop.__chef_list)
        remainder_list=[1]*remainder+[0]*(len(IceCreamShop.__chef_list)-remainder)
        return [sum(x) for x in zip(task_list,remainder_list)]



def icshop_simulation(second_count):
    icshop=IceCreamShop()
    ordering_q=OrderingQueue()
    waitingtimes=[]
    cust_id=0
    tmp_cust_id=0
    print("Start simulating the ice cream shop for %s seconds..." %second_count)
    print("%s: Nitro Ice-cream Shop opens." %seconds_to_hhmmss(0))
    print("Number of experienced chefs = %s\nNumber of new chefs = %s" %(icshop.exp_chef_num,icshop.new_chef_num))
    for current_second in range(second_count):
        if new_customer():
            new_cust=Customer(cust_id+1,current_second)
            ordering_q.enqueue(new_cust)
            print("+++ %s: New customer! Customer %s arrives." % (seconds_to_hhmmss(current_second),new_cust.get_cust_id()))
            queue_time=ordering_q.get_queue_time(new_cust)
            if icshop.current_cust!=None:
                current_serving_remaintime = icshop.current_cust.get_serving_time() - (current_second - icshop.current_cust.get_arrivaltime())
            else:
                current_serving_remaintime=0
            waiting_time=queue_time+current_serving_remaintime
            waitingtimes.append(waiting_time)
            if waiting_time>0:
                print("Customer %s waits for %s until his turn." %(new_cust.cust_id,seconds_to_mmss(int(waiting_time)+1)))
            cust_id+=1
        if not icshop.is_serving() and ordering_q.size()>0:
            next_cust=ordering_q.dequeue()
            print(">>> %s: Start serving customer %s. Order: %s icecream size S, %s icecream size M and %s icecream size L"
                  % (seconds_to_hhmmss(current_second),next_cust.cust_id, next_cust.s_icecream_num(), next_cust.m_icecream_num(),
                     next_cust.l_icecream_num()))
            icshop.start_nextserving(next_cust)
        icshop.servingtime_tick(current_second)
        if not icshop.is_preparing_ic() and icshop.ic_waiting_q.size()>0:
            #print("Current cust id=",tmp_cust_id)
            next_ic=icshop.ic_waiting_q.dequeue()
            #print("Next cust id=", next_ic[0])
            if tmp_cust_id!=next_ic[0] and tmp_cust_id!=0:
                print("*** %s: Ice-cream ready! Customer %s's icecream order is completed!" %(seconds_to_hhmmss(current_second),tmp_cust_id))
            tmp_cust_id=next_ic[0]
            icshop.start_nexticecream(next_ic)
        icshop.ic_preparingtime_tick()

    if ordering_q.size()>0:
        print("List of Customers still in queue:")
        for cust in ordering_q.items:
            print(cust.cust_id,cust.cust_order,cust.arrival_time,cust.order_time,cust.thinking_time)
    print("Waiting time of all customers: \n",waitingtimes)

    if icshop.ic_waiting_q.size()>0:
        print("Icecream waiting q:")
        for icecream in icshop.ic_waiting_q.items:
            print(icecream)

def seconds_to_hhmmss(second_number):
    return time.strftime('%H:%M:%S', time.gmtime(36000+second_number))

def seconds_to_mmss(second_number):
    return time.strftime('%M minutes and %S seconds', time.gmtime(second_number))


def new_customer():
    num=random.randint(0,600)
    if num==50:
        return True
    else:
        return False


if __name__ == '__main__':
    icshop_simulation(10000)



