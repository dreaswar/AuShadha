Setup the PostgreSQL database for your OS
------------------------------------------
Please refer to your OS notes on how to do this.  
AuShadha has been tested with PostgreSQL Server version 9.3  
Once you have installed Postgres server and pgadmin3 client you should be able to run `psql` from terminal and get a prompt

Creating and AuShadha PostgreSQL database
------------------------------------------
Preferred DB for running AuShadha is PostgreSQL. 

1. Set up PG for your OS
Please see your OS website for instructions on setting up PG 
PG should be is setup and accesible from command line as >> psql prompt


2. Set up a System user with same name as the Postgres user
Create an OS user with `<adduser>` command from terminal
Create a `/home/<user_name>` directory for the user and run `chown -R <user_name> /home/<user_name>`
The username used by default for DB and user is `'aushadha'` with password of `aushadha`


3. Create an empty DB and Grant permissions

From terminal run the `createuser` to create and user with username `'aushadha'`
Run `psql` to get into the pg command line from the user that is allowed to run `psql`

4. Run the following  

`CREATE DATABASE aushadha WITH OWNER aushadha;`  

`GRANT ALL ON DATABASE aushadha TO <system_os_user> WITH GRANT OPTION;`  

