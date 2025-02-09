# FraudSense - Real-Time Financial Fraud Detection  

## Team Members  

FraudSense was developed by a team of **four graduate students from George Mason University (GMU)** with expertise in **data engineering, machine learning, and cloud technologies**:  

- **Aravind Panchanthan**  
- **Praneeth Ravirala**  
- **Banudeep Reddy**  
- **Keerthana Reddy Singireddy**  

Our collective goal was to create an **efficient, scalable, and real-time fraud detection system** to improve **financial security** by leveraging **advanced data processing and machine learning techniques**.  

---

## Inspiration  

Financial fraud is a growing problem, leading to substantial financial losses for individuals and businesses. Traditional fraud detection systems often face challenges in accuracy, high false positives, and delayed response times. Our objective was to build a **real-time fraud detection system** that not only identifies fraudulent transactions efficiently but also gives businesses greater control over fraud prevention. By integrating **data engineering and machine learning**, we created a **scalable, automated pipeline** capable of handling large-scale financial transactions with precision.  

---

## What It Does  

FraudSense is a **real-time fraud detection system** that processes financial transactions every five minutes, detects anomalies using **machine learning**, and provides actionable insights. The system is designed to be **serverless, scalable, and highly secure**, ensuring seamless fraud identification while **minimizing false positives**.  

- **Ingests real-time transaction data** using an automated pipeline.  
- **Processes data efficiently** using AWS and Databricks.  
- **Detects fraudulent transactions** using machine learning models trained on financial fraud patterns.  
- **Generates fraud alerts** by integrating with ServiceNow for automated case management.  
- **Provides visualization dashboards** for fraud analysts to monitor and respond to fraudulent activities in real time.  

---

## How We Built It  

### **1. Model Architecture**  
We designed a robust **fraud detection pipeline** consisting of real-time ingestion, machine learning predictions, and alerting mechanisms. The architecture integrates **AWS, Databricks, and Tableau for seamless automation**.  

![Model Architecture](image3.jpg.jpg)  

---

### **2. Real-Time Data Ingestion**  
We started by setting up an automated **Python script** that executes **every 5 minutes** to fetch transaction data. The real-time data was then sent to **AWS EventBridge**, which was tied to an **AWS Lambda function**.  

- **IAM roles** were used to ensure security and access control.  
- Data was **stored in DynamoDB**, a NoSQL database optimized for high-speed transactions.  
- **Static data** from the IEEE-CIS Financial Fraud Dataset was stored separately in **Amazon S3** for batch processing.  



---

### **3. Data Processing & ML Pipeline**  
- The real-time data from **DynamoDB** and the static data from **Amazon S3** were **synced to Databricks**.  
- IAM access was configured using **instance profiles**, which was a complex task that took several hours to troubleshoot.  
- **Data preprocessing** was performed using **PySpark**, ensuring efficient feature extraction and transformation.  

---

### **4. Machine Learning Model Development**  
- We implemented a **LightGBM model**, trained on **seven key features** inspired by a Kaggle solution.  
- Feature selection focused on transactional attributes such as **user identity, card details, merchant information, device type, and time-based components**.  
- The model was trained on **Databricks**, optimizing it for fraud detection in **financial transactions**.  
- Predictions were generated every **5 minutes** to ensure real-time fraud detection.  
  
---

### **5. Fraud Alerts and Monitoring**  
- **ServiceNow integration** was implemented using REST APIs to automatically create **fraud case tickets** for high-risk transactions.  
- A **SQL Warehouse** was connected to Databricks, enabling **fraud analysts** to visualize transaction trends and identify fraud patterns.  
- **Email notifications** were configured to alert users about potentially fraudulent transactions, enhancing fraud prevention measures.  

---

## Tableau Dashboard  

We developed a **fraud detection dashboard** using **Tableau** to provide real-time visualization of fraud patterns and financial risks.  


---

## Challenges We Ran Into  

- **Complex AWS Integration**: Syncing data across **EventBridge, Lambda, DynamoDB, and S3** required extensive IAM role configurations, taking **3-4 hours** to resolve.  
- **Feature Selection & Model Optimization**: Finding the right features for fraud detection was time-consuming, requiring **several iterations** to optimize model accuracy.  
- **Real-Time Processing Constraints**: Ensuring that fraud predictions were generated **within minutes** while handling **large-scale transactions** was challenging.  
- **Webhook Implementation**: Setting up a **webhook-based sync** between **DynamoDB and Databricks** required extensive testing to achieve minimal latency.   

---

## Accomplishments That We're Proud Of  

- Successfully **built a real-time fraud detection pipeline** with end-to-end automation.  
- Implemented **real-time fraud predictions** with a **5-minute interval** between data ingestion and prediction generation.  
- Achieved **seamless integration** with **ServiceNow** for automated fraud case tracking.  
- Developed **a fully serverless solution** that is **scalable and cost-efficient**.  


---

## What We Learned  

![Learnings]

---

## What's Next for FraudSense  


---

## System Performance and Results  

The system was tested on **live transaction data** and successfully identified fraudulent patterns with **high accuracy and minimal false positives**.  

---

## GitHub Repository  

All code, datasets, and system architecture details can be found in our GitHub repository:  

[GitHub Repository Link](https://github.com/Banudeep/HACKNYU-fraud-data-detection-)  


---

## Final Thoughts  

FraudSense is a **real-time fraud detection system** that integrates **machine learning, big data processing, and cloud automation**. By leveraging AWS, Databricks, and ServiceNow, we have built a **scalable, automated fraud prevention solution**.  

This project was developed as part of **HackNYU 2025** under the **Capital One FinTech Track**, aiming to revolutionize fraud detection in financial transactions.  

---


 
