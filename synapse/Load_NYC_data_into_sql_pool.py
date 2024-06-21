from azureml.opendatasets import NycTlcYellow
from dateutil import parser

end_date = parser.parse('2018-06-06')
start_date = parser.parse('2018-05-01')
nyc_tlc = NycTlcYellow(start_date=start_date, end_date=end_date)
nyc_tlc_df = nyc_tlc.to_pandas_dataframe()
nyc_tlc_df = spark.createDataFrame(nyc_tlc_df)

nyc_tlc_df.write.mode("overwrite").saveAsTable("TestDatabase.NycTlcYellow")
