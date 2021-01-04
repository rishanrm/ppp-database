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