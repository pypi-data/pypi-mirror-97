def setmpl():
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    
    #Primary Colours
    intellify_blue = '#2f3649'
    intellify_orange = '#f4972d'

    #Secondary Colours
    intellify_pantone713 = '#febd85'
    intellify_pantone712 = '#fdc899'
    intellify_pantone7544 = '#748592'
    intellify_pantone7543 = '#96a3ad'
    intellify_white = '#ffffff'

    #Colours that go well with primary
    complementary_green = '#2395B5'
    complementary_skyblue = '#40B4A6'
    complementary_brown = '#603737'

    all_colors = [intellify_orange, intellify_blue, complementary_green, complementary_brown, complementary_skyblue]

    #Setting Colours for graphs
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=all_colors)

    #Setting Line Attributes
    plt.rc('lines', linewidth = 2, linestyle = '-')

    #Setting Font
    plt.rc('font', family = 'serif')
    plt.rcParams['font.serif'] = 'Arial'
    plt.rc('text', color = 'black' )

    #Setting Figure Properties
    plt.rc('figure', dpi = 150, figsize = (5,3), facecolor = 'white', edgecolor = 'white')
    plt.rcParams['figure.subplot.right'] = 0.9
    plt.rcParams['figure.subplot.left'] = 0.1

    #Setting Axes & Ticks
    plt.rc('axes', edgecolor = 'grey', titlesize = 16, labelsize = 14, titleweight = 'bold',
          labelweight = 'bold', labelcolor = intellify_blue, titlecolor = intellify_blue)
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10

    #Setting Legend
    plt.rc('legend', frameon = False, edgecolor = intellify_pantone7543, labelspacing = 0.3, fontsize = 8)
    

def getHeatMapColors():
	heatmap_colors = ['#2f3649', '#353a51', '#353a51', '#45405f', '#4e4365', '#58456b', '#63476f', \
                  '#6f4973', '#7b4a76', '#874c78', '#934d79', '#a04e78', \
                 '#ab5077', '#b75275', '#c15472', '#cb576e', '#d55b69', '#dd6063', \
                  '#e4655d', '#ea6c56', '#ee734f', '#f27b47', '#f4843f', '#f58d36', '#f4972d']
	return heatmap_colors