import wrapt
import psycopg2
import autodynatrace

@autodynatrace.trace
def query():
    conn = psycopg2.connect("dbname=invictus-dev user=invictus password=password host=localhost")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stocks")
    print(cursor.fetchone())
    cursor.close()
    conn.close()


def main():
    import time
    while True:
        query()
        time.sleep(5)



if __name__ == '__main__':
    main()




