from WeatherImport import weather_import
# NOAA Individual access code
Token = 'ExHqFtwmXTLwOevojJsTbCcgZdlVYuRh'
# Date range for data being pulled
BeginDate = [2019, 10, 14] # Year, Month, Day
EndDate=[2019, 10, 15]
# Geographical region for data being pulled (Currently: MN State)
LocationID = 'FIPS:27'
# Interpolation settings
horz_dims = 100
vert_dims = 100
pval = 5

# Data call (returns numpy array with grid for start date first and grid of end date at the bottom)
weather_import(Token, BeginDate, EndDate, LocationID, horz_dims, vert_dims, pval)

# **Visualizations are currently commented out in function 'gen_format'. Aren't practical when pulling multiple days.
