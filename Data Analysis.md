
Question of interest
====================

For owners of a small ice-cream shop, it's crucial to try to maximize customer satisfactory. Customer detention is key to the survival of small business, and customer satisfactory is related to customer detention rate. In this report, we use customer waiting time per day as the proxy to customer satisfactory. Our assumption is the number of different experienced level chef and cashier, along with average number of ice-cream per customer, number of small/medium/large ice-cream will have impact on waiting time.

NULL Hypothesis: coefficient of (the number of different experienced level chef and cashier, average number of ice-cream per customer, number of small/medium/large ice-cream) are equal to 0.

Alternative Hypothesis: At least one of the coefficients is different from 0.

Data
====

We generate thousands of data through simulation program under the same repository (icshop\_simulation.py).

load data
---------

``` r
library(readr)
fulldata <- read_csv("data/sample.csv",col_names = FALSE)
```

    ## Parsed with column specification:
    ## cols(
    ##   X1 = col_integer(),
    ##   X2 = col_integer(),
    ##   X3 = col_integer(),
    ##   X4 = col_integer(),
    ##   X5 = col_integer(),
    ##   X6 = col_integer(),
    ##   X7 = col_integer(),
    ##   X8 = col_double(),
    ##   X9 = col_integer(),
    ##   X10 = col_integer(),
    ##   X11 = col_integer(),
    ##   X12 = col_integer(),
    ##   X13 = col_double()
    ## )

``` r
colnames(fulldata) <- c("experienced chef", "new chef", "experienced cashier", "new cashier", "small icecream", "medium icecream", "large icecream", "total icecream", "number of customer", "order waiting time", "prepare waiting time", "waiting time", "profit")

# number of ice-cream/customer
fulldata$ic_per_cust = fulldata$`total icecream`/fulldata$`number of customer`
```

Statistic summary
-----------------

``` r
data <- fulldata[c(-13)]
summary(data)
```

    ##  experienced chef    new chef   experienced cashier  new cashier 
    ##  Min.   :1.0      Min.   :0.0   Min.   :1.0         Min.   :0.0  
    ##  1st Qu.:1.0      1st Qu.:0.0   1st Qu.:1.0         1st Qu.:0.0  
    ##  Median :1.5      Median :0.5   Median :1.5         Median :0.5  
    ##  Mean   :1.5      Mean   :0.5   Mean   :1.5         Mean   :0.5  
    ##  3rd Qu.:2.0      3rd Qu.:1.0   3rd Qu.:2.0         3rd Qu.:1.0  
    ##  Max.   :2.0      Max.   :1.0   Max.   :2.0         Max.   :1.0  
    ##  small icecream   medium icecream  large icecream  total icecream 
    ##  Min.   : 37.00   Min.   : 41.00   Min.   : 75.0   Min.   :258.0  
    ##  1st Qu.: 71.00   1st Qu.: 71.00   1st Qu.:114.0   1st Qu.:409.5  
    ##  Median : 79.00   Median : 79.00   Median :127.0   Median :450.5  
    ##  Mean   : 79.18   Mean   : 79.33   Mean   :127.4   Mean   :453.0  
    ##  3rd Qu.: 87.00   3rd Qu.: 88.00   3rd Qu.:140.0   3rd Qu.:495.5  
    ##  Max.   :119.00   Max.   :124.00   Max.   :190.0   Max.   :674.0  
    ##  number of customer order waiting time prepare waiting time
    ##  Min.   :38.00      Min.   : 0.000     Min.   :  7.00      
    ##  1st Qu.:46.00      1st Qu.: 0.000     1st Qu.: 10.00      
    ##  Median :46.00      Median : 0.000     Median : 17.00      
    ##  Mean   :46.92      Mean   : 1.187     Mean   : 26.63      
    ##  3rd Qu.:46.00      3rd Qu.: 1.000     3rd Qu.: 36.00      
    ##  Max.   :73.00      Max.   :20.000     Max.   :149.00      
    ##   waiting time     ic_per_cust    
    ##  Min.   :  7.00   Min.   : 6.143  
    ##  1st Qu.: 11.00   1st Qu.: 8.674  
    ##  Median : 18.00   Median : 9.598  
    ##  Mean   : 27.54   Mean   : 9.669  
    ##  3rd Qu.: 37.00   3rd Qu.:10.630  
    ##  Max.   :162.00   Max.   :13.480

Covariance table
----------------

