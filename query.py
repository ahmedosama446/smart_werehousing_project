QUERY_1_MAX_INDUSTRY = """
    SELECT TOP 1 ig.GroupName, COUNT(*) AS agreement_count
    FROM STORAGE_AGREEMENT sa
    JOIN Product p ON sa.AgreementID = p.AgreementID
    JOIN INDUSTRY_GROUP ig ON p.GroupID = ig.GroupID
    WHERE sa.StartDate BETWEEN '2026-04-01' AND '2026-04-30'
    GROUP BY ig.GroupName
    ORDER BY COUNT(*) DESC
"""

QUERY_2_NO_ACTIVITY = """
    SELECT p.ProductName
    FROM Product p
    WHERE p.ProductID NOT IN (
        SELECT p2.ProductID FROM Product p2
        JOIN STORAGE_AGREEMENT sa ON p2.AgreementID = sa.AgreementID
        WHERE sa.StartDate BETWEEN '2026-04-01' AND '2026-04-30'
    )
    AND p.ProductID NOT IN (
        SELECT ProductID FROM INVENTORY_MOVEMENT
        WHERE MoveAt BETWEEN '2026-04-01' AND '2026-04-30'
    )
"""

QUERY_3_MAX_STAFF_MOVEMENTS = """
    SELECT TOP 1 StaffName, COUNT(*) AS movement_count
    FROM INVENTORY_MOVEMENT
    WHERE MoveAt BETWEEN '2026-04-01' AND '2026-04-30'
    GROUP BY StaffName
    ORDER BY COUNT(*) DESC
"""

QUERY_4_MANUFACTURERS_NO_STORAGE = """
    SELECT m.Attributnamee_23
    FROM MANUFACTURER m
    WHERE m.manufacturer_id NOT IN (
        SELECT p.manufacturer_id
        FROM Product p
        JOIN STORAGE_AGREEMENT sa ON p.AgreementID = sa.AgreementID
        WHERE sa.StartDate BETWEEN '2026-04-01' AND '2026-04-30'
    )
"""

QUERY_5_PRODUCTS_PER_FACILITY = """
    SELECT f.Zone, p.ProductName
    FROM STORAGE_AGREEMENT sa
    JOIN Facility f ON sa.FacilityID = f.FacilityID
    JOIN Product p ON sa.AgreementID = p.AgreementID
    WHERE sa.StartDate BETWEEN '2026-04-01' AND '2026-04-30'
    ORDER BY f.Zone
"""

QUERY_6_CLIENT_TOTAL_QUANTITY = """
    SELECT c.ClientID, c.ClientName, c.Phone, c.Email,
           SUM(sa.Quantity) AS TotalQuantity
    FROM Client c
    JOIN STORAGE_AGREEMENT sa ON c.ClientID = sa.ClientID
    GROUP BY c.ClientID, c.ClientName, c.Phone, c.Email
"""
