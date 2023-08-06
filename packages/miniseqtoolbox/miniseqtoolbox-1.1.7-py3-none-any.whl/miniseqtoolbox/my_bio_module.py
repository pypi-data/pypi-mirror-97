import re
import sys

def getGCPercntage(sequence,decimals):
	#Calculates and returns the percentages of GC-letters in the target string. \
	#Allows the user to specify the number of decimals in the retuned number.
	lower_seq = sequence.lower()
	gc_count = lower_seq.count('c') \
		+ lower_seq.count('g')
	return round(100 * gc_count / len(sequence), decimals)


def rev_complement(sequence):
	#Return the reverse complement of a given sequence
	lower_seq = sequence.lower()
	complementA = re.sub('a', 'T', lower_seq)
	complementT = re.sub('t', 'A', complementA)
	complementG = re.sub('g', 'C', complementT)
	complement = re.sub('c', 'G', complementG)
	reverse_complement = complement[::-1]
	return (reverse_complement)


def oligo_match(sequence, oligo):
	#Retruns the number of oligo matches found the in the sequence
	seq_lower = sequence.lower()
	oli_lower = oligo.lower()
	all_oligo = re.findall(oli_lower, seq_lower)
	return len(all_oligo)

def oligo_match_file(filepath, oligo):
	#Returns how many times the oligo sequence occurs in the fasta file
	#It takes both the forward and reverse strand into account
	with open (filepath, 'r') as fin:
		no_oligo = 0
		for line in fin:
			if not line.startswith('>'):
				reverse_complement = rev_complement(line)
				no_oligo += oligo_match(line, oligo)
				no_oligo += oligo_match(reverse_complement, oligo)
		print(f"A total match of {no_oligo} is found for {oligo} in the sequences of file {filepath}")

if __name__ == '__main__':
	oligo_match_file("regions.fna", "cccccc")
