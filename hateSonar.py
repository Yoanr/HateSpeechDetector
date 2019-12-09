import matplotlib.pyplot as plt
import json


def perform(inputText):
    from hatesonar import Sonar
    sonar = Sonar()
    sonarResult = sonar.ping(text=inputText)

    hatespeech = sonarResult['classes'][0]['confidence']*100
    offensivespeech = sonarResult['classes'][1]['confidence']*100
    toxicspeech = hatespeech+offensivespeech
    neitherspeech = sonarResult['classes'][2]['confidence']*100

    '''
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Toxic', 'Neutral'
    sizes = [toxicspeech, neitherspeech]
    explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    fig1.canvas.set_window_title(inputText)
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
    '''

    lab = ["The tweet contains hate speech","The tweet is not offensive","The tweet uses offensive language "]
    if(neitherspeech > 50):
            label = 1
            confidence = neitherspeech
    elif (offensivespeech > 50):
            label = 2
            confidence = offensivespeech
    else:
            label = 0
            confidence = hatespeech
    print('hateSonar says: ' + lab[label] + ' with ' + str(round(confidence, 2)) + '% confidence.')