from matplotlib.dates import DateFormatter, MonthLocator
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import shapiro, pearsonr, linregress
from scipy.stats.morestats import _calc_uniform_order_statistic_medians, _parse_dist_kw
import seaborn as sns
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.manifold import TSNE
import umap.umap_ as umap


sns.set_theme(
    style='darkgrid', 
    palette='magma', 
    font='sans-serif', 
    font_scale=1, 
    color_codes=True, 
    rc=None)


def ts_outlier_plot(data, dt, y):
    
    fig,ax=plt.subplots(figsize=(12,7))

    date_form = DateFormatter("%m-%d")
    ax.xaxis.set_major_formatter(date_form)

    mu=data[y].mean()
    std=data[y].std()
    q3=data[y].quantile(.75)
    q1=data[y].quantile(.25)
    iqr=q3-q1
    uthresh=q3+1.5*iqr
    lthresh=q1-1.5*iqr

    df_high = data[(data[y]<lthresh) | (data[y]>uthresh)]

    sns.lineplot(data=data, x=dt, y=y, ax=ax, zorder=1)
    sns.scatterplot(data=df_high, x=dt, y=y, ax=ax, color=sns.color_palette()[3], zorder=2, s=120, label='outliers')
    plt.xticks(rotation=40)

    # Ensure a major tick for each week using (interval=1) 
    ax.xaxis.set_major_locator(MonthLocator(interval=1))

    ax.axhline(uthresh, ls='--', alpha=.9, label='q3+1.5*iqr', color=sns.color_palette()[3])
    ax.axhline(lthresh, ls='--', alpha=.9, label='q1-1.5*iqr', color=sns.color_palette()[3])

    ax.axhline(mu, ls=':', alpha=.3, color=sns.color_palette()[0])
    ax.axhline(mu+std, ls=':', alpha=.5, label='mu+std', color=sns.color_palette()[1])
    ax.axhline(mu-std, ls=':', alpha=.7, label='mu-std', color=sns.color_palette()[0])

    ax.legend()
    ax.set_title(f'Outlier plot for feature {y}', fontweight='bold', fontsize=17)
    plt.tight_layout()



def separability_plot(df, trgt):
    df=df.copy()
    
    cls = df.pop(trgt)
    df=df.select_dtypes(include='number')

    fig,ax=plt.subplots(1,3,figsize=(15,5))

    # TSNE
    clf = TSNE(n_components=2, perplexity=30, learning_rate=15, random_state=1)
    X_t = clf.fit_transform(df)
    x_=pd.DataFrame(X_t,columns=['x','y'])
    x_['class']=cls
    sns.scatterplot(data=x_, x='x', y='y', hue='class', ax=ax[0])
    ax[0].set_title('t-SNE', fontweight='bold')

    # LDA
    clf = LinearDiscriminantAnalysis(n_components=2)
    X_t = clf.fit_transform(df, cls)
    x_=pd.DataFrame(X_t,columns=['x','y'])
    x_['class']=cls
    sns.scatterplot(data=x_, x='x', y='y', hue='class', ax=ax[1])
    ax[1].set_title('LDA', fontweight='bold')

    # UMAP
    reducer = umap.UMAP(n_neighbors=10, min_dist=1, n_components=2)
    x_ = reducer.fit_transform(df)
    x_=pd.DataFrame(x_,columns=['x','y'])
    x_['class']=cls
    sns.scatterplot(data=x_, x='x', y='y', hue='class', ax=ax[2])
    _=ax[2].set_title('UMAP', fontweight='bold')

    fig.suptitle(f'Separability of data with respect to {trgt}', fontsize=16)
    plt.tight_layout()


def corel_scatter_(*args,**kwargs):
    df_ = pd.DataFrame(args).T
    r,p=pearsonr(x=df_.iloc[:,0], y=df_.iloc[:,1])
    
    if(r <= -.2):
        c=sns.color_palette()[1]
    elif(-.2 < r and r < .2):
        c=sns.color_palette()[2]
    else:
        c=sns.color_palette()[4]
        
    sns.regplot(data=df_, x=df_.columns[0], y=df_.columns[1],color=c,scatter_kws={'alpha':0.3})
    ax = plt.gca()
    ax.annotate('r = {:.2f}'.format(r), xy=(0.5,0.9), 
                xycoords='axes fraction', ha='center', fontsize=16, fontweight='bold')

def correl_plot(df, color=0):
    df=df.copy()
    df = df.select_dtypes(include='number')
    g = sns.PairGrid(df, height=1.5,aspect=1.5, diag_sharey=False, corner=True)
    g.map_diag(sns.histplot, color=sns.color_palette()[color])
    _=g.map_lower(corel_scatter_)


def qq_plot(data, x, ax):
    
    x_ = np.asarray(data[x])
    osm_uniform = _calc_uniform_order_statistic_medians(len(x_))
    dist = _parse_dist_kw('norm', enforce_subclass=False)
    osm = dist.ppf(osm_uniform)
    osr = np.sort(x_)
    slope, intercept, r, prob, _ = linregress(osm, osr)    
    plot_df = pd.DataFrame({'osm':osm, 'osr':osr,'slope':slope*osm+intercept})
    
    sns.scatterplot(data=plot_df, x='osm', y='osr')
    sns.lineplot(data=plot_df, x='osm', y='slope', color=sns.color_palette()[2])    

    # normality test
    stat, p = shapiro(x_)

    # interpret test statistic
    alpha = 0.05
    if p > alpha:
        normal_test= 'Shapiro-Wilk:\nStatistics=%.3f, \np=%.3f\n(Gaussian)' % (stat, p)#'Sample looks Gaussian (fail to reject H0)'
    else:
        normal_test='Shapiro-Wilk:\nStatistics=%.3f, \np=%.3f\n(NOT Gaussian)' % (stat, p)   
    
    # draw statistic on chart
    xmin, xmax = np.amin(osm), np.amax(osm)
    ymin, ymax = np.amin(x_), np.amax(x_)
    posx = xmin + 0.70 * (xmax - xmin)
    posy = ymin + 0.01 * (ymax - ymin)
    ax.text(posx, posy, normal_test)


def univariate_plot(data, x):

    fig, ax = plt.subplots(2,2, figsize=(12,7))

    # Histogram
    _=sns.histplot(data=data, x=x, ax=ax[0,0])
    ax[0,0].set_title('Histogram', fontweight='bold')

    # Emprirical CDF
    _=sns.ecdfplot(data=data, x=x, ax=ax[1,0])
    _=sns.rugplot(data=data, x=x, ax=ax[1,0], color=sns.color_palette()[2])
    ax[1,0].set_title('Cumulative Distribution Function', fontweight='bold')

    # Boxplot
    _=sns.boxplot(data=data, x=x, ax=ax[0,1], color=sns.color_palette()[2])
    _=ax[0,1].set_title('Boxplot', fontweight='bold')

    # QQ-plot
    _=qq_plot(data=data, x=x, ax=ax[1,1])
    ax[1,1].set_xlabel('Normal theoretical quantiles')
    ax[1,1].set_ylabel('Ordered values')
    ax[1,1].set_title('Data vs normal quantiles', fontweight='bold')

    # Title for plot and layoyt
    fig.suptitle(f'Distribution plots of feature: {x}', fontsize=16)
    plt.tight_layout()