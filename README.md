# Google-Core-Web-Vitals-Googlesheets-Dashboard
Populate GoogleSheets with Core Web Vitals Data against configurable URLs and visualise it

@Anthony - pls describe what Core Web Vitals are and its usage.

## Business Benefits

## Prerequisites
- Access to Google Core Web Vitals (CWV) API
- Access to  Google Developer Console
- Access to Google Cloud Pub-Sub, Scheduler and Functions (any other Enterperise Cloud will work as well)

## High level steps

[1. Get Google Core Web Vitals API Key](#step1)

[2. Create GoogleSheets](#step2)

[3. Create Google Service Account with GoogleSheets APIs](#step3)

[4. Share GoogleSheets with Google Service Account](#step4)

[5. Python code to read CWV data using API and update GoogleSheet](#step5)

[6. Schedule Python code to run recurrently using GCP Cloud Functions, Cloud Scheduler and Pub-Sub](#step6)

[7. Visualise activities data using Google Data Studio](#step7)

[8. Share GoogleSheet and Data Studio Dashboard](#step8)


## Detailed steps

### <a name="step1"></a> Step 1. Get CV API Key

### <a name="step2"></a> Step 2. Create GoogleSheets

### <a name="step3"></a> Step 3.Create a Google Service Account

Follow [steps to create a Google Service Account](https://github.com/pierian-co/custom-cxo-activity-dashboard-adobe-target-googlesheets/blob/main/create_googleserviceaccount.md).

### <a name="step4"></a> Step 4. Share GoogleSheets with Google Service Account

For read and update operations, both GoogleSheets must be given access to the Service Account Client email address.

a. Copy client-email address from the JSON file downloaded while creating Google Service Account in Step 3 above.

b. For both GoogleSheets (Credentials and ActivitiesData), click on Share button. Paste and select the client-email address.

![Share GoogleSheets with Google Service Account](https://user-images.githubusercontent.com/71815964/104570760-3b74a180-564a-11eb-97ae-899c8aebaaa9.png)

c. Make sure to provide Editor access to the client-email.
![Share GoogleSheets with Google Service Account Editor Access](https://user-images.githubusercontent.com/71815964/104573412-c3f44180-564c-11eb-81ce-c528fa7eb422.png)


### <a name="step5"></a> Step 5. Execute the Python code

### <a name="step6"></a> Step 6. Schedule Python code to run recurrently

### <a name="step7"></a> Step 7. Visualise data using Google Data Studio

### <a name="step8"></a> Step 8. Share the CWV-Data GoogleSheet and Data Studio Visualisation
