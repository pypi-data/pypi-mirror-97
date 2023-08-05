# metricserverremote Package

This package provide a python API to user the Opale Systems Metric Server product remotely.

Here is a simple example of usage :
from metricserverremote import server

def main():
    # Set name of Shark object
    ms = server.MetricServer()
    print(ms.logon("127.0.0.1", "admin", "admin"))
    processresult = ms.processfilepair('C:/temp/reference.wav', 'C:/temp/degraded.wav', 'Narrowband', 'Output 1')
    isint = isinstance(processresult, int)
    if isint:
        results = ms.results('Output 1', processresult)

    else:
        print(processresult)
        sys.exit(2)

    print("results:", results)

    if isinstance(results, (list,)):
        polqanb = results[13]
        polqanb = str(polqanb[2])
        print("Polqa NB:", polqanb)

    print(ms.saverst('Output 1', processresult, 'C:/Qualit/tmp'))


if __name__ == "__main__":
    main()
