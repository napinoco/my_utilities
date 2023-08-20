# query_analysis
Web application with streamlit for Query analysis
* Visualize the processing flow of the input Query, i.e., which tables and subqueries each subquery depends on, using graphviz.
* It also returns mermaid notation to facilitate documentation in markdown.

You can also try it on Google Colab.
https://colab.research.google.com/drive/1vSutSsSQ616BdaoC8cWyCR7UXH5USpja

## Limitations
* Only support one level of `WITH` clauses. For example, the following style will *NOT* be parsed correctly:
```
WITH subquery2 AS (
    WITH subquery1 AS ( -- `WITH` clauses of two or more levels
        SELECT * FROM original_table
    )
    SELECT * FROM subquery1
)
SELECT * FROM subquery2
```
```
WITH subquery1 AS (
    SELECT * FROM original_table
)
SELECT * 
FROM (SELECT * FROM subquery1) subquery2 -- Subqueries without `WITH` clause
```
These should be refactored as follows:
```
WITH subquery1 AS (
    SELECT * FROM original_table
), subquery2 AS (
    SELECT * FROM subquery1
)
SELECT * FROM subquery2
```
