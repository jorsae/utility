import re

def main():
    print('main')


# Matches filename to filefilter using regex
def file_match(filename, filefilter):
    try:
        s = re.search(filefilter, filename)
        return False if s is None else True
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()