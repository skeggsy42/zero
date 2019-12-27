from django.shortcuts import render
from django.http import HttpResponse
from  bme280 import BME280
from enviroplus import gas
from subprocess import PIPE, Popen
import yfinance
try:
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

# Create your views here.
def get_light():
        data = ltr559.get_lux()
        return str(data)

def get_cpu_temperature():
    	process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    	output, error = process.communicate()
    	return float(output[output.index('=') + 1:output.rindex("'")])

def get_temp():
	factor = 1.54
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

def get_quote_bid(str):
        quote=yfinance.Ticker(str).info["bid"]
        return quote

def index(request):
	temp = get_temp()
	humidity = get_humidity()
	light = get_light()
	pressure = get_pressure()
	reducing = get_reducing()
	oxidising = get_oxidising()

	return HttpResponse("<p>Temperature="+temp+" C"+"<BR>"+
			    "Pressure="+pressure+" hPa"+"<BR>"+
			    "Humidity="+humidity+" %"+"<BR>"+
			    "Reducing="+reducing+" kO"+"<BR>"+
			    "Oxidising="+oxidising+" kO"+"<BR>"+
                            "Light="+light+" Lux"+"<BR>"+
			    "<a href=\"http://192.168.1.39:8080/webapp/quotes/\">Quotes</a><BR></p>")

def quotes(request):
        amzn = get_quote("AMZN")
        apple = get_quote("AAPL")
        aviva  = get_quote("AV.L")
        bats = get_quote("BATS.L")
        brk = get_quote("BRK.L")
        brkbid = get_quote_bid("BRK.L")
        brk_b = get_quote("BRK-B")
        bt = get_quote("BT-A.L")
        dis = get_quote("DIS")
        ko = get_quote("KO")
        isrg = get_quote("ISRG")
        msft = get_quote("MSFT")
        wmt = get_quote("WMT")
        jch = get_quote("JCH.L")
        ibm = get_quote("IBM")
        jnj = get_quote("JNJ")
        tem = get_quote("TEM.L")
        tsco = get_quote("TSCO.L")
        googl = get_quote("GOOGL")
        goog = get_quote("GOOG")
        sse = get_quote("SSE.L")
        gsk = get_quote("GSK.L")
        hsba = get_quote("HSBA.L")
        rbs = get_quote("RBS.L")
        tmpl = get_quote("TMPL.L")
        pg = get_quote("PG")

        return HttpResponse("<p><b>Apple="+str(apple)+"</b><BR>"+
                                "Amazon="+str(amzn)+"<BR>"+
                                "Aviva="+str(aviva)+"<BR>"+
                          	"British American Tobacco="+str(bats)+"<BR>"+
                            	"Brooks="+str(brk)+"<BR>"+
                            	"<b>Brooks Bid="+str(brkbid)+"</b><BR>"+
                                "<b>Berkshire B="+str(brk_b)+"</b><BR>"+
                                "BT="+str(bt)+"<BR>"+
                                "Disney="+str(dis)+"<BR>"+
                                "ISRG="+str(isrg)+"<BR>"+
                                "JCH="+str(jch)+"<BR>"+
				"Coca Cola="+str(ko)+"<BR>"+
				"Goog="+str(goog)+"<BR>"+
                                "Googl="+str(googl)+"<BR>"+
                                "GSK="+str(gsk)+"<BR>"+
                                "HSBC="+str(hsba)+"<BR>"+
                                "JNJ="+str(jnj)+"<BR>"+
                                "<b>Microsoft="+str(msft)+"</b><BR>"+
                                "PG="+str(pg)+"<BR>"+
                                "RBS="+str(rbs)+"<BR>"+
                                "SSE="+str(sse)+"<BR>"+
                                "TEM="+str(tem)+"<BR>"+
                                "Tesco="+str(tsco)+"<BR>"+
                                "Walmart="+str(wmt)+"<BR>"+
                                "<a href=\"http://192.168.1.39:8080/webapp/\">Readings</a><BR></p>")
