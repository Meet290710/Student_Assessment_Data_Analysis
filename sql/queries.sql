-- S2a - Average score by department

SELECT
    c.department,
    ROUND(AVG(a.score),2) AS avg_score
FROM assessments a
JOIN courses c
ON a.course_id = c.course_id
GROUP BY c.department
ORDER BY avg_score ASC;


-- S2b - Underperforming courses

SELECT
    c.course,
    ROUND(AVG(a.score),2) AS avg_score
FROM assessments a
JOIN courses c
ON a.course_id = c.course_id
GROUP BY c.course
HAVING AVG(a.score) < 60;


-- S2c - Top two batches

SELECT
    batch,
    ROUND(AVG(score),2) AS avg_score
FROM assessments
GROUP BY batch
ORDER BY avg_score DESC, batch ASC
LIMIT 2;


-- Diagnostic query

SELECT
    c.course_id,
    COUNT(a.assessment_id) AS assessment_count
FROM courses c
LEFT JOIN assessments a
ON c.course_id = a.course_id
GROUP BY c.course_id;