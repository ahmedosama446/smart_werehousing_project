INSERT_CLIENT= '''INSERT INTO Client (ClientName, Phone, Email)
VALUES (?, ?, ?)'''

INSERT_AGREEMENT = '''INSERT INTO Storage_Agreement (FacilityID, ClientID, Quantity, StartDate, EndDate)
VALUES (?, ?, ?, ?, ?)'''

DELETE_AGREEMENT = '''DELETE FROM Storage_Agreement
WHERE AgreementID = ?'''

DELETE_MOVEMENT = '''DELETE FROM INVENTORY_MOVEMENT
WHERE MovementID = ?'''

UPDATE_PRODUCT = '''UPDATE Product
SET weight = ?
WHERE ProductID = ?'''

UPDATE_FACILITY = '''UPDATE Facility
SET capacity = ?
WHERE FacilityID = ?'''

