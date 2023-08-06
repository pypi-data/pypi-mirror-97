isONcorrect
===========

isONcorrect is a tool for error-correcting  Oxford Nanopore cDNA reads. It is designed to handle highly variable coverage and exon variation within reads and achieves about a 0.5-1% median error rate after correction. It leverages regions shared between reads from different isoforms achieve low error rates even for low abundant transcripts. See [preprint](https://www.nature.com/articles/s41467-020-20340-8) for details. 

**Update:** isONcorrect now uses different default parameters compared to what was used in paper. The new parameters make isONcorrect 2-3 times faster and use 3-8 times less memory with only a small cost of increased median post-correction error rate. With the new parameter setting the correction accuracy is 98.5-99.3% instead of 98.9–99.6% on the data used in the paper. Current default uses `--k 9 --w 20 --max_seqs 2000`. To invoke settings used in paper, set parameters `--k 9 --w 10 --max_seqs 1000`.

Processing and error correction of full-length ONT cDNA reads is achieved by the pipeline of running [pychopper](https://github.com/nanoporetech/pychopper) --> [isONclust](https://github.com/ksahlin/isONclust) --> [isONcorrect](https://github.com/ksahlin/isONcorrect) 


isONcorrect is distributed as a python package supported on Linux / OSX with python v>=3.4. [![Build Status](https://travis-ci.org/ksahlin/isONcorrect.svg?branch=master)](https://travis-ci.org/ksahlin/isONcorrect).

Table of Contents
=================

  * [INSTALLATION](#INSTALLATION)
    * [Using conda](#Using-conda)
    * [Using pip](#Using-pip)
    * [Downloading source from GitHub](#Downloading-source-from-github)
    * [Dependencies](#Dependencies)
    * [Testing installation](#testing-installation)
  * [USAGE](#USAGE)
    * [Running](#Running)
    * [Output](#Output)
    * [Parallelization across nodes](#Parallelization-across-nodes)
  * [CREDITS](#CREDITS)
  * [LICENCE](#LICENCE)



INSTALLATION
----------------

Typical install time on a desktop computer is about 10 minutes with conda for this software.

### Using conda
Conda is the preferred way to install isONcorrect.

1. Create and activate a new environment called isoncorrect

```
conda create -n isoncorrect python=3 pip 
conda activate isoncorrect
```

2. Install isONcorrect and its dependency `spoa`.

```
pip install isONcorrect
conda install -c bioconda spoa
```
3. You should now have 'isONcorrect' installed; try it:
```
isONcorrect --help
```

Upon start/login to your server/computer you need to activate the conda environment "isonclust" to run isONcorrect as:
```
conda activate isoncorrect
```

### Using pip 

`pip` is pythons official package installer and is included in most python versions. If you do not have `pip`, it can be easily installed [from here](https://pip.pypa.io/en/stable/installing/) and upgraded with `pip install --upgrade pip`. 

To install isONcorrect, run:
```
pip install isONcorrect
```
Then install [spoa](https://github.com/rvaser/spoa) and include it in your path.


### Downloading source from GitHub

#### Dependencies

Make sure the below listed dependencies are installed (installation links below). Versions in parenthesis are suggested as isONcorrect has not been tested with earlier versions of these libraries. However, isONcorrect may also work with earliear versions of these libaries.
* [spoa](https://github.com/rvaser/spoa) (1.1.5)
* [edlib](https://github.com/Martinsos/edlib/tree/master/bindings/python) (1.1.2)
* [NumPy](https://numpy.org/) (1.16.2)

In addition, please make sure you use python version >=3.

With these dependencies installed. Run

```sh
git clone https://github.com/ksahlin/isONcorrect.git
cd isONcorrect
./isONcorrect
```

### Testing installation

You can verify successul installation by running isONcorrect on this [small dataset of 100 reads](https://github.com/ksahlin/isONcorrect/tree/master/test_data/isoncorrect/0.fastq). Assuming you have cloned this repository and the repository is found in /my/path/isONcorrect, simply run:

```
isONcorrect --fastq /my/path/isONcorrect/test_data/isoncorrect/0.fastq \
            --outfolder [output path]
```
Expected runtime for this test data is about 15 seconds. The output will be found in `[output path]/corrected_reads.fastq` where the 100 reads have the same headers as in the original file, but with corrected sequence. Testing the paralleized version (by separate clusters) of isONcorrect can be done by running

```
./run_isoncorrect --t 3 --fastq_folder /my/path/isONcorrect/test_data/isoncorrect/ \
                  --outfolder [output path]
```
This will perform correction on `0.fastq` and `1.fastq` in parallel. Expected runtime for this test data is about 15 seconds. The output will be found in `[output path]/0/corrected_reads.fastq` and `[output path]/1/corrected_reads.fastq` where the 100 reads in each separate cluster have the same headers as in the respective original files, but with corrected sequence. 


USAGE
-------
 
### Running

For a fastq file with raw ONT cDNA reads, the following pipeline is recommended. A bash script to run this pipeline is provided below.
1.  Produce full-length reads (with [pychopper](https://github.com/nanoporetech/pychopper) (a.k.a. `cdna_classifier`))
2.  Cluster the full length reads into genes/gene-families ([isONclust](https://github.com/ksahlin/isONclust))
3.  Make fastq files of each cluster (`isONclust write_fastq` command)
4.  Correct individual clusters ([isONcorrect](https://github.com/ksahlin/isONcorrect))
5.  Join reads back to a single fastq file (This is of course optional)

Below shows specific pipeline script to go from raw reads `raw_reads.fq` to corrected full-length reads `all_corrected_reads.fq` (please modify/remove arguments as needed). 

```
#!/bin/bash

# Pipeline to get high-quality full-length reads from ONT cDNA sequencing

# Set path to output and number of cores
root_out="outfolder"
cores=20

mkdir -p $root_out

cdna_classifier.py  raw_reads.fq $root_out/full_length.fq -t $cores 

isONclust  --t $cores  --ont --fastq $root_out/full_length.fq \
             --outfolder $root_out/clustering

isONclust write_fastq --N 1 --clusters $root_out/clustering/final_clusters.csv \
                      --fastq $root_out/full_length.fq --outfolder  $root_out/clustering/fastq_files 

run_isoncorrect --t $cores  --fastq_folder $root_out/clustering/fastq_files  --outfolder $root_out/correction/ 

# OPTIONAL BELOW TO MERGE ALL CORRECTED READS INTO ONE FILE
touch $root_out/all_corrected_reads.fq
for f in in $root_out/correction/*/corrected_reads.fastq; 
do 
  cat {f} >> $root_out/all_corrected_reads.fq
done
```

isONcorrect does not need ONT reads to be full-length (i.e., produced by `pychopper`), but unless you have specific other goals, it is advised to run pychopper for any kind of downstream analysis to guarantee full-length reads. 

### Output

The output of `run_isoncorrect` is one file per cluster with identical headers to the original reads.

### Parallelization across nodes

isONcorrect currently supports parallelization across cores on a node (parameter `--t`), but not across several nodes. There is a way to overcome this limitation if you have access to multiple nodes as follows. The `run_isoncorrect` step can be parallilized across n nodes by (in bash or other environment, e.g., snakemake) parallelizing the following commands

```
run_isoncorrect --fastq_folder outfolder/clustering/fastq_files  --outfolder /outfolder/correction/ --split_mod n --residual 0
run_isoncorrect --fastq_folder outfolder/clustering/fastq_files  --outfolder /outfolder/correction/ --split_mod n --residual 1
run_isoncorrect --fastq_folder outfolder/clustering/fastq_files  --outfolder /outfolder/correction/ --split_mod n --residual 2
...
run_isoncorrect --fastq_folder outfolder/clustering/fastq_files  --outfolder /outfolder/correction/ --split_mod n --residual n-1
```
Which tells isONcorrect to only work with distinct cluster IDs.

CREDITS
----------------

Please cite [1] when using isONcorrect.

1. Sahlin, K., Medvedev, P. Error correction enables use of Oxford Nanopore technology for reference-free transcriptome analysis. Nat Commun 12, 2 (2021). https://doi.org/10.1038/s41467-020-20340-8  [Link](https://www.nature.com/articles/s41467-020-20340-8).

LICENCE
----------------

GPL v3.0, see [LICENSE.txt](https://github.com/ksahlin/isONcorect/blob/master/LICENCE.txt).

