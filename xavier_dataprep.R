library(tidyverse)

# DATA EXAMINATION -----------------------------------

## main covid dataset from ourworldindata.org && country data in extra excel file .xls data
#COVID DATASET -------------------------------------- 
dd <- read.csv("https://covid.ourworldindata.org/data/owid-covid-data.csv",header=T)

# validate rows x columns, assign 
#dim(dd)
n <- dim(dd)[1]
K <- dim(dd)[2]
#c(n,K)

# validate dataset class
#class(dd)
#names(dd)
    
# declare factors
attach(dd)

# identify types and categorical 
#sapply(dd, class)
  # Most of variables are numerical

# convert date type
dd$date <- as.Date(dd$date, format='%Y-%m-%d')
#class(dd$date)

  # Column `test_units` 
  
test_units <- as.factor(dd$tests_units)
#levels(test_units)
    # [1] ""                                "people tested"                  
    # [3] "people tested (incl. non-PCR)"   "samples tested"                 
    # [5] "tests performed"                 "tests performed (incl. non-PCR)"
    # [7] "units unclear"  
    
  
    # recoding levels in `test_units`
newvalues <- c("unknown", "people_PCR", "people_All", "samples", "performed_PCR", "performed_All","unclear")
test_units <- newvalues[match(test_units,levels(test_units))] # declare recoded levels in factor
    
  # propagate levels
dd[,34] <- as.factor(test_units)


# COUNTRY DATA -------------------------------------- 
temp = tempfile(fileext = ".xlsx")
dataURL <- "https://github.com/spepechen/MVTEC-covid-test/raw/main/data/InfoPaisosExtra.xlsx"
download.file(dataURL, destfile=temp, mode='wb')

ddExtra <- readxl::read_xlsx(temp, na = "NA")
#dim(ddExtra)
nExtra <- dim(ddExtra)[1]
KExtra <- dim(ddExtra)[2]
#c(nExtra,KExtra)

# validate dataset class
#class(ddExtra)
#names(ddExtra)

# declare factors
attach(ddExtra)

# identify types and categorical 
#sapply(ddExtra, class)
  
# RECODING LEVELS
# Column Continent 
  Continent <- as.factor(ddExtra$Continent)
 # levels(Continent)
  # [1] "Africa"  "America" "Asia"    "Europe"  "Oceania"
  
# Column Country_Clasification 
  Country_classification <- as.factor(ddExtra$Country_Clasification)
  #levels(Country_Clasification)
  # [1] "BRICS" "NC"    "OECD" 
  
# Column Government_Type 
  GovType <- as.factor(ddExtra$Government_Type)
  #levels(GovType)
  # [1] "Absolut monarchy"                       "Communist state"                       
  # [3] "Constitutional monarchy"                "Dictatorship"                          
  # [5] "In Transition (provisional government)" "Islamic Parlamentary Republic"         
  # [7] "Islamic Presidential Republic"          "Islamic Semipresidential Republic"     
  # [9] "Parlamentary republic"                  "Presidential limited democracy"        
  # [11] "Presidential republic"                  "Semipresidential republic"   
  
  # recoding levels in Government_type
  newvalues <- c("AbsMonar", "Communist", "ConstMonar", "Dictatorship", "Transition", "IslParRep","IslPreRep","IslSemPreRep","ParRep","PreLimDemo","PreRep","SemPreRep")
  GovType <- newvalues[match(GovType,levels(GovType))] # declare recoded levels in factor
  
# Column Corruption_preception  
  Corruption_preception <- as.factor(ddExtra$Corruption_preception)
  #levels(Corruption_preception)
  # [1] "Highly corrupt" "Less corrupt"   "NI"  
  
  newvalues <- c("high", "low", "unknown")
  Corruption_preception <- newvalues[match(Corruption_preception,levels(Corruption_preception))] # declare recoded levels in factor
  
# Column Development_Status 
  Development_Status  <- as.factor(ddExtra$Development_Status)
  #levels(Development_Status)
  # [1] "Developed economies"  "Developing economies" "Transition economies"
  
  newvalues <- c("developed", "developing", "transition")
  Development_Status <- newvalues[match(Development_Status,levels(Development_Status))] # declare recoded levels in factor
  
