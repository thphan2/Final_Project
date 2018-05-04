"""
590PR Spring 2018
Authors: Yuejun Wu, Thuong Phan
Final Project: Nitrogen Ice-cream Shop Monte Carlo Simulation


Add new customers
>>> cu1=Customer(1,120)
>>> has_raw_material(cu1,0)
False
>>> has_raw_material(cu1,1000000)
True

Add new cashiers
>>> ca1=Cashier(1,True)
>>> ca2=Cashier(2,False)
>>> ca1.get_salary()
12
>>> ca2.get_salary()
10

Add new chefs
>>> ch3=Chef(3,True)
>>> ch4=Chef(4,False)
>>> ch3.get_salary()
17
>>> ch4.get_salary()
14

Icecream shop test
>>> shop=Ice_creamShop(1,2,1,0)
>>> shop.total_variable_cost()
570.0
>>> shop.is_within_budget(500)
False
>>> shop.is_within_budget(1500)
True
>>> shop.update_total_s_ic(2)
>>> shop.total_s_ic
2
>>> shop.update_total_m_ic(9)
>>> shop.total_m_ic
9
>>> shop.update_total_l_ic(5)
>>> shop.total_l_ic
5
>>> shop.update_ic_num(shop.total_s_ic,shop.total_m_ic,shop.total_l_ic)
>>> shop.total_ic_num
25.5

"""

import random
from random import shuffle
import time
from collections import Counter
import sys


class Customer:
    # cust_order example: {'S':1, 'M':2 'L':1}
    def __init__(self, cust_id:int, arrival_time:int):
        """
        Customer visits the shop to buy icecream.
        A customer requires below information:
        - customer id to identify the customer (cust_id)
        - arrival time (arrival_time)
        - customer order containing the amount of icecream in each size he wants to buy (cust_order: dict)
        - amount of time to make the order (order_time)
        - amount of time to think about what to order (thinking_time)
        :param cust_id: customer id
        :param arrival_time: the second the customer arrives after the shop opens
        """
        self._cust_id = cust_id
        self._cust_order = {'S': GaussianDiscrete(1,1,1,5).random(), 'M': GaussianDiscrete(1,1,0,5).random(), 'L':GaussianDiscrete(2,1,0,5).random()}
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
        """
        Get the total amount of time for making order which equals the amount of time for ordering + thinking
        """
        return self._order_time+self._thinking_time

    def order_list(self)->list:
        """
        Convert the order dictionary of the customer to a list of ice-creams
        """
        order_list = []
        for size in self._cust_order:
            for num in range(self._cust_order[size]):
                order_list.append((self._cust_id,size,self.get_arrivaltime()))
        return order_list


class Employee:
    # base class for all kinds of employee
    def __init__(self, id, is_experienced:bool):
        """
        Employee of the ice cream shop
        :param id: employee id to identify an employee
        :param is_experienced: whether the employee has any experience (True or False)

        """
        self.id = id
        self.is_experienced = is_experienced

    def get_salary(self):
        pass


class Cashier(Employee):
    def __init__(self, id:int, is_experienced:bool):
        """
        Cashier is the person who takes order from customers.
        Each cashier requires data about his ID, experience level, salary based on the experience and the required time to process an order
        :param id: cashier id to identify an cashier, automatically assigned when a cashier is added
        :param is_experienced: whether the cashier has any experience (True or False)
        """
        Employee.__init__(self,id,is_experienced)
        if is_experienced:
            self._salary = 12  #$12/hr
            self._process_time = 0
        else:
            self._salary = 10  #$10/hr
            self._process_time = NormalDist(5,1,2,15).random()

    def get_process_time(self):
        """
        Return the amount of time a cashier needs to take order from a customer
        """
        return self._process_time

    def get_salary(self):
        """
        Return the salary of a cashier
        """
        return self._salary


