# PI2014 off by one problem

This document describes a major data inconsistency in CIK open data concerning the 2014 parlamentary elections.

The data is available for download here: <https://results.cik.bg/pi2014/csv.html>

## Context and problem 

 The file `votes_pe2014.txt` contains vote counts. According to the documentation (readme_pe2014.txt), each line starts with the section number and is followed by pairs of values, corresponding to valid and invalid votes for each party. The order is fixed in the readme file. 

The problem is that for an unknown number of lines the order in the data does not correspond to the order specified in the readme file, effectively attributing votes to the wrong party. 


## Example data

These three examples illustrate the inconsistency. They not exhaustive. We can not estimate how many lines (sections) are concerned.

As can be seen by the protocols, in all three of these sections, party DPS is the winner.

<https://results.cik.bg/pi2014/protokoli/17/0100089.html> 
<https://results.cik.bg/pi2014/protokoli/17/2300029.html>
<https://results.cik.bg/pi2014/protokoli/01/1100031.html> 

However in the corresponding lines in `votes_pe2014.txt` , in sections 170100089 and 172300029, the winners votes appear in the 18th position, whereas they should appear in the 19th position. 



Below are the corresponding lines and a breakdown of the vote values and their position.

## line 6279 - Problem
```
170100089;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;8;0;0;0;0;0;3;0;0;0;0;0;0;0;1;0;316;0;2;0;0;0;0;0;3;0;0;0;2;0;0;0;
```

1. 170100089; 
1. 0;0; 
1. 0;0; 
1. 0;0; 
1. 0;0; 
1. 0;0; 
1. 0;0; 
1. 0;0; 
1. 0;0; 
1. 8;0; 
1. 0;0; 
1. 0;0; 
1. 3;0;
1. 0;0; 
1. 0;0; 
1. 0;0; 
1. 1;0; 
1. **316;0;** 
1. 2;0;
1. 0;0;
1. 0;0;
1. 3;0;
1. 0;0;
1. 2;0;
1. 0;0;

## line 6489 - Problem 
```                  
172300029;0;0;6;0;0;0;0;0;0;0;1;0;2;0;0;0;12;0;0;0;1;0;0;0;16;0;0;0;0;0;0;0;290;2;1;0;0;0;0;0;1;0;0;0;0;0;0;0;
```

1. 172300029;
1. 0;0;
1. 6;0;
1. 0;0;
1. 0;0;
1. 0;0;
1. 1;0;
1. 2;0;
1. 0;0;
1. 12;0;
1. 0;0;
1. 1;0;
1. 0;0;
1. 16;0;
1. 0;0;
1. 0;0;
1. 0;0;
1. **290;2;**
1. 1;0;
1. 0;0;
1. 0;0;
1. 1;0;
1. 0;0;
1. 0;0;
1. 0;0;  


## line 189 - OK
This part of the file corresponds to the specification in the readme, DPS votes are in 19-th position 
```
011100031;0;0;0;0;0;0;0;0;0;0;1;0;8;0;1;0;18;0;0;0;1;0;0;0;3;0;5;0;0;0;0;0;0;0;506;0;0;0;0;0;0;0;10;0;0;0;3;0;0;0;0;0;
```
1. 011100031; 
1. 0;0; 
1. 0;0; 
1. 0;0; 
1. 0;0; 
1. 0;0; 
1. 1;0; 
1. 8;0; 
1. 1;0; 
1. 18;0; 
1. 0;0; 
1. 1;0; 
1. 0;0; 
1. 3;0;
1. 5;0; 
1. 0;0; 
1. 0;0; 
1. 0;0; 
1. **506;0;** 
1. 0;0; 
1. 0;0; 
1. 0;0; 
1. 10;0; 
1. 0;0; 
1. 3;0; 
1. 0;0; 
1. 0;0;