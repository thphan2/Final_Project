import Employee
import Customer
import time
from collections import Counter

class Ordering:
    # Ordering class instantiates order process between one customer and a cashier

    def __init__(self, cashier: Employee.Cashier):
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
        self.order_indiv = []
        self.order_stats = ((),)
        self.order_complete_time = 0

    def busy(self) ->bool:
        '''
        Check whether a cashier is serving customer or not
        :return: bool
        '''
        if self.curr_customer is not None:
            return True
        else:
            return False

    def tick(self, timelog=True):
        '''
        A function helps keep track of whether an order is completed or not based on remaining time
        :param timelog: whether to show the printing message or not
        :return: None
        '''
        if self.busy():
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                if timelog:
                    print("=== %s: Customer %s completes ordering." %
                          (seconds_to_hhmmss(self.order_complete_time), self.curr_customer.get_cust_id()))
                self.finishOrder = True
                self.curr_customer = None

    def startNext(self, new_customer: Customer, order_start_time):
        '''
        new customer will be served
        :param new_customer: Customer, next customer to be served by cashier
        :param order_start_time: the second that the next customer is served
        :return: None
        '''
        self.curr_customer = new_customer
        self.order_indiv = self.curr_customer.order_list()
        # total number of ice-cream the customer orders
        self.order_stats = (self.curr_customer.get_cust_id(), len(self.curr_customer.order_list()))
        self.time_remaining = new_customer.get_serving_time() + self.cashier.get_process_time()
        self.order_complete_time = order_start_time + self.time_remaining


class Preparing:
    # Preparing class instantiates one chef's preparation process of one ice-cream

    count_ic_order = Counter()  # record the number of each customer's current completed ice-cream
                                # (to check if one customer has all his/her order completed)

    def __init__(self, chef: Employee.Chef):
        '''
        Each preparing process requires information about:
        - curr_order: if there is an order being processed by the chef
        - time_remaining: the remaining time of the order
            (calculated based on chef's processing time - the time has passed)
        - chef: the chef of preparing object
        - finish_ic_order: flag of whether the one ice-cream order is finished
        - arrival_time: customer's arrival time (for calculating waiting time in simulation)
        - prepare_end_time: record one ice-cream 's completion timestamp
        - cust_id: each ice-cream order's customer id
        :param chef: chef object
        '''

        self.curr_order = None
        self.time_remaining = 0
        self.chef = chef
        self.finish_ic_order = False
        self.arrival_time = 0
        self.prepare_end_time = 0
        self.cust_id = 0

    def busy(self) ->bool:
        '''
        Check whether a chef is processing order or not
        :return: bool
        '''
        if self.curr_order is not None:
            return True
        else:
            return False

    def tick(self):
        '''
        A function helps keep track of whether a single ice-cream order is completed or not based on remaining time
        :return: None
        '''

        if self.busy():
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.finish_ic_order = True
                Preparing.count_ic_order[self.curr_order[0]] += 1
                self.arrival_time = self.curr_order[-1]
                self.curr_order = None

    def startNext(self, new_order: tuple, prepare_start_time: int):
        """
        next ice-cream to be prepared
        :param new_order: tuple, the next ice-cream to prepare - format (cust_id, size, arrival time)
        :param prepare_start_time: the second to start making the next ice-cream
        :return: None
        """
        self.curr_order = new_order
        self.cust_id = self.curr_order[0]
        self.time_remaining = self.chef.get_prep_time(new_order[1])  # example of new_order: (cust_id, "S", arrival time)
        self.prepare_end_time = prepare_start_time + self.time_remaining


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def getItem(self, index):
        return self.items[index]


def seconds_to_hhmmss(second_number: int):
    """
    convert the second number to current date time with format HH:MM:SS(AM/PM)
    Note that time starts at 12pm (12*3600 = 43200) as the shop opens
    >>> seconds_to_hhmmss(240)
    '12:04:00PM'
    """
    return time.strftime('%H:%M:%S%p', time.gmtime(43200 + second_number))

