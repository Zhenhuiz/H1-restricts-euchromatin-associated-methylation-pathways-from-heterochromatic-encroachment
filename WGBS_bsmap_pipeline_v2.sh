#!/bin/bash

# ------------------------------------------------------------------------------------
# v1.0 by Jake Harris
# 6th Jan 2021
# ------------------------------------------------------------------------------------

# Usage:

# Description printed when "help" option specified:
read -d '' usage <<"EOF"
v1.0 by Jake Harris
-------------------------------
Example usage:
./WGBS_bsmap_pipeline_v1.sh -a xxx_R1.fastq.gz -b name

Required arguments are:
	-a	R1 fastq file
	-b	name
		
------------------------------------------------------------------------------------
EOF

[[ $# -eq 0 ]] && { printf "%s\n" "$usage"; exit 0; } 		# if no user-supplied arguments, print usage and exit

# ----------------------
# Get user-specified arguments
# ----------------------


# Required arguments:
# ----------------------

infileR1=""
name=""

# ----------------------
while getopts "a:b:" opt; do
	case $opt in
		a)	# reads
			infileR1="$OPTARG"
			;;
		b)	# name
			name="$OPTARG"
			;;
		\?)
			echo "Invalid option: -$OPTARG" >&2
			exit 1
			;;
		:)
			echo "Option -$OPTARG requires an argument." >&2
			exit 1
			;;
	esac
done


# ----------------------
# Main code
# ----------------------

############
/u/home/c/cjharris/bsmap-2.89/bsmap -p 4 -w 1 -n 0 -v 0.04 -r 0 -a "${infileR1}" -d /u/project/jacobsen/resources/genomes/A_thaliana/fasta_and_bismark/TAIR10.fa -o "${name}".bam 2> "${name}"_bsmapsummary.txt 
python ~/project-jacobsen/Programmes/methratio_alt.py -u -z -r -S -o "${name}".txt -d /u/project/jacobsen/resources/genomes/A_thaliana/fasta_and_bismark/TAIR10.fa "${name}".bam
perl ~/project-jacobsen/Programmes/bsmap2wiggle_play.pl "${name}".txt
~/project-jacobsen/Programmes/wigToBigWig "${name}".txt.CG.wig /u/project/jacobsen/resources/genomes/A_thaliana/annotations/TAIR10/tair10.chrom.sizes "${name}".CG.bw
~/project-jacobsen/Programmes/wigToBigWig "${name}".txt.CHG.wig /u/project/jacobsen/resources/genomes/A_thaliana/annotations/TAIR10/tair10.chrom.sizes "${name}".CHG.bw
~/project-jacobsen/Programmes/wigToBigWig "${name}".txt.CHH.wig /u/project/jacobsen/resources/genomes/A_thaliana/annotations/TAIR10/tair10.chrom.sizes "${name}".CHH.bw
~/project-jacobsen/Programmes/wigToBigWig "${name}".txt.C_coverage.wig /u/project/jacobsen/resources/genomes/A_thaliana/annotations/TAIR10/tair10.chrom.sizes "${name}".C_coverage.bw
echo "Done!"

