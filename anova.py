import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import matplotlib.pyplot as plt
import pandas as pd
import argparse
from tkinter import *
from tkinter import ttk
import numpy as np

class ANOVA:
    def __init__(self, fn):
        df = pd.read_csv(fn)
        df = df[df.type != 'Garage']
        df = df.dropna()
        df.bedrooms = df.bedrooms.astype(int)

        self.form = 'form' in df.columns

        self.df = df
        self.fit()

    def fit(self):
        model = 'price ~ C(locality) + C(type) + bedrooms + area'
        if self.form: model += ' + C(form)'
        lm = ols(model, self.df).fit()
        self.lm = lm

    def plot_by_type(self, minct=10):
        plt.figure()
        df = self.df.copy()
        cts = df.groupby('type').count().price

        valid_locs = cts[cts>minct].index
        df = df[df.type.isin(valid_locs)]

        pbt = df.groupby('type').mean().sort_values(by='price')
        plt.bar(pbt.index, pbt.price)

        plt.xticks(rotation=30)

    def plot_by_loc(self, minct=10):
        df = self.df.copy()
        plt.figure()
        cts = df.groupby('locality').count().price

        valid_locs = cts[cts>minct].index
        df = df[df.locality.isin(valid_locs)]

        pbl = df.groupby('locality').mean().sort_values(by='price')
        plt.bar(pbl.index, pbl.price)

        plt.xticks(rotation=30)

    def plot_by_beds(self):
        plt.figure()
        pbb = self.df.groupby('bedrooms').mean()
        pbb.plot()

    def predict(self, X):
        return self.lm.get_prediction(X).predicted_mean[0]

    def __str__(self):
        return self.lm.summary().as_text()

class GUI:

    def __init__(self, model, width=500, height=250):
        self.model = model
        locs = np.unique(model.df.locality)
        types = np.unique(model.df.type)
        beds = np.unique(model.df.bedrooms)

        window = Tk()
        window.resizable(False, False)
        window.title('House price ANOVA')
        window.geometry(f'{width}x{height}')
        
        locvar = StringVar(window)
        typevar = StringVar(window)
        bedvar = StringVar(window)
        pricevar = StringVar(window)
        areavar = StringVar(window)

        locvar.set('Qawra')
        typevar.set('Penthouse')
        bedvar.set('3')

        vcmd = (window.register(self.callback))

        wloc = ttk.Combobox(window, textvariable=locvar, values=list(locs))
        wtype = ttk.Combobox(window, textvariable=typevar, values=list(types))
        wbed = ttk.Combobox(window, textvariable=bedvar, values=beds)
        warea = Entry(validate='all', validatecommand=(vcmd, '%P')) 
        warea.insert(0, 'Area in sq metres')
        wpricevar = Label(window, textvariable=pricevar)
        get_pred = Button(window, text="Get Prediction", command=self.get_prediction_action)

        wloc.place(relx=0.1, rely=0.15, anchor='nw')
        wtype.place(relx=0.1, rely=0.3, anchor='nw')
        wbed.place(relx=0.1, rely=0.45, anchor='nw')
        warea.place(relx=0.1, rely=0.6, anchor='nw')
        get_pred.place(relx=0.1, rely=0.8, anchor='nw')
        wpricevar.place(relx=0.6, rely=0.8, anchor='nw')

        if model.form:
            forms = np.unique(model.df.form)
            formvar = StringVar(window)
            wform = ttk.Combobox(window, textvariable=formvar, values=list(forms))
            wform.place(relx=0.6, rely=0.3, anchor='nw')

        self.model = model
        self.bedvar = bedvar
        self.locvar = locvar
        self.typevar = typevar
        self.pricevar = pricevar
        self.warea = warea
        self.wform = wform 

        mainloop()

    def callback(self, P): 
        return str.isdigit(P) or P == ""

    def get_prediction_action(self):
        loc = self.locvar.get()
        ptype = self.typevar.get()
        nbeds = int(self.bedvar.get())
        area = int(self.warea.get())
        example = {'locality': loc, 'type': ptype, 'bedrooms': nbeds, 'area': area}
        if self.model.form:
            form = self.wform.get()
            example['form'] = form
        price = self.model.predict(example)
        self.pricevar.set(f'€{int(price):,}')

if __name__=='__main__':

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--show_plots', action='store_true')
    parser.add_argument('--csv', help='csv to read properties', default='remax_properties.csv')
    args = parser.parse_args()

    fn = args.csv

    model = ANOVA(fn)
    
    if args.show_plots:
        model.plot_by_loc()
        model.plot_by_beds()
        model.plot_by_type()
        plt.show()

    gui = GUI(model)

    if 0:
        df['price_pred'] = lm.get_prediction(df).summary_frame()['mean']
        df.price.plot()
        df.price_pred.plot()
        plt.show()
