##### PYTHON #####
#Yegeon Seo
#Final Project makefile

.PHONY : build test run clean

run : fall1617 fall1718 winter1617 winter1718 winter1819
	python3 final.py fall1617
	python3 final.py fall1718
	python3 final.py winter1617
	python3 final.py winter1718
	python3 final.py winter1819

build : 
	@# "Python Makefile"
	chmod +x final.py

view : 
	@\less final.py

clean :
	@\rm *.ics


