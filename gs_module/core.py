#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from gs_interfaces.srv import Led,Live
from rospy import ServiceProxy
from std_msgs.msg import Bool,ColorRGBA
import RPi.GPIO as GPIO
import json, socket

class BoardLedController():
    def __init__(self):
        self.__leds = []
        for _ in range(0,4):
            self.__leds.append(ColorRGBA())
        rospy.wait_for_service("geoscan/alive")
        rospy.wait_for_service("geoscan/led/board/set")
        self.__alive = ServiceProxy("geoscan/alive",Live)
        self.__led_service = ServiceProxy("geoscan/led/board/set",Led)

    def changeColor(self,i,r,g,b):
        if self.__alive().status:
            try:
                if ( ( (r >= 0.0) and (r <= 255.0) ) and ( (g >= 0.0) and (g <= 255.0) ) and ( (b >= 0.0) and (b <= 255.0) ) ):
                    color = ColorRGBA()
                    color.r = r
                    color.g = g
                    color.b = b
                    self.__leds[i] = color
                    return self.__led_service(self.__leds).status
                else:
                    rospy.logerr("Color value must be between 0.0 and 255.0 inclusive")
            except:
                rospy.logerr("Index led: {} is not correct".format(i))
        else:
            rospy.logwarn("Wait, connecting to flight controller")
    
    def changeAllColor(self,r,g,b):
        if self.__alive().status:
            if ( ( (r >= 0.0) and (r <= 255.0) ) and ( (g >= 0.0) and (g <= 255.0) ) and ( (b >= 0.0) and (b <= 255.0) ) ):
                for i in range(0,len(self.__leds)):
                    color = ColorRGBA()
                    color.r = r
                    color.g = g
                    color.b = b
                    self.__leds[i] = color
                return self.__led_service(self.__leds).status
            else:
                rospy.logerr("Color value must be between 0.0 and 255.0 inclusive")
        else:
            rospy.logwarn("Wait, connecting to flight controller")

class ModuleLedController():
    def __init__(self):
        self.__leds = []
        for _ in range(0,25):
            self.__leds.append(ColorRGBA())
        rospy.wait_for_service("geoscan/alive")
        rospy.wait_for_service("geoscan/led/module/set")
        self.__alive = ServiceProxy("geoscan/alive",Live)
        self.__led_service = ServiceProxy("geoscan/led/module/set",Led)

    def changeColor(self,i,r,g,b):
        if self.__alive().status:
            try:
                if ( ( (r >= 0.0) and (r <= 255.0) ) and ( (g >= 0.0) and (g <= 255.0) ) and ( (b >= 0.0) and (b <= 255.0) ) ):
                    color = ColorRGBA()
                    color.r = r
                    color.g = g
                    color.b = b
                    self.__leds[i] = color
                    return self.__led_service(self.__leds).status
                else:
                    rospy.logerr("Color value must be between 0.0 and 255.0 inclusive")
            except:
                rospy.logerr("Index led: {} is not correct".format(i))
        else:
            rospy.logwarn("Wait, connecting to flight controller")
    
    def changeAllColor(self,r,g,b):
        if self.__alive().status:
            if ( ( (r >= 0.0) and (r <= 255.0) ) and ( (g >= 0.0) and (g <= 255.0) ) and ( (b >= 0.0) and (b <= 255.0) ) ):
                for i in range(0,len(self.__leds)):
                    color = ColorRGBA()
                    color.r = r
                    color.g = g
                    color.b = b
                    self.__leds[i] = color
                return self.__led_service(self.__leds).status
            else:
                rospy.logerr("Color value must be between 0.0 and 255.0 inclusive")
        else:
            rospy.logwarn("Wait, connecting to flight controller")

class CargoController():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.__gpio_number = 17
        GPIO.setup(self.__gpio_number, GPIO.OUT)

    def on(self):
        GPIO.output(self.__gpio_number, True)

    def off(self):
        GPIO.output(self.__gpio_number, False)

    def changeColor(self, r=0, g=0, b=0, n=0):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(('localhost', 9090))
        clientsocket.send(bytes(json.dumps({'r':r, 'g':g, 'b':b, 'n':n}), encoding='utf-8'))

    def changeAllColor(self, r=0, g=0, b=0):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(('localhost', 9090))
        clientsocket.send(bytes(json.dumps({'r':r, 'g':g, 'b':b, 'n':255}), encoding='utf-8'))