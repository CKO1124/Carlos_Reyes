/* Project: Northwind Logistics & Sales Performance Analysis
Description: This query aggregates sales and shipping data to evaluate 
             operational efficiency and financial impact of discounts.
*/

WITH OrderMetrics AS (
    -- CTE 1: Calculate shipping durations and identify late deliveries
    SELECT 
        o.OrderID,
        o.OrderDate,
        o.RequiredDate,
        o.ShippedDate,
        o.CustomerID,
        o.EmployeeID,
        o.ShipVia,
        o.Freight,
        -- Calculate total days from order to shipment
        DATEDIFF(day, o.OrderDate, o.ShippedDate) AS ShippingDuration,
        -- Calculate days late: compares ShippedDate vs RequiredDate
        CASE 
            WHEN o.ShippedDate > o.RequiredDate THEN DATEDIFF(day, o.RequiredDate, o.ShippedDate)
            ELSE 0 
        END AS DaysLate
    FROM Orders o
),
FinancialMetrics AS (
    -- CTE 2: Calculate financial KPIs at the line-item level
    SELECT 
        od.OrderID,
        p.ProductName,
        cat.CategoryName,
        -- Gross sales before discounts
        (od.UnitPrice * od.Quantity) AS GrossSales,
        -- Total amount lost due to discounts
        (od.UnitPrice * od.Quantity * od.Discount) AS DiscountAmount,
        -- Final revenue after discounts
        (od.UnitPrice * od.Quantity * (1 - od.Discount)) AS NetSales
    FROM [Order Details] od
    JOIN Products p ON od.ProductID = p.ProductID
    JOIN Categories cat ON p.CategoryID = cat.CategoryID
)
-- Consolidated metrics 
SELECT 
    om.OrderID,
    om.OrderDate,
    om.ShippedDate,
    om.DaysLate,
    om.ShippingDuration,
    c.ContactName AS Customer,
    e.FirstName + ' ' + e.LastName AS SalesRep,
    s.CompanyName AS ShippingCompany,
    fm.ProductName,
    fm.CategoryName,
    fm.GrossSales,
    fm.DiscountAmount,
    fm.NetSales,
    om.Freight AS FreightCost
FROM OrderMetrics om
JOIN FinancialMetrics fm ON om.OrderID = fm.OrderID
JOIN Customers c ON om.CustomerID = c.CustomerID
JOIN Employees e ON om.EmployeeID = e.EmployeeID
JOIN Shippers s ON om.ShipVia = s.ShipperID;
