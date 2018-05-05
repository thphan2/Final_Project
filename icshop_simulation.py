"""
590PR Spring 2018
Authors: Yuejun Wu, Thuong Phan
Final Project: Nitrogen Ice-cream Shop Monte Carlo Simulation


Add new customers
>>> cu1=Customer.Customer(1,120)
>>> has_raw_material(cu1,0)
False
>>> has_raw_material(cu1,1000000)
True

Add new cashiers
>>> ca1=Employee.Cashier(1,True)
>>> ca2=Employee.Cashier(2,False)
>>> ca1.get_salary()
12
>>> ca2.get_salary()
10

Add new chefs
>>> ch3=Employee.Chef(3,True)
>>> ch4=Employee.Chef(4,False)
>>> ch3.get_salary()
17
>>> ch4.get_salary()
14

Ice-cream shop test
>>> shop=Ice_creamShop(1,2,1,0,100)
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

from random import shuffle
import sys
import Employee
import Operation
import Customer


class Ice_creamShop:
    # shop opens from 12PM - 10PM (10 hours) 10hours = 36000 sec
    total_sec = 36000

    def __init__(self, exp_chef_num: int, new_chef_num: int, exp_cashier_num: int, new_cashier_num: int, raw_material_cost: float):
        """
        An ice-cream shop requires information about
        - number of experienced and non-experienced chefs it has for a day (exp_chef_num, new_chef_num)
        - number of experienced and non-experienced cashiers it has for a day (exp_cashier_num, new_cashier_num)
        - ice-cream price for different sizes S, M and L (price_S, price_M, price_L)
        - the current amount of raw material to make ice-cream (raw_material_cost).
          We assume that 1 small ice-cream costs $1 of raw material, 1 medium ice-cream costs $1.5 of raw material,
          and 1 large ice-cream costs $2 of raw material based on unit equivalency among different sizes.
        - a check variable whether it has enough raw material (is_enough_raw_material)
        - list of chefs and cashiers it has (chef_list, cashier_list)
        - total number of ice-cream size S, M and L it has sold for the day (total_s_ic, total_m_ic, total_l_ic)
        - total number of ice-cream units it has sold for the day (total_ic_num)
        :param exp_chef_num: number of experienced chefs
        :param new_chef_num: number of non-experienced chefs
        :param exp_cashier_num: number of experienced cashiers
        :param new_cashier_num: number of non-experienced cashiers
        """
        self.price_S = 4
        self.price_M = 6
        self.price_L = 8
        self.raw_material_cost = raw_material_cost
        self.is_enough_raw_material = True
        self.chef_list, self.cashier_list = [], []
        self.total_s_ic = 0
        self.total_m_ic = 0
        self.total_l_ic = 0
        self.total_ic_num = 0

        for i in range(new_chef_num):
            self.chef_list.append(Employee.Chef(i + 1, is_experienced=False))
        for i in range(exp_chef_num):
            self.chef_list.append(Employee.Chef(new_chef_num + i + 1, is_experienced=True))
        for i in range(new_cashier_num):
            self.cashier_list.append(Employee.Cashier(i + 1, is_experienced=False))
        for i in range(exp_cashier_num):
            self.cashier_list.append(Employee.Cashier(new_cashier_num + i + 1, is_experienced=True))

    def update_total_s_ic(self, s_ic_num: int):
        """
        Update the total ice-cream size S the shop has sold so far
        :param s_ic_num: number of ice-cream size S ordered by a customer
        :return: None
        """
        self.total_s_ic = self.total_s_ic + s_ic_num

    def update_total_m_ic(self, m_ic_num: int):
        """
        Update the total ice-cream size M the shop has sold so far
        :param m_ic_num: number of ice-cream size M ordered by a customer
        :return: None
        """
        self.total_m_ic = self.total_m_ic+m_ic_num

    def update_total_l_ic(self, l_ic_num: int):
        """
        Update the total ice-cream size L the shop has sold so far
        :param l_ic_num: number of ice-cream size L ordered by a customer
        :return: None
        """
        self.total_l_ic = self.total_l_ic+l_ic_num

    def update_ic_num(self, s_ic: int, m_ic: int, l_ic: int):
        """Convert ice-cream of different size into ice-cream units
        1 medium ice_cream ~ 1.5 small ice_cream;
        1 large ice_cream ~ 2 small ice_cream in terms of unit
        :param s_ic: number of S size ice-cream
        :param m_ic: number of M size ice-cream
        :param l_ic: number of L size ice-cream
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

    def is_within_budget(self, budget)->bool:
        """
        Check whether the variable cost is within the shop's budget
        :param budget: the budget set by the shop for variable cost
        :return: whether the variable cost is within the budget (True or False)
        """
        return Ice_creamShop.total_variable_cost(self) <= budget - self.raw_material_cost


