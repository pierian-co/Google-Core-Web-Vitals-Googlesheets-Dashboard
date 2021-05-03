# Google-Core-Web-Vitals-Googlesheets-Dashboard
Populate GoogleSheets with Core Web Vitals Data against configurable URLs and visualise it

## Introduction to Core Web Vitals
![image](https://user-images.githubusercontent.com/71815964/116887616-6a774900-ac22-11eb-8fbd-573d05f0a295.png)


In May 2020, Google announced that page experience signals will be included in Google Search Ranking. The new page experience signals combine Core Web Vitals with their existing search signals of mobile-friendliness, safe-browsing, HTTPS-security, and intrusive interstitial guidelines. Rolling out in May 2021, it’s important that you assess your website to align with Core Web Vitals. So very briefly, there are three signals that go into Core Web Vitals. 

1. Largest contentful paint (LCP)
The first being largest contentful paint (LCP). This basically asks, in layman's terms, how fast does the page load? Very easy concept. So this is hugely influenced by the render time, the largest image, video, text in the viewport.

That's what Google is looking at. The largest thing in the viewport, whether it be a desktop page or a mobile page, the largest piece of content, whether it be an image, video or text, how fast does that take to load? Very simple. That can be influenced by your server time, your CSS, JavaScript, client-side rendering.

All of these can play a part. So how fast does it load? 

2. Cumulative layout shift (CLS)
The second thing, cumulative layout shift (CLS). Google is asking with this question, how fast is the page stable? Now I'm sure we've all had an experience where we've loaded a page on our mobile phone, we go to click a button, and at the last second it shifts and we hit something else or something in the page layout has an unexpected layout shift.

That's poor user experience. So that's what Google is measuring with cumulative layout shift. How fast is everything stable? The number one reason that things aren't stable is that image sizes often aren't defined. So if you have an image and it's 400 pixels wide and tall, those need to be defined in the HTML. There are other reasons as well, such as animations and things like that.

But that's what they're measuring, cumulative layout shift. 

3. First input delay (FID)
Third thing within these Core Web Vitals metrics is first input delay (FID). So this question is basically asking, how fast is the page interactive? To put it another way, when a user clicks on something, a button or a JavaScript event, how fast can the browser start to process that and produce a result?

It's not a good experience when you click on something and nothing happens or it's very slow. So that's what that's measuring. That can depend on your JavaScript, third-party code, and there are different ways to dig in and fix those. So these three all together are Core Web Vitals and play into the page experience signals. So like I said, let's not get hung up on these.

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

There are 2 Googlesheets required for this project.
1. Config Googlesheet:
This Googlesheet contains all the configurations and keys for extracting the CWV data. This Googlesheet should not be shared with non-Admins. It contains 3 worksheets:
1.a Pages: list of page-URLs you want to report on
1.b Credentials: List of all API-Keys that are required to extract the CWV data

Template for this Googlesheet can be found [here](https://docs.google.com/spreadsheets/d/12hlKqNmwC0zOOapxRd9hwmMPsnVyIciQqtNLRUWjcEQ/edit?usp=sharing)


2. Data Googlesheet:
CWV data goes in this sheet. It contains columns corresponsing to Date, Time and various scores related to CWV.

Template for this Googlesheet can be found [here](https://docs.google.com/spreadsheets/d/1spMGw5MJziVbIv7yiS1bWw16i59bXnXIjwEafvjGzAQ/edit?usp=sharing)

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
