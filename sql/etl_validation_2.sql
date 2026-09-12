USE DWH;
GO

-- Check duplicate in TransactionID
SELECT
    TransactionID,
    COUNT(*) AS DuplicateCount
FROM dbo.FactTransaction
GROUP BY TransactionID
HAVING COUNT(*) > 1;