# Column Land_Conditions       
  Land_Conditions <- as.factor(ddExtra$Land_Conditions)
  #levels(Land_Conditions)
  # [1] "Islands"    "Landlocked" "Sea Access"
  newvalues <- c("islands", "landlocked", "sea_access")
  Land_Conditions <- newvalues[match(Land_Conditions,levels(Land_Conditions))] # declare recoded levels in factor
  
# Propagate new levels 
  ddExtra[,2] <- as.factor(Continent)
  ddExtra[,3] <- as.factor(Country_Clasification)
  ddExtra[,4] <- as.factor(GovType)
  ddExtra[,5] <- as.factor(Corruption_preception)
  ddExtra[,6] <- as.factor(Development_Status)
  ddExtra[,7] <- as.factor(Land_Conditions)
  
# Define ordered factors   
  ddExtra = ddExtra %>% mutate(Development_Status = factor(Development_Status, ordered=TRUE, c("developed","transition","developing")))
  
#DATA JOIN -----------------------------------

# Using library `countrycode`---
ddExtra2 <- ddExtra %>% 
  mutate(iso_code = countrycode::countrycode(COUNTRY, origin = 'country.name', destination = 'iso3c')) %>% 
  remove_rownames %>% 
  column_to_rownames(var="COUNTRY")
  
# XK for Kosovo
# GB-CHA for Channel Islands
# https://simple.wikipedia.org/wiki/ISO_3166-2:GB
  
ddExtra2["Kosovo", "iso_code"] = 'XK'
ddExtra2["Channel Islands", "iso_code"] = 'GB-CHA'
  
  
#DROP POPULATION ----     
# Quick calculation of 'total population' differences between datasets to drop the least updated
CountryPopul <- aggregate(ddExtra2$Population_total, by = list(factor(ddExtra2$iso_code)), FUN=mean)
dd_CountryPopul <- aggregate(dd$population, by = list(factor(dd$iso_code)), FUN=mean)
  
Popul_diff <- CountryPopul %>%
  left_join(dd_CountryPopul,by = "Group.1") 

  
  
Popul_diff$diff <- Popul_diff$x.x - Popul_diff$x.y
Popul_diff$percent <-scales::percent( (Popul_diff$x.x - Popul_diff$x.y)/Popul_diff$x.x )
  
#Popul_diff %>% arrange(desc(diff))
# Group.1       x.x       x.y      diff    percent
# 1       VEN  30045134  28435943   1609191  -5.65900%
# 2       UKR  45271947  43733759   1538188  -3.51716%
# 3       SYR  18715672  17500657   1215015  -6.94268%
# 4       FRA  66316100  65273512   1042588  -1.59726%
# 5       JPN 127276000 126476458    799542  -0.63217%
# 6       PRI   3534874   2860840    674034 -23.56070%
# 7       ROU  19908979  19237682    671297  -3.48949%
# 8       GRC  10892413  10423056    469357  -4.50307%
  
ddExtra2 <- ddExtra2 %>% select(-Population_total)
  
#Join datasets ----
# Set column_names
colnames(ddExtra2) <- c('continent',
                        'country_class',
                        'gov_type',
                        'corruption',
                        'dev_status',
                        'land_conditions',
                        'gdp_energy',
                        'urban_pop',
                        'iso_code')
  
# Join
merged_dataset <- select(dd, -continent) %>%
  left_join(ddExtra2, by = 'iso_code')
      

#Save file ----
# USING HEROKU EPHEMERAL SYSTEM -> https://stackoverflow.com/questions/12416738/how-to-use-herokus-ephemeral-filesystem
setwd(file.path(getwd(), fsep = .Platform$file.sep))
write.csv(merged_dataset, file='./tmp/merged_data.csv')

merged_dataset

# for (i in merged_dataset) {
#   NonNAindex <- cbind(NonNAindex, min(which(!is.na(i))))
#   }
# 
# firstNonNA <- min(NonNAindex)



#write.csv(merged_dataset, file='./output/merged_data.csv')
#saveRDS(merged_dataset, file="output/merged_data.RDS")