class Chef(Employee):
    def __init__(self, id, is_experienced:bool):
        """
        Chef is the person who makes icecream for customers
        Each chef requires info about his ID, experience level, salary based on the experience and the required time to process an icecream based on the icecream size
        :param id: chef id to identify an chef, automatically assigned when a chef is added
        :param is_experienced: whether the chef has any experience (True or False)
        """
        Employee.__init__(self, id, is_experienced)
        if is_experienced:
            self._salary = 17  #$17/hr
            self._prep_time = NormalDist(60,5,30,90).random()
        else:
            self._salary = 14  #$14/hr
            self._prep_time = NormalDist(120, 5, 70, 180).random()

    def get_salary(self):
        """
        Return the salary of a chef
        """
        return self._salary

    def get_prep_time(self, size:str):
        """
        Return the preparation time for an icecream based on its size
        :param size: size of an icecream (S, M or L)
        :return: preparation time
        """
        if size == "S":
            return self._prep_time
        elif size == "M":
            return self._prep_time*1.5
        else:
            return self._prep_time*2


class Ice_creamShop:
    # shop opens from 12PM - 10PM (10 hours) 10hours = 36000 sec
    total_sec = 36000
    def __init__(self,exp_chef_num:int,new_chef_num:int,exp_cashier_num:int,new_cashier_num:int):
        """
        An icecream shop requires information about
        - number of experienced and non-experienced chefs it has for a day (exp_chef_num, new_chef_num)
        - number of experienced and non-experienced cashiers it has for a day (exp_cashier_num, new_cashier_num)
        - icecream price for different sizes S, M and L (price_S, price_M, price_L)
        - the current amount of raw material to make icecream (raw_material_cost)
        - a check variable whether it has enough raw material (is_enough_raw_material)
        - list of chefs and cashiers it has (chef_list, cashier_list)
        - total number of icecream size S, M and L it has sold for the day (total_s_ic, total_m_ic, total_l_ic)
        - total number of icecream units it has sold for the day (total_ic_num)
        :param exp_chef_num: number of experienced chefs
        :param new_chef_num: number of non-experienced chefs
        :param exp_cashier_num: number of experienced cashiers
        :param new_cashier_num: number of non-experienced cashiers
        """
        self.price_S = 4
        self.price_M = 6
        self.price_L = 8
        self.raw_material_cost = 200
        self.is_enough_raw_material = True
        self.chef_list, self.cashier_list = [],[]
        self.total_s_ic=0
        self.total_m_ic=0
        self.total_l_ic=0
        self.total_ic_num = 0

        for i in range(new_chef_num):
            self.chef_list.append(Chef(i+1,is_experienced=False))
        for i in range(exp_chef_num):
            self.chef_list.append(Chef(new_chef_num+i+1, is_experienced=True))
        for i in range(new_cashier_num):
            self.cashier_list.append(Cashier(i+1,is_experienced=False))
        for i in range(exp_cashier_num):
            self.cashier_list.append(Cashier(new_cashier_num+i+1,is_experienced=True))

    def update_total_s_ic(self,s_ic_num:int):
        """
        Update the total icecream size S the shop has sold so far
        :param s_ic_num: number of icecream size S ordered by a customer
        :return: None
        """
        self.total_s_ic=self.total_s_ic+s_ic_num

    def update_total_m_ic(self,m_ic_num:int):
        """
        Update the total icecream size M the shop has sold so far
        :param m_ic_num: number of icecream size M ordered by a customer
        :return: None
        """
        self.total_m_ic=self.total_m_ic+m_ic_num

    def update_total_l_ic(self,l_ic_num:int):
        """
        Update the total icecream size L the shop has sold so far
        :param l_ic_num: number of icecream size L ordered by a customer
        :return: None
        """
        self.total_l_ic=self.total_l_ic+l_ic_num

    def update_ic_num(self, s_ic:int, m_ic:int, l_ic:int):
        """
        Convert icecreams of different size into icecream units
        1 medium ice_cream ~ 1.5 small ice_cream; 1 large ice_cream ~ 2 small ice_cream in terms of quantity/raw material
        :param s_ic: number of S size icecream
        :param m_ic: number of M size icecream
        :param l_ic: number of L size icecream
        :return: None
        """
        self.total_ic_num = (s_ic + m_ic*1.5 + l_ic*2)

    def total_variable_cost(self)->float:
        """
        Return the total variable cost for paying salary to employees
        """
        chef_cost, cashier_cost = 0, 0
        for chef in self.chef_list:
            chef_cost += chef.get_salary()
        for cashier in self.cashier_list:
            cashier_cost += cashier.get_salary()
        return (chef_cost + cashier_cost)*(Ice_creamShop.total_sec/3600)

    def is_within_budget(self,budget)->bool:
        """
        Check whether the variable cost is within the shop's budget
        :param budget: the budget set by the shop for variable cost
        :return: whether the variable cost is within the budget (True or False)
        """
        return Ice_creamShop.total_variable_cost(self) <= budget - self.raw_material_cost


