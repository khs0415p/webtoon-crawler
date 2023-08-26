import argparse
import scrapers


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', type=str)
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    domain = args.domain

    scraper = getattr(scrapers, f'{domain.capitalize()}Scraper')()
    scraper.do_scrap()

if __name__=="__main__":
    main()