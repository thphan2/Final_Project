import random
import time
from collections import Counter
import sys

class Customer:
    # cust_order example: {'S':1, 'M':2 'L':1}
    def __init__(self, cust_id, arrival_time):
        self._cust_id = cust_id
        self._cust_order = {'S': GaussianDiscrete(1,1,0,5).random(), 'M': GaussianDiscrete(1,1,0,5).random(), 'L':GaussianDiscrete(2,1,0,5).random()}
        self._arrival_time = arrival_time
        self._order_time = NormalDist(120,3,60,300).random()
        self._thinking_time = random.uniform(0,120)

    def get_cust_id(self):
        return self._cust_id

    def get_total_icecream(self):
        return self.s_icecream_num()+self.m_icecream_num()+self.l_icecream_num()

    def s_icecream_num(self):
        return self._cust_order['S']

    def m_icecream_num(self):
        return self._cust_order['M']

    def l_icecream_num(self):
        return self._cust_order['L']

    def get_arrivaltime(self):
        return self._arrival_time

    def get_order_time(self):
        return self._order_time

    def get_thinking_time(self):
        return self._thinking_time

    def get_serving_time(self):
        return self._order_time+self._thinking_time

    def order_list(self):
        order_list = []
        for size in self._cust_order:
            for num in range(self._cust_order[size]):
                order_list.append((self._cust_id,size,self.get_arrivaltime()))
        return order_list

class Employee:
    # base class for all kinds of employee
    def __init__(self, id, is_experienced:bool):
        self.id = id
        self.is_experienced = is_experienced

    def get_salary(self):
        pass

class Cashier(Employee):
    def __init__(self, id, is_experienced:bool):
        Employee.__init__(self,id,is_experienced)
        if is_experienced:
            self._salary = 12  #$12/hr
            self._process_time = 0
        else:
            self._salary = 10  #$10/hr
            self._process_time = NormalDist(5,1,2,15).random()

    def get_process_time(self):
        return self._process_time

    def get_salary(self):
        return self._salary

class Chef(Employee):
    def __init__(self, id, is_experienced:bool):
        Employee.__init__(self, id, is_experienced)
        if is_experienced:
            self._salary = 17  #$17/hr
            self._prep_time = NormalDist(60,5,30,90).random()
        else:
            self._salary = 14  #$14/hr
            self._prep_time = NormalDist(120, 5, 70, 180).random()

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
    # shop opens from 12PM - 10PM (10 hours) 10hours = 36000 sec
    total_sec = 36000
    def __init__(self,exp_chef_num,new_chef_num,exp_cashier_num,new_cashier_num):
        self.price_S = 4
        self.price_M = 6
        self.price_L = 8
        #self.rawMaterial_cost = 200
        self.chef_list, self.cashier_list = [],[]

        for i in range(new_chef_num):
            self.chef_list.append(Chef(i+1,is_experienced=False))
        for i in range(exp_chef_num):
            self.chef_list.append(Chef(new_chef_num+i+1, is_experienced=True))
        for i in range(new_cashier_num):
            self.cashier_list.append(Cashier(i+1,is_experienced=False))
        for i in range(exp_cashier_num):
            self.cashier_list.append(Cashier(new_cashier_num+i+1,is_experienced=True))

        self.total_s_ic=0
        self.total_m_ic=0
        self.total_l_ic=0
        self.total_ic_num = 0

    def update_total_s_ic(self,s_ic_num):
        self.total_s_ic=self.total_s_ic+s_ic_num

    def update_total_m_ic(self,m_ic_num):
        self.total_m_ic=self.total_m_ic+m_ic_num

    def update_total_l_ic(self,l_ic_num):
        self.total_l_ic=self.total_l_ic+l_ic_num

    def update_ic_num(self, s_ic, m_ic, l_ic):
        # 1 medium ice_cream ~ 1.5 small ice_cream; 1 large ice_cream ~ 2 small ice_cream in terms of quantity/raw material
        self.total_ic_num = (s_ic + m_ic*1.5 + l_ic*2)

    def total_variable_cost(self):
        chef_cost, cashier_cost = 0, 0
        for chef in self.chef_list:
            chef_cost += chef.get_salary()
        for cashier in self.cashier_list:
            cashier_cost += cashier.get_salary()
        return (chef_cost + cashier_cost)*(Ice_creamShop.total_sec/3600)

    def is_within_budget(self,budget):
        if Ice_creamShop.total_variable_cost(self) <= budget:
            return True
        return False

    def find_emp_combination(self,budget,exp_chef_sal,new_chef_sal,exp_cash_sal,new_cash_sal):
        onehour_budget=budget/Ice_creamShop.total_sec*3600

        max_chefs=int(onehour_budget-exp_chef_sal-exp_cash_sal/new_chef_sal)
        max_cashiers=int(onehour_budget-exp_chef_sal-exp_cash_sal/new_cash_sal)

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

    def tick(self,timelog=True):
        if self.busy():
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                if timelog:
                    print("=== %s: Customer %s completes ordering." % (seconds_to_hhmmss(self.order_complete_time), self.curr_customer.get_cust_id()))
                self.finishOrder = True
                self.curr_customer = None

    def startNext(self, new_customer:Customer, order_start_time):
        self.curr_customer = new_customer
        self.order_indiv = self.curr_customer.order_list()
        # total number of ice-cream the customer orders
        self.order_stats = (self.curr_customer.get_cust_id(), len(self.curr_customer.order_list()))
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
                self.arrival_time = self.curr_order[-1]
                self.curr_order = None

    def startNext(self, new_order, prepare_start_time):
        self.curr_order = new_order
        self.time_remaining = self.chef.get_prep_time(new_order[1])  #example of new_order: (cust_id, "S", arrival time)
        self.prepare_end_time = prepare_start_time + self.time_remaining

