# CSCI 355 Internet Web Technologies
# Summer 2024
# Abdul Mutallif
# Assignment 4 - Front End Development
# Worked with class
# Sources: Listed in the functions/code


import OutputUtil as ou


def read_file(filename):
    with open(filename) as file:
        lines = file.readlines()
        headers = lines[0].strip().split(",")
        data = [line.strip().split(",") for line in lines[1:]]
        return headers, data


def main():
    headers, data = read_file("Assignment04.csv")
    print(headers)
    print(data)
    title = "United States of America"
    types = ["S", "S", "S", "N"]
    alignments = ["L", "C", "L", "R"]
    ou.write_html_file("Assignment04.html", title, headers, types, alignments, data, True)
    ou.write_xml_file("Assignment04.xml", title, headers, data, do_open=True)


if __name__ == '__main__':
    main()