def has_raw_material(customer: Customer, raw_material_cost: float)->bool:
    """
    check whether the shop has enough raw material for the customer's ice-cream order
    We assume that 1 small ice-cream unit costs $1 of raw material, 1 medium ice-cream costs $1.5 of raw material,
    and 1 large ice-cream costs $2 of raw material.
    :param customer: Customer
    :param raw_material_cost: the remaining raw material the shop has currently
    :return: bool
    """
    return customer.s_icecream_num() + customer.m_icecream_num()*1.5 + customer.l_icecream_num()*2 <= raw_material_cost


def simulation(exp_chef_num, new_chef_num, exp_cashier_num, new_cashier_num, budget, raw_material_cost, filename="default", timelog=True):
    if exp_chef_num == new_chef_num == 0:
        print("Wrong simulation. Shop cannot operate without a chef!")
    elif exp_cashier_num == new_cashier_num == 0:
        print("Wrong simulation. Shop cannot operate without a cashier!")
    else:
        icshop = Ice_creamShop(exp_chef_num, new_chef_num, exp_cashier_num, new_cashier_num, raw_material_cost)
        cust_id = 0
        finish_status = False
        last_customer_id = 0
        ordering_waitingtimes = []  # keep track of each customer's ordering waiting time
        waitingtimes = []  # keep track of each customer's overall waiting time (ordering waiting time + preparing waiting time)
        order_q = Operation.Queue()
        prep_q = Operation.Queue()
        customer_num_ic = {}  # total number of ice-cream for each customer (to check if prep is finished for a certain customer)
        if icshop.is_within_budget(budget):
            if timelog:
                print(u"\u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665")
                print("%s: Nitro Ice-cream Shop opens. " % Operation.seconds_to_hhmmss(0))
                print(u"\u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665 \u2665\n")

            order_lis = []  # a list for different Ordering object (each cashier constructs an Ordering object)
            prepare_lis = []  # a list for different Preparing object (each chef constructs an Preparing object)
            for cashier in icshop.cashier_list:
                order_lis.append(Operation.Ordering(cashier))
            for chef in icshop.chef_list:
                prepare_lis.append(Operation.Preparing(chef))

            revenue = 0
            for currentSecond in range(sys.maxsize):
                # shop stops taking new order at 9:45pm or running out of raw material
                if currentSecond < Ice_creamShop.total_sec - 900 and icshop.is_enough_raw_material is True:
                    if Customer.new_customer(currentSecond):
                        customer = Customer.Customer(cust_id + 1, currentSecond)
                        cust_id += 1

                        # check if raw material is enough for making ice-cream
                        if has_raw_material(customer, icshop.raw_material_cost):
                            order_q.enqueue(customer)
                            if timelog:
                                print("+++ %s: New customer! Customer %s arrives." %
                                      (Operation.seconds_to_hhmmss(currentSecond), customer.get_cust_id()))
                            icshop.raw_material_cost -= (customer.s_icecream_num() + customer.m_icecream_num() * 1.5 + customer.l_icecream_num() * 2)
                        else:
                            icshop.is_enough_raw_material = False
                            last_customer_id = customer.get_cust_id()-1
                            if timelog:
                                print("Shop will run out of raw material soon. Only take order till customer ID %s. Stop taking new customers now!" % last_customer_id)
                                print("*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *")

                # avoid first cashier does most the work
                shuffle(order_lis)
                for ordering in order_lis:  # check if any cashier is not busy
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
                        preparing.startNext(next_ic_order, currentSecond)
                    else:
                        preparing.tick()

                    # By checking number of ice-cream in each dictionary, we will know whether the order for one customer is finished or not
                    if preparing.finish_ic_order and (Operation.Preparing.count_ic_order[preparing.cust_id] == customer_num_ic[preparing.cust_id]):
                        if preparing.cust_id == last_customer_id:
                            finish_status = True
                        Operation.Preparing.count_ic_order[preparing.cust_id] = 0
                        if timelog:
                            print(">>> %s: Ice-cream ready! Customer %s's ice-cream order is completed!" %
                                 (Operation.seconds_to_hhmmss(preparing.prepare_end_time), preparing.cust_id))
                        # waiting time for each customer
                        waitingtimes.append(currentSecond-preparing.arrival_time)
                        preparing.finish_ic_order = False

                if timelog and currentSecond == Ice_creamShop.total_sec - 900:
                    print("%s: Shop is closing in 15 minutes, no new orders accepted." % Operation.seconds_to_hhmmss(currentSecond))
                    print("Finishing the remaining orders...")

                if (currentSecond >= Ice_creamShop.total_sec and order_q.isEmpty() and prep_q.isEmpty()) or \
                    (icshop.is_enough_raw_material is False and finish_status is True and order_q.isEmpty() and prep_q.isEmpty()):
                    if timelog:
                        print("%s: All orders completed. \n==========================================================================="
                              "\nThere are %s customers coming in today. Average waiting time: %s minutes.\
                        \nTotal revenue is: $%s dollars. Today's profit is: $%s"
                        % (Operation.seconds_to_hhmmss(currentSecond), len(waitingtimes), round((sum(waitingtimes)/len(waitingtimes))/60),
                        "{:,}".format(revenue), "{:,}".format(revenue - icshop.total_variable_cost())))
                        print("Ice-cream Shop closes for the day. See you again!")
                    break

            icshop.update_ic_num(icshop.total_s_ic, icshop.total_m_ic, icshop.total_l_ic)
            preparing_waitingtimes = [i - j for i, j in zip(waitingtimes, ordering_waitingtimes)]
            if not timelog:
                outfile = open(filename + ".csv","a")
                # File header: #exp_chef,#new_chef,#exp_cashier,#new_cashier,#total_s_icecream, #total_m_icecream,
                # #total_l_icecream, #average ice_cream number,
                # #customers, avg_ordering_time, avg_preparing time, avg_waiting_time, profit
                print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %
                      (exp_chef_num, new_chef_num, exp_cashier_num, new_cashier_num, icshop.total_s_ic,
                       icshop.total_m_ic, icshop.total_l_ic, icshop.total_ic_num,
                       len(waitingtimes), round((sum(ordering_waitingtimes)/len(waitingtimes))/60),
                       round((sum(preparing_waitingtimes)/len(waitingtimes))/60),
                       round((sum(waitingtimes)/len(waitingtimes))/60), revenue - icshop.total_variable_cost()), file=outfile)
                outfile.close()
        else:
            if timelog:
                print("Budget is not enough. Please adjust employee numbers.")


if __name__ == '__main__':
    # simulate a situation when there are 2 experienced chef, 1 new chef, 1 experienced cashier in the shop, show time log
    # with budget of $5000 and $300 raw material cost
    simulation(1, 1, 1, 0, 5000, 300, "", True)

    # uncomment and run below codes to generate "sample.csv" file for data analysis
    # by iterating over number of experienced, non-experienced chefs and experienced, non-experienced cashiers
    # and setting a big enough budget so that all combinations will be within the budget
    # ====Start of codes====
    #for exp_chef_num in range(1, 3):
    #    for new_chef_num in range(0, 2):
    #        for exp_cashier_num in range(1, 3):
    #            for new_cashier_num in range(0, 2):
    #                for i in range(150):
    #                    simulation(exp_chef_num, new_chef_num, exp_cashier_num, new_cashier_num, 100000, 8000, "sample", False)

