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

class RandomDist():
    '''
    RandomDist is a base abstract class to build a Random distribution.
    This class contains an abstract method for building a random generator
    Inherited class must implement this method
    '''

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def random(self):
        """
        This class is an abstract method for implementation class
        should return a random value based on the configuration given in the implementation
        :return:
        """
        pass

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
    def check_queue_number(self,cust_id) ->int:
        for i in range(self.size()):
            if self.items[i].cust_id==cust_id:
                return i
        return 0

    def get_total_queue_time(self) -> float:
        '''
        Get total waiting time for the entire queue
        :return:
        '''
        total_queue_time=0
        for i in range(1,self.size()):
            temp_cust=self.items[i]
            total_queue_time+=temp_cust.get_order_time()+temp_cust.get_thinking_time()
        return total_queue_time

    def get_queue_time(self, cust: Customer) ->float:
        '''
        Get waiting time for the customer
        :param cust: customer object
        :return:
        '''
        q_index = self.check_queue_number(cust.cust_id)
        queue_time = 0
        for i in range(q_index + 1,self.size()):
            temp_cust = self.items[i]
            queue_time += temp_cust.get_order_time() + temp_cust.get_thinking_time()
        return queue_time

class Chef:
    def __init__(self,is_experience=True):
        self.is_experience=is_experience
        if self.is_experience:
            self.s_prep_time=random.uniform(300,600)
        else:
            self.s_prep_time = random.uniform(450, 750)

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
        print(">>> Start serving customer %s. Order: %s icecream size S, %s icecream size M and %s icecream size L"
              %(self.current_cust.cust_id,self.current_cust.s_icecream_num(),self.current_cust.m_icecream_num(),self.current_cust.l_icecream_num()))
        self.remainingtime=next_cust.get_serving_time()

    def servingtime_tick(self):
        if self.current_cust!=None:
            self.remainingtime=self.remainingtime-1
            if self.remainingtime<=0:
                print("*** Customer %s completed ordering." %(self.current_cust.cust_id))
                print("Customer %s's order will be ready in %s seconds." %(self.current_cust.cust_id,max(self.make_ic_together_duration(self.current_cust))))
                self.current_cust=None

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
    cust_q=CustomerQueue()
    waitingtimes=[]
    cust_id=0
    print("Start simulating the ice cream shop for %s seconds..." %second_count)
    print("Number of experienced chefs = %s\nNumber of new chefs = %s" %(icshop.exp_chef_num,icshop.new_chef_num))
    for current_second in range(second_count):
        if new_customer():
            new_cust=Customer(cust_id+1,current_second)
            cust_q.enqueue(new_cust)
            print("+++ New customer +++ Customer %s comes in at second %s." % (new_cust.get_cust_id(), new_cust.get_arrivaltime()))
            queue_time=cust_q.get_queue_time(new_cust)
            if icshop.current_cust!=None:
                current_serving_remaintime = icshop.current_cust.get_serving_time() - (current_second - icshop.current_cust.get_arrivaltime())
            else:
                current_serving_remaintime=0
            waiting_time=queue_time+current_serving_remaintime
            waitingtimes.append(waiting_time)
            if waiting_time>0:
                print("Customer %s waits for %s seconds until his turn." %(new_cust.cust_id,waiting_time))
            cust_id+=1
        if not icshop.is_serving() and cust_q.size()>0:
            next_cust=cust_q.dequeue()
            icshop.start_nextserving(next_cust)
        icshop.servingtime_tick()

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


if __name__ == '__main__':
    icshop_simulation(1000)



