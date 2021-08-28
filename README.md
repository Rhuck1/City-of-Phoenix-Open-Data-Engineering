# City of Phoenix Open Data Engineering

<img src="images/phx.jpg" width="800">  

## Overview Motivation  

This project will serve to highlight the data engineering process. I will automate the collection of the City of Phoenix City Checkbook fiance data from their Open Data website. It will then be processed through a data pipeline where a model will be applied and the results broadcast through a web application.  


Below is an outline of the data engineering pipeline  
<img src="images/pipeline_process.png" width="800">  


## Setting up an S3 bucket  

I am going to use an S3 bucket as the first stop on my data pipeline journey. The S3 bucket will be useful to collect the raw data from the City of Phoenix city checkbook as is. This means that there will not be any data transformation (aka business logic) applied to the data at this step.

First, you will navigate to AWS cloud services site [here](https://aws.amazon.com/). Create an account if you don't already have one, then log in. Once you are logged in you should see a Services dropdown in the upper left corner of the page, click it. Select the S3 option under the *Storage* category. Next, click Create Bucket, name it appropriately and you are off to the races.  
[Here](https://www.youtube.com/watch?v=fc05rd0iZhM) is a nice YouTube video for more assistance.


## Creating an EC2 instance and a PostgreSQL Database

**Step 1: Choose an Amazon Machine Image**  
While you are in your AWS management console you will again click the Services dropdown in the upper left corner of the page. This will display the EC2 instance option under the *Compute* category, select it. On the next page you will click Launch Instance. At this point you are free to use whatever OS you prefer, however this is what I used:  

**Ubuntu Server 20.04 LTS (HVM), SSD Volume Type** - ami-03d5c68bab01f3496 (64-bit x86) / ami-09d9c897fc36713bf (64-bit Arm)  
Ubuntu Server 20.04 LTS (HVM),EBS General Purpose (SSD) Volume Type. Support available from Canonical (http://www.ubuntu.com/cloud/services).  

**Step 2: Choose an Instance Type**  
Choose the **t2.micro** instance type.   

**Steps 3-5**  
Just click next until step 6 is reached...maybe it should be renamed a fourfold path?  

**Step 6: Configure Security Group**  
Now we are going to restrict SSH access on port 22 by selecting My IP under the *Source* column dropdown. Then click Add Rule, and in the new row that appears, select PostgreSQL under the *Type* column dropdown as well as selecting My IP under the *Source* column dropdown so we can apply the same rule to port 5432 which is used by the PostgreSQL service. Then click next.

**Step 7: Review Instance Launch**  

Click the Launch button in the lower right hand of page. Now we will create a new key pair by selecting this option in the first dropdown. Then type in the key pair name below the dropdown (i.e postgres-on-ec2) and click Download Key Pair to dowload the key pair. After it has been downloaded, click on Launch Instances.  

At this point it's probably best to follow the details in this video [here](https://www.youtube.com/watch?v=LV2ooRnZqpg) beginning at 1:40, however I will do my best to capture them.  


## Connecting to PostgreSQL Database  

While the instances launch jump into your terminal and navigate to your downloads directory and enable read-only mode on the pem file just downloaded. An example of the command to do so is below, just remember to use your pem file name:  

```console
chmod 0400 postgres-on-ec2.pem
```

This will allow us to read the file and allow us to authenticate with the server.  

Next, move the file to the .ssh directory:  

```console
mv postgres-on-ec2.pem ~/.ssh
```  

Open the ssh config in your coding environ:  

```console
code ~/ssh/config
```  

Then provide the following info, where HostName is the IP address of your EC2 instance:  
 
    Host postgres-on-ec2
        HostName ##.###.###.###
        User ubuntu
        IdentityFile ~/.ssh/postgres-on-ec2.pem
        IdentitiesOnly yes

Now we can connect to the remote machine with the following command:  

```console
ssh postgres-on-ec2.pem
```  

Next, update the package list and upgrade the system:  

```console
sudo apt-get update -y
```  

With the package list updated, let's install postgres:  

```console
sudo apt install postgresql -y
```  

The postgres installer will create a user for us named postgres, this user can be used to communicate with the postgres service. First we are going to login as postgres:  

```console
sudo su postgres
```  

Then we are going to use the postgres user to create a role named ubuntu:  

```console
psql -U postgres -c "CREATE ROLE ubuntu;"
```  

This role will be used to communicate with the database.  

```console
psql -U postgres -c "CREATE ROLE ubuntu;"
```  

Apparently the best practice is to create users with the minimum amount of priviledges they need to carry out whatever operations you want them to do. In this example we are going to allow the ubuntu role to login and create databases.  

```console
psql -U postgres -c "ALTER ROLE ubuntu WITH LOGIN;"
```  

Then:  

```console
psql -U postgres -c "ALTER USER ubuntu CREATEDB;"
```  

SIDE NOTE: In case you want to store multiple databases that will be consumed by different applications, make sure to create one user per application. This way you can control access and compartmentalize what databases will be accessible why which user.  

To finish up the user configuration we are going to assign a password, where 'password' is whatever password you decide to choose:  

```console
psql -U postgres -c "ALTER USER ubuntu WTIH PASSWORD 'password';"
```  

Then exit the postgres service:

```console
exit
```   

Right now our postgres server is only accessible from within the virtual machine. To make it accessible from the outside we will need to edit the postgres configuration file. To do this we will find it:  

```console
sudo find / -name "postgresql.conf"
```  
    >>>/usr/lib/tmpfiles.d/postgresql.conf
    >>>/etc/postgresql/12/main/postgresql.conf  
    
And then edit the line that says listen_addresses:  

```console
sudo nano /etc/postgresql/12/main/postgresql.conf
```  

It needs to be changed from *localhost* to *. This will allow Postgres to communicate over the public DNS name of this server:  

    listen_addresses = '*'  
    
Next we need to allow users to authenticate with the server. In order to do that we are going to find another file:  

```console
sudo find / -name "pg_hba.conf"
```  

    >>>/etc/postgresql/12/main/pg_hba.conf

We are going to edit this file with nano:  

```console
sudo nano /etc/postgresql/12/main/postgresql.conf
```  

And at the bottom of the file, drop in the following code:  

    host    all             all             0.0.0.0/0               md5
    host    all             all             ::/0                    md5  
    
Now we are going to restart postgres:  

```console
sudo systemctl restart postgresql
```  

At this point the server is ready for use. I am going to use pgAdmin to test it out by opening up pgAdmin in the browser: 

http://server_ip/pgadmin4  

Making sure to change server_ip with localhost, domain name pointed the system or system ip address. Then I will click on Add New Server. In the popup under the tab *General* I am going to give it the name *ec2-postgres*. Then under the *Connection* tab I am going populate the Host name/address field with the public DNS name from my EC2 instance (i.e. Public IPv4 DNS) in the AWS management console. Finally, I will provide the *Username* and *Password* that we configured from earlier and save.    

Now I will R-click on *Databases* -> Create -> Database... and name it *test_database* in the *Database* field. Head over to this database on the left side of the pgAdmin panel. Click the *Schemas* dropdown and R-click *Tables* -> Create -> Table... to create a *users* table by inputing users into the *Name* field. Then click on the *Columns* header to add a column *Name* "name" with a *Data type* "text" and save.  






