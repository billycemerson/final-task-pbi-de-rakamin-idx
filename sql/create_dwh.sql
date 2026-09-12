USE DWH;
GO

CREATE TABLE DimBranch (
    BranchID        INT PRIMARY KEY,
    BranchName      VARCHAR(100),
    BranchLocation  VARCHAR(200)
);

CREATE TABLE DimCustomer (
    CustomerID    INT PRIMARY KEY,
    CustomerName  VARCHAR(100),
    Address       VARCHAR(200),
    CityName      VARCHAR(100),
    StateName     VARCHAR(100),
    Age           INT,
    Gender        VARCHAR(20),
    Email         VARCHAR(100)
);

CREATE TABLE DimAccount (
    AccountID     INT PRIMARY KEY,
    CustomerID    INT,
    AccountType   VARCHAR(50),
    Balance       DECIMAL(18,2),
    DateOpened    DATE,
    Status        VARCHAR(20),
    CONSTRAINT FK_DimAccount_Customer FOREIGN KEY (CustomerID)
        REFERENCES DimCustomer(CustomerID)
);

CREATE TABLE FactTransaction (
    TransactionID    INT PRIMARY KEY,
    AccountID        INT,
    TransactionDate  DATETIME,
    Amount           DECIMAL(18,2),
    TransactionType  VARCHAR(50),
    BranchID         INT,
    CONSTRAINT FK_FactTransaction_Account FOREIGN KEY (AccountID)
        REFERENCES DimAccount(AccountID),
    CONSTRAINT FK_FactTransaction_Branch FOREIGN KEY (BranchID)
        REFERENCES DimBranch(BranchID)
);
GO