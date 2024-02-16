# Pinetrest Data Piplines
## Table of Contents
## A description of the project: what it does, the aim of the project, and what you learned
## Installation instructions

### Create.pem key
 Create a file with a .pem extention 
 Naviage to the Parameter store 
![alt text](Images/Images_1/image.png)
Find the specific key pair associated with your EC2 instance. 
![alt text](Images/Images_1/image-1.png)
Select this key pair and under the Value field select Show.
![alt text](Images/Images_1/image-2.png)![alt text](Images/Images_1/image-3.png)
This will reveal the content of your key pair.

 Copy its entire value (including the BEGIN and END header) and paste it in the .pem file in VSCode.
![alt text](Images/Images_1/image-4.png)


 Navigate to the EC2 console and identify the instance with your unique UserId. Select this instance, and under the Details section find the Key pair name and make a note of this. Save the previously created file in the VSCode using the following format: Key pair name.pem



### Connect to E2C instance on SSH Client 
Naviagte to EC2>Instances>your instance >Connect an instance.
Follow the SHH Client instructions
![alt text](Images/Images_1/image-5.png)
Create the following commands for your vs code terminal 

chmod 400 "C:\Users\quann\OneDrive\Desktop\Data Engineering\Projects\Pinetrest_data_pipline\pyvenv\name.pem"

ssh -i "C:\Users\quann\OneDrive\Desktop\Data Engineering\Projects\Pinetrest_data_pipline\pyvenv\name.
pem" ec2-user@ec2-3-80-205-48.compute-1.amazonaws.com

Once run ... Your terminal should look like this

![alt text](Images/Images_1/image-6.png)

### Run Kafta on E2C instance 
Update Java using this command :

sudo yum install java-1.8.0

Install Kafka on your client EC2 machine using this command

wget https://archive.apache.org/dist/kafka/2.8.1/kafka_2.12-2.8.1.tgz
tar -xzf kafka_2.12-2.8.1.tgz

Install the IAM MSK authentication package on your client EC2 machine using this command

wget https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.5/aws-msk-iam-auth-1.1.5-all.jar

Naviagte to Roles in IAM and change the Trust relationships json to add the ARN in the summary box above
![alt text](Images/Images_1/image-7.png)

Configure your Kafka client to use AWS IAM authentication to the cluster by adding a configration.proprties file in your kafka bin
Use this command to create the file
nano client.properties
![alt text](Images/Images_1/image-8.png)
The configuration file should look like this. Replace the awsRoleARN with your own ARN role

Find the Bootstrap servers string and the Plaintext Apache Zookeeper connection string. Make a note of these
![alt text](Images/Images_1/image-9.png)
Create a classpath in the bin of your Kafta file

export CLASSPATH=/home/ec2-user/kafka_2.12-2.8.1/libs/aws-msk-iam-auth-1.1.5-all.jar

Create these 3 topics using the Bootstap Server and Arn role 
![alt text](Images/Images_1/image-10.png)
The ARN needed can be found in MSK > Clusters
arn:aws:iam::584739742957:role/0abf7f0cd605-ec2-access-role

### Create a coustom plugin with MSK
Go to the S3 console and find the bucket that contains your UserId and make a note of it 
![alt text](Images/Images_1/image-11.png)
On your EC2 client, download the Confluent.io Amazon S3 Connector and copy it to the S3 bucket you have identified in the previous step. Use the code below:
![alt text](Images/Images_1/image-12.png)
Wget https://client.hub.confluent.io/confluent-hub-client-latest.tar.gz
create a class path for the above 
export CLASSPATH=/home/ec2-user/kafka_2.12-2.8.1/bin/onfluent-hub-client-latest.tar.gz

Once done your vs code should look like this 
![alt text](Images/Images_1/image-13.png)

Create your custom plugin in the MSK Connect console
![alt text](Images/Images_1/image-14.png)
![alt text](Images/Images_1/image-15.png)
![alt text](Images/Images_1/image-16.png)
![alt text](Images/Images_1/image-17.png)
![alt text](Images/Images_1/image-18.png)

