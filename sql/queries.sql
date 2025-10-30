-- ============================================
-- Queries de Análisis para Online Retail II
-- ============================================

-- 1. Top 10 productos más vendidos
SELECT TOP 10
    Description,
    SUM(Quantity) AS TotalQuantity,
    SUM(Quantity * Price) AS TotalRevenue,
    COUNT(DISTINCT Invoice) AS NumTransactions
FROM retail_transactions
WHERE Quantity > 0 AND Price > 0
GROUP BY Description
ORDER BY TotalRevenue DESC;

-- 2. Ventas por país
SELECT
    Country,
    COUNT(DISTINCT CustomerID) AS UniqueCustomers,
    COUNT(DISTINCT Invoice) AS TotalOrders,
    SUM(Quantity * Price) AS TotalRevenue,
    AVG(Quantity * Price) AS AvgOrderValue
FROM retail_transactions
WHERE Quantity > 0 AND Price > 0
GROUP BY Country
ORDER BY TotalRevenue DESC;

-- 3. Análisis temporal - Ventas por mes
SELECT
    FORMAT(InvoiceDate, 'yyyy-MM') AS YearMonth,
    COUNT(DISTINCT Invoice) AS TotalOrders,
    SUM(Quantity * Price) AS TotalRevenue,
    COUNT(DISTINCT CustomerID) AS UniqueCustomers
FROM retail_transactions
WHERE Quantity > 0 AND Price > 0
GROUP BY FORMAT(InvoiceDate, 'yyyy-MM')
ORDER BY YearMonth;

-- 4. Clientes de alto valor (Top 20)
SELECT TOP 20
    CustomerID,
    COUNT(DISTINCT Invoice) AS TotalOrders,
    SUM(Quantity * Price) AS TotalSpent,
    AVG(Quantity * Price) AS AvgOrderValue,
    MAX(InvoiceDate) AS LastPurchase
FROM retail_transactions
WHERE Quantity > 0 AND Price > 0
GROUP BY CustomerID
ORDER BY TotalSpent DESC;

-- 5. Análisis de productos por país
SELECT
    Country,
    Description,
    SUM(Quantity) AS TotalQuantity,
    SUM(Quantity * Price) AS Revenue
FROM retail_transactions
WHERE Quantity > 0 AND Price > 0
GROUP BY Country, Description
HAVING SUM(Quantity * Price) > 1000
ORDER BY Country, Revenue DESC;

-- 6. Análisis de recompra - Clientes recurrentes
SELECT
    CustomerID,
    COUNT(DISTINCT Invoice) AS NumPurchases,
    MIN(InvoiceDate) AS FirstPurchase,
    MAX(InvoiceDate) AS LastPurchase,
    DATEDIFF(DAY, MIN(InvoiceDate), MAX(InvoiceDate)) AS DaysBetween
FROM retail_transactions
WHERE Quantity > 0 AND Price > 0
GROUP BY CustomerID
HAVING COUNT(DISTINCT Invoice) > 1
ORDER BY NumPurchases DESC;

-- 7. Productos frecuentemente comprados juntos
SELECT TOP 20
    t1.Description AS Product1,
    t2.Description AS Product2,
    COUNT(*) AS TimesBoughtTogether
FROM retail_transactions t1
INNER JOIN retail_transactions t2
    ON t1.Invoice = t2.Invoice
    AND t1.Description < t2.Description
WHERE t1.Quantity > 0 AND t2.Quantity > 0
GROUP BY t1.Description, t2.Description
HAVING COUNT(*) > 10
ORDER BY TimesBoughtTogether DESC;

-- 8. Análisis de cancelaciones
SELECT
    FORMAT(InvoiceDate, 'yyyy-MM') AS YearMonth,
    COUNT(*) AS TotalCancellations,
    SUM(ABS(Quantity * Price)) AS CancelledValue
FROM retail_transactions
WHERE Invoice LIKE 'C%'
GROUP BY FORMAT(InvoiceDate, 'yyyy-MM')
ORDER BY YearMonth;
