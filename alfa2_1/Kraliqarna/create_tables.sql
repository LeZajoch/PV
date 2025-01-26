CREATE TABLE Customers (
    customer_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    date_registered DATETIME NOT NULL DEFAULT GETDATE(),
    is_active BIT NOT NULL DEFAULT 1
);

CREATE TABLE Products (
    product_id INT IDENTITY(1,1) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    product_status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT GETDATE()
);

CREATE TABLE Categories (
    category_id INT IDENTITY(1,1) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE ProductCategories (
    product_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

CREATE TABLE Orders (
    order_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL,
    order_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    order_date DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

CREATE TABLE OrderItems (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Dva příklady VIEW:
CREATE VIEW View_OrdersSummary
AS
SELECT
    o.order_status,
    COUNT(*) AS total_orders,
    SUM(p.price * oi.quantity) AS total_price
FROM Orders o
    INNER JOIN OrderItems oi ON o.order_id = oi.order_id
    INNER JOIN Products p ON oi.product_id = p.product_id
GROUP BY o.order_status;

CREATE VIEW View_ProductSales
AS
SELECT
    p.product_id,
    p.product_name,
    SUM(oi.quantity) AS total_sold
FROM Products p
    LEFT JOIN OrderItems oi ON p.product_id = oi.product_id
    LEFT JOIN Orders o ON oi.order_id = o.order_id
GROUP BY p.product_id, p.product_name;
