#!/usr/bin/env python

"""
Log2Table: Creates a table from PlotAggregate logfiles

@author: Mette Bentsen
@contact: mette.bentsen (at) mpi-bn.mpg.de
@license: MIT

"""

import os
import sys
import argparse
import re
import pandas as pd

#Utils from TOBIAS
from tobias.utils.utilities import * 
from tobias.utils.logger import *

#------------------------------------------------------------------------------------------------------#
def run_log2table(args):
	logger = TobiasLogger("Log2Table")
	logger.begin()

	#Test input / output
	check_required(args, ["logfiles"])
	
	make_directory(args.outdir)
	output_fpd = os.path.join(args.outdir, args.prefix + "_FPD.txt")
	output_corr = os.path.join(args.outdir, args.prefix + "_CORRELATION.txt")
	
	FPD_data = []
	CORR_data = []

	#Read all logfiles
	for log_f in args.logfiles:
		logger.info("Reading: {0}".format(log_f))
		with open(log_f) as f:
			for line in f:

				#Match FPD lines
				#...... FPD (PWM_uncorrected,MA0073.1_all): 20 0.620 0.602 -0.018
				m = re.match(".*FPD\s\((.+),(.+)\): (.+) (.+) (.+) (.+)", line.rstrip())
				if m:

					elements = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6)
					signal, sites, width, baseline, fp, fpd = elements
					
					columns = [signal, sites, width, baseline, fp, fpd]
					FPD_data.append(columns)
				
				#Match correlation lines
				#..... CORRELATION (PWM_uncorrected,MA0002.2_all) VS (PWM_corrected,MA0002.2_all): -0.17252
				m = re.match(".*CORRELATION \((.+),(.+)\) VS \((.+),(.+)\): (.+)", line.rstrip())
				if m:
					elements = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
					signal1, sites1, signal2, sites2, values_str = elements

					#split values (can be more than one depending on tobias version)
					values = values_str.split()
					columns = [signal1, sites1, signal2, sites2] + values
					CORR_data.append(columns)

					#Add reverse comparison as well
					if "PEARSONR" not in values:	#header should not be reversed
						columns = [signal2, sites2, signal1, sites1] + values
						CORR_data.append(columns)

	logger.info("Writing tables")
	
	#All lines from all files read, write out tables
	df_fpd = pd.DataFrame(FPD_data)
	df_fpd.drop_duplicates(keep="first", inplace=True)
	df_fpd.to_csv(output_fpd, sep="\t", index=False, header=False)

	df_corr = pd.DataFrame(CORR_data)
	df_corr.drop_duplicates(keep="first", inplace=True)
	df_corr.to_csv(output_corr, sep="\t", index=False, header=False)

	logger.end()
