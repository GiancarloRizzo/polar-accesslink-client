# Polar Open AccessLink example application

This is a python client for polar-accesslink-api based on the official example application from [polar](https://github.com/polarofficial/accesslink-example-python).
Unfortunally polar doesn't seem to review any merge-requests, even if they fix known bugs like authorisation etc. So I did this client based on the already given examples and added my data-queries based on this [documentation](https://www.polar.com/accesslink-api/#polar-accesslink-api)

## Prerequisites

* [Polar Flow](https://flow.polar.com) account
* Python 2 and pip related to Python 2

## Getting Started

#### 1. Register API client 
 
Navigate to https://admin.polaraccesslink.com. Log in with your Polar Flow account and create a new client.

Use `http://localhost:5000/oauth2_callback` as the authorization callback domain for this example.
  
#### 2. Configure client credentials

Fill in your client id and secret in credentials.yml:

```
client_id: 
client_secret: 
```
  
#### 3. Install python dependencies

```
pip install -r requirements.txt
```

#### 4. Link user 

User account needs to be linked to client application before client can get any user data. User is asked for authorization 
in Polar Flow, and user is redirected back to application callback url with authorization code once user has accepted the request.
 
To start example oauth.service:

```
python oauth.py
```

#### 5. Run 
    
```
python main.py
```
