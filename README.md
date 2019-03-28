### Author : Yegeon Seo

#### CS 265 Final Project

##### I did not upload sample input files since it containes some private information. Please contact me if you want a sample input file!

---
to run the program : 
```python3 final.py inputFile```
---

This program creates an ical file from drexel schedule.

I have talked to the Professor Mongan about reading the data directly from Drexel course registration system, but he suggested using a different source since it is hard to get data directly from Drexel. Therefore, I copied schedules from:

* DrexelOne -> Academics -> Weekly Course Schedule -> Detailed Information 

I copied 5 different schedules from my DrexelOne schedule and using them as inputs. 

----

##### Makefile

Makefile contains build, run, view, and clean. 

```run``` currently depends on the test files I included (fall1617, fall1718, winter1617, etc...).

```clean```  deletes all the `.ics` files made by ```run```

* To build: ```make build```
* To view: ```make view```
* To run: ```make run```
* To clean: ```make clean```

----
### Thanks!



