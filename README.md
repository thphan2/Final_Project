# Title: Nitrogen Ice-cream Shop Monte Carlo Simulation

## Team Member(s):
Yuejun Wu, Thuong Phan

# Monte Carlo Simulation Scenario & Purpose:
**Background**
We simulate one day operation of a nitrogen ice-cream shop in summer. This is a mom&pop style small shop, which means customer satisfactory is crucial to its survival.
Recently, some customers complain that waiting time is too long, and they are unhappy to wait in the sun especially in summer. This ice-cream shop doesn't have extra cash flow
to rent a bigger place for customers to sit and eat. They decide to optimize the combination of employees to minimize the waiting time. But first they would like to find out
whether there is a relationship between experienced/inexperienced chef/cashier and waiting time.
The waiting time is referred to average waiting time of customers per day.

**Products and Constraints**
The shop sells three kinds of sizes of ice-cream: small, medium and large. Raw materials for all of them are the same. Customers can order any number of ice-cream with different sizes as
long as the raw material in the shop is enough. When the shop runs out of raw material it will stop taking new orders but will complete the orders that have been ordered before. The shop
will also take account of employee salaries into consideration. All employees are hourly paid, and if the salary expense for employees is larger than one day budget of the shop, the shop
has to adjust employee numbers. It is also important that there should be at least one chef(experienced/inexperienced) and one cashier(experienced/inexperienced). Otherwise, the simulation
is not valid.

**Employee structure**
There are two kinds of employees in the shop: Cashier and Chef.
Nitrogen ice-cream is different from traditional ice-cream which requires specific skills. Therefore, cashier and chef cannot switch roles when the shop is busy.

**Operating process**
There are two operating processes in the shop: Ordering and Preparing. When customers come in, cashier will serve them first. Cashier will take notes of the number of each size of ice-cream
the customer orders. There could be more than 1 cashier, and they will serve customers concurrently when more customers come in. When any of cashiers finish customers' ordering process
Chef will start to prepare ice-cream. There could be more than 1 chef. They will process orders concurrently. For example, if one customer orders 2 small ice-cream and 1 medium ice-cream
this customer generates 3 preparing orders. If there are 3 chef who are not busy then 3 of them will prepare these 3 orders at the same time. For fairness, if there are few customers coming in
situation won't happen that one specific chef will always work. When preparing orders come and several chef are idle, then 1 of the chef will be selected randomly to work on it.

**Operating hour**
The shop operates from 12PM - 10PM. This is the real operating hour of Jarling icecream shop in Champaign. We use that in our simulation. The shop will stop taking orders at 9:45PM, and
will finish the remaining orders. It happens that chef work after 10PM to process the remaining orders.

**Analytical output**
We simulate the situation in a time log format. In this way, people can see details about when the new customer comes in, when their orders are completed and when their ice-cream are made.
An example of time log simulation can be viewed at [Analysis of simulation.ipynb] in this repository. We also give the owner a choice of whether to view the time log or have an output .csv
file. There are sample output files in the repo, and our statistical analysis uses these outputs.

## Simulation's variables of uncertainty

1. Ice-cream: Number of ice-cream for each size ordered by customers (uniform distribution + normal discrete distribution)
2. Customer: Ordering time (normal distribution) Parents with kids might take longer time to order as they got distracted by kids frequently. Elderly people speak slowly to order.
             Young people might speak faster and finish ordering quicker. In this shop, most customers are young people.
3. Customer: Thinking time (uniform distribution) This is a mom&pop shop, and many of the customers are old customers. They usually don't take much time to order.
             Besides, there are only three sizes of ice-cream to choose. It shouldn't take much time to think about what to order even for new customers.
4. Customer: Number of customers comes to the shop in different time during a day (normal distribution)
5. Chef: Preparation time based on various levels of experience (normal distribution)
6. Cashier: Preparation time based on various levels of experience (normal distribution)
7. Customer arrival interval: uniform distribution based on different range of time in a day.


## Hypothesis or hypotheses before running the simulation:
NULL Hypothesis: Total waiting time has no association with the experience of employees or the number of ice-cream customers buy
Alternative Hypothesis:


## Analytical Summary of your findings:
(e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)

## Instructions on how to use the program:
 - Simulation: [icshop_simulation.py]
                This will show time log in console. Feel free to try other parameters.
                simulation(exp_chef_num,new_chef_num,exp_cashier_num,new_cashier_num, budget, filename="default", timelog = True)
 - Data exploration: [Analysis of simulation.ipynb]
                     Demo of time log simulation; plots of waiting time and different combinations of employees; plots of profit and different combinations of employees
 - Data analysis: [Data_Analysis.md]
                  Summary/graph statistics -> fit linear regression model -> robustness of the model -> interpret model -> come to conclusion

## All Sources Used:
Miller & Ranum: Problem Solving with Algorithms and Data Structures Using Python, Section 3.4, pages 106-119
https://github.com/nikolausn/Final-project


