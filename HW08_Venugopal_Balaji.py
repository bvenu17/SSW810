"""
@author: Venugopal Balaji CWID: 10446195
this program uses various modules to perform certain functions
"""
import os as os
from typing import IO,DefaultDict, Iterator, List, Any,Dict, Optional, Set, Tuple
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from prettytable import PrettyTable

def date_arithmetic()-> Tuple[datetime, datetime, int]:
    """use the datetime module to do required atithmetic operations"""
    date1 : str = "February 27 2020"
    date2 : str = "February 27 2019"
    day1 : str = "February 1 2019"
    day2 : str = "September 30 2019"
    d1: datetime = datetime.strptime(date1,"%B %d %Y")
    d2: datetime = datetime.strptime(date2,"%B %d %Y")
    day1: datetime = datetime.strptime(day1,"%B %d %Y")
    day2: datetime = datetime.strptime(day2,"%B %d %Y")
    res1 : datetime = d1 + timedelta(days=3)
    res2 : datetime = d2 + timedelta(days=3)
    res3 : datetime = day2 - day1
    return (res1,res2,res3.days)

def file_reader(path : str, fields : int, sep: str = ',', header : bool=False) -> Iterator[List[str]]:
    """this functions reads the file and then separate the fields by the given separator and raise error for wrong fields"""
    try:
        fp: IO = open(path, "r")
    except FileNotFoundError:
        raise FileNotFoundError("The path was not found ")
    else:
        with fp:
             if header == True:
                    next(fp)
             for offset,line in enumerate(fp):
                 cnt : Dict[str,int] = Counter(line)
                 separator_number : int  = cnt[sep]
                 if separator_number + 1 != fields:
                    raise ValueError(f"File name: {path} Line number: {offset} Number of fields: {separator_number+1} Number of fields expected: {fields}")
                 else:
                     allFields = line.rstrip().split(sep)
                     yield allFields

class FileAnalyzer:
    """This class analyzes the files in a given directory"""

    def __init__(self,directory : str) -> None:
        """function to initialize the variables in class"""
        self.directory : str = directory
        self.files_summary: Dict[str, Dict[str, int]] = dict()
        self.analyze_files()


    def analyze_files(self)->None:
        """function to find python files and number of class,functions, lines and characters in those files"""
        try:
            allFiles : List[str] = os.listdir(self.directory)
        except FileNotFoundError:
            raise FileNotFoundError("The given directory does not exist")
        else:
            for i in allFiles:
                if i.endswith(".py"):
                    try:
                        fp : IO = open(os.path.join(self.directory,i), "r")
                    except FileNotFoundError:
                        raise FileNotFoundError("File cannot be open")
                    else:
                        with fp:
                            num_class : int = 0
                            num_func : int = 0
                            num_lines : int = 0
                            num_char : int = 0
                            for line in fp:
                                line = line.strip()
                                num_lines+=1
                                num_char+=len(line)
                                if line.startswith("def ") and line.endswith(":"):
                                    num_func+=1
                                if line.startswith("class ") and line.endswith(":"):
                                    num_class+=1
                            self.files_summary[i] = {
                                "class":num_class,
                                "function":num_func,
                                "line":num_lines,
                                "char":num_char
                            }
    
    def pretty_print(self) -> None:
        """this functions create a table for the file summary"""
        pt: PrettyTable = PrettyTable(field_names=["File Name","Classes","Functions","Lines","Characters"])
        for key,values in self.files_summary.items():
            pt.add_row([key,values["class"],values["function"],values["line"],values["char"]])
        return pt

def main():
    """ main program """
    print(date_arithmetic())
    print(list(file_reader("file.txt", 3, sep='|', header=True)))
    for cwid, name, major in file_reader("file.txt", 3, sep='|', header=True):  
        print(f"cwid: {cwid} name: {name} major: {major}") 
    fa = FileAnalyzer("/Users/venugopal/Documents/Fall20/SSW810/Week7")
    print(fa.files_summary)
    print(fa.pretty_print())

if __name__ == "__main__":
    main()
