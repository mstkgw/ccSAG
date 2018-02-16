# 1. Preparation
## 1-1 Confirmation of required tools
#### requirements:

	perl
	python
	java
	fastqc
	fastx_toolkit
	prinseq
	spades
	bwa
	blastn

## 1-2 Making a path

#### Rewrite 'XXXX' of path.txt


# 2. Usage

## 2-1 ccSAG_cross_reference_cleaning.sh  

#### In this script, following steps are conducted.  
* Quality control of paired-end reads by fastqc, fastx_toolkit and prinseq  
* Assembling using each paired-end read file by SPAdes  
* Cross-reference read cleaning using bwa  
* Assembling using all cleaned reads by SPAdes  
  

#### At first, make a config of ccSAG_cross_reference_cleaning.sh including  
* Output directory of cleaned contigs and reads or intermediate files  
* Directory containing input pairend read files  
* Output cleaned contigs  
* Assemble condition without input fastq  
#### (example is ccSAG_cross_reference_cleaning.config)  
  

#### Then, execute ccSAG_cross_reference_cleaning.sh  
#### command is here:

	bash ccSAG_cross_reference_cleaning.sh config  


#### As the output files,  
* Cleaned contig file from all cleaned reads is in the desinated output directory.  
* Cleaned read file of each SAG is in the "output directory/QC" named "*_cleaned.fastq".  
  

#### example SAG data is contained in "example" directory.  
#### try

	bash ccSAG_cross_reference_cleaning.sh example/example_ccSAG_cross_reference_cleaning.config  


## 2-2 ccSGA_clamping.sh  
#### In this script, following steps are conducted.  
* Assembling contig clamps using non-cleaned reads by SPAdes  
* connecting cleaned contigs by contig clamps using blastn  
  

#### At first, make a config of ccSAG_clamping.sh including  
* Output directory of clamped contigs and intermediate files  
* Directory containing input pairend read files for assembling contig clamps  
* Output cleaned contigs of ccSAG_cross_reference_cleaning.sh  
* Output clamped contigs  
* Assemble condition without input fastq  
#### (example is ccSAG_clamping.config)  
  

#### Then, execute ccSAG_clamping.sh  
#### command is here:  

	bash ccSAG_clamping.sh config  
  

#### As the output files,  
* Clamped contig file is in the desinated output directory  
  

#### example config is prepared in "example" directory as 2-1.  
#### try after executing 2-1(ccSAG_cross_reference_cleaning.sh)

	bash ccSAG_clamping.sh example/example_ccSAG_clamping.config  
