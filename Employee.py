import Distribution

class Employee:
    # base class for all kinds of employee
    def __init__(self, id, is_experienced: bool):
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
    def __init__(self, id: int, is_experienced: bool):
        """
        Cashier is the person who takes order from customers.
        Each cashier requires data about his ID, experience level, salary based on the experience
        and the required time to process an order
        :param id: cashier id to identify an cashier, automatically assigned when a cashier is added
        :param is_experienced: whether the cashier has any experience (True or False)
        """
        Employee.__init__(self, id, is_experienced)
        if is_experienced:
            self._salary = 12  # $12/hr
            self._process_time = 0
        else:
            self._salary = 10  # $10/hr
            self._process_time = Distribution.NormalDist(5, 1, 2, 15).random()

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
    def __init__(self, id, is_experienced: bool):
        """
        Chef is the person who makes ice-cream for customers
        Each chef requires info about his ID, experience level, salary based on the experience
        and the required time to process an ice-cream based on the ice-cream size
        :param id: chef id to identify an chef, automatically assigned when a chef is added
        :param is_experienced: whether the chef has any experience (True or False)
        """
        Employee.__init__(self, id, is_experienced)
        if is_experienced:
            self._salary = 17  # $17/hr
            self._prep_time = Distribution.NormalDist(60, 5, 30, 90).random()
        else:
            self._salary = 14  # $14/hr
            self._prep_time = Distribution.NormalDist(120, 5, 70, 180).random()

    def get_salary(self):
        """
        Return the salary of a chef
        """
        return self._salary

    def get_prep_time(self, size: str):
        """
        Return the preparation time for an ice-cream based on its size
        :param size: size of an ice-cream (S, M or L)
        :return: preparation time
        """
        if size == "S":
            return self._prep_time
        elif size == "M":
            return self._prep_time*1.5
        else:
            return self._prep_time*2

