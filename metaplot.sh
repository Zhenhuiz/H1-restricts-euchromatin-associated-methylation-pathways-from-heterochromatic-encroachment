# 1. normalization
bamCoverage --bam sample_merge.bam -o sample_merge.bw --normalizeUsing RPKM --binSize 1 -p 6
bigwigCompare -b1 sample_merge.bw -b2 input.bw --operation subtract -o sample_minus_input.bw --binSize 1 -p 6
# 2. metaplot
computeMatrix scale-regions -S sample1_minus_input.bw sample2_minus_input.bw -R ClassA_TEs.bed --beforeRegionStartLength 2000 --regionBodyLength 4000 --afterRegionStartLength 2000 --skipZeros  --missingDataAsZero -o over_classA_TE.matrix.mat.gz -bs 40 -p 6
plotHeatmap -m over_classA_TE.matrix.mat.gz -out over_classA_TE.pdf --zMin -400 --zMax 400 --colorMap RdYlBu_r
