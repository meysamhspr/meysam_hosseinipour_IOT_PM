'''
-----------Real Word(task1)------------
'''

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO 

class device:
    def __init__(self,topic,mqtt_broker='localhost',port=1883):
        
        self.topic=topic
        
        self.topic_list=self.topic.split('/')
        
        self.location=self.topic_list[0]
        self.group=self.topic_list[1]
        self.device_type=self.topic_list[2]
        self.name=self.topic_list[3]
        
        self.mqtt_broker=mqtt_broker
        self.port=port
        
        self.connect_mqtt()
        self.setup_gpio()
        
    def connect_mqtt(self):
        self.mqtt_client=mqtt.client()
        
        self.mqtt_client.connect(self.mqtt_broker,self.port)
        
    def setup_gpio(self):
        
        if self.device_type=='lamps':
            GPIO.setup(17,GPIO.OUT)
        
        elif self.device_type=='doors':
            GPIO.setup(27,GPIO.OUT)
            
        elif self.device_type=='fans':
            GPIO.setup(22,GPIO.OUT)
            
        elif self.device_type=='cameras':
            GPIO.setup(100,GPIO.OUT)
            
    def turn_on(self):
        self.mqtt.client.publish(self.topic,'TURN_ON')
        print('turn on successfully')
        
    def turn_off(self):
        self.mqtt.client.publish(self.topic,'TURN_OFF')
        print('turn off successfully')        

'''
-----------final structure(task 2&3)------------
'''
class Device:
    def __init__(self,topic):
        self.topic=topic
        self.topic_list=self.topic.split('/')
        self.location=self.topic_list[0]
        self.group=self.topic_list[1]
        self.device_type=self.topic_list[2]
        self.name=self.topic_list[3]
        
        self.status='off'
        
 
    def turn_on(self):
        self.status='on'
        print('turn on successfully')
        

    def turn_off(self):
        self.status='off'
        print('turn off successfully')


class Sensor:
    def __init__(self,topic,pin=100):
        self.topic=topic
        self.topic_list=self.topic.split('/')
        self.location=self.topic_list[0]
        self.group=self.topic_list[1]
        self.sensor_type=self.topic_list[2]
        self.name=self.topic_list[3]
    def read_sensor(self):
        return 25


class admin_panel:
    def __init__(self):
        self.groups={}
         
    def create_group(self,group_name):
        if group_name not in self.groups:
            self.groups[group_name]=[]
            print(f'group {group_name} is created')
        
        else:
            print('your group name is existed already')
        
        
    def add_device_to_group(self,group_name,new_device):
        if group_name in self.groups:
            self.groups[group_name].append(new_device)
            print(f'{new_device} is added to {group_name}')
        else: 
            print(f'group {group_name} is not exist')


    def create_device(self,group_name,device_type,name):
        if group_name in self.groups:
            topic=f'home/{group_name}/{device_type}/{name}'
            new_device=Device(topic)
            self.add_device_to_group(group_name,new_device)
            print(f'{new_device} is created and added to {group_name}')
            
        else:
            print(f'group {group_name} is not exist')
            

    def create_multiple_devices(self,group_name,device_type,number_of_devices):
        if group_name in self.groups:
            for i in range(1,number_of_devices+1):
                topic=f'home/{group_name}/{device_type}/{device_type}{i}'
                new_device=Device(topic)
                self.add_device_to_group(group_name, new_device)
            print(f'{number_of_devices} devices are created and added to {group_name}')
                
        else:
            print(f'group {group_name} is not exist')
        
        
    def turn_on_devices_in_group(self,group_name):
        if group_name in self.groups:
            things_list=self.groups[group_name]
            for thing in things_list:
                if type(thing)== Device:
                    thing.turn_on()   
            print(f'all devices in {group_name} are turn on successfully')
            
        else:
            print(f'group {group_name} is not exist')
    
    
    def turn_off_devices_in_group(self,group_name):
        if group_name in self.groups:
            things_list=self.groups[group_name]
            for thing in things_list:
                if type(thing)== Device:
                    thing.turn_off()  
            print(f'all devices in {group_name} are turn off successfully')
            
        else:
            print(f'group {group_name} is not exist')
      
        
    def turn_on_all(self):
        for group ,things_list in self.groups.items():
            self.turn_on_devices_in_group(group)
        print(f'all devices in {self.groups} are turn on successfully')
        
        
    def turn_off_all(self):
        for group ,things_list in self.groups.items():
            self.turn_off_devices_in_group(group)
        print(f'all devices in {self.groups} are turn off successfully')
       
    def get_status_in_group(self,group_name):
        if group_name in self.groups:
            things_list=self.groups[group_name]
            for thing in things_list:
                if type(thing)== Device:
                    print(f'in {group_name} device{thing} is {thing.status}')

        else:
            print(f'group {group_name} is not exist')
       
    
    def get_status_in_device_type(self,device_type):
        for things_list in self.groups.values():
            for thing in things_list:
                if type(thing)== Device and thing.device_type==device_type:
                    print (f'in {thing.group} device {thing} is {thing.status}')
    
    def create_sensor(self,group_name,sensor_type,name):
        if group_name in self.groups:
            topic=f'home/{group_name}/{sensor_type}/{name}'
            new_sensor=Sensor(topic)
            self.groups[group_name].append(new_sensor)
            print(f'{new_sensor} is created and added to {group_name}')

        else:
            print(f'group {group_name} is not exist')  
    
    def get_status_sensor_in_group(self,group_name):
        if group_name in self.groups:
            things_list=self.groups[group_name]
            for thing in things_list:
                if type(thing)== Sensor:
                    print(f'in {group_name} sensor{thing} is {thing.read_sensor()}')
        else:
            print(f'group {group_name} is not exist')
        
        