class Ordering():
    '''
    Ordering class instantiates order process between one customer and a cashier
    '''
    def __init__(self, cashier: Cashier):
        '''
        Each ordering process requires information about:
        - curr_customer: if there is a customer being served
        - time_remaining: the remaining time of the order
            (calculated based on customer's ordering time, thinking time and cashier's process time - the time has passed)
        - cashier: the cashier of ordering object
        - finishOrder: flag of whether the order is finished
        - order_indiv: a list of all ice-cream one customer ordered
        - order_stats: record information of customer id, and the number of ice-cream this customer ordered
        - order_complete_time: record order completion timestamp
        :param cashier: cashier object
        '''
        self.curr_customer = None
        self.time_remaining = 0
        self.cashier = cashier
        self.finishOrder = False
        self.order_indiv=[]
        self.order_stats=((),)
        self.order_complete_time=0

    def busy(self) ->bool:
        '''
        Check wether a cashier is serving customer or not
        :return: bool
        '''
        if self.curr_customer != None:
            return True
        else:
            return False

    def tick(self,timelog=True):
        '''
        A function helps keep track of whether an order is completed or not based on remaining time

        :param timelog: whether to show the printing message or not
        :return: None
        '''
        if self.busy():
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                if timelog:
                    print("=== %s: Customer %s completes ordering." % (seconds_to_hhmmss(self.order_complete_time), self.curr_customer.get_cust_id()))
                self.finishOrder = True
                self.curr_customer = None

    def startNext(self, new_customer:Customer, order_start_time):
        '''
        new customer will be served

        :param new_customer:
        :param order_start_time:
        :return:
        '''
        self.curr_customer = new_customer
        self.order_indiv = self.curr_customer.order_list()
        # total number of ice-cream the customer orders
        self.order_stats = (self.curr_customer.get_cust_id(), len(self.curr_customer.order_list()))
        self.time_remaining = new_customer.get_serving_time() + self.cashier.get_process_time()
        self.order_complete_time = order_start_time + self.time_remaining


class Preparing:
    '''
    Preparing class instantiates one chef's preparation process of one ice-cream
    '''
    count_ic_order = Counter()  # record the number of each customer's current completed ice-cream
                                # (to check if one customer has all his/her order completed)
    def __init__(self, chef:Chef):
        '''
        Each preparing process requires information about:
        - curr_order: if there is an order being processed by the chef
        - time_remaining: the remaining time of the order
            (calculated based on chef's processing time - the time has passed)
        - chef: the chef of preparing object
        - finish_ic_order: flag of whether the one ice-cream order is finished
        - arrival_time: customer's arrival time (for calculating waiting time in simulation)
        - prepare_end_time: record one icecream 's completion timestamp
        :param chef: chef object
        '''
        self.curr_order = None
        self.time_remaining = 0
        self.chef = chef
        self.finish_ic_order = False
        self.arrival_time = 0
        self.prepare_end_time = 0

    def busy(self) ->bool:
        '''
        Check wether a chef is processing order or not
        :return: bool
        '''
        if self.curr_order is not None:
            return True
        else:
            return False

    def tick(self):
        if self.busy():
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.finish_ic_order = True
                Preparing.count_ic_order[self.curr_order[0]] += 1
                self.arrival_time = self.curr_order[-1]
                self.curr_order = None

    def startNext(self, new_order, prepare_start_time):
        self.curr_order = new_order
        self.cust_id = self.curr_order[0]
        self.time_remaining = self.chef.get_prep_time(new_order[1])  #example of new_order: (cust_id, "S", arrival time)
        self.prepare_end_time = prepare_start_time + self.time_remaining


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


