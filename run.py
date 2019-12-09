import matplotlib.pyplot as plt
import sys
import warnings
import json
import hatespeech

def main():
    warnings.filterwarnings("ignore")
    inputText = input("Type what you want: ")
    print(inputText)

    hatesonar(inputText)
    hatespeech.perform(inputText)

def hatesonar(inputText):
    from hatesonar import Sonar
    sonar = Sonar()
    sonarResult = sonar.ping(text=inputText)
    print(sonarResult)

    hatespeech = sonarResult['classes'][0]['confidence']*100
    offensivespeech = sonarResult['classes'][1]['confidence']*100
    toxicspeech = hatespeech+offensivespeech
    neitherspeech = sonarResult['classes'][2]['confidence']*100

    print("\n")
    print("(hate speech: ", hatespeech)
    print("offensive speech: ",offensivespeech, ")")

    print("\n")
    print("toxic: ", toxicspeech)
    print("neither: ", neitherspeech)


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

if __name__ == "__main__":
    main()
