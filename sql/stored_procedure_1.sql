USE DWH;
GO

CREATE PROCEDURE BalancePerCustomer
    @name VARCHAR(100)
AS
BEGIN
    SELECT
        dc.CustomerName,
        da.AccountType,
        da.Balance,
        da.Balance + ISNULL(SUM(
            CASE WHEN ft.TransactionType = 'Deposit' THEN ft.Amount ELSE -ft.Amount END
        ), 0) AS CurrentBalance
    FROM DimAccount da
    JOIN DimCustomer dc ON da.CustomerID = dc.CustomerID
    LEFT JOIN FactTransaction ft ON ft.AccountID = da.AccountID
    WHERE da.Status = 'active'
      AND dc.CustomerName LIKE '%' + UPPER(@name) + '%'
    GROUP BY dc.CustomerName, da.AccountType, da.Balance;
END
GO