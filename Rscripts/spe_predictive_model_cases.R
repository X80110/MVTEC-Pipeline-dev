#+ setup, include=FALSE
knitr::opts_chunk$set(collapse = TRUE)

#+ message=FALSE
library(dplyr)
library(tidyverse)
library(caret)

#' TODO
#' residual analysis
#' different currency

# load(file="/Users/spechen/Desktop/MVTEC/mid-term/MVTEC-covid-test/output/joined_data_by_isocode.RData")

#' ## Preprocessing

df <- read.csv("./data/owid-covid-data-new.csv",header=T)

df$date <- as.Date(df$date, format='%Y-%m-%d')

usa <- df %>% 
  filter(iso_code == 'USA') %>%
  mutate(yest_new_deaths = lag(new_deaths), 
         yest_new_cases = lag(new_cases),
         yest_icu_patients = lag(icu_patients),
         yest_hosp_patients = lag(hosp_patients),
         yest_new_cases_smoothed = lag(new_cases_smoothed),
         yest_new_deaths_smoothed = lag(new_deaths_smoothed), 
         yest_icu_patients_per_million = lag(icu_patients_per_million),
         yest_hosp_patients_per_million = lag(hosp_patients_per_million),
         yest_stringency_index = lag(stringency_index),
         yest_new_tests_smoothed_per_thousand = lag(new_tests_smoothed_per_thousand)) %>%
  filter(date > "2020-09-30") #starts with March

# excluding outliers after residul analysis 
# #57,58 Thanksgiving
# #64, #65, #66 Dec 3-5
# 85 Chirstmas eve, 86, Christmas, 87 the day after Christmas
# usa_tuned <- usa[-c(85, 86, 87, 64, 65, 66, 57, 58),] 

usa_tuned <- usa[-c(64, 57, 59),] 



hist(usa$new_deaths_smoothed)

usa %>% 
  select(date, new_deaths, yest_new_deaths)
  
#' ## Data partitioning
#' split training and testing data set
set.seed(123)

# for time series, shuffle before splitting
idx_shuffled <- sample(nrow(usa))
usa_shuffled <- usa[idx_shuffled,] 

training.samples <- usa_shuffled$new_deaths %>%
  createDataPartition(p = 0.8, list = FALSE)

train.data  <- usa[training.samples, ]
test.data <- usa[-training.samples, ]

# usa_tuned
# for time series, shuffle before splitting
idx_shuffled_t <- sample(nrow(usa_tuned))
usa_shuffled_t <- usa_tuned[idx_shuffled_t,] 

training.samples.t <- usa_shuffled_t$new_deaths %>%
  createDataPartition(p = 0.8, list = FALSE)

train.data.tuned  <- usa[training.samples.t, ]
test.data.tuned <- usa[-training.samples.t, ]

#' ## Linear regression starts here
#' http://www.sthda.com/english/articles/40-regression-analysis/162-nonlinear-regression-essentials-in-r-polynomial-and-spline-regression-models/#polynomial-regression
#' plot the data out to check linearity
#' besides new_cases, other variables' relationship with stringency_index & tests are not obvious.  
#' so decided to drop it.
usa_selected <- usa %>% select(new_cases_smoothed, new_deaths_smoothed, icu_patients_per_million, 
                               new_tests_smoothed_per_thousand, hosp_patients_per_million, stringency_index)
plot(usa_selected)


#' ### Start with the most obvious trends
# Build the model
deaths.model <- lm(new_deaths_smoothed ~ yest_icu_patients_per_million, data = train.data ) # fit the model
summary(deaths.model)

par(mfrow = c(1, 1))
plot(usa$yest_icu_patients_per_million, usa$new_deaths_smoothed)
abline(deaths.model, col="blue")


#' the model is influenced by a few outliers 

#' ## Residual analysis
#'✖️ linearity,  🔺normality
par(mfrow = c(2, 2))
plot(deaths.model)

# Make a histogram of the residuals
# https://www.rpubs.com/stevenlsenior/normal_residuals_with_code
qplot(deaths.model$residuals,
            geom = "histogram",
            bins = 10) +
  labs(title = "Histogram of residuals",
       x = "residual")


#' ## Multiple Regression
#' try add new var and do multiple reg
#' first attempt

usa_selected <- usa %>%
select(new_deaths_smoothed,
       yest_new_deaths_smoothed,
       yest_icu_patients_per_million, 
       yest_new_cases_smoothed, 
       yest_new_tests_smoothed_per_thousand, #🚫
       yest_hosp_patients_per_million)
