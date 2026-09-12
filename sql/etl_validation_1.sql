USE DWH;
GO

-- Check duplicate in DimAccount
SELECT 
    'DimAccount' AS TableName,
    AccountID,
    COUNT(*) AS DuplicateCount
FROM dbo.DimAccount
GROUP BY AccountID
HAVING COUNT(*) > 1;


-- Check duplicate in DimCustomer
SELECT 
    'DimCustomer' AS TableName,
    CustomerID,
    COUNT(*) AS DuplicateCount
FROM dbo.DimCustomer
GROUP BY CustomerID
HAVING COUNT(*) > 1;


-- Check duplicate in DimBranch
SELECT 
    'DimBranch' AS TableName,
    BranchID,
    COUNT(*) AS DuplicateCount
FROM dbo.DimBranch
GROUP BY BranchID
HAVING COUNT(*) > 1;


-- Check uppercase in DimCustomer
SELECT
    CustomerID,
    CustomerName,
    Address,
    CityName,
    StateName,
    Age,
    Gender,
    Email
FROM dbo.DimCustomer
WHERE CustomerName <> UPPER(CustomerName)
   OR Address      <> UPPER(Address)
   OR CityName     <> UPPER(CityName)
   OR StateName    <> UPPER(StateName)
   OR Gender       <> UPPER(Gender);