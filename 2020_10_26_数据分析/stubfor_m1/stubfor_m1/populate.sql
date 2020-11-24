/* Once you have your SQL Schema, you need to write **SQL statements which pull data 
from `Import`** and push it into your schema's tables. After running this script we 
should be able to delete `Impor`t with no loss of information.

This will likely be a *multistatement* SQL document with each statement terminated 
with a semicolon.

They will typically be of the form:
	insert into TABLENAME select ... from Import ...
This will put the results of your query into table TABLENAME. */