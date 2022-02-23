-- populate dataship database 

-- populate users table
INSERT INTO users (name, username, email, password, color_scheme, created_at) 
    VALUES 
        ('Admin', 'admin',NULL, '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'default', DATE('now')),
        ('Agustin Zavala Arias', 'agus', '1930120@upv.edu.mx', '37d4cc4e380b9d4dc8c42ac018dec3c2f58e65b118ef75dadc2d1125857491f6', 'default', DATE('now')),
        ('Daniel Sanchez Sanchez', 'daniel', NULL, 'bd3dae5fb91f88a4f0978222dfd58f59a124257cb081486387cbae9df11fb879', 'default', DATE('now'));