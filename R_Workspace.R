#library('Catflow')
# OR Initialise own version of R package codes
# initialize Catflow
library('Catflow')
library(zoo)

testde_3 <- read.csv("C:/Users/as2023/bwSyncShare/01_Analysis/02_Europe_Flood/03_CATFLOW/in/climate/testde_3.csv")

data_era5 = zoo(testde_3$total_precipitation_sum, order.by = as.Date(testde_3$date))
data_lstm = zoo(testde_3$testde_2, order.by = as.Date(testde_3$date))
data_eobs = zoo(testde_3$eobs, order.by = as.Date(testde_3$date))
data_dwd = zoo(testde_3$Daily_Precipitation, order.by = as.Date(testde_3$date))

options(scipen = 999)
write.precip(data_era5,'Precip_era5.dat',start.time='02.01.1980 00:00:00'
             ,time.unit='s',faktor.p = 1)
write.precip(data_lstm,'Precip_lstm.dat',start.time='02.01.1980 00:00:00'
             ,time.unit='s',faktor.p = 1.157407408e-08)
write.precip(data_eobs,'Precip_eobs.dat',start.time='02.01.1980 00:00:00'
             ,time.unit='s',faktor.p = 1.157407408e-08)
write.precip(data_dwd,'Precip_dwd.dat',start.time='02.01.1980 00:00:00'
             ,time.unit='s',faktor.p = 1.157407408e-08)

write.printout(output.file = "printout_2010_16.prt",
               start.time = "01.01.2010 00:00:00",
               end.time = "31.12.2016 00:00:00",
               intervall = 10, time.unit = "d",
               flag = 1)

# Reading Output Files
setwd("C:/Users/ashish/bwSyncShare/01_Analysis/01_Krebsbach_Reservoir/W22/CATFLOW")
system( './Catflow.exe' , show.output.on.console = TRUE, invisible = FALSE, wait=T)
write.printout(output.file = "printout.prt",
               start.time = "08.06.2016 00:00:00",
               end.time = "09.06.2016 00:00:00",
               intervall = 300, time.unit = "s",
               flag = 1)

geometry = read.geofile('./in/hillgeo/rep_hill.geo')
soilmoisture = read.catf.resultmat('./out/theta.out')
soil = read.soil.mat(input.file = "boden.dat")
colfunc <- colorRampPalette(c("orange", "blue"))
colfunc(10)
colorsForCuts = colfunc(5)
lowercut =0.20
uppercut =0.50
lencut =4
plot.catf.movie(soilmoisture,geometry,begindate='08.06.2016 00:00:00.00')
resultmat = soilmoisture
geof = geometry
color.codes()

plot.catf.grid(x = geometry$sko, y = geometry$hko, 
                sel = NULL, boundcol = 1, 
               plotting = TRUE, plotpoints = F)

# Reading Output Files


# Extracting from Raster
setwd("C:/Users/ashish/bwSyncShare/01_Analysis/01_Krebsbach_Reservoir/W22/ClimateData")
SM = "SoilMoisture.grib"
library(terra)
##Downloading file
grib_data <- terra::rast(SM)
print(grib_data)

## Convert to data frame
df <- as.data.frame(grib_data, xy=TRUE)