``` r
attach(data)
cor(data[,c(5:13)])  # exclude discrete variables
```

    ##                      small icecream medium icecream large icecream
    ## small icecream            1.0000000       0.6907463      0.7488858
    ## medium icecream           0.6907463       1.0000000      0.7546622
    ## large icecream            0.7488858       0.7546622      1.0000000
    ## total icecream            0.8461398       0.8815179      0.9639845
    ## number of customer        0.1544587       0.1383247      0.1660308
    ## order waiting time        0.1849741       0.2153531      0.2281448
    ## prepare waiting time      0.2284962       0.2239271      0.2504186
    ## waiting time              0.2364961       0.2335005      0.2602688
    ## ic_per_cust               0.7796838       0.8208456      0.8919165
    ##                      total icecream number of customer order waiting time
    ## small icecream            0.8461398          0.1544587         0.18497410
    ## medium icecream           0.8815179          0.1383247         0.21535310
    ## large icecream            0.9639845          0.1660308         0.22814484
    ## total icecream            1.0000000          0.1698969         0.23567876
    ## number of customer        0.1698969          1.0000000         0.24143565
    ## order waiting time        0.2356788          0.2414357         1.00000000
    ## prepare waiting time      0.2599639          0.6198227         0.03657756
    ## waiting time              0.2702248          0.6375075         0.10558594
    ## ic_per_cust               0.9261805         -0.2111362         0.14457003
    ##                      prepare waiting time waiting time  ic_per_cust
    ## small icecream                0.228496180   0.23649608  0.779683811
    ## medium icecream               0.223927093   0.23350052  0.820845628
    ## large icecream                0.250418551   0.26026885  0.891916487
    ## total icecream                0.259963857   0.27022482  0.926180496
    ## number of customer            0.619822717   0.63750746 -0.211136226
    ## order waiting time            0.036577559   0.10558594  0.144570032
    ## prepare waiting time          1.000000000   0.99717686  0.008887213
    ## waiting time                  0.997176859   1.00000000  0.012765841
    ## ic_per_cust                   0.008887213   0.01276584  1.000000000

``` r
pairs(data[,c(5,6,7,12,13)],pch = ".", main = "Pairwise scatter plots")
```

![](Data%20Analysis_figs/Data%20Analysis-unnamed-chunk-4-1.png)

From the plot and coveriance table we can see that total ice-cream is highly correlated with small/medium/large ice-cream, which is not surprised. In our case, we are interested in different sizes of ice-cream's influence on waiting time so we will exclude varibale of total icecream. As for waiting time, waiting time = order waiting time + prepare waiting time. We will use waiting time as dependent variable.

### Plots of average waiting time per customer

``` r
# We first explore dependent variable 

par(mfrow = c(2,1))
# density plot
hist(`waiting time`, breaks = 400, freq = FALSE, col = "lightgreen", border = "darkgreen",axes = F
     ,xlab = "Waiting time (minuets)", main="Density plot of average waiting time/customer")
axis(1, at=seq(0,100,5))
axis(2, at = seq(0,0.2,0.05))

# boxplot
boxplot(`waiting time`, horizontal = T,xlab = "Waiting time(minutes)",main = "Boxplot of average waiting time",axes = F,staplewex = 1)
text(x=fivenum(`waiting time`), labels =fivenum(`waiting time`), y = 1.25)
```

![](Data%20Analysis_figs/Data%20Analysis-unnamed-chunk-5-1.png)

We can tell from the plot that average waiting time is around 9 minutes 20% of the time, and the data has a heavy tail, which suggests many unrealistic simulation data. Boxplot also suggests many outlier data. The medium average waiting is 18 minutes based on boxplot.

### Fit model based on observations

``` r
mod1 <- lm(`waiting time`~ `experienced cashier` + `experienced chef` + `new cashier` + `new chef` + `small icecream`+`medium icecream`+`large icecream` + ic_per_cust)
summary(mod1)
```

    ## 
    ## Call:
    ## lm(formula = `waiting time` ~ `experienced cashier` + `experienced chef` + 
    ##     `new cashier` + `new chef` + `small icecream` + `medium icecream` + 
    ##     `large icecream` + ic_per_cust)
    ## 
    ## Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -50.899  -7.612  -1.482   5.456  75.841 
    ## 
    ## Coefficients:
    ##                        Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)            28.16309    2.24118  12.566  < 2e-16 ***
    ## `experienced cashier`   3.45460    0.52750   6.549 7.07e-11 ***
    ## `experienced chef`    -23.94613    0.56316 -42.521  < 2e-16 ***
    ## `new cashier`           0.47786    0.50859   0.940    0.348    
    ## `new chef`            -12.93931    0.56509 -22.898  < 2e-16 ***
    ## `small icecream`        0.41055    0.03494  11.749  < 2e-16 ***
    ## `medium icecream`       0.64025    0.03845  16.652  < 2e-16 ***
    ## `large icecream`        0.83791    0.03532  23.725  < 2e-16 ***
    ## ic_per_cust           -15.89571    0.64452 -24.663  < 2e-16 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 12.31 on 2391 degrees of freedom
    ## Multiple R-squared:  0.7261, Adjusted R-squared:  0.7251 
    ## F-statistic: 792.1 on 8 and 2391 DF,  p-value: < 2.2e-16

``` r
par(mfrow = c(2,2))
plot(mod1)
```

