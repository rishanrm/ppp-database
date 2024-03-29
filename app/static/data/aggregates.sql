/*
Data columns:
    Total number of loans
    Total Jobs
    Total $

*/

-- SQL Query:
SELECT
    state,
    COUNT(loanamount) as loancount,
    SUM(jobsreported) as totaljobsreported,
    SUM(loanamount) as totalloansreported
FROM
    ppp_data_all_merged
GROUP BY
    state
ORDER BY
    loancount DESC
;

--------------------------------------------------------------------------------
/*
Data columns:
    Avg. $/loans
*/

-- SQL Query:
SELECT
    state,
    SUM(loanamount) / COUNT(loanamount) as avgloansize
FROM
    ppp_data_all_merged
GROUP BY
    state
ORDER BY
    avgloansize DESC
;

--------------------------------------------------------------------------------
/*
Data columns:
    Avg jobs / loan
    Avg $ / job
*/

-- SQL Query:
SELECT
    state,
    ROUND(SUM(jobsreported::NUMERIC) / COUNT(loanamount::NUMERIC),1) as jobsperloan,
    CAST(SUM(loanamount::NUMERIC) / SUM(jobsreported) AS MONEY) as dollarsperjob

FROM
    ppp_data_all_merged
WHERE
    loanamount IS NOT NULL AND jobsreported IS NOT NULL AND jobsreported > 0 AND state != 'AE'
GROUP BY
    state
ORDER BY
    dollarsperjob DESC
;

--------------------------------------------------------------------------------
/*
Data columns:
    Count of loans not reporting jobs
    Sum of loans not reporting jobs
    Average loan size of loans not reporting jobs
*/

-- SQL QUERY:
SELECT
    state,
    COUNT(loanamount) as loancountnulljobs,
    CAST(SUM(loanamount) AS MONEY) as totalloansreportednulljobs,
    CAST(SUM(loanamount) / COUNT(loanamount) AS MONEY) as avgloansizenulljobs
FROM
    ppp_data_all_merged
WHERE
    jobsreported = 0 OR jobsreported IS NULL
GROUP BY
    state
ORDER BY
    loancountnulljobs DESC
;

--------------------------------------------------------------------------------

--OLD QUERIES


SELECT
	state,
	COUNT(loanrange) as loancount,
	SUM(jobsreported) as totaljobsreported,
	ROUND(AVG(jobsreported)::numeric,1) as avgjobsreported,
	SUM(loanrange::NUMERIC) as totalloansreported,
	ROUND(SUM(loanrange::NUMERIC) / COUNT(loanrange)::numeric,1) as avgloansize,
	ROUND(SUM(loanrange::NUMERIC) / SUM(jobsreported)::numeric,1) as dollarsperjob

FROM
    ppp_data_150k_and_up_080820
WHERE
    loanrange IS NOT NULL AND jobsreported IS NOT NULL AND state != 'AE'
GROUP BY
    state
ORDER BY
    dollarsperjob ASC
;


SELECT
	state,
	COUNT(loanamount) as loancount,
	SUM(jobsreported) as totaljobsreported,
	ROUND(AVG(jobsreported)::numeric,1) as avgjobsreported,
	SUM(loanamount::NUMERIC) as totalloansreported,
	ROUND(SUM(loanamount::NUMERIC) / COUNT(loanamount)::numeric,1) as avgloansize,
	ROUND(SUM(loanamount::NUMERIC) / SUM(jobsreported)::numeric,1) as dollarsperjob
FROM
    ppp_data_all_merged
WHERE
    loanamount IS NOT NULL AND jobsreported IS NOT NULL AND state != 'AE'
GROUP BY
    state
ORDER BY
    dollarsperjob ASC
;









