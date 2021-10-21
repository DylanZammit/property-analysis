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
    def __init__(self, df):
        '''
        TODO: apply PCA on data first
        '''
        df = df[df.type != 'Garage']
        df = df.dropna()
        df.bedrooms = df.bedrooms.astype(int)

        self.form = 'form' in df.columns

        self.df = df
        self.fit()

    def PCA(self, cutoff=0.99):
        covariates = 'bedrooms area int_area ext_area'.split()
        data = self.df[covariates]
        data = data.sub(data.mean()).div(data.std())
        vcv = data.cov()
        val, vec = np.linalg.eigh(vcv)
        val = [v/sum(val) for v in val]
        
        feature = vec[:,2:] # choose 2 appropraitely!!

        data1 = feat.T@data.T

        return data1

    def get_model_eqn(self, categ, covar):

        if(len(categ)>0 and len(covar)>0):
            return 'price ~ ' + '+'.join(categ)+'+'+'+'.join(covar)
        elif(len(covar)==0 and len(categ) > 0):
            return 'price ~ ' + '+'.join(categ)
        elif(len(covar) > 0 and len(categ) == 0):
            return 'price ~ ' + '+'.join(covar)
        else: 
            return 0

    def perform_analysis_dyn(self, categ=['locality', 'type'], covar=['area'], suppress_output=False):
        categ = [f'C({c})' for c in categ]

        model_eqn = self.get_model_eqn(categ, covar)

        if(model_eqn==0): 
            print('No significant variable')
            return

        #apply anova
        lm = ols(model_eqn, data=self.df).fit()
        table = sm.stats.anova_lm(lm, typ=2)
        p_vals = table['PR(>F)']

        print(lm.summary())
        print(table)

        #value and index of largest p value
        max_p = np.max(p_vals)
        argmax_p = np.argmax(p_vals)

        if(max_p>0.05):

            #removes insignificant variables with largest p val
            if(argmax_p<len(categ)):
                del categ[argmax_p]
            else:
                del covar[argmax_p-len(categ)]

            #performs analysis without the insignificant variable
            self.perform_analysis_dyn(self.df, categ, covar)
        else:
            #all remaining variables significant, so output info
            coefficients = lm.params
            r = lm.rsquared_adj
            adj_r = lm.rsquared
            if not suppress_output:
                print('Adjusted R-Squared: ' + str(adj_r))
                print(coefficients)
                print(p_vals)
            self.lm = lm

    def fit(self):
        categ = ['locality', 'type']
        covar = ['bedrooms', 'area']

        categ = ['locality', 'type', 'region']
        covar = ['bedrooms', 'area', 'int_area', 'ext_area']

        if self.form: categ.append('form')
        self.perform_analysis_dyn(categ, covar)
        #lm = ols(model, self.df).fit()
        #self.lm = lm


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
            self.wform = wform 

        self.model = model
        self.bedvar = bedvar
        self.locvar = locvar
        self.typevar = typevar
        self.pricevar = pricevar
        self.warea = warea

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

    parser = argparse.ArgumentParser(description='Property price prediction using ANOVA.')
    parser.add_argument('--show_plots', action='store_true')
    parser.add_argument('--csv', help='csv to read properties', default='remax_properties.csv')
    args = parser.parse_args()

    fn = args.csv
    df = pd.read_csv(fn)

    model = ANOVA(df)
    
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