![](Data%20Analysis_figs/Data%20Analysis-unnamed-chunk-6-1.png) \#\#\# Diagnostic From diagnostic plot, we can tell mod1 violates some assumptions of linear regression model. Upper left plot shows the model is not linear, Q-Q plot indicates it violates normality and lower left plot shows mod1 doesn't have constant variance in errors. Lower right plot suggests there are outliers in data which conforms our finding in the previous plot regrding average waiting time.

Next we will do transformation and exclude outliers before refitting the model.

### Transformation

``` r
# Exclude outliers
new_data <- data[c(-10,-69, -48),]

# Since mod1 violates constant variance assumption, we will do transformation on dependant variable using boxbox transformation. 
library(MASS)
boxcox(mod1)
```

![](Data%20Analysis_figs/Data%20Analysis-unnamed-chunk-7-1.png)

``` r
# boxcox shows that lambda=-0.5
mod2 <- lm((new_data$`waiting time`) ^(-0.5) ~ new_data$`experienced cashier` + new_data$`experienced chef` + new_data$`new cashier` + new_data$`new chef` + new_data$`small icecream`+new_data$`medium icecream`+new_data$`large icecream` + new_data$ic_per_cust, data = new_data)
summary(mod2)
```

    ## 
    ## Call:
    ## lm(formula = (new_data$`waiting time`)^(-0.5) ~ new_data$`experienced cashier` + 
    ##     new_data$`experienced chef` + new_data$`new cashier` + new_data$`new chef` + 
    ##     new_data$`small icecream` + new_data$`medium icecream` + 
    ##     new_data$`large icecream` + new_data$ic_per_cust, data = new_data)
    ## 
    ## Residuals:
    ##       Min        1Q    Median        3Q       Max 
    ## -0.139125 -0.018576 -0.000969  0.019465  0.131259 
    ## 
    ## Coefficients:
    ##                                  Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)                     1.644e-01  5.258e-03  31.269  < 2e-16 ***
    ## new_data$`experienced cashier`  7.499e-04  1.237e-03   0.606    0.544    
    ## new_data$`experienced chef`     1.187e-01  1.322e-03  89.749  < 2e-16 ***
    ## new_data$`new cashier`          1.644e-03  1.192e-03   1.379    0.168    
    ## new_data$`new chef`             5.100e-02  1.327e-03  38.437  < 2e-16 ***
    ## new_data$`small icecream`      -5.054e-04  8.202e-05  -6.161 8.43e-10 ***
    ## new_data$`medium icecream`     -7.821e-04  9.092e-05  -8.602  < 2e-16 ***
    ## new_data$`large icecream`      -1.046e-03  8.381e-05 -12.482  < 2e-16 ***
    ## new_data$ic_per_cust            1.027e-02  1.541e-03   6.665 3.28e-11 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.02886 on 2388 degrees of freedom
    ## Multiple R-squared:  0.856,  Adjusted R-squared:  0.8555 
    ## F-statistic:  1774 on 8 and 2388 DF,  p-value: < 2.2e-16

``` r
# Diagnostic plot
par(mfrow = c(2,2))
plot(mod2)
```

![](Data%20Analysis_figs/Data%20Analysis-unnamed-chunk-7-2.png)

Diagnostic plots of mod2 show a better model than mod1. Assumptions of linear model are satisfied. Besides, we can tell from summary that adjusted R squared improved from 0.7251 to 0.8559, indicating a better model of mod2. The summary shows that the number of new cashier and nubmer of experienced cashier do not have significant effect on waiting time. All other variables have significant effect on waiting time.

Let's analyze mod2.

### Collinearity

There are several variables are significant based on p-value, we want to check if there are collinearity among them.

``` r
library(faraway)
vif(mod2)
```

    ## new_data$`experienced cashier`    new_data$`experienced chef` 
    ##                       1.100744                       1.258022 
    ##         new_data$`new cashier`            new_data$`new chef` 
    ##                       1.022492                       1.266644 
    ##      new_data$`small icecream`     new_data$`medium icecream` 
    ##                       2.821986                       3.577318 
    ##      new_data$`large icecream`           new_data$ic_per_cust 
    ##                       6.596487                      11.997304

Variance inflation factor are all below 10 except ice-cream per customer, indicating no severe collinearity problems. But we need to drop ic\_per\_cust.

Summary
=======

NULL hypothesis is rejected as p-value of F-statistics is less than 5% (assume 95% confidence interval), meaning at least one variable indicated in the begining of the report is different from 0.

Our final model: *w**a**i**t**i**n**g**t**i**m**e*<sup>−1/2</sup> = constant + (1.187*e* − 01)experienced chef + (5.100*e* − 02)new chef + (−5.054*e* − 04)small icecream + (−7.821*e* − 04)medium icecream + (−1.046*e* − 03)large icecream

The result matches what we've analyzed in [jupyter notebook](https://github.com/sayaaoi/Final_Project/blob/master/Analysis%20of%20simulation.ipynb), we find out that experience level is not very important on how the cashier performs while experience is indeed important in hiring chef.