plot(usa_selected)


# fit the model
# remove yest_hosp_patients
multiple.regression.test <- lm(new_cases_smoothed ~ 
                            yest_new_deaths_smoothed
                          + yest_icu_patients_per_million 
                          + yest_new_cases_smoothed 
                          + yest_new_tests_smoothed_per_thousand #🚫
                          + stringency_index, 
                          data = train.data) 
summary(multiple.regression.test)


multiple.regression <- lm(new_cases_smoothed ~ 
                                 yest_new_deaths_smoothed
                               + yest_new_cases_smoothed 
                               + yest_icu_patients_per_million 
                               + stringency_index, 
                               data = train.data) 
summary(multiple.regression)

multi_predictions <- multiple.regression %>% predict(test.data)
# ✅️ validation 
data.frame(
  RMSE = RMSE(multi_predictions, test.data$new_cases_smoothed),
  R2 = R2(multi_predictions, test.data$new_cases_smoothed)
)

# Residual analysis
# https://data.library.virginia.edu/diagnostic-plots/
# https://www.youtube.com/watch?v=E27HcS9QaT0
# 🔺 linearity,  ✖ normality
par(mfrow = c(2, 2))
plot(multiple.regression)


qplot(multiple.regression$residuals,
      geom = "histogram",
      bins = 10) +
  labs(title = "Histogram of residuals",
       x = "residual")


#' Improving the model with tuned data
#' It fails the normality test still but improves in leverage and resi/fitted
#' Conclusion liner models might not be the best fit tho
#' But we will take it for now and move on 

multiple.regression.tuned <- lm(new_cases_smoothed ~ 
                            yest_new_deaths_smoothed
                          + yest_new_cases_smoothed 
                          + yest_icu_patients_per_million 
                          + yest_stringency_index, 
                          data = train.data.tuned) 

summary(multiple.regression.tuned)

multi_predictions_tuned <- multiple.regression %>% predict(test.data.tuned)


# Residual analysis
# 🔺 linearity,  ✖ normality
par(mfrow = c(2, 2))
plot(multiple.regression.tuned)


usa_tunded_selected <- usa_tuned %>% select(new_cases_smoothed, 
                                            yest_new_deaths_smoothed,
                                            yest_new_cases_smoothed,
                                            yest_icu_patients_per_million,
                                            yest_stringency_index)
plot(usa_tunded_selected)

# + yest_icu_patients_per_million #🚫


.fit <- lm(new_cases_smoothed ~ 
            yest_new_deaths_smoothed
          + yest_new_cases_smoothed 
          + yest_stringency_index, 
          data = usa_tuned) 

summary(.fit)

par(mfrow = c(2, 2))
plot(.fit)

#' # add predicted values back to df
#' add to the full data set so we will have full time series
intercept <- summary(.fit)$coefficients[1]
coeff_yest_new_deaths_smoothed <- summary(.fit)$coefficients[2]
coeff_yest_new_cases_smoothed <- summary(.fit)$coefficients[3]
coeff_yest_stringency_index <- summary(.fit)$coefficients[4]

usa$predicted_new_cases_smoothed <- usa$yest_new_deaths_smoothed * coeff_yest_new_deaths_smoothed 
                                      # + usa$yest_new_cases_smoothed * coeff_yest_new_cases_smoothed 
                                      # + usa$yest_stringency_index * coeff_stringency_index 
                                      + intercept

usa$deaths_variance <- usa$predicted_new_deaths_smoothed - usa$new_deaths_smoothed
usa$deaths_variance_pct <- usa$deaths_variance/usa$new_deaths_smoothed

result <- usa %>% select(date, new_deaths_smoothed, predicted_new_deaths_smoothed, deaths_variance, deaths_variance_pct) %>%
        mutate(across(deaths_variance_pct, round, 3)) %>%
        mutate("deaths_variance_%" = deaths_variance_pct * 100) %>%
        mutate(across(deaths_variance, round, 0)) 
        
result4plot <- result %>% select(date, new_deaths_smoothed, predicted_new_deaths_smoothed)

long <- reshape2::melt(result4plot, id.vars = "date")
ggplot(long, aes(x = date, y = value, 
                 group = variable, colour = variable)) +
  geom_line() +
  scale_y_log10() 

write.csv( result , "/Users/spechen/Desktop/MVTEC/mid-term/MVTEC-covid-test/output/for_d3/usa_prediction.csv", row.names = FALSE)