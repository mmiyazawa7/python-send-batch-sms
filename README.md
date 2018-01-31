# python-send-batch-sms
Python scripts to send batch SMS from a CSV file


# Installation 
## Install Python 3.5
- Windows:  https://docs.python.org/3/using/windows.html
- Mac: http://www.marinamele.com/2014/07/install-python3-on-mac-os-x-and-use-virtualenv-and-virtual envwrapper.html

## Install Python modules
(pip should be installed tith Python)
- RateLimiter: pip3 install ratelimiter
- Requests: pip3 install requests

## Settings
In the code, setup the following parameters
- `SENDER_ID = ''` in most countries you swill be able to add an alpha sender id, e.g. YOUBRAND. In the US/Canada, you will need to use a Nexmo LVN
- `CALLBACK_URL = ''` Set your callback url to log message status and responses. Use the PHP file `batchsmscallback.php` on your server if you can
- `OPT_OUT = ''` This will add an opt-out text to your messages. Please refer to your country legislation

# Usage
From a command prompt: 

```python
python3 SendMassSMS.py -k <key> -s <secret> -i <source.csv> -o <dest.csv>
```

Where:
- `key` and `secret` are your API_KEY and API_SECRET from your Nexmo dashboard (https://dashboard.nexmo.com/) > Username > Settings
- `source.csv` is your file containning a header with `telephone` and `message` (with no whitespace). Messages can contains commas as the delimiter is a semicolumn ';'.
Example: telephone;message
447971245857;This is the marketing message
- `dest.csv` is your target file and will contain the date and time from Nexmo's API response, the message sent, the Nexmo messageid and the status of the call.
Example:
timestamp;telephone;message;messageid;status
2016-12-16 12:31:47;447971245857;This is a marketing message;0B000000259D4299;0

# Limitations
- Messages are sent using the type text, whichever the characters used in the message. Characters not within the GSM 7 bits characters map will be replaced by random ones. The single quote is supported, however please make sure to use the correct one `'`
- SMS will be sent at 25 SMS per second (90,000 per hour), depending on your computer's performance and network connection. Do not change the `max_calls` value.

rate_limiter = ratelimiter.RateLimiter( max_calls = 25 ,  period = 1 )  #x call per x seconds - Do not exceed 25 calls per seconds

# Regulations and restrictions 
Check your country specifications in terms of SMS
In France, SFR, Bouygues and Orange will only accept messages for delivery between 8am and 8pm local time Monday to Saturday.
Special characters in sender IDs are not allowed and will either be replaced by character escape or the message will be rejected.

# Data
Messages status will be logged in real time within a text file in http://your_server/batchsms.txt
