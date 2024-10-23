-- Clean de la data
DELETE FROM immo.real_estate_transaction WHERE value IS NULL;
DELETE FROM immo.real_estate_transaction WHERE value > 1000000;
DELETE FROM immo.real_estate_transaction WHERE local_type = 'Local industriel. commercial ou assimilé';
DELETE FROM immo.real_estate_transaction WHERE local_type = '';

-- Par type de local
SELECT local_type, AVG(value) AS average_value
FROM immo.real_estate_transaction
WHERE local_type <> ''
GROUP BY local_type;

-- Par type de local et par code postal
SELECT
                postal_code,
                local_type,
                AVG(value) AS average_value
            FROM immo.real_estate_transaction
            GROUP BY postal_code, local_type
            ORDER BY average_value DESC;