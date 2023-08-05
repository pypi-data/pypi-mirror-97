#Python SDK for Aliyun IoT device

This is a python sdk for Aliyun IoT device. 
* MQTT connection:MQTTV31,MQTTV311
* Aliyun IoT Thing Model


## Release Notes
### 1.2.1
* [ADD] support to configure the custom endpoint for MQTT config_mqtt 
* [ADD] support to configure the custom endpoint for HTTP2 config_http2
* [UPDATE] support to receive any unsubscribed message by on_topic_message


### 1.2.2
* [UPDATE] fix the onConnect callback invoked at wrong time issue

### 1.2.3
* [UPDATE] fix tsl parsing error for simplified tsl products
