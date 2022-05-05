#! /usr/bin/env python

# Author: Ramin Dehghanpoor

# import libraries
import argparse
import numpy as np
import glob
import sys
from .utils.io import read_fasta
from .utils import aa_letters
from .utils.data_loaders import to_one_hot
import pandas as pd
from .getDistance import getDistanceFunction
from .family_list import print_families

if sys.version_info < (3, 9):
    # importlib.resources either doesn't exist or lacks the files()
    # function, so use the PyPI version:
    import importlib_resources
else:
    # importlib.resources has files(), so use that:
    import importlib.resources as importlib_resources

class SearchOutput:

    def __init__(self, ls, distance_metric, closest, distance):
        self.ls = ls
        self.distance_metric = distance_metric
        self.closest = closest
        self.distance = distance
    
    def to_stdout(self):
        print('The closest protein family to ' + self.ls + ' is ' + self.closest + ' with ' + self.distance_metric + ' distance: ' + self.distance)
    
    def to_file(self, fname, ftype, mode):
        with open(fname, mode) as outf:
            if ftype == "text":
                outf.write('The closest protein family to ' + self.ls + ' is ' + self.closest + ' with ' + self.distance_metric + ' distance: ' + self.distance + '\n')
            else:
                outf.write(self.ls + ',' + self.distance_metric + ',' + self.closest + ',' + self.distance + '\n')

def run(args):
    # create package data reference object
    pkg = importlib_resources.files("CLI")
    
    # get the arguments
    
    # show names or not
    names_flag = args.show_names_bool
    
    output_filename = args.output_file
    out_format = args.output_format
    out_mode = args.output_mode

    # The p-norm to apply for Minkowski
    p_norm = args.p_norm # default is 2
    
    # new latent space
    nl1 = args.nl1 # default is ""
    
    # set the distance metric
    distance_function = getDistanceFunction(args.distance_metric);  
    
    # when the user asks for the names of the proteins
    if names_flag:
        print_families()
        return
            
    # when the user provides a new latent space and we want to find the closest latent space to that new one
    elif nl1 != "":
        #find closest
        lspath = pkg / 'Latent_spaces'
        latent_space_list = []
        for f in lspath.iterdir():
            latent_space_list.append(f.name)
        a1 = np.loadtxt(nl1)
        min_dist = float("inf")
        for j in range(0, len(latent_space_list)):
            if args.distance_metric == 'minkowski':
                distance_result = distance_function(a1, np.loadtxt(lspath / latent_space_list[j]), p_norm)
            else:
                distance_result = distance_function(a1, np.loadtxt(lspath / latent_space_list[j]))
                
            if distance_result < min_dist:
                min_dist = distance_result
                closest_family = latent_space_list[j]
        
        res = SearchOutput(nl1, str(distance_function).split()[1], closest_family[0:len(closest_family)-4], str(min_dist))
        
        if output_filename != "":
            res.to_file(output_filename, out_format, out_mode)
        
        else:
            res.to_stdout()

        return
    
    # show the usage to the user
    else:
        print(args.help_text)
        return
 
    
def main():

    metrics = ['euclidean', 'minkowski', 'cityblock', 'sqeuclidean', 'cosine', 'correlation', 'hamming', 'jaccard', 'chebyshev', 'canberra', 'braycurtis', 'yule', 'dice', 'kulsinski', 'rogerstanimoto', 'russellrao', 'sokalmichener', 'sokalsneath']
    
    parser=argparse.ArgumentParser(description='''Find the closest protein family to a new latent space or protein sequence. 
    
Available metrics: 
    euclidean, minkowski, cityblock, sqeuclidean, cosine, correlation, hamming, jaccard, chebyshev, canberra, braycurtis, yule, dice, kulsinski, rogerstanimoto, russellrao, sokalmichener, sokalsneath

To see all the available protein families, run command:
    search -names 1
            
Or you can find the closest protein family to first_new_latent_example.txt in cosine distance by running the command:
    search -nl1 first_new_latent_example.txt -m cosine
    
    ''',
                                  formatter_class=argparse.RawTextHelpFormatter)
    #parser.add_argument('--argument', default=None, help=''' ''')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-names",help="Boolean, Show available protein family names" ,dest="show_names_bool", nargs='?', const=1, type=bool, default=0)
    group.add_argument("-nl1",help="The file name of a new latent space. Provide a new protein family latent space. The closest protein family to this new latent space will be shown." ,dest="nl1", type=str, default="")
    group.add_argument("-nl2",help="The file name of a new latent space. Provide a new protein family latent space. The closest protein family to this new latent space will be shown." ,dest="nl1", metavar="NL2", type=str, default="")
    parser.add_argument("-m",help="[optional] Distance metric. Default: euclidean" ,dest="distance_metric", type=str, choices=metrics ,default="euclidean")
    parser.add_argument("-p",help="[optional] Scalar, The p-norm to apply for Minkowski, weighted and unweighted. Default: 2" ,dest="p_norm", type=int, default=2)
    parser.add_argument("-out",help="[optional] Output filename" ,dest="output_file", type=str, default="")
    parser.add_argument("-of",help="[optional] Output format. Default: text" ,dest="output_format", type=str, choices = ["text", "csv"], default="text")
    parser.add_argument("-om",help="[optional] Output mode. Default: a" ,dest="output_mode", type=str, choices = ['a', 'w'], default='a')

    #parser.add_argument("-V",help="ndarray The variance vector for standardized Euclidean. Default: var(vstack([XA, XB]), axis=0, ddof=1)" ,dest="variance_vector", type=np.ndarray, default='None')
    #parser.add_argument("-VI",help="ndarray The inverse of the covariance matrix for Mahalanobis. Default: inv(cov(vstack([XA, XB].T))).T" ,dest="inverse_covariance", type=np.ndarray, default='None')
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.help_text = parser.format_help()
    args.func(args)

if __name__=="__main__":
    main()