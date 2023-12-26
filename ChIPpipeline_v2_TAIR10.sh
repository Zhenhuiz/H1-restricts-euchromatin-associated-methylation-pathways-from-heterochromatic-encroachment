#!/bin/bash

# ------------------------------------------------------------------------------------
# v1.0 by Jake Harris
# 25th Aug 2020
# ------------------------------------------------------------------------------------

# Usage:

# Description printed when "help" option specified:
read -d '' usage <<"EOF"
v1.0 by Jake Harris
-------------------------------
Example usage:
./ChIPpipeline_v1_TAIR10.sh -a xxx_R1.fastq.gz -b xxx_R2.fastq.gz -c name

Note - requires at least 10G of memory for Java mark duplicates

Required arguments are:
	-a	R1 fastq file
	-b	R2 fastq file
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
infileR2=""
name=""

# ----------------------
while getopts "a:b:c:" opt; do
	case $opt in
		a)	# forward reads
			infileR1="$OPTARG"
			;;
		b)	# reverse reads
			infileR2="$OPTARG"
			;;		
		c)	# name
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

bowtie2 --no-unal --no-mixed --no-discordant --phred33 -I 10 -X 700 -x /u/project/jacobsen/resources/genomes/A_thaliana/bowtie2/TAIR10 -1 ./"${infileR1}" -2 ./"${infileR2}" 2> "${name}"_bowtie_summary.txt 1> "${name}".sam
#only output alignments with reads mapped in proper pair (-f 2), and do not output alignments from reads unmapped (-F 4)
samtools view -f 2 -F 4 -b "${name}".sam | samtools sort -o "${name}".bam -T "${name}".bam
rm "${name}".sam
java -Xmx10g -jar /u/local/apps/picard-tools/current/picard.jar MarkDuplicates I="${name}".bam O="${name}"_nodup.bam REMOVE_DUPLICATES=true M="${name}"_deduplication_metrix.txt
rm "${name}".bam
samtools index "${name}"_nodup.bam
bamCoverage -b "${name}"_nodup.bam --normalizeUsing RPGC --blackListFileName /u/project/jacobsen/cjharris/Reference/blacklist_copyUnderEst.bed --effectiveGenomeSize 119481543 --binSize 1 -o "${name}"_nodup_RPGC_1bp.bw
echo "Done!"
