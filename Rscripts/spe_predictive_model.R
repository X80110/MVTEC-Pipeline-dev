#+ setup, include=FALSE
knitr::opts_chunk$set(collapse = TRUE)

#+ message=FALSE
library(dplyr)
library(tidyr)

#' TODO
#' residual analysis
#' different currency

load(file="/Users/spechen/Desktop/MVTEC/mid-term/MVTEC-covid-test/output/joined_data_by_isocode.RData")

# c <- read.csv("./data/USD_SGD_Historical_Data_investingDotCom.csv",header=T)

c <- read.csv("./data/USD_TWD_Historical_Data.csv",header=T)

df <- read.csv("./data/owid-covid-data-new.csv",header=T)

df$date <- as.Date(df$date, format='%Y-%m-%d')


#' Missing values in currency is filled with the previous date's price

c$date <- as.Date(c$Date, format='%b %d, %Y')

currency <- c %>% 
  select(Price, date) %>%
  complete(date = seq(min(date), max(date), by = "day"),
           fill = list(price = NA)) %>%
  fill(Price) %>%
  rename(usd2twd = Price)

# usa <- joined %>% 
#   filter(iso_code == 'USA') %>%
#   merge(currency, by='date')

usa_original <- df %>% 
  filter(iso_code == 'USA') %>%
  merge(currency, by='date') %>% 
  filter(date > "2020-02-29") %>% #starts with March
  filter(!is.na(stringency_index)) 

# remove outliers
usa <- usa_original %>% 
  filter(new_cases < 100000) 

#' quick test for outliers
usa_outliers <- usa_original %>%  filter(new_cases > 100000) 
outlier_fit <- lm(usd2twd ~ new_cases, data = usa_outliers ) # fit the model
summary(outlier_fit)
plot(usa_outliers$new_cases, usa_outliers$usd2twd, main="daily cases over 100k only")
abline(outlier_fit, col="blue")

#' Data partitioning
#' split training and testing data set
set.seed(123)

# for time series, shuffle before splitting
idx_shuffled <- sample(nrow(usa))
usa_shuffled <- usa[idx_shuffled,] 

training.samples <- usa_shuffled$usd2twd %>%
  createDataPartition(p = 0.8, list = FALSE)

train.data  <- usa[training.samples, ]
test.data <- usa[-training.samples, ]

set.seed(567)
# for time series, shuffle before splitting
idx_shuffled_o <- sample(nrow(usa_original))
usa_shuffled_o <- usa_original[idx_shuffled_o,] 

training.samples.original <- usa_shuffled_o$usd2twd %>%
  createDataPartition(p = 0.8, list = FALSE)

train.data.original  <- usa_original[training.samples.original, ]
test.data.original <- usa_original[-training.samples.original, ]
  
#' linear regression starts here
#' http://www.sthda.com/english/articles/40-regression-analysis/162-nonlinear-regression-essentials-in-r-polynomial-and-spline-regression-models/#polynomial-regression
# Build the model
newcases_model <- lm(usd2twd ~ new_cases, data = train.data ) # fit the model
newcases_model_original <- lm(usd2twd ~ new_cases, data = usa_original ) # fit the model

# Make predictions
newcases_predictions <- newcases_model %>% predict(test.data)
# Model performance
# we want low RMSE and high R2
# 0.329 RMSE seems low enough but put in the context of the currency conversion usd2twd... then it might not be?
data.frame(
  RMSE = RMSE(newcases_predictions, test.data$usd2twd),
  R2 = R2(newcases_predictions, test.data$usd2twd)
)

#' Comparing models with or without outliers
summary(newcases_model)
plot(usa$new_cases, usa$usd2twd, main="excluding daily cases over 100k")
abline(newcases_model, col="blue")

summary(newcases_model_original)
plot(usa_original$new_cases, usa_original$usd2twd,main="including daily cases over 100k")
abline(newcases_model_original, col="blue")

par(mfrow = c(2, 1))

ggplot(train.data.original, aes(new_cases, usd2twd) ) +
  geom_point() +
  stat_smooth(method = lm, formula = y ~ x)

#' ## Residual analysis
par(mfrow = c(2, 2))
plot(newcases_model)

#a few outliers
par(mfrow = c(2, 2))
plot(newcases_model_original)


# Make a histogram of the residuals
# https://www.rpubs.com/stevenlsenior/normal_residuals_with_code
qplot(newcases_model$residuals,
            geom = "histogram",
            bins = 10) +
  labs(title = "Histogram of residuals",
       x = "residual")


#' Polynomial regression, 2nd degree / exponential? 
#' try to improve the model a bit. seems a curvy line might fit better
#' with outliers
poly_model <- lm(usd2twd ~ poly(new_cases, 2, raw = TRUE), data = train.data.original)
poly_predictions <- poly_model %>% predict(test.data.original)
data.frame(
  RMSE = RMSE(poly_predictions, test.data.original$usd2twd),
  R2 = R2(poly_predictions, test.data.original$usd2twd)
)

summary(poly_model)

ggplot(train.data.original, aes(new_cases, usd2twd) ) +
  geom_point() +
  stat_smooth(method = lm, formula = y ~ poly(x, 2, raw = TRUE))


ggplot(usa_original, aes(new_cases, usd2twd) ) +
  geom_point() +
  stat_smooth(method = lm, formula = y ~ poly(x, 2, raw = TRUE))


par(mfrow = c(2, 2))
plot(poly_model)


#' ## Multiple Regression
#' try add new var and do multiple reg
usa_selected <- usa %>% select(usd2twd, new_cases, new_deaths)
plot(usa_selected)
# fit the model
multiple.regression <- lm(usd2twd ~ new_cases + new_deaths, data = train.data) 
multi_predictions <- multiple.regression %>% predict(test.data)
summary(multiple.regression)
data.frame(
  RMSE = RMSE(multi_predictions, test.data$usd2twd),
  R2 = R2(multi_predictions, test.data$usd2twd)
)

par(mfrow = c(2, 2))
plot(multiple.regression)


#' discuss other variable options
usa_selected2 <- usa %>% select(icu_patients , new_cases, new_deaths, new_tests)
plot(usa_selected2)


#' IGNORE THE BELOW
#' results are not meaningful
newdeaths_fit <- lm(usd2twd ~ new_deaths, data = usa) # fit the model
summary(newdeaths_fit)
plot(usa$new_deaths, usa$usd2twd)
abline(newdeaths_fit, col="blue")

stringency_index_fit <- lm(usd2twd ~ stringency_index, data = usa) # fit the model
summary(stringency_index_fit)
plot(usa$stringency_index, usa$usd2twd)
abline(stringency_index_fit, col="blue")

#' try add new var and do multiple reg
usa_selected <- usa %>% select(usd2twd, new_cases, stringency_index)
plot(usa_selected)

usa_selected <- usa %>% select(usd2twd, new_cases, new_deaths)
plot(usa_selected)

multiple.regression <- lm(usd2twd ~ new_cases + new_deaths, data = usa) # fit the model
summary(multiple.regression)