def has_raw_material(customer:Customer, raw_material_cost:float)->bool:
    """
    check whether the shop has enough raw material for the customer's icecream order
    :param customer: Customer
    :param raw_material_cost: the remaining raw material the shop has currently
    :return: bool
    """
    return customer.s_icecream_num() + customer.m_icecream_num()*1.5 + customer.l_icecream_num()*2 <= raw_material_cost


def simulation(exp_chef_num,new_chef_num,exp_cashier_num,new_cashier_num, budget, filename="default", timelog = True):
    if (exp_chef_num == new_chef_num == 0):
        print("Wrong simulation. Shop cannot operate without a chef!")
    elif (exp_cashier_num == new_cashier_num == 0):
        print("Wrong simulation. Shop cannot operate without a cashier!")
    else:
        icshop = Ice_creamShop(exp_chef_num,new_chef_num,exp_cashier_num,new_cashier_num)
        cust_id = 0
        finish_status=False
        last_customer_id=0
        ordering_waitingtimes = []  # keep track of each cutomer's ordering waiting time
        waitingtimes = []  # keep track of each customer's overall waiting time (ordering waiting time + preparing waiting time)
        order_q = Queue()
        prep_q = Queue()
        customer_num_ic = {}  # total number of ice-cream for each customer (to check if prep is finished for a certain customer)
        if icshop.is_within_budget(budget):
            if timelog:
                print("%s: Nitro Ice-cream Shop opens." % seconds_to_hhmmss(0))

            order_lis = []  # a list for different Ordering object (each cashier constructs an Ordering object)
            prepare_lis = []  # a list for different Preparing object (each chef constructs an Preparing object)
            for cashier in icshop.cashier_list:
                order_lis.append(Ordering(cashier))
            for chef in icshop.chef_list:
                prepare_lis.append(Preparing(chef))

            revenue = 0
            for currentSecond in range(sys.maxsize):
                # shop stops taking new order at 9:45pm or running out of raw material
                if currentSecond<Ice_creamShop.total_sec-900 and icshop.is_enough_raw_material==True :
                    if new_customer(currentSecond):
                        customer = Customer(cust_id + 1, currentSecond)
                        cust_id += 1

                        # check if raw material is enough for making ice-cream
                        if has_raw_material(customer,icshop.raw_material_cost):
                            order_q.enqueue(customer)
                            if timelog:
                                print("+++ %s: New customer! Customer %s arrives." % (seconds_to_hhmmss(currentSecond), customer.get_cust_id()))
                            icshop.raw_material_cost -= (customer.s_icecream_num() + customer.m_icecream_num() * 1.5 + customer.l_icecream_num() * 2)
                        else:
                            icshop.is_enough_raw_material=False
                            last_customer_id=customer.get_cust_id()-1
                            if timelog:
                                print("Shop will run out of raw material soon. Only take order till customer ID %s. Stop taking new customers now!" %last_customer_id)

                # avoid first cashier does most the work
                shuffle(order_lis)
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

                    # when each ordering process is finished, add all ice-cream orders into prep_q
                    if ordering.finishOrder:
                        # record total ice-cream number for the customer who has finished ordering
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

                # avoid first chef in the list does most the work
                shuffle(prepare_lis)
                for preparing in prepare_lis:  # check if any chef is not busy
                    if (not preparing.busy()) and (not prep_q.isEmpty()):
                        next_ic_order = prep_q.dequeue()
                        preparing.startNext(next_ic_order,currentSecond)
                    else:
                        preparing.tick()

                    # By checking number of ice-cream in each dictionary, we will know whether the order for one customer is finished or not
                    if preparing.finish_ic_order and (Preparing.count_ic_order[preparing.cust_id] == customer_num_ic[preparing.cust_id]):
                        if preparing.cust_id==last_customer_id:
                            finish_status=True
                        Preparing.count_ic_order[preparing.cust_id]=0
                        if timelog:
                            print("*** %s: Ice-cream ready! Customer %s's icecream order is completed!" % (
                        seconds_to_hhmmss(preparing.prepare_end_time), preparing.cust_id))
                        # waiting time for each customer
                        waitingtimes.append(currentSecond-preparing.arrival_time)
                        preparing.finish_ic_order = False

                if timelog and currentSecond==Ice_creamShop.total_sec-900:
                    print("%s: Shop is closing in 15 minutes, no new orders accepted." %seconds_to_hhmmss(currentSecond))
                    print("Finishing the remaining orders...")
                #print("Order q:",order_q.items)
                #print("Prep q:", prep_q.items)
                #if (currentSecond >= Ice_creamShop.total_sec and order_q.isEmpty() and prep_q.isEmpty()) or \
                        #(icshop.is_enough_raw_material == False and order_q.isEmpty() and prep_q.isEmpty()):
                if (icshop.is_enough_raw_material == False and finish_status==True and order_q.isEmpty() and prep_q.isEmpty()):
                    if timelog:
                        print("%s: All orders completed. \nThere are %s customers coming in today. Average waiting time: %s minutes.\
                        \nTotal revenue is: $%s dollars. Today's profit is: $%s" \
                                  %(seconds_to_hhmmss(currentSecond), len(waitingtimes),round((sum(waitingtimes)/len(waitingtimes))/60),\
                                    "{:,}".format(revenue),"{:,}".format(revenue - icshop.total_variable_cost())))
                        print("Icecream Shop closes for the day. See you again!")
                    break

            icshop.update_ic_num(icshop.total_s_ic, icshop.total_m_ic, icshop.total_l_ic)
            preparing_waitingtimes = [i - j for i, j in zip(waitingtimes, ordering_waitingtimes)]
            if not timelog:
                outfile=open(filename+".csv","a")
                # File header: #exp_chef,#new_chef,#exp_cashier,#new_cashier,#total_s_icecream, #total_m_icecream, #total_l_icecream, #average ice_cream number,
                # #customers, avg_ordering_time, avg_preparing time, avg_waiting_time, profit
                print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %\
                      (exp_chef_num,new_chef_num,exp_cashier_num,new_cashier_num,icshop.total_s_ic,icshop.total_m_ic,icshop.total_l_ic,icshop.total_ic_num,\
                       len(waitingtimes),round((sum(ordering_waitingtimes)/len(waitingtimes))/60),round((sum(preparing_waitingtimes)/len(waitingtimes))/60),\
                       round((sum(waitingtimes)/len(waitingtimes))/60),revenue - icshop.total_variable_cost()),file=outfile)
                outfile.close()
        else:
            if timelog:
                print("Budget is not enough. Please adjust employee numbers.")


