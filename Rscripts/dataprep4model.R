suppressMessages(library(tidyverse))
suppressMessages(library(zoo))

# load data
c <- read.csv("https://mvtec-group3.s3-eu-west-1.amazonaws.com/project/currency_output.csv",header=T)
df <- read.csv("https://covid.ourworldindata.org/data/owid-covid-data.csv",header=T)

# Preprocessing 
names(c) <- tolower(names(c))
df$date <- as.Date(df$date, format='%Y-%m-%d')
c$date <- as.Date(c$date, format='%Y-%m-%d')


currency <- c %>% 
  select(price, date) %>%
  complete(date = seq(min(date), max(date), by = "day"), # fill missing rate with previous date's
           fill = list(price = NA)) %>%
  fill(price) %>%
  rename(usd2twd = price) %>%
  mutate(usd2twd_avg = zoo::rollmean(usd2twd, k = 3, fill = NA)) # 3 day rolling avg to get smoother line
  
usa <- df %>% 
  filter(iso_code == 'USA') %>%
  merge(currency, by='date') %>% 
  filter(date > "2020-09-29") %>% # to preserve one extra day for lagging nad start from OCT
  mutate(yest_new_cases_smoothed = lag(new_cases_smoothed), 
         yest_new_deaths_smoothed = lag(new_deaths_smoothed)) 

# Add preditcted value column 
# usa$predicted_usd2twd <- usa$yest_new_cases_smoothed * coeff_new_cases + usa$yest_new_deaths_smoothed * coeff_new_deaths + intercept
usa$predicted_usd2twd <- usa$yest_new_cases_smoothed * -0.00000103668 + usa$yest_new_deaths_smoothed * -0.000210322 + 28.90744

result_curr <- usa %>% select(date, usd2twd, usd2twd_avg, predicted_usd2twd)%>% 
                        filter(date > "2020-09-30") #actually starts from OCT

# output to capture in stdout
cat(format_csv(result_curr))

# write.csv( result_curr , "/Users/spechen/Desktop/MVTEC/mid-term/MVTEC-covid-test/output/for_d3/usa_prediction_curr.csv", row.names = FALSE)
