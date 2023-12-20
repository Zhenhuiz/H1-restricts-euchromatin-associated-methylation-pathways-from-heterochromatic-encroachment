This folder contains all related files for paper "H1 restricts euchromatin-associated methylation pathways from heterochromatic encroachment".

The paper is available at https://www.biorxiv.org/content/10.1101/2023.05.10.539968v1 and https://elifesciences.org/reviewed-preprints/89353

ChIP-seq data analysis
ChIP-seq data were aligned to the TAIR10 reference genome with Bowtie2 (v2.1.0) (Langmead and Salzberg, 2012) allowing only uniquely mapping reads with zero mismatch. Duplicated reads were removed by Samtools. ChIP-seq peaks were called by MACS2 (v2.1.1) and annotated with ChIPseeker (Yu et al., 2015). Differential peaks were called by bdgdiff function in MACS2 (Zhang et al., 2008). ChIP-seq data metaplots were plotted by deeptools (v2.5.1) (Ramírez et al., 2016).

Whole-genome bisulfite sequencing (BS-seq) data analysis
Previously published whole-genome bisulfite sequencing data for mutants and wild type were reanalyzed from previous paper (Stroud et al., 2013). Briefly, Trim_galore (http://www.bioinformatics.babraham.ac.uk/projects/trim_galore/) was used to trim adapters. BS-seq reads were aligned to TAIR10 reference genome by BSMAP (v2.90) and allowed 2 mismatches and 1 best hit (-v 2 -w 1) (Xi and Li, 2009). Reads with three or more consecutive CHH sites were considered as unconverted reads and filtered. DNA methylation levels were defined as #C/ (#C + #T). DMR overlapping analysis were conducted by mergePeaks (-d 100) of Homer (Heinz et al., 2010) with WGBS data published previously (Stroud et al., 2013). The estimated conversion rates for all WGBS libraries are provided in Supplementary Table 1.
