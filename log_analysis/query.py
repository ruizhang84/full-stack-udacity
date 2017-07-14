#!/usr/bin/python3
import psycopg2

def popular_articles():
    """
    Query database what are the most popular
    three articles of all time.
    Print this information as a sorted list
    with the most popular article at the top.
    """
    conn = psycopg2.connect("dbname=news")
    cur = conn.cursor()
    cur.execute("SELECT \
                     articles.title, \
                     count(articles.title) \
                     AS views \
                 FROM \
                     articles, log \
                 WHERE \
                     '/article/' || articles.slug = log.path \
                     AND log.path in \
                     ( \
                         SELECT \
                             path \
                         FROM \
                             log \
                         WHERE \
                             path like '/article%' \
                             GROUP BY path ORDER BY count(path) DESC \
                             LIMIT 3 \
                     ) \
                     GROUP BY articles.title ORDER BY views DESC;"
                )
    #print out results
    for row in cur.fetchall():
        print ('\t"' + row[0] + '"' + "\t -- " + str(row[1]) + " views")
        
    cur.close()
    conn.close()
    return 

def popular_authors():
    """
    Query database who are the most popular
    article authors of all time.
    Print this information as a sorted list
    with the most popular author at the top.
    """
    conn = psycopg2.connect("dbname=news")
    cur = conn.cursor()
    cur.execute("SELECT \
                     authors.name, COUNT(authors.name) AS views \
                 FROM \
                     ( \
                       articles INNER JOIN log \
                       ON '/article/' || articles.slug = log.path \
                     ) \
                     INNER JOIN authors ON articles.author = authors.id \
                     GROUP BY authors.name ORDER BY views DESC;"
                )
    #print out results
    for row in cur.fetchall():
        print ("\t" + row[0] + "\t\t\t" + " --" + str(row[1]) + " views")
        
    cur.close()
    conn.close()
    return 

def percent_error():
    """
    Query database on which days did more than
    1% of requests lead to errors?.
    Print the date and precentage of error occurs.
    """
    conn = psycopg2.connect("dbname=news")
    cur = conn.cursor()
    cur.execute("SELECT \
                     to_char(date_trunc('day', time), 'Mon DD, YYYY') \
                     AS date, \
                     1.0*COUNT \
                         ( \
                           CASE \
                               status \
                           WHEN \
                               '404 NOT FOUND' \
                           THEN \
                               1 \
                           ELSE \
                               null \
                           END \
                         ) \
                     / COUNT(*) AS error \
                 FROM \
                     log \
                     GROUP BY date_trunc('day', time) \
                     HAVING 1.0*COUNT \
                         ( \
                           CASE \
                               status \
                           WHEN \
                               '404 NOT FOUND' \
                           THEN \
                               1 \
                           ELSE \
                               null \
                           END \
                         ) \
                    /COUNT(*) > 0.01;"
                )
    #print out results
    for row in cur.fetchall():
        print ("\t%s\t\t\t -- %.2f%% errors" %(row[0], row[1]*100))
        
    cur.close()
    conn.close()
    return 
    
#run queries
if __name__ == '__main__':
    print ("What are the most popular three articles of all time?")
    popular_articles()
    print ('-------------------------------------------------')
    print ("Who are the most popular article authors of all time?")
    popular_authors()
    print ('-------------------------------------------------')
    print ("On which days did more than 1% of requests lead to errors? ")
    percent_error()
    print ()



