import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_GPIO,GPIO.OUT)

GPIO.output(BUZZER_GPIO, GPIO.LOW)
