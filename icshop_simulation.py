import random
import time
from collections import Counter

#preparation time=#S_icecream*prepartion_time+#M_icecream*preparation_time*1.5+#L_icecream*preparation_time*2
#queue time=sum(order_time(random)+thinking_time(random) for previous customers)

class Customer:
    #cust_order:dict {'small':1, 'medium':2 'large':1}
    def __init__(self, cust_id, arrival_time):
        self.cust_id = cust_id
        self.cust_order = {'S': random.randint(0, 5), 'M': random.randint(0, 5), 'L':GaussianDiscrete(2,1,0,5).random()}
        self.arrival_time = arrival_time
        self.order_time = NormalDist(120,3,60,300).random()
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

    def order_list(self):
        order_list = []
        for size in self.cust_order:
            for num in range(self.cust_order[size]):
                order_list.append((self.cust_id,size))
        return order_list

class Cashier:
    def __init__(self, is_experienced:bool):
        if is_experienced:
            self._salary = 12  #$12/hr
            self._process_time = 0
        else:
            self._salary = 10  #$10/hr
            self._process_time = NormalDist(5,1,2,15).random()
        self.customer = None

    def busy(self):
        if self.customer != None:
            return True
        else:
            return False

    def get_process_time(self):
        return self._process_time

    def get_salary(self):
        return self._salary

class Chef:
    def __init__(self, is_experienced:bool):
        if is_experienced:
            self._salary = 17  #$17/hr
            self._prep_time = NormalDist(120,5,100,200).random()
        else:
            self._salary = 14  #$14/hr
            self._prep_time = NormalDist(200, 5, 150, 400).random()
        self.order = None

    def busy(self):
        if self.order != None:
            return True
        else:
            return False

    def get_salary(self):
        return self._salary

    def get_prep_time(self, size:str):
        if size == "S":
            return self._prep_time
        elif size == "M":
            return self._prep_time*1.5
        else:
            return self._prep_time*2

class Ice_creamShop:
    # shop opens from 10AM - 9PM (11 hours) 11hours = 39600 sec
    total_sec = 39600
    def __init__(self):
        exp_chef_num = random.randint(1, 2)
        new_chef_num = random.randint(0, 2)
        exp_cashier_num = random.randint(1, 2)
        new_cashier_num = random.randint(0, 1)

        self.chef_list, self.cashier_list = [],[]
        for i in range(exp_chef_num):
            self.chef_list.append(Chef(is_experienced=True))
        for i in range(new_chef_num):
            self.chef_list.append(Chef(is_experienced=False))
        for i in range(exp_cashier_num):
            self.cashier_list.append(Cashier(is_experienced=True))
        for i in range(new_cashier_num):
            self.cashier_list.append(Cashier(is_experienced=False))
        print("There are %s experienced chef, %s inexperienced chef, %s experienced cashier and %s inexperienced cashier in the shop."
              %(exp_chef_num, new_chef_num, exp_cashier_num, new_cashier_num))

    def total_variable_cost(self):
        chef_cost, cashier_cost = 0, 0
        for chef in self.chef_list:
            chef_cost += chef.get_salary()
        for cashier in self.cashier_list:
            cashier_cost += cashier.get_salary()
        return (chef_cost + cashier_cost)*(Ice_creamShop.total_sec/3600)

class Ordering():
    def __init__(self, cashier: Cashier):
        self.curr_customer = None
        self.time_remaining = 0
        self.cashier = cashier
        self.finishOrder = False

    def busy(self):
        if self.curr_customer != None:
            return True
        else:
            return False

    def tick(self):
        if self.busy():
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                print("=== %s: Customer %s completes ordering." % (seconds_to_hhmmss(self.order_complete_time), self.curr_customer.get_cust_id()))
                self.finishOrder = True
                self.curr_customer = None

    def startNext(self, new_customer:Customer, order_start_time):
        self.curr_customer = new_customer
        self.order_indiv = self.curr_customer.order_list()
        self.order_stats = [(self.curr_customer.get_cust_id(), len(self.curr_customer.order_list()))]
        self.time_remaining = new_customer.get_serving_time() + self.cashier.get_process_time()
        self.order_complete_time = order_start_time + self.time_remaining


class Preparing:
    count_ic_order = Counter()
    def __init__(self, chef:Chef):
        self.curr_order = None
        self.time_remaining = 0
        self.chef = chef
        self.finish_ic_order = False

    def busy(self):
        if self.curr_order != None:
            return True
        else:
            return False

    def tick(self):
        if self.busy():
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.finish_ic_order = True
                Preparing.count_ic_order[self.curr_order[0]] += 1
                self.cust_id = self.curr_order[0]
                self.curr_order = None

    def startNext(self, new_order, prepare_start_time):
        self.curr_order = new_order
        self.time_remaining = self.chef.get_prep_time(new_order[1])  #example of new_order: (cust_id, "S")
        self.prepare_end_time = prepare_start_time + self.time_remaining

