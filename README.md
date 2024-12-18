There are 3 python files: 
- scrapper.py
- server.py
- client.py

Scrapper uses selenium to fetch all the employee names from the RIT Dubai faculty website, and automates the process. Just run "python scrapper.py" and it will open firefox 
by default and fetch all the data. The Load more button is clicked automatically. 
To change the browser to any browser of you choice, the options should be changed in the scrapper load_page() funciton. Chrome driver is already in this repository. 

Server is ran with "python server.py" and it will display that server is running, and will print out the results when the client is ran. 

Client is ran with command "python client.py <query file> <response file>", however note that query file must be in XML form and must already exist in the directory. 
The response file is created when the command is executed, and all the results are saved. 

Note that Query file should be in the following format if the client wishes to make custom queries: 

<query>
  <condition>
  <column>"Insert Column to search"</column>
  <value>"Insert value you are looking for"</value>
  </condition>
</query>

Multiple condition tags could be made, as long as it is inside the query tag.

Open the response file and hit Ctrl + Shift + Alt + B to see the response XML file in a pretty and organized manner. 

