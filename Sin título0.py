import csv 
def create(estructura):
        with open(estructura) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                for i in range(9):
                    print(row[0][i])
                print(row)
               
                line_count+=1
            print(line_count)
create('estructura.csv')