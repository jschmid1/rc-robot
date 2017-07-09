import RPi.GPIO as gpio
import time
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

class Robo(object):

    def __init__(self):
      gpio.setmode(gpio.BCM)
      self.IN_1 = 17
      self.IN_2 = 27
      self.IN_3  = 23
      self.IN_4 = 24
      self.PWM = 18
      gpio.setup(self.IN_3, gpio.OUT)
      gpio.setup(self.IN_4, gpio.OUT)
      gpio.setup(self.IN_1, gpio.OUT)
      gpio.setup(self.IN_2, gpio.OUT)
      gpio.setup(self.PWM, gpio.OUT)
      self.pwm1 = gpio.PWM(self.PWM, 1000)
      """
      1 HIGH
      2 LOW
      -> rear back

      2 HIGH
      1 LOW
      -> rear front
      """
     
    def forward(self, tf):
      print "forward"
      #self.pwm1.ChangeFrequency(1.0)
      self.pwm1.start(90)
      gpio.output(self.IN_2, True)
      gpio.output(self.IN_1, False)
      #self.pwm1.ChangeDutyCycle(40)
      time.sleep(tf)
      self.pwm1.stop()
      gpio.output(self.IN_2, False)
      gpio.output(self.IN_1, False)

    def backward(self, tf):
      print "backward"
      #self.pwm1.ChangeFrequency(1.0)
      self.pwm1.start(90)
      gpio.output(self.IN_1, True)
      gpio.output(self.IN_2, False)
      #self.pwm1.ChangeDutyCycle(40)
      time.sleep(tf)
      self.pwm1.stop()
      gpio.output(self.IN_2, False)
      gpio.output(self.IN_1, False)

    def left(self, tf):
      print 'left'
      gpio.output(self.IN_3, True)
      gpio.output(self.IN_4, False)
      time.sleep(tf)
      gpio.output(self.IN_3, False)
      gpio.output(self.IN_4, False)

    def right(self, tf):
      print 'right'
      gpio.output(self.IN_3, False)
      gpio.output(self.IN_4, True)
      time.sleep(tf)
      gpio.output(self.IN_3, False)
      gpio.output(self.IN_4, False)
     
@app.route('/left')
def left():
        rob = Robo()
        rob.left(1)
        return jsonify(result='left')

@app.route('/right')
def right():
        rob = Robo()
        rob.right(1)
        return jsonify(result='right')

@app.route('/backward')
def backward():
        rob = Robo()
        rob.backward(1)
        return jsonify(result='back')

@app.route('/forward')
def forward():
        rob = Robo()
        rob.forward(1)
        return jsonify(result='front')

@app.route('/')
def index():
    return render_template('index.html')

gpio.cleanup()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
