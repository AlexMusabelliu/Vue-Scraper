from bs4 import BeautifulSoup

class VueScraper():
    '''
    A scraper for a given StudentVue class's quarter page. (e.g. BC Calculus Gantz, Q3)
    To use:

        Go to a StudentVue class for one quarter.
        Right-click and save the page with some accessible name.
        
        Then, to pass the page to the Scraper, either:
            1) pass the absolute path (e.g. C:\\Users\\Username\\Downloads\\test.html)
            2) change the directory, then pass the relative path (e.g. test.html)

        From there, utilize the scraper's functions to easily calculate your potential GPA.
    '''
    def __init__(self, doc):
        with open(doc, "rb") as f:
            t = BeautifulSoup(f, "html5lib")

            self.alldata = [x.string for x in t.find_all("td") if x.string not in (None, "\n        ", "0")][2:-2]
            self.alldata = [x for x in self.alldata if (self.alldata.index(x) + 1) % 5 != 0]

            self.typeMods = {}

            self.gradeMod = ([], [])

            types = self.get_types()

            print("Give the following as a decimal:")
            for t in set(types):
                self.typeMods.update({t:float(input(f"Please define the weight (percentage of the grade) of \"{t}\" grades:    "))})

    def get_grades(self):
        '''
        Returns a list of all StudentVue grades from the input page in order from top to bottom.
        '''
        return self.alldata[3::4]

    def get_types(self):
        '''
        Returns a list of all types of all grade entries from the input page in order from top to bottom.
        '''
        return self.alldata[1::4]

    def get_dates(self):
        '''
        Returns a list of all dates of all grade entries from the input page in order from top to bottom.
        '''
        return self.alldata[::4]

    def get_stratified_info(self):
        '''
        Returns a tuple of (date, type, grade) for all grade entries from the input page from top to bottom.
        '''
        return tuple(zip(self.get_dates(), self.get_types(), self.get_grades()))

    def calc_grade(self, weights={}):
        '''
        Returns the calculated grade of the input page. 
        If no weights are specified, uses initialized weight dict. 
        If the weights dict. is improperly defined, the default weight is 1. 
        '''
        total = 0
        cur = 0

        grades = self.get_grades() + self.gradeMod[0]
        types = self.get_types() + self.gradeMod[1]
        weightDic = self.typeMods

        if weights:
            weightDic = weights

        for i in range(len(grades)):
            mod = self.typeMods.get(types[i], 1)

            c, ma = tuple([float(x) for x in grades[i].split("/")])

            total += mod * ma
            cur += mod * c

        return cur / total

    def mod_grade(self, points, type=None):
        '''
        Modifies the current grade by appending a new modifier grade. 
        Optional parameter type is used to specify the type of grade it is and thus weight. If empty, the weight is 1. 
        Returns nothing.
        '''
        self.gradeMod[0].append(str(points) + "/0")
        self.gradeMod[1].append(type)