def simulation(budget):
    while True:
        icshop = Ice_creamShop()
        cust_id = 0
        waitingtimes = []
        order_q = Queue()
        customer_num_ic = {}  #total number of ice-cream for each customer
        prep_q = Queue()
        if icshop.total_variable_cost() < budget:
            print("%s: Nitro Ice-cream Shop opens." % seconds_to_hhmmss(0))

            order_lis = []  # a list for different Ordering object (each cashier constructs an Ordering object)
            prepare_lis = []  # a list for different Preparing object (each chef constructs an Preparing object)
            for cashier in icshop.cashier_list:
                order_lis.append(Ordering(cashier))
            for chef in icshop.chef_list:
                prepare_lis.append(Preparing(chef))

            for currentSecond in range(Ice_creamShop.total_sec):
                if new_customer():
                    customer = Customer(cust_id + 1, currentSecond)
                    cust_id += 1
                    order_q.enqueue(customer)
                    print("+++ %s: New customer! Customer %s arrives." % (seconds_to_hhmmss(currentSecond), customer.get_cust_id()))

                for ordering in order_lis: # check if any cashier is not busy
                    if (not ordering.busy()) and (not order_q.isEmpty()):
                        next_customer = order_q.dequeue()
                        print(">>> %s: Start serving customer %s. Order: %s size S icecream, %s size M icecream and %s size L icecream"
                                          % (seconds_to_hhmmss(currentSecond),next_customer.cust_id, next_customer.s_icecream_num(), next_customer.m_icecream_num(),
                                             next_customer.l_icecream_num()))
                        ordering.startNext(next_customer, currentSecond)
                    ordering.tick()
                    if ordering.finishOrder:
                        customer_num_ic[ordering.order_stats[0][0]] = ordering.order_stats[0][1]
                        ordering.finishOrder = False
                        for ic_order in ordering.order_indiv:
                            prep_q.enqueue(ic_order)

                for preparing in prepare_lis:  # check if any chef is not busy
                    if (not preparing.busy()) and (not prep_q.isEmpty()):
                        next_ic_order = prep_q.dequeue()
                        preparing.startNext(next_ic_order,currentSecond)
                    preparing.tick()
                    if preparing.finish_ic_order and (Preparing.count_ic_order[preparing.cust_id] == customer_num_ic[preparing.cust_id]):
                        print("*** %s: Ice-cream ready! Customer %s's icecream order is completed!" % (
                        seconds_to_hhmmss(preparing.prepare_end_time), preparing.cust_id))
                        Preparing.count_ic_order[preparing.cust_id] = 0
                        preparing.finish_ic_order = False
            break