### Create a custom connector with MSK Connect
Now, open the MSK console and select Custom plugins under the MSK Connect section on the left side of the console. Choose Create custom plugin.
![alt text](Images/Images_1/image-19.png)
In the list of plugin, select the plugin you have just created, and then click Next
![alt text](Images/Images_1/image-22.png)
then choose your MSK cluster from the cluster list.
![alt text](Images/Images_1/image-23.png)
Change connector capacity to the following
![alt text](Images/Images_1/image-24.png)
Select IAM role previously created 
![alt text](Images/Images_1/image-25.png)

### Build a Kafka REST proxy integration method for the API
Create a resource that allows you to build a PROXY integration for your API.
![alt text](Images/Images_1/image-26.png)
![alt text](Images/Images_1/image-27.png)
![alt text](Images/Images_1/image-28.png)
![alt text](Images/Images_1/image-29.png)
![alt text](Images/Images_1/image-30.png)
create a HTTP ANY method
To get started go to the API Gateway console and select one of your previously created APIs. Your API should have a {proxy+} resource. To set up an integration click on the ANY resource, then on the Edit integration button
![alt text](Images/Images_1/image-31.png)
For HTTP method select ANY.
For the Endpoint URL
![alt text](Images/Images_1/image-32.png)
Public IPv4 DNS copied : http://ec2-3-80-205-48.compute-1.amazonaws.com:8082/{proxy}
![alt text](Images/Images_1/image-33.png)

### Set up the Kafka REST proxy on the EC2 client 
First, install the Confluent package for the Kafka REST Proxy on your EC2 client machine.
To install the REST proxy package run the following commands on your EC2 instance:
sudo wget https://packages.confluent.io/archive/7.2/confluent-7.2.0.tar.gz
tar -xvzf confluent-7.2.0.tar.gz 
Your screen should look like this :
![alt text](Images/Images_1/image-34.png)
Once the file is downloaded and unzipped 

navigate to confluent-7.2.0/etc/kafka-rest
nano kafka-rest.properties and add this code changing the arn as necessary and  bootstrap.servers and the zookeeper.connect variables in this file, with the corresponding Boostrap server string and Plaintext Apache Zookeeper connection string respectively
![alt text](Images/Images_1/image-35.png)

 Deploy the API and make a note of the Invoke URL

 ![alt text](Images/Images_1/image-36.png)
 https://kdnbpq3ufb.execute-api.us-east-1.amazonaws.com/Pinetrest

 Set up the Kafka REST proxy on the EC2 client 
 
 ./kafka-rest-start /home/ec2-user/confluent-7.2.0/etc/kafka-rest/kafka-rest.properties

 ![alt text](Images/Images_1/image-37.png)

 Modify the user_posting_emulation.py to send data to your Kafka topics using your API Invoke URL.
 
 
 You should have one invoke URL per a topic 
 
 invoke_url = "https://kdnbpq3ufb.execute-api.us-east-1.amazonaws.com/Pinetrest/topics/0abf7f0cd605.pin"
 
 invoke_url = "https://kdnbpq3ufb.execute-api.us-east-1.amazonaws.com/Pinetrest/topics/0abf7f0cd605.geo"
 
 invoke_url = "https://kdnbpq3ufb.execute-api.us-east-1.amazonaws.com/Pinetrest/topics/0abf7f0cd605.user"

 
 Check data is sent to the cluster by running a Kafka consumer (one per topic).
 Check if data is getting stored in the S3 bucket. Notice the folder organization
 ![alt text](Images/Images_1/image-38.png)

 ### Mount a S3 bucket to Databricks
 
 We will need to import the following libraries first
 ![alt text](Images/Images_1/image-39.png)
 Now let's read the table containing the AWS keys to Databricks using the code below:
 ![alt text](Images/Images_1/image-40.png)
 We can extract the access key and secret access key from the spark dataframe created above. 
 ![alt text](Images/Images_1/image-41.png)
 We can now mount the S3 bucket by passing in the S3 URL and the desired mount name to dbutils.fs.mount(). 
 ![alt text](Images/Images_1/image-42.png)

 Read the JSON format dataset from S3 into Databricks using the code cells below:
 ![alt text](Images/Images_1/image-43.png)
 and now create 3 new Dataframes

![alt text](Images/Images_1/image-45.png)
![alt text](Images/Images_1/image-46.png)
![alt text](Images/Images_1/image-47.png)
 

 
 
 
 
 










## Usage instructions
## File structure of the project
## License information# Pinterest-data-pipeline
# Pinterest-data-pipeline
# Pinterest-data-pipeline
# Pinterest-data-pipeline
