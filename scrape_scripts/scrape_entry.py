import racename_raceid
import entry_list
import summary

racename_raceid_dict = racename_raceid.racename_raceid()

def main():
    entry_list.scrape(racename_raceid_dict)
    summary.output_summary(racename_raceid_dict)

if __name__ == '__main__':
    main()