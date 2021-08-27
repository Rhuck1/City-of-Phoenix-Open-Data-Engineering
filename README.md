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


## Creating an EC2 instance: The sevenfold path  

**Step 1: Choose an Amazon Machine Image**  
While you are in your AWS management console you will again click the Services dropdown in the upper left corner of the page. This will display the EC2 instance option under the *Compute* category, select it. On the next page you will click Launch Instance. At this point you are free to use whatever OS you prefer, however this is what I used:  

**Ubuntu Server 20.04 LTS (HVM), SSD Volume Type** - ami-03d5c68bab01f3496 (64-bit x86) / ami-09d9c897fc36713bf (64-bit Arm)  
Ubuntu Server 20.04 LTS (HVM),EBS General Purpose (SSD) Volume Type. Support available from Canonical (http://www.ubuntu.com/cloud/services).  

**Step 2: Choose an Instance Type**  
Choose the **t2.micro** instance type.   

**Steps 3-5**  
Just click next until step 6 is reached...maybe it should be renamed a fourfold path?  

**Step 6: Configure Security Group**  
Now we are going to restrict SSH access on port 22 by selecting My IP under the *Source* column dropdown. Then click Add Rule, and in the new row that appears, select PostgreSQL under the *Type* column dropdown as well as selecting My IP under the *Source* column dropdown so we can apply the same rule to port 5432 which is used by the PostgreSQL service.



## Creating and Connecting to PostgreSQL Database  