def new_customer():
    num = random.randrange(1,2000)  #need modification for peak/non-peak hour
    if num == 198:
        return True
    else:
        return False

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
        should return a random value
        :return:
        """
        pass

class NormalDist(RandomDist):
    def __init__(self, mu: float, sigma: float, low: float, high: float):
        """
        To use this class we must provide mu (mean), sigma (standard deviation), low value, and high value
        :param mu: mean, in which the normal gaussian will have most distribution
        :param sigma: a standard deviation for a random normal distribution parameter
        :param low: the lowest value this random generator must provide
        :param high: the highest value this random generator must provide
        """
        RandomDist.__init__(self, "Normal")
        self._mu = mu
        self._sigma = sigma
        self._low = low
        self._high = high

    def random(self):
        """
        This will return a random gaussian generator by checking the low value and highest value
        :return:
        """
        while True:
            x = random.gauss(self._mu, self._sigma)
            if x >= self._low and x <= self._high:
                return x

class GaussianDiscrete(NormalDist):
    """
    A random Gaussian Discrete generator
    This will include all the feature that gaussian has but will return a discrete value using round
    """

    def __init__(self, mu: float, sigma: float, low: float, high: float):
        """
        To use this class we must provide mu (mean), sigma (standard deviation), low value, and high value
        :param mu: mean, in which the normal gaussian will have most distribution
        :param sigma: a standard deviation for a random gaussian parameter
        :param low: the lowest value this random generator must provide
        :param high: the highest value this random generator must provide
        """
        NormalDist.__init__(self, mu, sigma, low, high)
        RandomDist.__init__(self, "GaussianDiscrete")

    def random(self):
        return round(NormalDist.random(self))

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


# class OrderingQueue(Queue):
#     def check_queue_number(self,cust_id) ->int:
#
#         for i in range(self.size()):
#             if self.items[i].cust_id==cust_id:
#                 return i
#         return 0
#
#     def get_total_queue_time(self) -> float:
#         '''
#         Get total waiting time for the entire queue
#         '''
#         total_queue_time=0
#         for i in range(1,self.size()):
#             temp_cust=self.items[i]
#             total_queue_time+=temp_cust.get_order_time()+temp_cust.get_thinking_time()
#         return total_queue_time
#
#     def get_queue_time(self, cust: Customer) ->float:
#         '''
#         Get waiting time for the customer
#         '''
#         q_index = self.check_queue_number(cust.cust_id)
#         queue_time = 0
#         for i in range(q_index + 1,self.size()):
#             temp_cust = self.items[i]
#             queue_time += temp_cust.get_order_time() + temp_cust.get_thinking_time()
#         return queue_time

# class Employee:
#     def __init__(self,is_experience=True):
#         self.is_experience=is_experience
#         if self.is_experience:
#             self.s_prep_time=NormalDist(120,5,100,200).random()
#         else:
#             self.s_prep_time = NormalDist(200, 5, 150, 400).random()
#
#     def make_ic_duration(self,icecream:list):
#         if icecream[2]=='L':
#             return self.s_prep_time*2
#         elif icecream[2]=='M':
#             return self.s_prep_time*1.5
#         else:
#             return self.s_prep_time
#
#
#     def make_ic_alone_duration(self,s_ic_num,m_ic_num,l_ic_num):
#         return self.s_prep_time*(s_ic_num+1.5*m_ic_num+2*l_ic_num)


# class IceCreamShop:
#     __employee_list=[]
#     def __init__(self):
#         self.exp_chef_num=random.randint(1,2)
#         self.new_chef_num=random.randint(0,2)
#         #self.ready_icecream=random.randint(0,5)
#         self.current_cust=None
#         self.remainingtime=0
#         self.ic_waiting_q=Queue()
#         self.current_ic=None
#         self.ic_remainingtime=0
#         self.complete_icecream=0
#         for i in range(self.exp_chef_num):
#             IceCreamShop.__employee_list.append(Employee())
#         for i in range(self.new_chef_num):
#             IceCreamShop.__employee_list.append(Employee(is_experience=False))
#
#     def is_serving(self):
#         if self.current_cust!=None:
#             return True
#         return False
#
#     def start_nextserving(self,next_cust:Customer):
#         self.current_cust=next_cust
#         #print(">>> Start serving customer %s. Order: %s icecream size S, %s icecream size M and %s icecream size L"
#         #      %(self.current_cust.cust_id,self.current_cust.s_icecream_num(),self.current_cust.m_icecream_num(),self.current_cust.l_icecream_num()))
#         self.remainingtime=next_cust.get_serving_time()
#
#     def servingtime_tick(self,current_second):
#         if self.is_serving():
#             self.remainingtime=self.remainingtime-1
#             if self.remainingtime<=0:
#                 print("*** %s: Customer %s completed ordering." %(time.strftime('%H:%M:%S', time.gmtime(36000+current_second)),self.current_cust.cust_id))
#                 self.add_icecream(self.current_cust)
#                 #print("Customer %s's order will be ready in %s seconds." %(self.current_cust.cust_id,max(self.make_ic_together_duration(self.current_cust))))
#                 self.current_cust=None
#
#     def is_preparing_ic(self):
#         if self.current_ic!=None:
#             return True
#         else:
#             return False
#
#     def start_nexticecream(self, next_ic: list):
#         self.current_ic = next_ic
#         self.ic_remainingtime = IceCreamShop.__employee_list[0].make_ic_duration(next_ic)
#
#     def ic_preparingtime_tick(self):
#         if self.current_ic!=None:
#             self.ic_remainingtime=self.ic_remainingtime-1
#         if self.ic_remainingtime<=0:
#             self.current_ic=None
#
#     def add_icecream(self,cust:Customer):
#         for size in cust.cust_order.keys():
#             if cust.cust_order[size]>0:
#                 for i in range(cust.cust_order[size]):
#                     self.ic_waiting_q.enqueue([cust.cust_id,1,size])

    #not using
    # def make_ic_together_duration(self,cust:Customer):
    #     prepare_time_list=[]
    #     if len(IceCreamShop.__employee_list)==1:
    #         return IceCreamShop.__employee_list[0].make_ic_alone_duration(cust.s_icecream_num(),cust.m_icecream_num(),cust.l_icecream_num())
    #     else:
    #         #[3,3,2,2]
    #         #[Chef1, Chef2, Chef3, Chef4]
    #         #{S:3,M:5,L:2}
    #         task_list=self.split_order(cust)
    #         ic_num_list=[cust.l_icecream_num(),cust.m_icecream_num(),cust.s_icecream_num()]
    #         for i in range(len(IceCreamShop.__employee_list)):
    #             temp_cust_order=[0,0,0]
    #             self.match_ic_to_chef(ic_num_list,task_list,temp_cust_order,i,0)
    #             print(temp_cust_order)
    #             prepare_time_list.append(IceCreamShop.__employee_list[i].make_ic_alone_duration(temp_cust_order[2],temp_cust_order[1],temp_cust_order[0]))
    #     return prepare_time_list

    #not using
    # def match_ic_to_chef(self,ic_num_list,task_list,temp_cust_order,i,j):
    #     if j < 3:
    #         if ic_num_list[j] >= task_list[i]:
    #             temp_cust_order[j] = task_list[i]
    #             ic_num_list[j] = ic_num_list[j] - task_list[i]
    #             task_list[i] = 0
    #         else:
    #             temp_cust_order[j] = ic_num_list[j]
    #             task_list[i] = task_list[i] - ic_num_list[j]
    #             ic_num_list[j] = 0
    #             self.match_ic_to_chef(ic_num_list, task_list, temp_cust_order, i, j + 1)
    #
    #
    # def split_order(self,cust:Customer):
    #     task_list=[cust.get_total_icecream()//len(IceCreamShop.__employee_list)]*len(IceCreamShop.__employee_list)
    #     remainder=cust.get_total_icecream()%len(IceCreamShop.__employee_list)
    #     remainder_list=[1]*remainder+[0]*(len(IceCreamShop.__employee_list)-remainder)
    #     return [sum(x) for x in zip(task_list,remainder_list)]



# def icshop_simulation(second_count):
#     icshop=IceCreamShop()
#     ordering_q=OrderingQueue()
#     waitingtimes=[]
#     cust_id=0
#     tmp_cust_id=0
#     print("Start simulating the ice cream shop for %s seconds..." %second_count)
#     print("%s: Nitro Ice-cream Shop opens." %seconds_to_hhmmss(0))
#     print("Number of experienced chefs = %s\nNumber of new chefs = %s" %(icshop.exp_chef_num,icshop.new_chef_num))
#     for current_second in range(second_count):
#         if new_customer():
#             new_cust=Customer(cust_id+1,current_second)
#             ordering_q.enqueue(new_cust)
#             print("+++ %s: New customer! Customer %s arrives." % (seconds_to_hhmmss(current_second),new_cust.get_cust_id()))
#             queue_time=ordering_q.get_queue_time(new_cust)
#             if icshop.current_cust!=None:
#                 current_serving_remaintime = icshop.current_cust.get_serving_time() - (current_second - icshop.current_cust.get_arrivaltime())
#             else:
#                 current_serving_remaintime=0
#             waiting_time=queue_time+current_serving_remaintime
#             waitingtimes.append(waiting_time)
#             if waiting_time>0:
#                 print("Customer %s waits for %s until his turn." %(new_cust.cust_id,seconds_to_mmss(int(waiting_time)+1)))
#             cust_id+=1
#         if not icshop.is_serving() and ordering_q.size()>0:
#             next_cust=ordering_q.dequeue()
#             print(">>> %s: Start serving customer %s. Order: %s icecream size S, %s icecream size M and %s icecream size L"
#                   % (seconds_to_hhmmss(current_second),next_cust.cust_id, next_cust.s_icecream_num(), next_cust.m_icecream_num(),
#                      next_cust.l_icecream_num()))
#             icshop.start_nextserving(next_cust)
#         icshop.servingtime_tick(current_second)
#         if not icshop.is_preparing_ic() and icshop.ic_waiting_q.size()>0:
#             #print("Current cust id=",tmp_cust_id)
#             next_ic=icshop.ic_waiting_q.dequeue()
#             #print("Next cust id=", next_ic[0])
#             if tmp_cust_id!=next_ic[0] and tmp_cust_id!=0:
#                 print("*** %s: Ice-cream ready! Customer %s's icecream order is completed!" %(seconds_to_hhmmss(current_second),tmp_cust_id))
#             tmp_cust_id=next_ic[0]
#             icshop.start_nexticecream(next_ic)
#         icshop.ic_preparingtime_tick()
#
#     if ordering_q.size()>0:
#         print("List of Customers still in queue:")
#         for cust in ordering_q.items:
#             print(cust.cust_id,cust.cust_order,cust.arrival_time,cust.order_time,cust.thinking_time)
#     print("Waiting time of all customers: \n",waitingtimes)
#
#     if icshop.ic_waiting_q.size()>0:
#         print("Icecream waiting q:")
#         for icecream in icshop.ic_waiting_q.items:
#             print(icecream)

def seconds_to_hhmmss(second_number):
    return time.strftime('%H:%M:%S', time.gmtime(36000+second_number))

def seconds_to_mmss(second_number):
    return time.strftime('%M minutes and %S seconds', time.gmtime(second_number))


# def new_customer():
#     num=random.randint(0,600)
#     if num==50:
#         return True
#     else:
#         return False


if __name__ == '__main__':
    #icshop_simulation(10000)
    simulation(1000)



