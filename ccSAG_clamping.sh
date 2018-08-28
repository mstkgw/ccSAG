#!/bin/sh
#$ -S /bin/sh
#$ -cwd

ccSAGdir=$(dirname $0)
source $ccSAGdir/path.txt
source $1

# make contig clamps

if [ -s $Outdir/raw_SAG_merge_contigs.fasta ]; then
    echo "Skipped raw-merged-contig assembly."
else

echo -n > $Outdir/raw_merge_R1_001.fastq
echo -n > $Outdir/raw_merge_R2_001.fastq
for raw_reads in `ls $Rawreaddir | grep "_R1_001.fastq$" | sed 's/_R1_001.fastq/\t/g'`;
do
cat $Rawreaddir/${raw_reads}_R1_001.fastq >> $Outdir/raw_merge_R1_001.fastq
cat $Rawreaddir/${raw_reads}_R2_001.fastq >> $Outdir/raw_merge_R2_001.fastq
done

$spades_path $spades_option -1 $Outdir/raw_merge_R1_001.fastq -2 $Outdir/raw_merge_R2_001.fastq -o $Outdir/raw_merge_SPAdes
cp $Outdir/raw_merge_SPAdes/contigs.fasta $Outdir/raw_SAG_merge_contigs.fasta
rm $Outdir/raw_merge_SPAdes/ -r
rm $Outdir/raw_merge_R1_001.fastq $Outdir/raw_merge_R2_001.fastq

fi 

python $ccSAGdir/bin/longercontig.py $cleaned_contig $Outdir/cleaned_500.fasta 500
python $ccSAGdir/bin/longercontig.py $Outdir/raw_SAG_merge_contigs.fasta $Outdir/noncleaned_500.fasta 500

# make first_fished_contigs
makeblastdb -in $Outdir/cleaned_500.fasta -dbtype nucl -out $Outdir/fish_index -hash_index
blastn -query $Outdir/noncleaned_500.fasta -out $Outdir/fish_blastresult -db $Outdir/fish_index -perc_identity 99 -outfmt 6 -max_target_seqs 1
python $ccSAGdir/bin/chimera_cross_reference_third_uniq_blastresult.py $Outdir/fish_blastresult $Outdir/fish_uniq_blastresult 250 on
python $ccSAGdir/bin/chimera_cross_reference_third_fishing_from_noncleaned_merge.py $Outdir/fish_uniq_blastresult $Outdir/noncleaned_500.fasta $Outdir/fished_contigs.fasta 250
rm $Outdir/fish_index* $Outdir/fish_blastresult $Outdir/fish_uniq_blastresult 

# remove short contigs from cleaned_merge_contigs
makeblastdb -in $Outdir/fished_contigs.fasta -dbtype nucl -out $Outdir/fished_index -hash_index
blastn -query $Outdir/cleaned_500.fasta -out $Outdir/cleaned_blastresult -db $Outdir/fished_index -perc_identity 99 -outfmt 6 -max_target_seqs 1
python $ccSAGdir/bin/chimera_cross_reference_third_uniq_blastresult.py $Outdir/cleaned_blastresult $Outdir/cleaned_uniq_blastresult 250 off
python $ccSAGdir/bin/chimera_cross_reference_third_remove_short_contig_in_cleaned.py $Outdir/cleaned_uniq_blastresult $Outdir/cleaned_500.fasta $Outdir/cleaned_long.fasta $Outdir/cleaned_keep.fasta 250
rm $Outdir/cleaned_blastresult $Outdir/cleaned_uniq_blastresult 

# connect contigs
makeblastdb -in $Outdir/cleaned_long.fasta -dbtype nucl -out $Outdir/cleaned_long_index -hash_index
blastn -query $Outdir/cleaned_long.fasta -out $Outdir/cleaned_to_fished_blastresult -db $Outdir/fished_index -perc_identity 99 -outfmt 6 -max_target_seqs 2
python $ccSAGdir/bin/chimera_cross_reference_third_connect_contigs.py $Outdir/cleaned_to_fished_blastresult $Outdir/cleaned_long.fasta $Outdir/fished_contigs.fasta $Outdir/connected_contigs.fasta 150
cat $Outdir/cleaned_keep.fasta $Outdir/connected_contigs.fasta > $Outdir/$outcontig
rm $Outdir/*index.* $Outdir/cleaned_to_fished_blastresult $Outdir/cleaned_long.fasta $Outdir/fished_contigs.fasta $Outdir/noncleaned_500.fasta $Outdir/cleaned_500.fasta $Outdir/connected_contigs.fasta $Outdir/cleaned_keep.fasta
