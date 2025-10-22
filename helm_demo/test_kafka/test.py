"""
This is my python test file executed in a k8s pod.
It simply prints "hello world" every second for 10,000 times.

How to make the hello world log exported using kubectl logs

Provide to be step by step instructions
"""
import time
for i in range(10000):
    print('hello world')
    time.sleep(1)