-- populate dataship database 

-- populate users table
INSERT INTO users (name, username, email, password, color_scheme, created_at) 
    VALUES 
        ('Admin', 'admin',NULL, '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'default', DATE('now')),
        ('Agustin Zavala Arias', 'agus', '1930120@upv.edu.mx', '37d4cc4e380b9d4dc8c42ac018dec3c2f58e65b118ef75dadc2d1125857491f6', 'default', DATE('now')),
        ('Daniel Sanchez Sanchez', 'daniel', NULL, 'bd3dae5fb91f88a4f0978222dfd58f59a124257cb081486387cbae9df11fb879', 'default', DATE('now'));

-- populate feedback_type table
INSERT INTO feedback_type (name, created_at) 
    VALUES 
        ('Bug', DATE('now')),
        ('Feature', DATE('now')),
        ('Vulnerability', DATE('now'));

-- populate modules table
-- TODO: add description to modules
INSERT INTO modules(name, description, created_at)
    VALUES
        ('Mean', '', DATE('now')),
        ('Median', '', DATE('now')),
        ('Mode', '', DATE('now')),
        ('Standard Deviation', '', DATE('now')),
        ('Variance', '', DATE('now')),
        ('Linear Regression', '', DATE('now')),
        ('Clusterization', '', DATE('now')),
        ('Graphing', '', DATE('now'));