def simulation(exp_chef_num,new_chef_num,exp_cashier_num,new_cashier_num, budget, filename, timelog = True):
    icshop = Ice_creamShop(exp_chef_num,new_chef_num,exp_cashier_num,new_cashier_num)
    cust_id = 0
    ordering_waitingtimes = []
    waitingtimes = []
    order_q = Queue()
    prep_q = Queue()
    customer_num_ic = {}  #total number of ice-cream for each customer (to check if prep is finished for a certain customer)
    if icshop.is_within_budget(budget):
        if timelog:
            print("%s: Nitro Ice-cream Shop opens." % seconds_to_hhmmss(0))

        order_lis = []  # a list for different Ordering object (each cashier constructs an Ordering object)
        prepare_lis = []  # a list for different Preparing object (each chef constructs an Preparing object)
        for cashier in icshop.cashier_list:
            order_lis.append(Ordering(cashier))
        for chef in icshop.chef_list:
            prepare_lis.append(Preparing(chef))

        cashier_index = 0
        chef_index=0
        revenue = 0
        for currentSecond in range(sys.maxsize):
            # shop stops taking new order at 9:45pm
            if currentSecond<Ice_creamShop.total_sec-900:
                if new_customer(currentSecond):
                    customer = Customer(cust_id + 1, currentSecond)
                    cust_id += 1
                    order_q.enqueue(customer)
                    if timelog:
                        print("+++ %s: New customer! Customer %s arrives." % (seconds_to_hhmmss(currentSecond), customer.get_cust_id()))

            for ordering in order_lis: # check if any cashier is not busy
                if (not ordering.busy()) and (not order_q.isEmpty()):
                    next_customer = order_q.dequeue()
                    icshop.update_total_s_ic(next_customer.s_icecream_num())
                    icshop.update_total_m_ic(next_customer.m_icecream_num())
                    icshop.update_total_l_ic(next_customer.l_icecream_num())
                    ordering_waitingtimes.append(currentSecond - next_customer.get_arrivaltime())
                    ordering.startNext(next_customer, currentSecond)
                else:
                    ordering.tick(timelog)
                if ordering.finishOrder:
                    customer_num_ic[ordering.order_stats[0]] = ordering.order_stats[1]
                    ordering.finishOrder = False
                    for ic_order in ordering.order_indiv:
                        prep_q.enqueue(ic_order)
                        if ic_order[1] == "S":
                            revenue += icshop.price_S
                        elif ic_order[1] == "M":
                            revenue += icshop.price_M
                        else:
                            revenue += icshop.price_L

            for preparing in prepare_lis:  # check if any chef is not busy
                if (not preparing.busy()) and (not prep_q.isEmpty()):
                    next_ic_order = prep_q.dequeue()
                    preparing.startNext(next_ic_order,currentSecond)
                else:
                    preparing.tick()
                if preparing.finish_ic_order and (Preparing.count_ic_order[preparing.cust_id] == customer_num_ic[preparing.cust_id]):
                    if timelog:
                        print("*** %s: Ice-cream ready! Customer %s's icecream order is completed!" % (
                    seconds_to_hhmmss(preparing.prepare_end_time), preparing.cust_id))
                    # waiting time for each customer
                    waitingtimes.append(currentSecond-preparing.arrival_time)
                    Preparing.count_ic_order[preparing.cust_id] = 0
                    preparing.finish_ic_order = False
            if timelog and currentSecond==Ice_creamShop.total_sec-900:
                print("%s: Shop is closing in 15 minutes, no new orders accepted." %seconds_to_hhmmss(currentSecond))
                print("Finishing the remaining orders...")
            if currentSecond>=Ice_creamShop.total_sec and order_q.isEmpty() and prep_q.isEmpty():
                if timelog:
                    print("%s: All orders completed. \nThere are %s customers coming in today. Average waiting time: %s minutes.\nTotal revenue is: $%s dollars. Today's profit is: $%s" \
                              %(seconds_to_hhmmss(currentSecond), len(waitingtimes),round((sum(waitingtimes)/len(waitingtimes))/60),"{:,}".format(revenue),"{:,}".format(revenue - icshop.total_variable_cost())))
                    print("Icecream Shop closes for the day. See you again!")
                break

        icshop.update_ic_num(icshop.total_s_ic, icshop.total_m_ic, icshop.total_l_ic)
        preparing_waitingtimes = [i - j for i, j in zip(waitingtimes, ordering_waitingtimes)]
        outfile=open(filename+".csv","a")
        #File header: #exp_chef,#new_chef,#exp_cashier,#new_cashier,#total_s_icecream,#total_m_icecream,#total_l_icecream,#average ice_cream number,#customers,avg_waiting_time, profit
        print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %\
              (exp_chef_num,new_chef_num,exp_cashier_num,new_cashier_num,icshop.total_s_ic,icshop.total_m_ic,icshop.total_l_ic,icshop.total_ic_num,len(waitingtimes),round((sum(preparing_waitingtimes)/len(waitingtimes))/60),round((sum(ordering_waitingtimes)/len(waitingtimes))/60),round((sum(waitingtimes)/len(waitingtimes))/60),revenue - icshop.total_variable_cost()),file=outfile)
        outfile.close()
    else:
        if timelog:
            print("Budget is not enough. Please adjust employee numbers.")


# More customers come from 3PM - 5PM and 7PM - 8:30PM
def new_customer(currentSecond):
    if (10800 < currentSecond < 18000) or (25200 < currentSecond < 30600):
        num = random.randrange(1,240) #peak-hour: customer/240 sec on average
        if num == 20:
            return True
        else:
            return False
    else:
        num = random.randrange(1,2400) #non-peak hour: customer/2400 sec on average
        if num == 800:
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

def seconds_to_hhmmss(second_number):
    # time starts at 12pm (12*3600 = 43200) as the shop opens
    return time.strftime('%H:%M:%S%p', time.gmtime(43200+second_number))

if __name__ == '__main__':
    count=0
    for exp_chef_num in range (1,3):
        for new_chef_num in range (0,2):
            for exp_cashier_num in range(1,3):
                for new_cashier_num in range(0,2):
                    for i in range(5):
                        count+=1
                        print(count)
                        simulation(exp_chef_num,new_chef_num,exp_cashier_num,new_cashier_num,1000, "sample", True)
