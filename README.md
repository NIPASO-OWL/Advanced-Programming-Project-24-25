# Advanced-Programming-Project-24-25
This program handles genomic data and provides an interactive interface with simple motif search and sequence alignment capabilities.

The program takes a user inputted fasta file  and subsequently shows the file as a table. 
	expected output: number of rows = number of sequences, columns: Sequence Id, Sequence, GC content(%), length, description.

The user is then prompter to choose between 'motif search' and 'Pairwise alignment'. (prompt is below the table)

Motif search: requires the user to input a specific motif to search (i.e. ATCG, not 'ATCG' or atcg)
	expected output: a table showing the seq id, motif location, and number of occurrences in the columns.

Pairwise Alignment: requires the user to input 2 sequence Ids from the uploaded fasta file.
	expected output: a text visualization of the alignment and the alignment score.

Functions specifications:

-process_file(): takes the user input file path as parameter and returns a pandas data frame representing that data, with the addition of GC content(%) and sequence length for each sequence in the fasta file.

-motif_search(): takes a user inputted motif as parameter and a data frame with the sequences to recognize that motif in, the function returns a data frame with the location of occurrence of the motif in each sequence and the number of occurrences for each sequence,

-pairwise_alignment(): takes in 2 user inputted sequence ID form the input file and a data frame containing the sequences, the function returns the alignment with the highest score and the score itself.

The templates and static folders are necessary for the correct functioning of the program. The templates folder contains all the necessary html templates and the static folder contains a files directory which is used to store the user inputted file.
