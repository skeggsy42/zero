from django.shortcuts import render
from django.http import HttpResponse
from  bme280 import BME280
from enviroplus import gas
from subprocess import PIPE, Popen
import yfinance

# Create your views here.
def get_cpu_temperature():
    	process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    	output, error = process.communicate()
    	return float(output[output.index('=') + 1:output.rindex("'")])

def get_temp():
	factor = 0.8
	cpu_temps = [get_cpu_temperature()] * 5
	bme280 = BME280()
	cpu_temp = get_cpu_temperature()
	cpu_temps = cpu_temps[1:] + [cpu_temp]
	avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
	raw_temp = bme280.get_temperature()
	data = raw_temp - ((avg_cpu_temp - raw_temp) /factor)
	return str(data)

def get_pressure():
	bme280 = BME280()
	data = bme280.get_pressure()
	return str(data)

def get_humidity():
	bme280 = BME280()
	data = bme280.get_humidity()
	return str(data)

def get_reducing():
	bme280 = BME280()
	data = gas.read_all()
	data = data.reducing /1000
	return str(data)

def get_oxidising():
	bme280 = BME280()
	data = gas.read_all()
	data = data.oxidising /1000
	return str(data)

def get_quote(str):
	quote=yfinance.Ticker(str).info["regularMarketPrice"]
	return quote 

def index(request):
	temp = get_temp()
	humidity = get_humidity()
	pressure = get_pressure()
	reducing = get_reducing()
	oxidising = get_oxidising()

	return HttpResponse("<p>Temperature="+temp+" C"+"<BR>"+
			    "Pressure="+pressure+" hPa"+"<BR>"+
			    "Humidity="+humidity+" %"+"<BR>"+
			    "Reducing="+reducing+" kO"+"<BR>"+
			    "Oxidising="+oxidising+" kO"+"<BR>"+
                            "<a href=\"http://192.168.1.39:8080/webapp/quotes/\">Quotes</a><BR></p>")

def quotes(request):
        apple = get_quote("AAPL")
        bats = get_quote("BATS.L")
        brk = get_quote("BRK.L")
        dis = get_quote("DIS")
        ko = get_quote("KO")
        msft = get_quote("MSFT")
        wmt = get_quote("WMT")

        return HttpResponse("<p>Apple="+str(apple)+"<BR>"+
                            "British American Tobacco="+str(bats)+"<BR>"+
                            "Brooks="+str(brk)+"<BR>"+
                            "Disney="+str(dis)+"<BR>"+
                            "Coca Cola="+str(ko)+"<BR>"+
                            "Microsoft="+str(msft)+"<BR>"+
                            "Walmart="+str(wmt)+"<BR>"+
                            "<a href=\"http://192.168.1.39:8080/webapp/\">Readings</a><BR></p>")
