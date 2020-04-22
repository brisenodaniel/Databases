
1. ```SQL 
    SELECT CategoryName, Description 
    FROM Categories;```
2. ```SQL
    SELECT ContactName, CustomerID, CompanyName
    FROM Customers
    WHERE City = 'London';``` 
3. ```SQL
    SELECT *
    FROM Suppliers
    WHERE ContactTitle IN ('Marketing Manager','Sales Representative') AND Fax IS NOT NULL; ```
4. ```SQL
    SELECT CustomerID
    FROM Orders
    WHERE (RequiredDate BETWEEN '1997-01-01 00:00:00' AND '1998-01-01 23:59:59') AND Freight<100;```
5. ```SQL
    SELECT CompanyName, ContactName
    FROM Customers
    WHERE Country IN ('Mexico','Sweden','Germany');```
6. ```SQL
   SELECT COUNT(ProductID)
   FROM Products
   WHERE Discontinued = 1;```
7. ```SQL
   SELECT CategoryName, Description
    FROM Categories
    WHERE CategoryName LIKE 'Co%';```
8. ```SQL
    SELECT CompanyName, City, Country, PostalCode
    FROM Suppliers
    WHERE Address LIKE '% rue %'
    ORDER BY CompanyName ASC;```
9.  ```SQL
    SELECT ProductID, SUM(Quantity)
    FROM OrderDetails
    GROUP BY ProductID;```
10. ```SQL
    SELECT DISTINCT ContactName, Address
    FROM Customers
    INNER JOIN Orders ON Customers.CustomerID = Orders.CustomerID
    WHERE Orders.ShipVia IN (SELECT ShipperID FROM Shippers WHERE CompanyName = 'Speedy Express');```
11. ```SQL
    SELECT s.CompanyName, s.ContactName, s.ContactTitle, r.RegionDescription
    FROM Suppliers s
    JOIN Territories t on s.city = t.TerritoryDescription
    JOIN Region r ON t.RegionID = r.RegionID;```
12. ```SQL
    SElECT ProductName
    FROM Products
    WHERE CategoryID IN (SELECT CategoryID FROM Categories WHERE CategoryName = 'Condiments');```
13. ```SQL
    SELECT ContactName
    FROM Customers
    WHERE CustomerID NOT IN(SELECT CustomerID FROM Orders);```
14. ```SQL
    INSERT INTO Shippers(CompanyName) 
    VALUES('Amazon');```
15. ```SQL
    UPDATE Shippers
    SET  CompanyName = 'Amazon Prime Shipping'
    WHERE CompanyName = 'Amazon';```
16. ```SQL
    SELECT s.CompanyName, ROUND(SUM(o.Freight),0)
    FROM Shippers s
    LEFT JOIN Orders o ON o.ShipVia = s.ShipperID
    GROUP BY s.CompanyName;```
17. ```SQL
    SELECT CONCAT(LastName, ', ', FirstName)
    FROM Employees```
18. ```SQL
    INSERT INTO Customers(CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax),
    VALUES ('BRISE','Briseno Company','Daniel Dominic Briseno','Artisan Aglet Craftsman','10 Downing Street','New York','Middle Earth','92615','Gondor','867-5309','867-5309');
    INSERT INTO Orders (CustomerID, OrderDate, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry)
    SELECT CustomerID, NOW(), Address, City, Region, PostalCode, Country
    FROM Customers
    WHERE CustomerID = 'BRISE';
    INSERT INTO OrderDetails(OrderID, ProductID, UnitPrice, Quantity, Discount)
    SELECT DISTINCT LAST_INSERT_ID(), ProductID, UnitPrice, 1, 0
    FROM Products
    WHERE ProductName = 'Grandma\'s Boysenberry Spread';```
19. ```SQL
    DELETE FROM OrderDetails
    WHERE OrderID IN (SELECT OrderID FROM Orders WHERE CustomerID = 'BRISE');
    DELETE FROM Orders
    WHERE CustomerID = 'BRISE';
    DELETE FROM Customers
    WHERE CustomerID = 'BRISE';```
20. ```SQL
    SELECT ProductName, UnitsInStock AS TotalUnits
    FROM Products
    WHERE UnitsInStock > 100;```







SELECT ContactName FROM Customers WHERE CustomerID NOT IN (SELECT DISTINCT CustomerID FROM Orders)