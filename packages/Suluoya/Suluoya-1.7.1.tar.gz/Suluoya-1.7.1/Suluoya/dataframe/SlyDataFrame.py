class SlyDataFrame(object):
    
    def __init__(self,df=None):
        self.df = df
    
    @property    
    def report(self):
        import pandas_profiling
        a = pandas_profiling.ProfileReport(self.df)
        a.to_file('report.html')
    
    @property
    def gui(self):
        from pandasgui import show
        show(self.df)
    
    @property
    def sweetviz(self):
        import sweetviz as sv 
        x=sv.analyze(self.df)
        x.show_html()
        

