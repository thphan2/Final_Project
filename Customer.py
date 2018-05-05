import Distribution
import random

class Customer:
    # cust_order example: {'S':1, 'M':2 'L':1}
    def __init__(self, cust_id: int, arrival_time: int):
        """
        Customer visits the shop to buy ice-cream.
        A customer requires below information:
        - customer id to identify the customer (cust_id)
        - arrival time (arrival_time)
        - customer order containing the amount of ice-cream in each size he wants to buy (cust_order: dict)
        - amount of time to make the order (order_time)
        - amount of time to think about what to order (thinking_time)
        :param cust_id: customer id
        :param arrival_time: the second the customer arrives after the shop opens
        """
        self._cust_id = cust_id
        self._cust_order = {'S': Distribution.GaussianDiscrete(1, 1, 1, 5).random(), 'M': Distribution.GaussianDiscrete(1, 1, 0, 5).random(), 'L': Distribution.GaussianDiscrete(2, 1, 0, 5).random()}
        self._arrival_time = arrival_time
        self._order_time = Distribution.NormalDist(120, 3, 60, 300).random()
        self._thinking_time = random.uniform(0, 120)

    def get_cust_id(self):
        return self._cust_id

    def get_total_icecream(self):
        return self.s_icecream_num() + self.m_icecream_num() + self.l_icecream_num()

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
                order_list.append((self._cust_id, size, self.get_arrivaltime()))
        return order_list


def new_customer(currentSecond: int)->bool:
    """
    Randomly generate a customer coming to the ice-cream shop during peak hour and non-peak hour
    Assume that more customers come from 3PM - 5PM and 7PM - 8:30PM
    During peak hour, every 240 seconds (4 mins) there is a customer
    During non-peak hour, every 1200 seconds (20 mins) there is a customer
    :param currentSecond: the current second after the shop opens
    :return: whether a customer arrives (True or False)
    """

    if (10800 < currentSecond < 18000) or (25200 < currentSecond < 30600):
        num = random.randrange(1, 240)   # peak-hour: customer/240 sec on average
        if num == 20:
            return True
        else:
            return False
    else:
        num = random.randrange(1, 1200)  # non-peak hour: customer/1200 sec on average
        if num == 800:
            return True
        else:
            return False

