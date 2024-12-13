test: 
	g++ -c Test.cpp .\BibTeXParser.cpp .\PublicationDatabase.cpp .\Publication.cpp .\Author.cpp
	g++ -g -o TestDebug Test.o .\BibTeXParser.o .\PublicationDatabase.o .\Publication.o .\Author.o
	g++ -O3 -o TestOptimize Test.o .\BibTeXParser.o .\PublicationDatabase.o .\Publication.o .\Author.o

clean:
	rm -f Test.o BibTeXParser.o PublicationDatabase.o Publication.o Author.o
	rm -f TestDebug TestOptimize