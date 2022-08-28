import time

from postprocess import Postprocessor
from search_report import ReportSearcher
from tracer import BitcoinTracer


def run_programme(addr, trace_depth, min_amount):
    """ ------------------ Trace ------------------------"""
    tic = time.perf_counter()  # start timer
    tracer = BitcoinTracer(addr, trace_depth, min_amount=min_amount)  # initialise tracer
    [source_addr, amount] = tracer.trace()  # construct network and get the source addresses
    for i in range(len(source_addr)):
        print(source_addr[i], amount[i])
    print("total number of source:", len(source_addr))
    toc = time.perf_counter()  # stop timer
    print(f"Time spent {toc - tic:0.4f} seconds")

    """ ------------------ Classify ------------------------"""
    tracer.classify_all_result_addr()
    tac = time.perf_counter()  # stop timer
    print(f"Time spent {tac - toc:0.4f} seconds")
    tracer.save_results()

    """ ------------------ Process ------------------------"""
    pp = Postprocessor(addr, trace_depth,min_amount)
    # pp.print_data()
    pp.print_data_info()
    pp.plot(save=True)

    report_searcher = ReportSearcher()
    report_searcher.check_bitcoin_abuse(source_addr)


if __name__ == "__main__":
    # bc1qmxjefnuy06v345v6vhwpwt05dztztmx4g3y7wp another very rich address with 8 unspent
    # "1ArJTD4iR3SCwjuyiP3H6pbwvPBHduX6WB" # bitpay.com

    address = "1ArJTD4iR3SCwjuyiP3H6pbwvPBHduX6WB"
    min_BTC = 0.001  # 0.00000001 -- 1 statoshi
    depth_begin = 5
    depth_end = 10
    depth_list = range(depth_begin, depth_end+1)  # include end
    # run programme with all the tracing depth values
    for i in depth_list:
        run_programme(address, i, min_BTC)
