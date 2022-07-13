# holostyak-bot
It is a telegram bot that will help you with your cooking ideas. 

## commands
+ /save — will save your idea (only admins)
+ /idea — will give you random cooking idea
+ /show_all — will show all your ideas
+ /delete — will delete idea (only admins)
## Setting up
You need to install psycopg2
```
    pip3 install psycopg2
```
You should have [PostgreSQL](https://www.postgresql.org/) installed on your machine. 

In the directory of the project you need to create config.json file in configs folder. You can use config_template.json as an example. 

Then you need to run **create_table.py**
