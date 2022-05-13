import sys
from .output_results import output_result


def seq_search(args):
    if sys.version_info[:3] == (3, 7, 6):
        # don't import function and dependencies if you don't need to
        from .SearchSQ import SearchSQ
        for ns in args.sequence:
            try:
                res = SearchSQ(ns).result
                output_result(res, args.output_file, args.output_format, args.output_mode)
            except Exception as err:
                print("Error")
                exit(err)

    else:
        print('sequence searches only available with python 3.7.6')