def new_customer(currentSecond:int)->bool:
    """
    Randomly generate a customer coming to the icecream shop during peak hour and non-peak hour
    Assume that more customers come from 3PM - 5PM and 7PM - 8:30PM
    During peak hour, every 240 seconds (4 mins) there is a customer
    During non-peak hour, every 1200 seconds (20 mins) there is a customer
    :param currentSecond: the current second after the shop opens
    :return: whether a customer arrives (True or False)
    """
    if (10800 < currentSecond < 18000) or (25200 < currentSecond < 30600):
        num = random.randrange(1,240) #peak-hour: customer/240 sec on average
        if num == 20:
            return True
        else:
            return False
    else:
        num = random.randrange(1,1200) #non-peak hour: customer/1200 sec on average
        if num == 800:
            return True
        else:
            return False


def seconds_to_hhmmss(second_number:int):
    """
    convert the second number to current date time with format HH:MM:SS(AM/PM)
    Note that time starts at 12pm (12*3600 = 43200) as the shop opens
    >>> seconds_to_hhmmss(240)
    '12:04:00PM'
    """
    return time.strftime('%H:%M:%S%p', time.gmtime(43200+second_number))


if __name__ == '__main__':
    # simulate a situation when there are 2 experienced chef, 1 new chef, 1 experienced cashier in the shop, show time log
    random.seed(1)
    simulation(2,1,1,0, 5000, "", True)

