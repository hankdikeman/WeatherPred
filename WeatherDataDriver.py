from WeatherImport import weather_import
Token = 'ExHqFtwmXTLwOevojJsTbCcgZdlVYuRh'
BeginDate = [2019, 10, 14] # Year, Month, Day
EndDate=[2019, 10, 14]
LocationID = 'FIPS:27'
weather_import(Token, BeginDate, EndDate, LocationID)
