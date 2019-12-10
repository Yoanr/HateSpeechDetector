import warnings
import hatespeech
import hateSonar

def main():
    warnings.filterwarnings("ignore")
    inputText = input("Type what you want: ")

    hateSonar.perform(inputText)
    #hatespeech.dump(inputText)
    hatespeech.performFast(inputText)


if __name__ == "__main__":
    main()
